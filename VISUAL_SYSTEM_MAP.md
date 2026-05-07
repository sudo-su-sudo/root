# Visual System Map

```
┌──────────────────────────────────────────────────────────────────────┐
│                    REPOSITORY PRESERVATION SYSTEM                     │
│                                                                       │
│              "All knowledge can only be added, never removed"        │
└──────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │ START_HERE.md│
                              │   (YOU ARE   │
                              │     HERE)    │
                              └──────┬───────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
        ┌─────────────────┐  ┌─────────────┐  ┌──────────────┐
        │ PRESERVATION_   │  │  ARCHIVAL_  │  │   COMPLETE_  │
        │   README.md     │  │  POLICY.md  │  │    SYSTEM_   │
        │                 │  │             │  │   SUMMARY.md │
        │ (User Guide)    │  │(Philosophy) │  │  (Overview)  │
        └────────┬────────┘  └──────┬──────┘  └──────┬───────┘
                 │                  │                 │
                 │    ┌─────────────┴─────────────┐   │
                 │    │                           │   │
                 ▼    ▼                           ▼   ▼
    ┌─────────────────────────────────────────────────────────┐
    │                   CORE DOCUMENTS                        │
    │                                                          │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
    │  │  HISTORY.md  │  │ TIMELINE.md  │  │   AGENT_     │  │
    │  │              │  │              │  │ DEFINITION.md│  │
    │  │ (What & Who) │  │(When & Why)  │  │(Philosophy)  │  │
    │  └──────────────┘  └──────────────┘  └──────────────┘  │
    │                                                          │
    │  ┌────────────────────────────────────────────────┐    │
    │  │         INTEGRATION_GUIDE.md                   │    │
    │  │         (How to Merge)                         │    │
    │  └────────────────────────────────────────────────┘    │
    └─────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
        ┌─────────────────────┐       ┌──────────────────────┐
        │    AUTOMATION        │       │   CONFIGURATION      │
        │                      │       │                      │
        │ verify_preservation  │       │  .gitattributes      │
        │      .py             │       │                      │
        │                      │       │  git config:         │
        │ preserve.sh          │       │  - merge.ff=false    │
        │                      │       │  - pull.rebase=false │
        └─────────────────────┘       └──────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                         WORKFLOW DIAGRAM                              │
└──────────────────────────────────────────────────────────────────────┘

    NEW WORK                DEVELOPMENT              INTEGRATION
    ────────                ───────────              ───────────

      START
        │
        ▼
  ┌──────────┐
  │ ./preserve│         ┌────────────┐         ┌────────────────┐
  │ .sh      │────────▶│   Code &   │────────▶│  ./preserve.sh │
  │new-branch│         │   Commit   │         │     merge      │
  └──────────┘         └────────────┘         └────────────────┘
        │                     │                       │
        │                     │                       │
        ▼                     ▼                       ▼
  ┌──────────┐         ┌────────────┐         ┌────────────────┐
  │  Update  │         │   Push     │         │     Update     │
  │ TIMELINE │         │   Often    │         │   TIMELINE &   │
  └──────────┘         └────────────┘         │    HISTORY     │
                                              └────────────────┘
                                                      │
                                                      ▼
                                              ┌────────────────┐
                                              │    Verify      │
                                              │  ./preserve.sh │
                                              │     verify     │
                                              └────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                        GIT BRANCH STRUCTURE                           │
└──────────────────────────────────────────────────────────────────────┘

    main (or master)
      │
      ├─── feature/something
      │     │
      │     ├─ commit 1
      │     ├─ commit 2
      │     └─ commit 3
      │         │
      │         └─────┐
      │               │ (merge --no-ff)
      │◄──────────────┘
      │
      ├─── exploration/topic
      │     │
      │     ├─ commit 1
      │     └─ commit 2
      │         │
      │         └─────┐
      │               │ (merge --no-ff)
      │◄──────────────┘
      │
      └─── archive/2026-02-snapshot (preserved forever)

    ✓ All branches kept alive forever
    ✓ All merge commits use --no-ff
    ✓ Branch structure visible in history
    ✓ Can navigate to any point

┌──────────────────────────────────────────────────────────────────────┐
│                     COMMAND QUICK REFERENCE                           │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┬────────────────────────────────────────────┐
│ TASK                    │ COMMAND                                    │
├─────────────────────────┼────────────────────────────────────────────┤
│ Configure Git           │ ./preserve.sh config                       │
│ Verify System           │ ./preserve.sh verify                       │
│ Create New Branch       │ ./preserve.sh new-branch feature/name      │
│ Merge Branch            │ ./preserve.sh merge feature/name           │
│ View History            │ ./preserve.sh history                      │
│ Check Status            │ ./preserve.sh status                       │
│ Preview Merge           │ ./preserve.sh check-merge feature/name     │
│ Update Timeline         │ ./preserve.sh update-timeline              │
│ Create Snapshot         │ ./preserve.sh snapshot                     │
│ Manual Verification     │ python3 verify_preservation.py             │
└─────────────────────────┴────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                        KEY PRINCIPLES                                 │
└──────────────────────────────────────────────────────────────────────┘

    ✅ ALWAYS                          ❌ NEVER
    ────────                          ──────
    
    git merge --no-ff              git rebase
    git commit -m "detail"         git push --force
    git branch feature/name        git merge --squash
    Update TIMELINE.md             git branch -D merged
    Document decisions             Delete history
    Push branches                  Rewrite commits
    Preserve context              Lose information

┌──────────────────────────────────────────────────────────────────────┐
│                     SYSTEM VERIFICATION                               │
└──────────────────────────────────────────────────────────────────────┘

    Run: python3 verify_preservation.py
    
    Checks:
    ✓ Required files present
    ✓ Git configuration correct
    ✓ No force pushes
    ✓ Merge commits have good messages
    ✓ File attributes configured
    ✓ Documentation current
    ✓ Branch naming conventions
    ✓ No squashed merges
    ✓ History integrity

┌──────────────────────────────────────────────────────────────────────┐
│                      FILE RELATIONSHIPS                               │
└──────────────────────────────────────────────────────────────────────┘

    Policy Layer
    ────────────
    ARCHIVAL_POLICY.md ────┐
                           ├──▶ Philosophy & Rules
    AGENT_DEFINITION.md ───┘

    Historical Layer
    ────────────────
    HISTORY.md ────────────┐
                           ├──▶ What, Who, How
    TIMELINE.md ───────────┘     When, Why, Context

    User Layer
    ──────────
    START_HERE.md ─────────┐
                           │
    PRESERVATION_README ───┼──▶ Guides & How-To
                           │
    INTEGRATION_GUIDE.md ──┘

    System Layer
    ────────────
    COMPLETE_SYSTEM_SUMMARY.md ──▶ Overview

    Tool Layer
    ──────────
    verify_preservation.py ───┐
                              ├──▶ Automation
    preserve.sh ──────────────┘

    Config Layer
    ────────────
    .gitattributes ────────────▶ Git Behavior

┌──────────────────────────────────────────────────────────────────────┐
│                     PRESERVATION LIFECYCLE                            │
└──────────────────────────────────────────────────────────────────────┘

    1. PLAN
       ├─ Read documentation
       ├─ Understand philosophy
       └─ Configure git
       
    2. CREATE
       ├─ ./preserve.sh new-branch
       ├─ Update TIMELINE.md
       └─ Document intent
       
    3. DEVELOP
       ├─ Write code
       ├─ Commit often
       ├─ Good messages
       └─ Push frequently
       
    4. INTEGRATE
       ├─ Update TIMELINE.md
       ├─ ./preserve.sh merge
       ├─ Preserve branch
       └─ Update HISTORY.md
       
    5. VERIFY
       ├─ ./preserve.sh verify
       ├─ Check history graph
       └─ Confirm preservation
       
    6. SNAPSHOT (Periodic)
       ├─ ./preserve.sh snapshot
       ├─ Tag milestone
       └─ Archive state

┌──────────────────────────────────────────────────────────────────────┐
│                      PHILOSOPHY DIAGRAM                               │
└──────────────────────────────────────────────────────────────────────┘

                    ┌────────────────────┐
                    │  CORE PRINCIPLE    │
                    │                    │
                    │  "All knowledge    │
                    │   can only be      │
                    │   added, never     │
                    │   removed"         │
                    └─────────┬──────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
      ┌──────────┐    ┌──────────┐    ┌──────────┐
      │ Commits  │    │ Branches │    │ Context  │
      │  are     │    │   are    │    │   is     │
      │ sacred   │    │ timelines│    │  sacred  │
      └─────┬────┘    └────┬─────┘    └────┬─────┘
            │              │               │
            │              │               │
            └──────────────┼───────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   RESULTS IN    │
                  └─────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐      ┌───────────┐      ┌──────────┐
    │Complete│      │ Complete  │      │ Complete │
    │History │      │ Context   │      │ Learning │
    └────────┘      └───────────┘      └──────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  ENABLES        │
                  └─────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐      ┌───────────┐      ┌──────────┐
    │  Time  │      │Navigation │      │ Learning │
    │ Travel │      │& Recovery │      │   From   │
    │Possible│      │ Possible  │      │ History  │
    └────────┘      └───────────┘      └──────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                           SUMMARY                                     │
└──────────────────────────────────────────────────────────────────────┘

    This repository implements a COMPLETE PRESERVATION SYSTEM:

    ✓ Philosophy documented      (ARCHIVAL_POLICY.md)
    ✓ History tracked           (HISTORY.md, TIMELINE.md)
    ✓ Integration defined       (INTEGRATION_GUIDE.md)
    ✓ Agent principles          (AGENT_DEFINITION.md)
    ✓ User guides created       (PRESERVATION_README.md)
    ✓ Tools provided            (verify_preservation.py, preserve.sh)
    ✓ Configuration set         (.gitattributes, git config)
    ✓ Entry point clear         (START_HERE.md)
    ✓ System overview           (COMPLETE_SYSTEM_SUMMARY.md)
    ✓ Visual map                (This file!)

    RESULT: Nothing is ever lost, everything is preserved forever.

    "The repository is not just the current code—
     it's the entire story of how that code came to be."

┌──────────────────────────────────────────────────────────────────────┐
│                      GET STARTED NOW                                  │
└──────────────────────────────────────────────────────────────────────┘

    Step 1: ./preserve.sh config
    Step 2: ./preserve.sh verify
    Step 3: cat PRESERVATION_README.md
    Step 4: Start working!

    Questions? Read START_HERE.md
```
