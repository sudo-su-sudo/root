#!/bin/bash
# Repository Preservation Helper Script
# Provides convenient commands for working within the archival system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "\n${BOLD}${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "  $1"
}

# Check if in git repo
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository!"
        exit 1
    fi
}

# Show usage
show_usage() {
    cat << EOF
${BOLD}Repository Preservation Helper${NC}

Usage: $0 <command> [options]

Commands:
  ${BOLD}new-branch${NC} <name>       Create a new properly-named branch
  ${BOLD}merge${NC} <branch>          Merge a branch preserving full history
  ${BOLD}snapshot${NC}                Create an archive snapshot
  ${BOLD}verify${NC}                  Run preservation verification
  ${BOLD}status${NC}                  Show repository status and history
  ${BOLD}history${NC}                 View complete git history graph
  ${BOLD}check-merge${NC} <branch>    Preview what would be merged
  ${BOLD}update-timeline${NC}         Open TIMELINE.md for editing
  ${BOLD}config${NC}                  Configure git for preservation

Examples:
  $0 new-branch feature/mobile-ui
  $0 merge feature/mobile-ui
  $0 snapshot
  $0 verify

EOF
}

# Create new branch
create_branch() {
    local branch_name="$1"
    
    if [ -z "$branch_name" ]; then
        print_error "Branch name required!"
        echo "Usage: $0 new-branch <category/description>"
        echo "Categories: feature/, fix/, docs/, exploration/, parallel/, archive/"
        exit 1
    fi
    
    print_header "Creating New Branch: $branch_name"
    
    # Update main first
    print_info "Updating main branch..."
    git checkout main
    git pull origin main
    
    # Create and checkout new branch
    print_info "Creating branch $branch_name..."
    git checkout -b "$branch_name"
    
    # Prompt to update timeline
    print_success "Branch created!"
    print_warning "Don't forget to update TIMELINE.md with branch purpose"
    
    read -p "Open TIMELINE.md now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-vim} TIMELINE.md
    fi
}

# Merge branch preserving history
merge_branch() {
    local branch_name="$1"
    
    if [ -z "$branch_name" ]; then
        print_error "Branch name required!"
        echo "Usage: $0 merge <branch-name>"
        exit 1
    fi
    
    print_header "Merging Branch: $branch_name"
    
    # Ensure we're on main
    print_info "Switching to main..."
    git checkout main
    git pull origin main
    
    # Check if branch exists
    if ! git rev-parse --verify "$branch_name" > /dev/null 2>&1; then
        print_error "Branch $branch_name does not exist!"
        exit 1
    fi
    
    # Preview merge
    print_info "\nChanges to be merged:"
    git log main.."$branch_name" --oneline | head -10
    echo
    
    # Prompt for merge message
    print_info "Enter merge description (or press Ctrl+C to cancel):"
    read -p "> " merge_desc
    
    if [ -z "$merge_desc" ]; then
        print_error "Merge description required!"
        exit 1
    fi
    
    # Perform merge with --no-ff
    print_info "Performing merge with full history preservation..."
    
    # Create detailed merge message
    merge_msg="Merge branch '$branch_name': $merge_desc

Branch: $branch_name
Date: $(date +%Y-%m-%d)

Key commits:
$(git log main.."$branch_name" --oneline | head -5)

See TIMELINE.md for complete context."
    
    if git merge --no-ff "$branch_name" -m "$merge_msg"; then
        print_success "Merge completed successfully!"
        
        # Push main
        print_info "Pushing to remote..."
        git push origin main
        
        # Keep branch alive
        print_info "Preserving branch reference..."
        git push origin "$branch_name"
        
        print_success "Done! Branch history fully preserved."
        print_warning "Remember to update TIMELINE.md with merge details"
        
        read -p "Open TIMELINE.md now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-vim} TIMELINE.md
        fi
    else
        print_error "Merge failed! Resolve conflicts and run:"
        print_info "git merge --continue"
    fi
}

# Create snapshot
create_snapshot() {
    print_header "Creating Archive Snapshot"
    
    local snapshot_name="archive/$(date +%Y-%m-%d)-snapshot"
    
    print_info "Creating snapshot branch: $snapshot_name"
    git branch "$snapshot_name"
    git push origin "$snapshot_name"
    
    # Create tag
    local tag_name="snapshot-$(date +%Y-%m-%d)"
    print_info "Creating tag: $tag_name"
    git tag -a "$tag_name" -m "Archive snapshot $(date +%Y-%m-%d)"
    git push origin "$tag_name"
    
    print_success "Snapshot created!"
    print_info "Branch: $snapshot_name"
    print_info "Tag: $tag_name"
}

# Run verification
run_verification() {
    print_header "Running Preservation Verification"
    python3 verify_preservation.py
}

# Show status
show_status() {
    print_header "Repository Status"
    
    print_info "Current branch:"
    git branch --show-current
    
    print_info "\nAll branches:"
    git branch -a
    
    print_info "\nRecent commits:"
    git log --oneline -10
    
    print_info "\nUncommitted changes:"
    git status --short
}

# Show history
show_history() {
    print_header "Complete Repository History"
    git log --all --graph --decorate --oneline
}

# Check merge preview
check_merge() {
    local branch_name="$1"
    
    if [ -z "$branch_name" ]; then
        print_error "Branch name required!"
        exit 1
    fi
    
    print_header "Merge Preview: $branch_name"
    
    print_info "Commits to be merged:"
    git log main.."$branch_name" --oneline
    
    print_info "\nFiles changed:"
    git diff main..."$branch_name" --stat
    
    print_info "\nPotential conflicts:"
    git merge-tree $(git merge-base main "$branch_name") main "$branch_name" | grep -A 5 "changed in both"
}

# Update timeline
update_timeline() {
    print_header "Updating Timeline"
    ${EDITOR:-vim} TIMELINE.md
    
    read -p "Commit timeline update? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add TIMELINE.md
        read -p "Commit message: " commit_msg
        git commit -m "$commit_msg"
        git push
        print_success "Timeline updated and pushed"
    fi
}

# Configure git
configure_git() {
    print_header "Configuring Git for Preservation"
    
    print_info "Setting merge.ff to false (prevent fast-forward)..."
    git config merge.ff false
    
    print_info "Setting pull.rebase to false (prevent rebase on pull)..."
    git config pull.rebase false
    
    print_success "Git configured for history preservation!"
    
    print_info "\nCurrent preservation-related config:"
    git config --get merge.ff
    git config --get pull.rebase
}

# Main command dispatcher
main() {
    check_git_repo
    
    local command="$1"
    shift
    
    case "$command" in
        new-branch)
            create_branch "$@"
            ;;
        merge)
            merge_branch "$@"
            ;;
        snapshot)
            create_snapshot
            ;;
        verify)
            run_verification
            ;;
        status)
            show_status
            ;;
        history)
            show_history
            ;;
        check-merge)
            check_merge "$@"
            ;;
        update-timeline)
            update_timeline
            ;;
        config)
            configure_git
            ;;
        help|--help|-h|"")
            show_usage
            ;;
        *)
            print_error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
