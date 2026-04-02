---
description: Show project status and suggest the next action to take
allowed-tools: Bash(ls:*), Bash(git:*), Read, Grep, Glob
---

# Status

## Gather state

Use your native tools to collect project state:

1. Run `git branch --show-current` (Bash) to get the current branch
2. Read `specs/roadmap.md` to get the roadmap (if it doesn't exist, note "__NO_ROADMAP__")
3. Use `Glob("specs/[0-9]*/spec.md")` to find all feature tracks
4. For each track found, read its `spec.md`, and check for `plan.md`, `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md
   - If tasks.md exists, count `[x]` (done) and `[ ]` (pending) items, find the first pending task

## Present status

### 1. Roadmap overview

If no roadmap: "No roadmap. Run `/roadmap` to get started."

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
| No roadmap | "Run `/roadmap` to define your features." |
| Roadmap exists, no tracks | "Run `/specify` to start the first feature." |
| Track has draft spec | "Review and approve the spec, then `/plan {name}`." |
| Track has spec, no plan | "Run `/plan {name}`." |
| Track has plan, no tasks | "Run `/tasks {name}`." |
| Track has unchecked tasks | "Run `/implement {name}` — next: {task title}." |
| Track has all tasks done | "Run `/review {name}`, or `/build {name}` to automate review → qa → ship." |
| Track reviewed, ready to merge | "Run `/qa` then `/ship {name}`." |
| All roadmap features complete | "All features done! Run `/roadmap` to add more or prepare for deployment." |

Format the recommendation prominently:

```
> Next action: /implement auth-client
  (Task T-2.3: Add token refresh logic)
```

### 4. Git branch reminder

If the current branch doesn't match the active track's branch, note it:
"You're on branch `main` but the active track uses `feat/002-auth-client`. Switch with `git checkout feat/002-auth-client`."
