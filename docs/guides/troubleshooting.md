# Troubleshooting

## "Worker worktrees did not start from this branch"

`/build` stopped before merging because a worker's `base_sha` did not match your branch's `HEAD`. Claude Code started the worktree from the default branch. Set

```json
{ "worktree": { "baseRef": "head" } }
```

in your user or project settings, restart the session, and re-run `/build`. Or use `--isolate=none`. Nothing was merged, so it is safe to retry.

## "Uncommitted changes outside this track"

Worktree isolation needs a clean `HEAD` containing all previous work. `/build` auto-commits only `specs/NNN-feature/` and the declared `Files` of finished tasks. Commit or stash anything else, or use `--isolate=none`.

## "Merge conflict between T-x and earlier tasks"

Two tasks of one wave edited overlapping lines even though their `Files` were disjoint on paper (or a directory entry covered the other's file). `/build` aborted that merge and re-runs the task alone. Fix the `Files`/`Depends-on` of the two tasks in `tasks.md`; the task will otherwise run serially each time.

## "Out-of-scope edit by a worker"

A worker changed a file not listed in its `Files`. In worktree mode the task is rejected and not merged; in shared mode the build stops. Add the file to the task's `Files` (and to `Depends-on` if another task owns it) or fix the plan.

## A reviewer returned no valid report

The reviewer is relaunched once; if it fails again `review.md` records "reviewer returned no valid report" for that role instead of inventing findings. Re-run `/review`.

## "Commit the foundation artifacts to main first"

`/specify` creates the worktree from `main`; uncommitted `PRD.md`, `CLAUDE.md`, `DESIGN.md` or `specs/` would be missing in it. Commit them.

## Convergence stalled

A round did not reduce the number of failing criteria plus blocker/major issues. Read the remaining issues in `review.md`; typically a criterion is unachievable as written (run `/clarify`) or the plan is wrong (edit `plan.md`, re-run `/tasks`).

## Leftover worktrees

After a crash you may find `worktree-agent-*` worktrees:

```bash
git worktree list
git worktree remove --force .claude/worktrees/<name>   # after checking it holds nothing you need
git branch -D worktree-agent-<id>
git worktree prune
```

Claude Code also sweeps old subagent worktrees automatically (see its worktree documentation).

## `/specify` can't create a worktree

Claude Code refuses worktrees when `.claude` or `.claude/worktrees` is a symlink, and in repositories with certain git configuration (filter drivers, `includeIf`). The error message names the cause. Fallback: `git switch -c feat/NNN-name` in the main checkout (single-feature mode).

## Agents not found

Installed with `install.sh`: make sure `.claude/agents/` contains the four agent files (re-run the script). Installed as a plugin: agents are `feature-flow:<name>`. The commands fall back to a `general-purpose` agent with the agent file as its role if a type is unavailable.
