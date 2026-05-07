# Archival Policy: Immutable Knowledge Base

## Philosophy: Append-Only History

This repository operates on a fundamental principle: **knowledge can only be added, never removed**. Every branch, every commit, every decision made throughout the project's evolution is preserved forever.

## Core Principles

### 1. All History is Sacred
- Every commit represents a moment of understanding
- Every branch represents a parallel exploration of ideas
- Every merge represents the synthesis of different approaches
- Nothing is ever force-pushed, rebased away, or deleted

### 2. Branches as Timelines
Each branch represents a complete timeline of thought:
- Parallel branches represent parallel explorations
- Divergent branches show different approaches to the same problem
- All branches maintain their complete history when merged

### 3. Git as Time Machine
The repository structure enables:
- Reverting to any point in history
- Understanding context of any decision
- Tracking evolution of ideas over time
- Reconstructing thought processes from any moment

## Technical Implementation

### Protected Operations

**ALLOWED:**
- `git add` - Stage new work
- `git commit` - Record new state
- `git merge --no-ff` - Merge with full history preservation
- `git branch` - Create new exploration timelines
- `git push` - Share work with remote

**PROHIBITED:**
- `git reset --hard` (except on local uncommitted work)
- `git rebase` - Rewrites history, loses context
- `git push --force` - Overwrites remote history
- `git filter-branch` - Removes commits
- `git branch -D` on merged branches - Loses reference points

### Merge Strategy

Always use **merge commits with full history**:
```bash
# Correct approach
git merge --no-ff branch-name -m "Merge parallel timeline: [description]"

# Never do this
git rebase main  # NO! This rewrites history
git merge --squash branch-name  # NO! This loses individual commits
```

### Branch Naming Convention

Branches should describe their purpose and timeline:
```
feature/[description]      - New capabilities
exploration/[topic]        - Experimental work
parallel/[timeline-name]   - Parallel development
archive/[date]-[snapshot]  - Explicit preservation points
```

## History Preservation Rules

### 1. Commit Messages as Documentation
Every commit message should answer:
- **What** changed (code diff shows this)
- **Why** it changed (reasoning, context)
- **When** in the project timeline (implicit in timestamp)
- **How** it relates to other work (references to issues/PRs)

### 2. Branch Documentation
Before merging any long-lived branch:
1. Document its purpose in TIMELINE.md
2. Explain its relationship to other branches
3. Describe what was learned, even if approach wasn't used
4. Record any parallel work that informed it

### 3. Merge Documentation
Every merge commit should include:
- Summary of what the branch accomplished
- How it relates to the main timeline
- Any conflicts resolved and why
- Links to detailed documentation of the work

## Practical Guidelines

### Starting New Work

```bash
# 1. Always start from a clean base
git checkout main
git pull origin main

# 2. Create a descriptive branch
git checkout -b exploration/agent-configuration

# 3. Make commits frequently with clear messages
git add file.md
git commit -m "Define agent first principles

This establishes the core values that should guide
agent decision-making based on ethical foundations
and practical effectiveness."

# 4. Push early and often
git push -u origin exploration/agent-configuration
```

### Merging Work

```bash
# 1. Update TIMELINE.md before merging
vim TIMELINE.md
git add TIMELINE.md
git commit -m "Document exploration/agent-configuration timeline"

# 2. Merge with full history preservation
git checkout main
git merge --no-ff exploration/agent-configuration -m "Merge: Agent Configuration System

This parallel exploration developed a comprehensive agent
configuration system including:
- First principles definition
- Value hierarchy
- Decision-making framework
- Configuration templates

All commits preserved for future reference."

# 3. Keep the branch reference
# DO NOT delete the branch - it's part of the historical record
git push origin exploration/agent-configuration
```

### Recovering Historical Context

```bash
# View complete history across all branches
git log --all --graph --decorate --oneline

# Examine a specific point in time
git checkout <commit-hash>
git log

# Return to present
git checkout main

# See what existed at any point
git show <commit-hash>:path/to/file.md
```

## Conflict Resolution Philosophy

When merge conflicts occur:

1. **Preserve Both Perspectives**: Include both approaches in documentation
2. **Document Resolution Reasoning**: Explain why one approach was chosen
3. **Keep Alternative in Comments**: Leave commented code showing the other approach
4. **Reference in Commit**: Link to discussion of why resolution was chosen

Example conflict resolution commit:
```
Resolve merge conflict in orchestrator logic

Conflict between two approaches to decision confidence:
- Branch A: Threshold-based confidence (>0.7)
- Branch B: Dynamic confidence based on context

Resolution: Implemented Branch B's dynamic approach because
it handles edge cases better. Branch A's threshold approach
preserved in comments for future reference.

See DECISION_LOG.md entry #47 for full analysis.
```

## Archive Snapshots

Periodically create explicit archive points:

```bash
# Create a snapshot branch
git checkout -b archive/2026-02-02-complete-system
git push origin archive/2026-02-02-complete-system

# Tag important milestones
git tag -a v1.0-complete-integration -m "Complete integration of all sessions"
git push origin v1.0-complete-integration
```

## Verification Checklist

Before pushing any changes, verify:

- [ ] All commits have meaningful messages
- [ ] No force-push flags used
- [ ] Merge uses `--no-ff` to preserve history
- [ ] TIMELINE.md updated if new branch or merge
- [ ] No branches deleted that contain unique work
- [ ] Tags created for major milestones
- [ ] Documentation explains the "why" not just "what"

## Recovery Procedures

### If History is Accidentally Lost

```bash
# Git reflog can recover recent history
git reflog

# Restore a lost commit
git checkout <commit-hash-from-reflog>
git branch recovery/lost-work
git checkout main
git merge --no-ff recovery/lost-work
```

### If Remote is Corrupted

```bash
# Always maintain local copies
git clone --mirror <repository-url> backup-$(date +%Y%m%d)

# Can restore from local if needed
cd backup-YYYYMMDD
git push --mirror <new-remote-url>
```

## Philosophy Summary

This repository is a **knowledge artifact** that grows over time. Like a journal, we add new entries but never tear out old pages. Every contribution, every experiment, every decision is part of the story of how this system evolved.

Future visitors to this repository should be able to:
1. Understand how any current state was reached
2. Explore alternative approaches that were considered
3. Learn from the decision-making process
4. Revert to or build upon any historical state
5. Trace the evolution of ideas over time

**The repository is not just the current code—it's the entire journey of how that code came to be.**

---

*This policy ensures that this repository serves as an undeletable archive of knowledge, where every contribution is valued and preserved for future learning and reference.*
