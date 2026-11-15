---
description: Break a plan into atomic tasks. Auto-detects the feature if no argument given.
argument-hint: "[feature-name]"
allowed-tools: Bash(git:*), Bash(ls:*), Read, Write, Edit, Grep, Glob, EnterWorktree
---

# Tasks

## Step 0: Detect current state

**Locate the track first.** Features in progress live in their own git worktrees (`.claude/worktrees/{NNN}-{name}`), so `specs/{NNN}-{name}/` may not exist in your current directory. If a feature name is given and its `spec.md` is not found here, run `git worktree list --porcelain` and look in each worktree. If it is found in another worktree, switch to it with the `EnterWorktree` tool (`path` = that worktree) and continue from there; if it exists nowhere, use the usual "run `/specify`" message. With no feature name, consider the tracks of all worktrees and prefer the one in your current worktree.

Use your native tools to collect project state:

1. Use `Glob("specs/[0-9]*/spec.md")` to find all feature tracks
2. For each track found, read its `spec.md` and check for `plan.md`, `tasks.md`
   - Extract the **Status** field from spec.md
   - If tasks.md exists, count `[x]` (done) and `[ ]` (pending) items

### State routing

**No tracks exist →** "No features found. Start with `/roadmap` then `/specify`." STOP.

**`$ARGUMENTS` is empty →** Find the first track that has a plan but NO tasks.md. Propose: "Ready to create tasks for **{feature-name}**. Proceed?" Wait for confirmation.

**`$ARGUMENTS` provided, no matching track →** "No spec found for '$ARGUMENTS'. Run `/specify $ARGUMENTS` first." STOP.

**`$ARGUMENTS` provided, track exists →** Check state:
- No plan → "No plan yet. Run `/plan $ARGUMENTS` first." STOP.
- Has tasks, none completed → "Tasks already exist (0 done). Overwrite them, or start with `/implement $ARGUMENTS`?"
- Has tasks, some completed → "Tasks in progress ({done}/{total} completed). Overwrite will lose progress! Continue implementing with `/implement $ARGUMENTS` instead?" Wait for explicit confirmation to overwrite.
- Has tasks, all completed → "All {total} tasks done! Next step: `/review $ARGUMENTS`" STOP.
→ STOP and suggest unless user confirms overwrite.

Only proceed to Step 1 if the track has a plan and no tasks, OR user confirms overwrite.

---

## Step 1: Read the plan

Read:
- `specs/{NNN}-$ARGUMENTS/spec.md`
- `specs/{NNN}-$ARGUMENTS/plan.md`
- `CLAUDE.md` (coding conventions — if missing, WARN: "No CLAUDE.md found. Tasks will be created without project conventions context.")

## Step 2: Write tasks.md

Create `specs/{NNN}-$ARGUMENTS/tasks.md`.

### Rules for good tasks
1. **One concern per task** — "Add user search endpoint" not "Add all search endpoints"
2. **Explicit dependencies** — every task declares `Depends-on` (task ids, or `none`). T-1.2 can depend on T-1.1, never reverse
3. **Backend before integration** — Models → services → endpoints → wiring → tests
4. **Each task has a test** — command to run or behavior to check
5. **Max scope** — 1 new file + 2-3 modifications per task
6. **Declared write scope** — every task lists the exact files it creates or modifies in `Files`. This is the contract `/build` uses to run tasks in parallel safely and to detect out-of-scope edits
7. **Traceable** — every task lists the acceptance criteria it advances in `Covers` (`AC-n`). Pure scaffolding tasks may use `Covers: none`

```markdown
# Tasks: {Feature Name}

**Plan**: specs/{NNN}-{feature-name}/plan.md
**Status**: Ready
**Total**: {X} tasks across {Y} phases, {W} execution waves

## Phase 1: {Name}

- [ ] **T-1.1**: {Task title}
  - **Covers**: AC-1, AC-2
  - **Depends-on**: none
  - **Files**: `src/models/user.py` (new), `src/models/__init__.py`
  - **Do**: {Precise description — files to create/modify, functions to implement}
  - **Test**: {Verification command — use the test command and selector syntax from CLAUDE.md, e.g., `{test_command} {test_selector}`}

- [ ] **T-1.2** [P]: {Task title}
  - **Covers**: AC-3
  - **Depends-on**: T-1.1
  - **Files**: `src/services/search.py` (new)
  - **Do**: ...
  - **Test**: ...

## Phase 2: {Name}

- [ ] **T-2.1**: ...

## Execution Waves

| Wave | Tasks | Parallel? |
|------|-------|-----------|
| 1 | T-1.1 | no |
| 2 | T-1.2, T-1.3 | yes |
```

### Compute the execution waves

A **wave** is a set of tasks that can run at the same time. Compute them deterministically:

1. `wave(T) = 1` if `Depends-on` is `none`, else `1 + max(wave(d))` over its dependencies. A dependency cycle is an error: fix the tasks, do not write the file.
2. Within one wave, if two tasks share any path in `Files` (same file, or one is a directory containing the other's file), move the **later** task to the next wave and re-propagate to its dependents. Tasks in a wave must have pairwise-disjoint `Files`.
3. Tasks that end up in a wave with at least one other task get the `[P]` marker. Single-task waves have no marker.
4. Write the `## Execution Waves` table and the wave count in the header.

Order of tasks inside the file stays "phase order"; waves are the execution contract. A task without `Depends-on`/`Files` (hand-edited or legacy `tasks.md`) is executed alone, in file order — never in parallel.

### Coverage check (before writing)

Every `AC-n` of `spec.md` must appear in the `Covers` of at least one task. If an AC is uncovered, add the task that covers it (or, if the AC is not implementable as written, STOP and tell the user to run `/clarify`). Print the AC → tasks matrix in the review step.

## Step 3: Update status

Update spec.md status to "In Progress". (Do not edit `specs/roadmap.md`: statuses are derived from tracks so parallel features never conflict.)

## Step 4: Present for review

1. Summary table: Phase → tasks count
2. Execution waves table (and how many tasks can run in parallel)
3. AC → tasks coverage matrix (no uncovered AC)
4. Total task count and estimated scope
5. **"Ready to build! Run `/implement $ARGUMENTS` to start with T-1.1, or `/build $ARGUMENTS` to automate all tasks (parallel by waves)."**
