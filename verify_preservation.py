#!/usr/bin/env python3
"""
Repository Preservation Verification Script

This script verifies that the repository follows the archival policy
and that all history is properly preserved.
"""

import subprocess
import sys
import re
from datetime import datetime
from typing import List, Dict, Tuple

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def run_git_command(command: List[str]) -> Tuple[str, int]:
    """Run a git command and return output and return code"""
    try:
        result = subprocess.run(
            ['git'] + command,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return f"Error: {e}", 1

def print_section(title: str):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.RESET}\n")

def print_success(message: str):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message: str):
    """Print an error message"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_warning(message: str):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def print_info(message: str):
    """Print an info message"""
    print(f"  {message}")

def check_git_repo() -> bool:
    """Verify we're in a git repository"""
    _, code = run_git_command(['rev-parse', '--git-dir'])
    return code == 0

def check_required_files() -> Tuple[bool, List[str]]:
    """Check that all required preservation files exist"""
    required_files = [
        'ARCHIVAL_POLICY.md',
        'HISTORY.md',
        'TIMELINE.md',
        'INTEGRATION_GUIDE.md',
        'AGENT_DEFINITION.md',
        'PRESERVATION_README.md',
        '.gitattributes'
    ]
    
    missing = []
    for file in required_files:
        output, code = run_git_command(['ls-files', file])
        if not output:
            missing.append(file)
    
    return len(missing) == 0, missing

def check_branch_protection() -> Tuple[bool, str]:
    """Check if dangerous operations are prevented"""
    # Check git config for safety settings
    configs_to_check = {
        'merge.ff': 'false',  # Prevent fast-forward merges
    }
    
    warnings = []
    
    for config, expected in configs_to_check.items():
        output, code = run_git_command(['config', '--get', config])
        if output != expected:
            warnings.append(f"{config} should be set to '{expected}' (currently: '{output or 'not set'}')")
    
    return len(warnings) == 0, warnings

def check_commit_history() -> Tuple[bool, Dict]:
    """Analyze commit history for preservation compliance"""
    # Get all commits
    output, _ = run_git_command(['log', '--all', '--oneline'])
    commits = output.split('\n') if output else []
    
    # Get merge commits
    merge_output, _ = run_git_command(['log', '--all', '--merges', '--oneline'])
    merges = merge_output.split('\n') if merge_output else []
    
    # Check for force-pushed commits (harder to detect, checking reflog)
    reflog_output, _ = run_git_command(['reflog', '--all'])
    force_pushes = len([line for line in reflog_output.split('\n') if 'forced' in line.lower()])
    
    stats = {
        'total_commits': len(commits),
        'merge_commits': len(merges),
        'force_pushes': force_pushes,
        'branches': 0
    }
    
    # Count branches
    branch_output, _ = run_git_command(['branch', '-a'])
    stats['branches'] = len([b for b in branch_output.split('\n') if b.strip()])
    
    return force_pushes == 0, stats

def check_merge_commits() -> Tuple[bool, List[str]]:
    """Check that merge commits have proper messages"""
    output, _ = run_git_command(['log', '--merges', '--pretty=format:%H|||%s', '--all'])
    
    if not output:
        return True, []
    
    issues = []
    for line in output.split('\n'):
        if not line:
            continue
        
        commit_hash, message = line.split('|||', 1)
        short_hash = commit_hash[:7]
        
        # Check for poor merge messages
        if message.lower() in ['merge', 'merge branch', 'merged']:
            issues.append(f"{short_hash}: Generic merge message '{message}'")
        elif len(message) < 20:
            issues.append(f"{short_hash}: Very short merge message '{message}'")
    
    return len(issues) == 0, issues

def check_file_attributes() -> Tuple[bool, str]:
    """Verify .gitattributes is configured correctly"""
    output, code = run_git_command(['check-attr', '--all', '.gitattributes'])
    
    if code != 0:
        return False, ".gitattributes not found or not readable"
    
    # Check critical files have proper attributes
    critical_files = [
        'HISTORY.md',
        'TIMELINE.md',
        'ARCHIVAL_POLICY.md'
    ]
    
    issues = []
    for file in critical_files:
        attr_output, _ = run_git_command(['check-attr', 'merge', file])
        if 'union' not in attr_output and 'unset' in attr_output:
            issues.append(f"{file} should have merge=union attribute")
    
    return len(issues) == 0, issues

def check_documentation_current() -> Tuple[bool, List[str]]:
    """Check if documentation files have been updated recently"""
    docs = ['HISTORY.md', 'TIMELINE.md']
    
    warnings = []
    for doc in docs:
        output, code = run_git_command(['log', '-1', '--format=%cr', doc])
        if code == 0 and output:
            # Parse relative time
            if 'month' in output or 'year' in output:
                warnings.append(f"{doc} last updated {output} - consider updating")
    
    return len(warnings) == 0, warnings

def verify_no_squashed_merges() -> Tuple[bool, int]:
    """Detect if any merges appear to have squashed commits"""
    # This is a heuristic: look for commits that might be squashed
    # (single commit with merge-like message but no merge commit)
    
    output, _ = run_git_command(['log', '--all', '--grep=merge', '--no-merges', '--oneline'])
    potential_squashes = len(output.split('\n')) if output else 0
    
    return potential_squashes == 0, potential_squashes

def check_branch_naming() -> Tuple[bool, List[str]]:
    """Check that branches follow naming conventions"""
    output, _ = run_git_command(['branch', '-a'])
    
    if not output:
        return True, []
    
    branches = [b.strip().replace('* ', '').replace('remotes/origin/', '') 
                for b in output.split('\n') if b.strip()]
    
    # Check for good naming patterns
    good_patterns = [
        r'^feature/',
        r'^fix/',
        r'^docs/',
        r'^exploration/',
        r'^parallel/',
        r'^archive/',
        r'^copilot/',
        r'^main$',
        r'^master$'
    ]
    
    poorly_named = []
    for branch in branches:
        if not any(re.match(pattern, branch) for pattern in good_patterns):
            poorly_named.append(branch)
    
    return len(poorly_named) == 0, poorly_named

def main():
    """Main verification function"""
    print(f"\n{Colors.BOLD}Repository Preservation Verification{Colors.RESET}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_passed = True
    
    # Check 1: Git repository
    print_section("1. Git Repository Check")
    if check_git_repo():
        print_success("Running in a valid git repository")
    else:
        print_error("Not in a git repository!")
        return 1
    
    # Check 2: Required files
    print_section("2. Required Preservation Files")
    files_ok, missing = check_required_files()
    if files_ok:
        print_success("All required preservation files present")
    else:
        print_error("Missing required files:")
        for file in missing:
            print_info(f"  - {file}")
        all_passed = False
    
    # Check 3: Git config
    print_section("3. Git Configuration")
    config_ok, warnings = check_branch_protection()
    if config_ok:
        print_success("Git configuration follows best practices")
    else:
        print_warning("Git configuration could be improved:")
        for warning in warnings:
            print_info(f"  - {warning}")
    
    # Check 4: Commit history
    print_section("4. Commit History Analysis")
    history_ok, stats = check_commit_history()
    print_info(f"Total commits: {stats['total_commits']}")
    print_info(f"Merge commits: {stats['merge_commits']}")
    print_info(f"Branches: {stats['branches']}")
    print_info(f"Force pushes detected: {stats['force_pushes']}")
    
    if history_ok:
        print_success("No force pushes detected")
    else:
        print_error(f"Found {stats['force_pushes']} force pushes - this violates archival policy!")
        all_passed = False
    
    # Check 5: Merge commit quality
    print_section("5. Merge Commit Quality")
    merges_ok, issues = check_merge_commits()
    if merges_ok:
        print_success("All merge commits have good messages")
    else:
        print_warning("Some merge commits could have better messages:")
        for issue in issues[:5]:  # Show first 5
            print_info(f"  - {issue}")
        if len(issues) > 5:
            print_info(f"  ... and {len(issues) - 5} more")
    
    # Check 6: File attributes
    print_section("6. Git Attributes")
    attr_ok, attr_issues = check_file_attributes()
    if attr_ok:
        print_success("File attributes configured correctly")
    else:
        print_warning("File attribute issues:")
        for issue in attr_issues:
            print_info(f"  - {issue}")
    
    # Check 7: Documentation currency
    print_section("7. Documentation Currency")
    docs_ok, doc_warnings = check_documentation_current()
    if docs_ok:
        print_success("Documentation appears up to date")
    else:
        print_warning("Documentation may need updating:")
        for warning in doc_warnings:
            print_info(f"  - {warning}")
    
    # Check 8: No squashed merges
    print_section("8. Merge Integrity")
    squash_ok, squash_count = verify_no_squashed_merges()
    if squash_ok:
        print_success("No evidence of squashed merges")
    else:
        print_warning(f"Found {squash_count} commit(s) that might be squashed merges")
        print_info("  (This is a heuristic check - manual verification recommended)")
    
    # Check 9: Branch naming
    print_section("9. Branch Naming Conventions")
    naming_ok, poorly_named = check_branch_naming()
    if naming_ok:
        print_success("All branches follow naming conventions")
    else:
        print_warning("Some branches don't follow naming conventions:")
        for branch in poorly_named[:10]:
            print_info(f"  - {branch}")
        if len(poorly_named) > 10:
            print_info(f"  ... and {len(poorly_named) - 10} more")
    
    # Summary
    print_section("Summary")
    if all_passed:
        print_success("All critical checks passed! Repository follows archival policy.")
        print_info("\nThis repository properly preserves history and follows")
        print_info("the append-only archival philosophy.")
        return 0
    else:
        print_error("Some critical checks failed!")
        print_info("\nPlease review the failures above and correct them to ensure")
        print_info("proper history preservation according to ARCHIVAL_POLICY.md")
        return 1

if __name__ == '__main__':
    sys.exit(main())
