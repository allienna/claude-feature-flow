---
description: Review a completed feature against its spec. Auto-detects the feature if no argument given.
argument-hint: "[feature-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
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
- Review already exists → "Review already done. Overwrite it?" Wait for confirmation. (When called from `/build` during convergence, overwrite without asking and keep the `## Convergence History`.)
- All tasks done, no review → Proceed to Step 1.

---

## Step 1: Locate artifacts

Resolve the paths (do not read the source code yourself — the reviewers do):
- `specs/{NNN}-$ARGUMENTS/spec.md` — acceptance criteria
- `specs/{NNN}-$ARGUMENTS/plan.md` — architecture decisions
- `specs/{NNN}-$ARGUMENTS/tasks.md` — task list
- `specs/constitution.md`, `PRD.md`, `DESIGN.md` (only when the plan has a "Design Mobilization" section), `CLAUDE.md` — whichever exist

Read `CLAUDE.md` and extract the test, lint, format and type check commands. If missing: WARN "No build commands found in CLAUDE.md — quality gates will be SKIP. Add a '## Build & Run Commands' section to enable them."

## Step 2: Task completion check

Verify all tasks are checked. List any `[BLOCKED]` tasks. Check traceability: every `AC-n` appears in at least one task's `Covers`.

## Step 3: Independent review (fan-out)

The reviewers must not be the agent that wrote the code. Launch **both in a single message** (parallel):

1. `spec-reviewer` — spec/plan/constitution/DESIGN.md compliance, acceptance criteria with evidence.
2. `quality-reviewer` — build commands and code quality of the feature's diff.

(Plugin install: `subagent_type` is `claude-feature-flow:spec-reviewer` / `claude-feature-flow:quality-reviewer`; symlink install: bare names; if unavailable, use `general-purpose` with the matching `agents/*.md` as its role.)

Give each only: the artifact paths from Step 1, the build commands, and the base branch to diff against (`git merge-base HEAD main`). Wait for both (barrier). Each ends with one fenced `json` block; if a block is missing or malformed, relaunch that reviewer once, then record the review as `WARN: reviewer returned no valid report` instead of guessing.

## Step 4: Merge the reports (fan-in)

You are the only writer of `review.md`. Merge:
- **Acceptance criteria**: from `spec-reviewer.acceptance_criteria` (all ACs must be present; a missing AC is `WARN`)
- **Architecture / Constitution / Spec compliance**: from `spec-reviewer`
- **Quality gates**: from `quality-reviewer.quality_gates`
- **Issues**: union of both `issues` lists; deduplicate issues that point at the same cause (keep the highest severity and both fixes), sort by severity (`blocker` > `major` > `minor`)

Verdict rules (apply mechanically):
- **Needs work**: any `blocker` or `major` issue, any `FAIL` AC, or any quality gate `FAIL`
- **Pass with notes**: only `minor` issues or `WARN` items
- **Ready to merge**: no issue, no `WARN`

## Step 5: Write review.md

Create `specs/{NNN}-$ARGUMENTS/review.md`:

```markdown
# Review: {Feature Name}

**Date**: {today}
**Reviewers**: spec-reviewer, quality-reviewer (independent agents)

## Task Completion
- Total: {X} | Completed: {Y} | Blocked: {Z}

## Acceptance Criteria
| # | Criterion | Status | Evidence | Notes |
|---|---|---|---|---|
| AC-1 | ... | PASS / FAIL / WARN | file:line / test | ... |

## Traceability
| AC | Covered by tasks | Test |
|---|---|---|

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
| Design tokens applied | PASS/FAIL/N/A | {UI code uses declared tokens, no raw values} |
| Component inventory respected | PASS/FAIL/N/A | {no undeclared components rendered} |
| State coverage (loading/empty/error/success/offline) | PASS/FAIL/N/A | {all five handled per surface} |
| A11y baseline | PASS/FAIL/N/A | {focus, keyboard, contrast, reduced-motion, color-independence} |

## Constitution Compliance
{If specs/constitution.md exists, check each principle. Otherwise: "No constitution — run `/constitution` to create one."}

| Principle | Status | Notes |
|---|---|---|

## Issues Found
| Severity | Source | Location | Description | Fix |
|---|---|---|---|---|

## Convergence History
| Round | Failing ACs | Blocker+major issues | Verdict |
|---|---|---|---|

## Verdict
**{Ready to merge / Pass with notes / Needs work}**
```

## Step 6: Update statuses

If ready to merge (or pass with notes): update spec.md status to "Complete". (Do not edit `specs/roadmap.md`: a feature is complete for the roadmap once its track is merged into `main` with a "Complete" spec.)

## Step 7: Present verdict and next steps

1. Show verdict
2. If ready to merge:
   - Suggest: "Run `/qa` for a project-wide health check, then `/ship $ARGUMENTS` to create the PR."
   - Check roadmap for next feature: "Next from the roadmap: **{next-feature}** — run `/specify`"
3. If needs work — **convergence**:
   - List the exact fixes (the `fix` field of each blocker/major issue).
   - Propose: "Add these {N} corrective tasks to `tasks.md` (as `Phase C{round}`, with `Covers`/`Depends-on`/`Files`) and run `/build $ARGUMENTS`?" On confirmation, append them using the same task format and wave rules as `/tasks`, then stop. (`/build` does this automatically, up to `--max-rounds`.)
   - Otherwise: "Fix these, then run `/review $ARGUMENTS` again."
