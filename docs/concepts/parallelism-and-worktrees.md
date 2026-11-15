# Parallelism and worktrees

Isolation happens at **two levels**. They solve different problems and are independent.

| Level | Unit | Problem solved | Mechanism |
|---|---|---|---|
| **Feature** | one feature = one worktree + branch | Two features in progress can't share a checkout (switching branches discards the other's working state) | `/specify` creates `.claude/worktrees/NNN-name` on `feat/NNN-name` |
| **Worker** | one task of a wave = one temporary worktree + branch | Parallel workers must not see each other's half-written files, which break tests | `/build` runs each `implementer` with `isolation: worktree`, then merges |

## Why worktrees (and not only disjoint `Files`)

Disjoint `Files` prevent two workers from **writing** the same file. They do not prevent **test pollution**: worker A's test run fails because worker B's file is half-written; build tools with shared caches or locks collide; a failed worker leaves partial edits in the shared tree. A worktree gives each worker a private tree, a clean rollback (discard the worktree), and a safety net if `Files` was declared wrong (the merge conflicts instead of silently overwriting).

The cost: a fresh checkout has no installed dependencies and no ignored files, services and ports are shared, and results must be merged. `/build` therefore only isolates **waves with 2+ tasks**; single-task waves run in place.

## Feature level

```
repo/                              main checkout (branch: main) — foundations, merged features
repo/.claude/worktrees/
  001-auth/                        branch feat/001-auth       ← session A
  003-search/                      branch feat/003-search     ← session B
```

- **Numbering** comes from the roadmap id (`F-003` → `003`), so parallel worktrees can never pick the same number.
- **Foundations first:** a new worktree starts from `main`. `PRD.md`, `CLAUDE.md`, `DESIGN.md`, the constitution and the roadmap must be committed on `main` before `/specify` (it checks and offers to commit).
- **No shared status file:** feature commands never edit `specs/roadmap.md`. Status is derived from tracks, so parallel features never conflict.
- **Dependencies:** you can specify/plan/task a feature whose dependencies are still in progress; `/build` refuses to start until they are merged into `main` (their code must exist).
- **Cleanup:** `/merge` leaves the worktree, squash merges, removes the worktree and branches.
- **Gitignore:** add `.claude/worktrees/`.

See the [parallel features guide](../guides/parallel-features.md).

## Worker level

For a wave with 2+ tasks (default `--isolate=worktree`):

1. **Baseline** — worktrees start from the branch's `HEAD`, so everything done so far must be committed. If the tree is dirty, `/build` commits only the track's files as `chore(build): wave N baseline` (these commits vanish in the squash merge). Dirty paths outside the track stop the build.
2. **Fan-out** — each worker gets its own worktree and branch, runs the **Worktree Setup** commands from `CLAUDE.md`, implements its task, runs the task's test, and commits once.
3. **Base guard** — each report carries `base_sha`; it must equal the baseline `HEAD`. If not, the worktrees did not start from your feature branch (see below) and the build stops before merging anything.
4. **Scope check** — `git diff --name-only BASE..branch` must be inside the task's `Files`.
5. **Merge** — branches are merged one at a time (`git merge --no-ff`), in task order. A conflict aborts that merge and re-runs the task alone in the next batch: it means the declared `Files` overlapped in practice.
6. **Wave checks** run on the integrated tree; then worker worktrees and branches are removed.

### The `worktree.baseRef` requirement

By default Claude Code starts subagent worktrees from the repository's default branch on the remote. For `/build` they must start from the current feature branch. Set:

```json
{ "worktree": { "baseRef": "head" } }
```

Inside a feature worktree, `"head"` resolves to that worktree's `HEAD`, which is what you want. The base guard detects a missing setting automatically, so you cannot silently build on the wrong base.

### What a worker worktree does not have

| Missing | Fix |
|---|---|
| Installed dependencies (`node_modules`, virtualenv…) | `## Worktree Setup` in `CLAUDE.md` ([guide](../guides/claude-md-setup.md)) |
| Gitignored files (`.env`, local config) | a `.worktreeinclude` file at the repository root |
| Your instruction files from the worktree's own `CLAUDE.md` | Subagents inherit the main conversation's instructions |
| Isolated ports, databases, external services | Use `--parallel=1` or `--isolate=none` for tests that bind fixed ports or share a database |

## When to use `--isolate=none`

Shared working tree, protected only by disjoint `Files` and a post-wave `git status` scope check. Choose it when per-worktree setup is too slow (large dependency installs), when the project is not a git repository, or when the wave's tests are fully independent. It is not recommended for waves whose tasks run tests touching shared build output.

## Limits

- `--parallel` default is 3 (a sensible start; 3–5 is the commonly reported range on disjoint files). Cost grows linearly with parallel workers.
- Worktrees need a git repository with at least one commit.
- Worker branches are named by Claude Code (`worktree-agent-…`); `/build` deletes them after merging or discarding.
