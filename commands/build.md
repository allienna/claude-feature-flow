---
description: "Full pipeline: implement all tasks → review → qa → ship. Use /build quick to skip review and ship."
argument-hint: "[quick] [feature-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Build — Automated Feature Pipeline

Orchestrates: `/implement` (loop all tasks) → `/review` → `/qa` → `/ship`

**Modes**:
- `/build [feature]` — Full pipeline: implement all → review → qa → ship
- `/build quick [feature]` — Implement all → qa quick (skip review + ship)

Parse `$ARGUMENTS`: if the first word is `quick`, set `QUICK_MODE=true` and treat the rest as the feature name. Otherwise `QUICK_MODE=false` and the entire argument is the feature name.

---

## Step 0: Detect state

Use your native tools to collect project state:

1. Use `Glob("specs/[0-9]*/spec.md")` to find all feature tracks
2. For each track found, read its `spec.md` and check for `plan.md`, `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md
   - If tasks.md exists, count `[x]` (done) and `[ ]` (pending) items

### Discover build commands

Read `CLAUDE.md` and extract test, lint, format, and type check commands. If `CLAUDE.md` is missing or doesn't define build commands: WARN "No build commands found in CLAUDE.md. The build pipeline will implement tasks but cannot run automated checks. Add a '## Build & Run Commands' section to enable quality gates."

### State routing

**No tracks exist →** "No features found. Start with `/roadmap`." STOP.

**Feature name is empty →** Find the first track that has tasks.md with unchecked items. Propose: "Building **{feature-name}** — {pending} tasks remaining. Proceed?" Wait for confirmation.

**Feature name provided, no matching track →** "No spec for '{name}'. Run `/specify {name}` first." STOP.

**Feature name provided, track exists →** Check state:
- No plan → "No plan. Run `/plan {name}` first." STOP.
- No tasks → "No tasks. Run `/tasks {name}` first." STOP.
- All tasks checked + review exists → "Feature already complete. Run `/ship {name}` to create the PR." STOP.
- Has unchecked tasks → Proceed to Step 1.
- All tasks checked, no review → Skip to Step 2 (or Step 3 in quick mode).

Print mode: "**Build mode**: {full | quick}" and proceed.

---

## Step 1: Implement loop

Read `specs/{NNN}-{feature}/tasks.md`. Count pending `- [ ]` tasks.

Print: "**Implementing {feature}** — {pending}/{total} tasks remaining"

For each pending `- [ ]` task, in order:

### 1a. Load context
Read:
- `specs/{NNN}-{feature}/spec.md` and `plan.md`
- `CLAUDE.md`
- Source files that this task modifies

### 1b. Implement
Implement the task fully. Follow existing codebase patterns.

### 1c. Run tests
Run the test, lint, and format commands discovered from `CLAUDE.md`. If no commands were found, WARN and skip.

Fix failures and explain what went wrong.

### 1d. Mark complete
In tasks.md, change `- [ ]` to `- [x]` for this task.

### 1e. Report progress
Print: "T-X.Y — {title} ({done}/{total})"

### 1f. Gate check
**If tests failed and could not be fixed → STOP.**
Print: "Build stopped at T-X.Y — {failure reason}. Fix the issue and re-run `/build {feature}` to resume."
Do NOT continue to the next task.

After all tasks complete, print: "All {total} tasks implemented."

---

## Step 2: Review (full mode only)

**If `QUICK_MODE=true` → skip to Step 3.**

Run the `/review` procedure:
1. Load artifacts (spec, plan, tasks)
2. Task completion check
3. Quality checks (using commands from CLAUDE.md)
4. Spec-specific checks (verify implementation matches spec requirements)
5. Write review.md

### Gate check
- **Verdict: "Needs work"** → STOP. Print: "Build stopped at review — fixes needed. See `specs/{NNN}-{feature}/review.md` for details. Fix issues and re-run `/build {feature}`."
- **Verdict: "Ready to merge" or "Pass with notes"** → Continue to Step 3.

---

## Step 3: QA

Run the `/qa` procedure:
- **Full mode**: Run full QA
- **Quick mode**: Run `/qa quick` (automated checks only)

### Gate check
- **Verdict: FAIL** → STOP. Print: "Build stopped at QA — see `qa-report.md` for details. Fix issues and re-run `/build {feature}`."
- **Verdict: PASS or WARN** → Continue to Step 4 (or STOP in quick mode).

**If `QUICK_MODE=true` → STOP here.** Print: "Quick build complete — {total} tasks implemented, QA {verdict}. Run `/review {feature}` then `/ship {feature}` when ready."

---

## Step 4: Ship (full mode only)

Run the `/ship` procedure:
- Create branch (if not already on feature branch)
- Stage and commit with message: `feat({NNN}): {feature name}`
- Push and open PR

---

## Resume behavior

`/build` auto-detects state and resumes from where it left off:
- Unchecked tasks → resumes at Step 1 (first unchecked task)
- All tasks done, no review → resumes at Step 2
- Review done, no QA → resumes at Step 3
- QA done, not shipped → resumes at Step 4
