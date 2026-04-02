---
mode: agent
description: "Show project status — roadmap progress, active tracks, and recommended next action"
tools: ['runCommands', 'search', 'codebase']
---

# Status

Display the current project status and recommend the next action.

## Gather state

1. Run `git branch --show-current` to get the current branch
2. Read `specs/roadmap.md` to get the roadmap (if it doesn't exist, note that no roadmap exists)
3. Search for `specs/*/spec.md` to find all feature tracks
4. For each track found, read its `spec.md`, and check for `plan.md`, `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md
   - If tasks.md exists, count `[x]` (done) and `[ ]` (pending) items, find the first pending task

## Present status

### 1. Roadmap overview

If no roadmap: "No roadmap. Run the roadmap prompt to get started."

If roadmap exists: Show each feature from specs/roadmap.md with its current status, cross-referencing with existing tracks. Use this format:

```
Roadmap Progress
=======================================
F-001 project-scaffold       ██████████ 5/5   complete
F-002 auth-client             ████████░░ 8/10  implementing
F-003 core-api                ░░░░░░░░░░ —     next up
F-004 feature-module-a        ░░░░░░░░░░ —
F-005 feature-module-b        ░░░░░░░░░░ —
=======================================
Milestone M1 (Foundation): 1/2 features
```

### 2. Active tracks detail

For each active track (not complete), show:

```
Active: 002-auth-client
   Status: In Progress
   Spec: done  Plan: done  Tasks: 8/10  Review: —
   Next task: T-2.3 — Add token refresh logic
   Branch: feat/002-auth-client
```

### 3. Recommended action

Based on the state, suggest ONE clear next action:

| State | Recommendation |
|---|---|
| No roadmap | "Run the roadmap prompt to define your features." |
| Roadmap exists, no tracks | "Run the specify prompt to start the first feature." |
| Track has draft spec | "Review and approve the spec, then run the plan prompt." |
| Track has spec, no plan | "Run the plan prompt." |
| Track has plan, no tasks | "Run the tasks prompt." |
| Track has unchecked tasks | "Run the implement prompt — next: {task title}." |
| Track has all tasks done | "Run the review prompt, or the build prompt to automate review → qa → ship." |
| Track reviewed, ready to merge | "Run the QA prompt then the ship prompt." |
| All roadmap features complete | "All features done! Run the roadmap prompt to add more or prepare for deployment." |

Format the recommendation prominently:

```
> Next action: run the implement prompt for auth-client
  (Task T-2.3: Add token refresh logic)
```

### 4. Git branch reminder

If the current branch doesn't match the active track's branch, note it:
"You're on branch `main` but the active track uses `feat/002-auth-client`. Switch with `git checkout feat/002-auth-client`."
