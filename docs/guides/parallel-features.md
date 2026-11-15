# Running several features in parallel

Goal: work on features `001-auth` and `003-search` at the same time, in two Claude Code sessions, without either touching the other's files.

## Prerequisites

- Foundations (`PRD.md`, `CLAUDE.md`, `DESIGN.md`, constitution, roadmap) are **committed on `main`**.
- Both features exist in the roadmap and are independent (neither lists the other under *Depends on*), or the dependency is already merged.
- `.claude/worktrees/` is in `.gitignore`.

## Step by step

**Session A** (in the main checkout):

```
/specify auth        # creates .claude/worktrees/001-auth on feat/001-auth and enters it
/clarify auth
/plan auth
/tasks auth
/build auth
```

**Session B** (a second terminal, in the main checkout):

```
/specify search      # creates .claude/worktrees/003-search on feat/003-search and enters it
...
```

Each session ends up inside its own worktree. They share the repository's history but not working files, branches, `tasks.md` or `review.md`.

Check progress from anywhere:

```
/status
Active worktrees
   001-auth      feat/001-auth      tasks 6/9
   003-search    feat/003-search    plan done
```

## Shipping and merging

Ship and merge each feature independently:

```
/ship auth           # confirm the commit message, PR opened
/merge <pr-number>   # squash merge; the worktree and branches are removed
```

The second feature to merge may need to update from `main` first (`git merge main` or rebase inside its worktree) if the first one touched shared files. Declare shared files (routers, registries, config) in each plan's *Parallelism Notes* to see this coming.

## Dependent features

You can specify, plan and break down a feature while its dependency is still in progress. `/build` refuses to start until the dependency is merged into `main`, because the code it needs must exist in the worktree. Merge the dependency, then update the dependent branch from `main` and build.

## Combining with parallel workers

Feature-level and worker-level isolation stack. Session A building with `--parallel=3` creates temporary worker worktrees under `.claude/worktrees/` too; they are removed when each wave finishes. Mind the cost: two sessions × three workers is six concurrent agents.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `/specify` stops: "Commit the foundation artifacts" | Uncommitted `PRD.md`, `specs/`… in the main checkout | Commit them to `main` first |
| Two features got the same number | Hand-made branches | Use `/specify`; numbers come from `F-NNN` |
| Roadmap shows nothing in progress | You read the file; statuses are derived | Run `/status` |
| Fixed-port tests fail when two builds run | Shared port/database between worktrees | Make ports configurable per worktree, or run one build at a time |
