# Archive Guidelines

## Purpose

This document provides best practices for maintaining an immutable, append-only git archive that preserves complete development history, context, and decision-making processes. These guidelines ensure that future developers and AI agents can understand not just what was done, but why it was done.

## Core Principles

### 1. Immutability
**Never rewrite history.** Once committed and pushed, history should remain unchanged.

### 2. Append-Only Development
Add new commits, branches, and documentation without removing or modifying existing history.

### 3. Complete Context
Every commit should contain sufficient context to understand the change independently.

### 4. Decision Documentation
Document not just the code changes, but the reasoning and alternatives considered.

### 5. Accessible History
Structure history so it can be easily navigated, searched, and understood.

## Git Strategies for Append-Only History

### Branch Protection

#### Recommended Settings
```
Main/Protected Branches:
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Prohibit force pushes
- Prohibit deletions
```

#### Configuration
```bash
# Protect a branch from force pushes and deletion
git config --local receive.denyNonFastForwards true
git config --local receive.denyDeletes true

# For GitHub, configure via Settings > Branches > Branch protection rules
```

### Commit Strategies

#### 1. Meaningful Commit Messages
Every commit message should follow this structure:

```
[Type] Brief description (50 chars or less)

- Detailed explanation of what was changed
- Why the change was necessary
- What alternatives were considered
- Impact on existing functionality
- Related issues or PRs

Context: Additional background or reasoning
References: Links to related commits, issues, PRs
```

**Types:** `[FEAT]`, `[FIX]`, `[DOCS]`, `[REFACTOR]`, `[TEST]`, `[CHORE]`

#### 2. Atomic Commits
Each commit should be:
- **Self-contained**: Represents one logical change
- **Reversible**: Can be reverted without breaking functionality
- **Testable**: Includes tests if applicable
- **Documented**: Has clear commit message

#### 3. Never Use Force Push
Force pushing rewrites history and should be avoided on shared branches.

**Instead of:**
```bash
git push -f  # NEVER on shared branches
```

**Use:**
```bash
# If you need to fix something, create a new commit
git revert <commit-hash>
# Or add a new corrective commit
git commit -m "[FIX] Correct issue from previous commit"
```

### Merge Strategies

#### 1. Preserve Full History (Recommended)
Use merge commits to preserve complete branch history:

```bash
git merge --no-ff feature-branch -m "Merge feature: description"
```

Benefits:
- Complete history of parallel development
- All commits preserved with context
- Easy to see feature boundaries
- Can revert entire features

#### 2. Never Use Destructive Merges
Avoid squashing or rebasing shared branches:

```bash
# AVOID these on shared/public branches:
git merge --squash feature-branch  # Loses commit history
git rebase main  # Rewrites history
```

#### 3. Merge Commit Messages
Include comprehensive information:

```
Merge branch 'feature/learning-system' into main

Added preference learning and meta-reasoning capabilities.

Features:
- Preference learning from decision history
- Meta-reasoning with gap analysis
- Pattern recognition system
- Strategic progress reporting

Related PRs: #5, #6, #7
Documentation: LEARNING_IMPLEMENTATION.md
```

### Branch Management

#### 1. Branch Naming Convention
```
<type>/<description>

Types:
- feature/  : New features
- fix/      : Bug fixes
- docs/     : Documentation updates
- refactor/ : Code refactoring
- test/     : Test additions/improvements
- chore/    : Maintenance tasks

Examples:
- feature/meta-reasoning
- fix/persistence-bug
- docs/archive-guidelines
```

#### 2. Branch Lifecycle
1. **Create**: Branch from latest main/protected branch
2. **Develop**: Make commits with clear messages
3. **Document**: Add relevant documentation
4. **Test**: Ensure tests pass
5. **Review**: Submit pull request with complete description
6. **Merge**: Use `--no-ff` to preserve history
7. **Preserve**: Never delete branches that contain unique history

#### 3. Long-Lived Branches
Keep these branches indefinitely:
- `main` / `master`: Production-ready code
- `develop`: Integration branch (if using git-flow)
- Major feature branches with significant history

### Tag Strategy

#### 1. Version Tags
Use semantic versioning for releases:

```bash
git tag -a v1.0.0 -m "Release 1.0.0: Initial public release"
git push origin v1.0.0
```

#### 2. Milestone Tags
Tag significant milestones:

```bash
git tag -a milestone-learning-system -m "Completed learning system implementation"
```

#### 3. Archive Tags
Tag states you want to preserve:

```bash
git tag -a archive-2026-02-01 -m "Archive state as of Feb 1, 2026"
```

## Documentation Strategies

### 1. In-Repository Documentation
Maintain comprehensive documentation within the repository:

#### Required Documents
- **README.md**: Project overview and quick start
- **REPOSITORY_HISTORY.md**: Complete commit history documentation
- **ARCHIVE_GUIDELINES.md**: This document
- **CONTEXT_PRESERVATION.md**: Decision contexts and reasoning
- **AGENT_PRINCIPLES.md**: Agent design principles

#### Feature Documentation
For each major feature:
- Implementation guide
- Design decisions
- Usage examples
- Testing approach

### 2. Commit-Linked Documentation
Reference documentation in commits:

```
[FEAT] Add meta-reasoning capabilities

Implemented 8-type knowledge gap analysis system.

Documentation: LEARNING_IMPLEMENTATION.md
Related: See FINAL_SUMMARY.md for design rationale
Tests: tests/test_meta_reasoning.py
```

### 3. Decision Records
Create Architecture Decision Records (ADRs) for significant decisions:

```markdown
# ADR-001: Use SQLite for Persistence

## Status
Accepted

## Context
Need persistent storage for learning data across sessions.

## Decision
Use SQLite with SQLAlchemy ORM.

## Consequences
- Simple setup, no external dependencies
- File-based, easy to backup
- Sufficient for single-user scenarios
- May need migration for multi-user

## Alternatives Considered
- PostgreSQL: Too heavy for initial use case
- JSON files: No querying, difficult to scale
- MongoDB: Overkill for structured data
```

## Backup and Recovery

### 1. Regular Backups
```bash
# Clone with full history
git clone --mirror <repository-url> backup.git

# Update backup
cd backup.git
git fetch --all
```

### 2. Export History
```bash
# Export all commits to archive
git log --all --pretty=fuller --stat > git-history-$(date +%Y%m%d).txt

# Export with patches
git log --all -p > git-patches-$(date +%Y%m%d).txt
```

### 3. Bundle Repository
```bash
# Create self-contained bundle
git bundle create repo-backup-$(date +%Y%m%d).bundle --all

# Restore from bundle
git clone repo-backup.bundle restored-repo
```

## Verification and Validation

### 1. History Integrity
```bash
# Verify repository integrity
git fsck --full

# Check for missing objects
git fsck --lost-found
```

### 2. Documentation Completeness
Regularly verify:
- [ ] All major features documented
- [ ] All commits have clear messages
- [ ] Decision contexts preserved
- [ ] Links between related documents work
- [ ] Examples are up to date

### 3. Branch Health
```bash
# List branches with last commit date
git for-each-ref --sort=-committerdate refs/heads/ \
  --format='%(refname:short) %(committerdate:short) %(subject)'

# Check for unmerged branches
git branch --no-merged main
```

## Working with AI Agents

### Guidelines for AI Development
When AI agents work on the repository:

1. **Always pull before starting work**
2. **Create feature branches for changes**
3. **Document decisions in commit messages**
4. **Reference related documentation**
5. **Never force push or rewrite history**
6. **Preserve all context for future sessions**
7. **Update relevant documentation with changes**

### Agent-Specific Branches
Consider prefixing agent branches:
```
copilot/update-readme-documentation
gemini/add-feature-x
claude/refactor-y
```

This makes it clear which agent made which changes and preserves that context.

## Emergency Procedures

### If History Is Accidentally Rewritten

1. **Don't panic** - Git rarely loses data permanently
2. **Check reflog**: `git reflog` shows all HEAD positions
3. **Recover**: `git reset --hard <previous-commit>`
4. **Communicate**: Inform team about the issue
5. **Document**: Record what happened and how it was fixed

### If Force Push Occurred

1. **Locate original commits** in reflog
2. **Create recovery branch**: `git branch recovery <original-commit>`
3. **Merge recovery**: Merge the recovery branch to restore history
4. **Document incident**: Create incident report

## Best Practices Summary

✅ **DO:**
- Use `git merge --no-ff` for features
- Write comprehensive commit messages
- Document decisions and reasoning
- Tag important milestones
- Keep long-lived branches
- Back up regularly
- Link commits to documentation
- Preserve all context

❌ **DON'T:**
- Force push to shared branches
- Squash merge without good reason
- Delete branches with unique history
- Rewrite public history
- Skip documentation
- Remove old tags
- Lose context

## Tools and Automation

### Git Hooks
Implement hooks to enforce guidelines:

```bash
# .git/hooks/commit-msg
# Enforce commit message format

# .git/hooks/pre-push
# Prevent force pushes to protected branches
```

### CI/CD Integration
- Run tests on all branches
- Generate documentation automatically
- Create backups on merges
- Validate commit message format

## Maintenance Schedule

### Daily
- [ ] Review new commits for message quality
- [ ] Check CI/CD status

### Weekly
- [ ] Verify documentation is up to date
- [ ] Check branch health
- [ ] Review open PRs

### Monthly
- [ ] Create full backup
- [ ] Verify repository integrity
- [ ] Update archive documentation
- [ ] Tag significant milestones

### Quarterly
- [ ] Review and update guidelines
- [ ] Archive old branches (but don't delete)
- [ ] Comprehensive documentation review
- [ ] Update context preservation records

---

*This document is part of the immutable archive system. For repository history, see REPOSITORY_HISTORY.md. For context preservation, see CONTEXT_PRESERVATION.md.*
