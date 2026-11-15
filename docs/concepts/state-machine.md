# State machine

State is derived from files, never stored elsewhere.

## Spec status

```
Draft ──/plan──► Approved ──/tasks──► In Progress ──/review (OK)──► Complete
```

| Status | Set by | Meaning |
|---|---|---|
| Draft | `/specify` | Being written/clarified. May contain `[NEEDS CLARIFICATION]`. |
| Approved | `/plan` | Plan written. |
| In Progress | `/tasks` | Tasks exist; building. |
| Complete | `/review` | Verdict "Ready to merge" or "Pass with notes". |

## Roadmap status is derived

`specs/roadmap.md` is **not** edited by feature commands (parallel features would conflict on it). `/status` computes each feature's state:

| Condition | Derived status |
|---|---|
| No track in any worktree or on `main` | Not started |
| Track in a worktree | the spec's own Status |
| Track on `main` with a `Complete` spec | Complete |

## What a command can see

Features in progress live in their own worktrees, so commands that need a global view (`/status`, `/specify`) read `git worktree list` and look at every checkout.

## `/build` state routing

| On disk | `/build` resumes at |
|---|---|
| Unchecked tasks | Step 1: the first incomplete wave |
| All tasks checked, no review, or verdict "Needs work" | Step 2: review (and convergence) |
| Review OK, no QA | Step 3: QA |
| QA done, not shipped | Step 4: ship |
| All checked + verdict OK | "Run `/ship`" |

Because the only mutable state is checkboxes, review files and git history, an interrupted build is always safe to restart.

## Review verdict (mechanical)

| Verdict | Rule |
|---|---|
| Needs work | any `blocker` or `major` issue, any `FAIL` acceptance criterion, or any failing quality gate |
| Pass with notes | only `minor` issues or `WARN` items |
| Ready to merge | nothing to report |

## QA verdict

PASS = no WARN/FAIL (SKIP is fine) · WARN = any WARN, no FAIL · FAIL = any FAIL.
