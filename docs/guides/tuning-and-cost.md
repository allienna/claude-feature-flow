# Tuning and cost

Parallel agents multiply token usage. These are the controls.

## `/build` options

| Option | Default | Effect |
|---|---|---|
| `--parallel=N` | 3 | Max concurrent workers per wave. Higher = faster wall-clock, linear cost, more merge risk. 3–5 is a sensible range; beyond that rarely pays off. |
| `--sequential` | | Same as `--parallel=1`: still isolated workers and independent review, no concurrency. |
| `--isolate=worktree\|none` | `worktree` for waves of 2+ | `none` = shared tree, cheaper setup, weaker isolation. |
| `--max-rounds=N` | 2 | Convergence rounds. Each round = new waves + a full review. |
| `quick` | | Implement + quick QA only: no review, no convergence, no ship. |

## Where tokens go

| Item | Cost driver |
|---|---|
| Workers | One fresh context per task; reads spec + plan + the files it touches |
| Review | Two agents read the feature's diff and artifacts |
| Convergence | A round repeats workers for corrective tasks and the whole review |
| Worktree setup | Shell time, not tokens — but each worker pays it |

Cheap wins: tasks with a small `Files` scope (workers read less), a sharp `plan.md`, and `/clarify` before `/plan` (re-planning is the most expensive correction).

## Models per agent

Agents inherit the session model unless their frontmatter says otherwise. Edit the `model:` line of an agent file to tune cost and quality, for example a lighter model for `qa-verifier` and your strongest for `spec-reviewer`. Precedence: per-invocation model, then the agent's `model`, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the session model.

## Claude Code limits to know

| Limit | Value |
|---|---|
| Concurrent subagents | 20 by default (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) |
| Subagent nesting depth | 3 (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) |

## Start small

Run the first `/build` on a feature of 4–6 tasks with `--parallel=2` and read `review.md` and the convergence history before scaling up.
