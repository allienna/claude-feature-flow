---
description: "Feature Flow workflow context — artifact structure, status conventions, and command chain for structured feature development"
applyTo: "**/specs/**,**/PRD.md,**/CLAUDE.md"
---

# Feature Flow — Workflow Context

This project uses the **Feature Flow** methodology for structured feature development. All AI-assisted work should follow the conventions below.

## Artifact Structure

```
PRD.md                              # Product Requirements Document (project root)
specs/
  constitution.md                   # Non-negotiable project principles
  roadmap.md                        # Feature roadmap with dependencies
  {NNN}-{feature-name}/            # Feature track (e.g., 001-auth-client/)
    spec.md                         # Feature specification & acceptance criteria
    plan.md                         # Technical implementation plan
    tasks.md                        # Atomic task breakdown
    review.md                       # Spec compliance review
qa-report.md                        # Project-wide quality audit (project root)
```

## Status Conventions

### Spec Status (in spec.md)
`Draft` → `Approved` → `In Progress` → `Complete`

### Roadmap Feature Status (in roadmap.md)
`Not started` → `Specifying` → `Planning` → `In Progress` → `Complete`

### Task Status (in tasks.md)
`- [ ]` (pending) → `- [x]` (completed)

## Workflow Chain

The commands chain together in this order. Each step depends on artifacts from the previous:

```
/prd            → Creates PRD.md
/constitution   → Creates specs/constitution.md (reads PRD.md)
/roadmap        → Creates specs/roadmap.md (reads PRD.md)
/specify        → Creates specs/{NNN}-{name}/spec.md (reads roadmap.md, PRD.md)
/plan           → Creates specs/{NNN}-{name}/plan.md (reads spec.md, codebase)
/tasks          → Creates specs/{NNN}-{name}/tasks.md (reads plan.md)
/implement      → Implements one task at a time (reads tasks.md, CLAUDE.md)
/review         → Creates specs/{NNN}-{name}/review.md (reads spec.md, code)
/qa             → Creates qa-report.md (runs tests, lint, security checks)
/ship           → Creates branch, commits, pushes, opens PR
/merge          → Addresses PR comments, squash merges
```

## Feature Track Naming

- Directory: `specs/{NNN}-{feature-name}/` where NNN is zero-padded (001, 002, etc.)
- Branch: `feat/{NNN}-{feature-name}`
- Commit: `feat({NNN}): {description}`

## State Detection

Commands auto-detect project state by checking which artifacts exist. Before starting any workflow step:
1. Search for `specs/*/spec.md` to find all feature tracks
2. Read each track's spec.md for its Status field
3. Check for plan.md, tasks.md, review.md existence
4. Count `[x]` and `[ ]` in tasks.md for progress

## Build Commands

Commands reference `CLAUDE.md` for project-specific build commands (test, lint, format, type check). If CLAUDE.md is missing, automated quality checks are skipped with a warning.
