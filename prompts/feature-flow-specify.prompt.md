---
mode: agent
description: "Create a detailed feature specification — auto-detects the next feature from the roadmap"
tools: ['editFiles', 'runCommands', 'search', 'codebase', 'changes']
---

# Specify

Create a detailed feature specification with acceptance criteria, user stories, and error scenarios.

## Step 0: Detect current state

1. Read `specs/roadmap.md` (if it doesn't exist, note that no roadmap exists yet)
2. Search for `specs/*/spec.md` to find all feature tracks
3. For each track found, read its `spec.md` and check for `plan.md`, `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md

### State routing

**No roadmap exists →** "No roadmap found. Run the roadmap prompt first to define your features." STOP.

**No feature name provided →** Find the first feature in specs/roadmap.md whose status is "Not started" and has no matching track in `specs/`. Propose: "Next from the roadmap: **{feature-name}** — {summary}. Specify it?" Wait for confirmation.

**Feature name provided, track already exists →** Check what's already done:
- Has spec (Draft) → "A draft spec exists. Overwrite it, or move on with the plan prompt?"
- Has spec (Approved/In Progress) + no plan → "Spec is approved. Next step: run the plan prompt"
- Has plan + no tasks → "Plan exists. Next step: run the tasks prompt"
- Has tasks with unchecked items → "Tasks exist with work remaining. Next step: run the implement prompt"
- Has tasks all checked + no review → "All tasks done! Next step: run the review prompt"
- Has review → "Feature is complete."
→ In all cases, STOP and suggest the right next step. Don't redo work.

**Feature name provided, no track, not in roadmap →** "This feature isn't in the roadmap. Add it with the roadmap prompt first, or confirm to proceed as an unplanned feature."

**Feature name provided, no track, in roadmap, has unmet dependencies →** Warn about missing dependencies but allow override.

**All roadmap features have tracks →** "All features specified! Run the status prompt to see progress."

Only proceed to Step 1 if none of the above conditions cause a STOP.

---

## Step 1: Gather context

Read:
- `specs/roadmap.md` (get PRD sections and dependencies for this feature)
- `PRD.md` (focus on sections referenced in roadmap — if missing, WARN: "No PRD.md found. The spec will be based on roadmap information only.")
- `CLAUDE.md` (if missing, WARN: "No CLAUDE.md found. Conventions will not be incorporated into the spec.")

## Step 2: Check dependencies

From roadmap, verify each dependency has a track with status "In Progress" or "Complete".
Warn if unmet, but allow override.

## Step 3: Create the feature track

Determine next feature number. Create `specs/{NNN}-{feature-name}/` directory.
Create and switch to branch `feat/{NNN}-{feature-name}`.

## Step 4: Write spec.md

Create `specs/{NNN}-{feature-name}/spec.md`:

```markdown
# Spec: {Feature Name}

**Track ID**: {NNN}-{feature-name}
**Roadmap ref**: F-{NNN}
**Status**: Draft
**Created**: {today's date}
**Branch**: feat/{NNN}-{feature-name}
**PRD sections**: {from roadmap}
**Depends on**: {from roadmap, with status of each dependency}

## Context
Why are we building this? What problem does it solve?

## User Stories
- As a [persona], I want to [action] so that [benefit]

## Functional Requirements
### FR-1: {Requirement}
{Detailed description}

## API Endpoints Involved (if applicable)
| Source API | Method | Path | Purpose |
|------------|--------|------|---------|
{Relevant API endpoints or interfaces from the PRD, if applicable. Remove this section entirely if the project does not involve external APIs.}

## Error Scenarios
{How errors should be handled — reference the PRD's error handling section if it exists}

## Acceptance Criteria
- [ ] AC-1: {Testable criterion}

## Out of Scope
- {Explicit exclusions}

## Open Questions
- {Unresolved items needing human decision}
```

## Step 5: Update roadmap status

In `specs/roadmap.md`, update this feature's status from "Not started" to "Specifying".

## Step 6: Present for review

1. User stories (one line each)
2. Acceptance criteria
3. Open questions requiring input
4. Dependencies and their status
5. **"Review this spec. Once approved, run the plan prompt."**
