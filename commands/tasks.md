---
description: Break a plan into atomic tasks. Auto-detects the feature if no argument given.
argument-hint: "[feature-name]"
allowed-tools: Bash(ls:*), Read, Write, Grep, Glob
---

# Tasks

## Step 0: Detect current state

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

Create `specs/{NNN}-$ARGUMENTS/tasks.md`:

### Rules for good tasks
1. **One concern per task** — "Add user search endpoint" not "Add all search endpoints"
2. **Ordered by dependency** — T-1.2 can depend on T-1.1, never reverse
3. **Backend before integration** — Models → services → endpoints → wiring → tests
4. **Each task has a test** — command to run or behavior to check
5. **Max scope** — 1 new file + 2-3 modifications per task

```markdown
# Tasks: {Feature Name}

**Plan**: specs/{NNN}-{feature-name}/plan.md
**Status**: Ready
**Total**: {X} tasks across {Y} phases

## Phase 1: {Name}

- [ ] **T-1.1**: {Task title}
  - **Do**: {Precise description — files to create/modify, functions to implement}
  - **Test**: {Verification command — use the test command and selector syntax from CLAUDE.md, e.g., `{test_command} {test_selector}`}

- [ ] **T-1.2**: ...

## Phase 2: {Name}

- [ ] **T-2.1**: ...
```

## Step 3: Update status

Update spec.md status to "In Progress".
Update specs/roadmap.md feature status to "In Progress".

## Step 4: Present for review

1. Summary table: Phase → tasks count
2. Total task count and estimated scope
3. **"Ready to build! Run `/implement $ARGUMENTS` to start with T-1.1, or `/build $ARGUMENTS` to automate all tasks."**
