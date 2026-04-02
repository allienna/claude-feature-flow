---
description: Implement the next pending task. Auto-detects the feature if no argument given.
argument-hint: "[feature-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Implement

## Step 0: Detect current state

Use your native tools to collect project state:

1. Use `Glob("specs/[0-9]*/spec.md")` to find all feature tracks
2. For each track found, read its `spec.md` and check for `plan.md`, `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md
   - If tasks.md exists, count `[x]` (done) and `[ ]` (pending) items, find the first pending task

### State routing

**No tracks exist →** "No features found. Start with `/roadmap`." STOP.

**`$ARGUMENTS` is empty →** Find the first track that has tasks.md with unchecked items. Propose: "Continuing **{feature-name}** — next task: {task title} ({done}/{total}). Go?" Wait for confirmation.

**`$ARGUMENTS` provided, no matching track →** "No spec for '$ARGUMENTS'. Run `/specify $ARGUMENTS` first." STOP.

**`$ARGUMENTS` provided, track exists →** Check state:
- No plan → "No plan. Run `/plan $ARGUMENTS` first." STOP.
- No tasks → "No tasks. Run `/tasks $ARGUMENTS` first." STOP.
- All tasks checked, no review → "All {total} tasks done! Run `/review $ARGUMENTS` to review." STOP.
- All tasks checked, review exists → "Feature complete. Start the next feature with `/specify`." STOP.
- Has unchecked tasks → Proceed to Step 1.

### Discover build commands

Read `CLAUDE.md` and extract:
- **Test command**: (e.g., `pytest`, `jest`, `go test`, `cargo test`)
- **Lint command**: (e.g., `ruff check`, `eslint`, `golangci-lint`)
- **Format command**: (e.g., `ruff format`, `prettier`, `gofmt`)

If `CLAUDE.md` is missing or doesn't define build commands: WARN "No build commands found in CLAUDE.md. Tasks will be implemented without automated checks. Consider adding a '## Build & Run Commands' section."

---

## Step 1: Find the next task

Read `specs/{NNN}-$ARGUMENTS/tasks.md`. Find the first `- [ ]` task.

## Step 2: Load context

Read:
- `specs/{NNN}-$ARGUMENTS/spec.md` and `plan.md`
- `CLAUDE.md`
- Source files that this task modifies (if they exist)

## Step 3: Implement

Implement the task fully based on the **Do** field. Key guidelines:
- Follow patterns established in the existing codebase
- Follow coding conventions from `CLAUDE.md` (if it exists)
- Follow error handling patterns from the spec and PRD (if they exist)
- Type all function signatures where the language supports it

## Step 4: Run tests

Run the specific test from the task's **Test** field using the test command discovered from `CLAUDE.md`.

Then run lint and format commands if they were discovered.

If `CLAUDE.md` doesn't specify test/lint/format commands, WARN: "No test/lint commands found in CLAUDE.md — skipping automated checks."

Fix failures before proceeding.

## Step 5: Mark task complete

In tasks.md, change `- [ ]` to `- [x]` for this task.

## Step 6: Report

1. **Done**: Brief summary of what was implemented
2. **Tests**: Pass/fail
3. **Progress**: "{done}/{total} tasks ({percent}%)"
4. **Next**:
   - If more tasks: "Next: T-X.Z — {title}. Run `/implement $ARGUMENTS` to continue, or `/build $ARGUMENTS` to automate the rest."
   - If all done: "All tasks complete! Run `/review $ARGUMENTS`, or `/build $ARGUMENTS` for automated review → qa → ship."

IMPORTANT: ONE task only, then stop.
