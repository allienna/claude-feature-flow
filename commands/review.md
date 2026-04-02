---
description: Review a completed feature against its spec. Auto-detects the feature if no argument given.
argument-hint: "[feature-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Review

## Step 0: Detect current state

Use your native tools to collect project state:

1. Use `Glob("specs/[0-9]*/spec.md")` to find all feature tracks
2. For each track found, read its `spec.md` and check for `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md
   - If tasks.md exists, count `[x]` (done) and `[ ]` (pending) items

### State routing

**No tracks exist →** "Nothing to review. Start with `/roadmap`." STOP.

**`$ARGUMENTS` is empty →** Find the first track where all tasks are checked but no review.md exists. Propose: "Ready to review **{feature-name}** ({total} tasks completed). Proceed?" Wait for confirmation.

**`$ARGUMENTS` provided, no matching track →** "No spec for '$ARGUMENTS'." STOP.

**`$ARGUMENTS` provided, track exists →** Check state:
- No tasks → "No tasks yet. Run `/tasks $ARGUMENTS` first." STOP.
- Unchecked tasks remain → "There are {remaining} unfinished tasks. Complete them with `/implement $ARGUMENTS` first, or confirm to review partial progress." Wait for confirmation.
- Review already exists → "Review already done. Overwrite it?" Wait for confirmation.
- All tasks done, no review → Proceed to Step 1.

---

## Step 1: Load artifacts

Read:
- `specs/{NNN}-$ARGUMENTS/spec.md` — Acceptance criteria
- `specs/{NNN}-$ARGUMENTS/plan.md` — Architecture decisions
- `specs/{NNN}-$ARGUMENTS/tasks.md` — Task list
- `specs/constitution.md` — Non-negotiable principles (if it exists)
- `PRD.md` — Error handling patterns, relevant requirements (if it exists)

## Step 2: Task completion check

Verify all tasks checked. List any `[BLOCKED]` tasks.

## Step 3: Quality checks

### Discover and run build commands

Read `CLAUDE.md` and extract test, lint, format, and type check commands.

If `CLAUDE.md` is missing or doesn't define build commands: WARN "No build commands found in CLAUDE.md — skipping automated quality checks. Add a '## Build & Run Commands' section to enable them."

Run each discovered command and record results.

## Step 4: Spec-specific checks

Review the implementation against patterns defined in the spec and constitution:

### 4.1 Constitution compliance
If `specs/constitution.md` exists, verify each principle against the implementation. Otherwise: "No constitution found — run `/constitution` to create one. Skipping compliance checks."

### 4.2 Error handling
If the spec or PRD defines error handling patterns, verify they are followed.
Use Grep to search for error handling patterns in the source files modified by this feature.

### 4.3 Codebase patterns
Read `CLAUDE.md` for "Key patterns" or architectural conventions. Verify the implementation follows them.
If CLAUDE.md defines specific patterns (e.g., structured error returns, response formatting), grep for adherence.

### 4.4 Acceptance criteria
For each acceptance criterion in the spec, verify:
- Is there code that implements it?
- Is there a test that covers it?
- Does it pass?

## Step 5: Write review.md

Create `specs/{NNN}-$ARGUMENTS/review.md`:

```markdown
# Review: {Feature Name}

**Date**: {today}
**Reviewer**: Claude Code (automated)

## Task Completion
- Total: {X} | Completed: {Y} | Blocked: {Z}

## Acceptance Criteria
| # | Criterion | Status | Notes |
|---|---|---|---|
| AC-1 | ... | PASS / FAIL / WARN | ... |

## Architecture Compliance
| Decision | Followed? | Notes |
|---|---|---|
| AD-1 | PASS / FAIL | ... |

## Quality Gates
| Check | Status | Details |
|---|---|---|
| Test | PASS/FAIL/SKIP | {result or "No test command in CLAUDE.md"} |
| Lint | PASS/FAIL/SKIP | {result or "No lint command in CLAUDE.md"} |
| Format | PASS/FAIL/SKIP | {result or "No format command in CLAUDE.md"} |
| Type check | PASS/FAIL/SKIP | {result or "No type check command in CLAUDE.md"} |

## Spec Compliance
| Check | Status | Notes |
|---|---|---|
| Error handling | PASS/FAIL/N/A | {matches spec patterns?} |
| Codebase patterns | PASS/FAIL/N/A | {follows CLAUDE.md conventions?} |

## Constitution Compliance
{If specs/constitution.md exists, check each principle. Otherwise: "No constitution — run `/constitution` to create one."}

| Principle | Status | Notes |
|---|---|---|

## Issues Found
| Severity | Description | Fix |
|---|---|---|

## Verdict
**{Ready to merge / Pass with notes / Needs work}**
```

## Step 6: Update statuses

If ready to merge: update spec.md status to "Complete", update specs/roadmap.md feature status to "Complete".

## Step 7: Present verdict and next steps

1. Show verdict
2. If ready to merge:
   - Suggest: "Run `/qa` for a project-wide health check, then `/ship $ARGUMENTS` to create the PR."
   - Check roadmap for next feature: "Next from the roadmap: **{next-feature}** — run `/specify`"
3. If needs work:
   - List exact fixes needed
   - "Fix these, then run `/review $ARGUMENTS` again."
