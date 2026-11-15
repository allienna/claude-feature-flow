# `implementer`

**Role.** Implements exactly one task from `tasks.md` in a fresh context and reports the result.

**Launched by.** `/build`, one instance per task of a wave, possibly in parallel and possibly in its own worktree.

**Input.** The task block (`id`, title, **Do**, **Test**, **Files**, **Covers**); paths to `spec.md`, `plan.md`, `CLAUDE.md`, `DESIGN.md`; the build commands; `mode` (`worktree` or `none`); in worktree mode the Worktree Setup commands; for a retry, the previous blockers.

**Hard rules.**
- Writes only inside the task's `Files`. Needs another file → `status: "blocked"` and names it.
- Never edits `tasks.md`, `spec.md`, `plan.md`, `review.md` or `roadmap.md`.
- Runs only the task's **Test**, never the full suite (the orchestrator runs wave checks once).
- `none` mode: no state-changing git. `worktree` mode: one final commit of specific files on its own branch; nothing else.
- Applies `DESIGN.md` tokens and components by name; never invents any.

**Report.**

```json
{
  "task_id": "T-1.1",
  "status": "done | failed | blocked",
  "summary": "…",
  "files_changed": ["…"],
  "tests_run": ["…"],
  "tests_passed": true,
  "blockers": [],
  "mode": "worktree | none",
  "base_sha": "worktree mode: HEAD before any change",
  "head_sha": "worktree mode: HEAD after the commit",
  "branch": "worktree mode: the branch name"
}
```

`done` requires `tests_passed: true`. Schema: [`implementer.schema.json`](../../schemas/implementer.schema.json). Source: [`agents/implementer.md`](../../agents/implementer.md).
