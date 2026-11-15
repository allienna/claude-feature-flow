---
description: Show project status and suggest the next action to take
allowed-tools: Bash(ls:*), Bash(git:*), Read, Grep, Glob
---

# Status

## Gather state

Use your native tools to collect project state:

1. Run `git branch --show-current` (Bash) to get the current branch
2. Check for the foundational artifacts: `PRD.md`, `specs/constitution.md`, `DESIGN.md` — note which are present (each missing one is a possible "next action").
3. Read `specs/roadmap.md` to get the roadmap (if it doesn't exist, note "__NO_ROADMAP__")
4. Run `git worktree list --porcelain`. Features in progress live in their own worktrees (`.claude/worktrees/{NNN}-{feature}`), so use `Glob("specs/[0-9]*/spec.md")` in the main checkout **and** in every listed worktree, and merge the results (a track in a worktree wins over the same track on `main`).
5. For each track found, read its `spec.md`, and check for `plan.md`, `tasks.md`, `review.md`
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

### 2b. Active worktrees

If `git worktree list` shows more than the main checkout, list one line per feature worktree, so parallel work is visible at a glance:

```
Active worktrees
   001-auth        feat/001-auth        tasks 4/9    <- you are here
   003-search      feat/003-search      plan done
```

Statuses of roadmap features are **derived** from their tracks: no track = Not started; a track on `main` with a Complete spec = Complete; otherwise the spec's Status. `specs/roadmap.md` is not edited by feature commands.

### 3. Recommended action

Based on the state, suggest ONE clear next action. Evaluate the rows **top to bottom and stop at the first match** — the foundational artifacts (PRD → constitution → DESIGN → roadmap) take precedence over track-level state, since the workflow can't meaningfully proceed without them.

| State | Recommendation |
|---|---|
| No `PRD.md` | "Run `/prd` to define what you are building." |
| `PRD.md` exists, no `specs/constitution.md` | "Run `/constitution` to set the non-negotiables." |
| Constitution exists, no `DESIGN.md` | "Run `/design` to define the design system." |
| No roadmap | "Run `/roadmap` to define your features." |
| Roadmap exists, no tracks | "Run `/specify` to start the first feature." |
| Track has spec with `[NEEDS CLARIFICATION` markers | "Run `/clarify {name}` to resolve {N} open question(s)." |
| Track has draft spec | "Review and approve the spec, then `/plan {name}`. (`/clarify {name}` first if it feels ambiguous.)" |
| Track has spec, no plan | "Run `/plan {name}`." |
| Track has plan, no tasks | "Run `/tasks {name}`." |
| Track has tasks, never analyzed and spec/plan edited since | "Optional: `/analyze {name}` to cross-check artifacts before building." |
| Track has unchecked tasks | "Run `/implement {name}` — next: {task title}." |
| Track has all tasks done | "Run `/review {name}`, or `/build {name}` to automate review → convergence → qa → ship." |
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
