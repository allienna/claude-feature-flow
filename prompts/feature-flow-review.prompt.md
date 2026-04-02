---
mode: agent
description: "Review a completed feature against its spec — checks acceptance criteria, architecture compliance, and quality gates"
tools: ['editFiles', 'runCommands', 'search', 'codebase', 'runTests', 'problems', 'changes']
---

# Review

Review a completed feature against its specification, checking acceptance criteria, architecture decisions, and quality gates.

## Step 0: Detect current state

1. Search for `specs/*/spec.md` to find all feature tracks
2. For each track found, read its `spec.md` and check for `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md
   - If tasks.md exists, count `[x]` (done) and `[ ]` (pending) items

### State routing

**No tracks exist →** "Nothing to review. Start with the roadmap prompt." STOP.

**No feature name provided →** Find the first track where all tasks are checked but no review.md exists. Propose: "Ready to review **{feature-name}** ({total} tasks completed). Proceed?" Wait for confirmation.

**Feature name provided, no matching track →** "No spec for '{feature-name}'." STOP.

**Feature name provided, track exists →** Check state:
- No tasks → "No tasks yet. Run the tasks prompt first." STOP.
- Unchecked tasks remain → "There are {remaining} unfinished tasks. Complete them with the implement prompt first, or confirm to review partial progress." Wait for confirmation.
- Review already exists → "Review already done. Overwrite it?" Wait for confirmation.
- All tasks done, no review → Proceed to Step 1.

---

## Step 1: Load artifacts

Read:
- `specs/{NNN}-{feature-name}/spec.md` — Acceptance criteria
- `specs/{NNN}-{feature-name}/plan.md` — Architecture decisions
- `specs/{NNN}-{feature-name}/tasks.md` — Task list
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
If `specs/constitution.md` exists, verify each principle against the implementation. Otherwise: "No constitution found — run the constitution prompt to create one. Skipping compliance checks."

### 4.2 Error handling
If the spec or PRD defines error handling patterns, verify they are followed.
Search for error handling patterns in the source files modified by this feature.

### 4.3 Codebase patterns
Read `CLAUDE.md` for "Key patterns" or architectural conventions. Verify the implementation follows them.
If CLAUDE.md defines specific patterns (e.g., structured error returns, response formatting), search for adherence.

### 4.4 Acceptance criteria
For each acceptance criterion in the spec, verify:
- Is there code that implements it?
- Is there a test that covers it?
- Does it pass?

## Step 5: Write review.md

Create `specs/{NNN}-{feature-name}/review.md`:

```markdown
# Review: {Feature Name}

**Date**: {today}
**Reviewer**: Copilot (automated)

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
{If specs/constitution.md exists, check each principle. Otherwise: "No constitution — run the constitution prompt to create one."}

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
   - Suggest: "Run the QA prompt for a project-wide health check, then the ship prompt to create the PR."
   - Check roadmap for next feature: "Next from the roadmap: **{next-feature}** — run the specify prompt"
3. If needs work:
   - List exact fixes needed
   - "Fix these, then run the review prompt again."
