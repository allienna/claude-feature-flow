---
description: Create a feature specification. Auto-detects the next feature if no argument given.
argument-hint: "[feature-name]"
allowed-tools: Bash(mkdir:*), Bash(ls:*), Bash(git:*), Read, Write, Edit, Grep, Glob, EnterWorktree
---

# Specify

## Step 0: Detect current state

Use your native tools to collect project state:

1. Read `specs/roadmap.md` (if it doesn't exist, note "__NO_ROADMAP__")
2. **Discover tracks in every checkout**: features in progress live in their own worktrees, so a track may not exist in your current directory. Run `git worktree list --porcelain` and `Glob("specs/[0-9]*/spec.md")` in the main checkout **and** in each listed worktree path. A feature "has a track" if any checkout has it.
3. For each track found, read its `spec.md` and check for `plan.md`, `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md

### State routing

**No roadmap exists →** "No roadmap found. Run `/roadmap` first to define your features." STOP.

**`$ARGUMENTS` is empty →** Find the first feature in specs/roadmap.md whose status is "Not started" and has no matching track in `specs/`. Propose: "Next from the roadmap: **{feature-name}** — {summary}. Specify it?" Wait for confirmation.

**`$ARGUMENTS` provided, track already exists →** Check what's already done:
- Has spec (Draft) → "A draft spec exists. Overwrite it, or move on with `/plan $ARGUMENTS`?"
- Has spec (Approved/In Progress) + no plan → "Spec is approved. Next step: `/plan $ARGUMENTS`"
- Has plan + no tasks → "Plan exists. Next step: `/tasks $ARGUMENTS`"
- Has tasks with unchecked items → "Tasks exist with work remaining. Next step: `/implement $ARGUMENTS`"
- Has tasks all checked + no review → "All tasks done! Next step: `/review $ARGUMENTS`"
- Has review → "Feature is complete."
→ In all cases, STOP and suggest the right command. Don't redo work.

**`$ARGUMENTS` provided, no track, not in roadmap →** "This feature isn't in the roadmap. Add it with `/roadmap` first, or confirm to proceed as an unplanned feature."

**`$ARGUMENTS` provided, no track, in roadmap, has unmet dependencies →** Warn about missing dependencies but allow override.

**All roadmap features have tracks →** "All features specified! Run `/status` to see progress."

Only proceed to Step 1 if none of the above conditions cause a STOP.

---

## Step 1: Gather context

Read:
- `specs/roadmap.md` (get PRD sections and dependencies for this feature)
- `PRD.md` (focus on sections referenced in roadmap — if missing, WARN: "No PRD.md found. The spec will be based on roadmap information only.")
- `CLAUDE.md` (if missing, WARN: "No CLAUDE.md found. Conventions will not be incorporated into the spec.")
- `DESIGN.md` if it exists. If it's missing, decide whether this feature is user-facing using the signals you *do* have — the roadmap entry, the PRD sections it references, and the feature name (anything involving UI, screens, pages, CLI output, or a named surface). If it looks user-facing and `DESIGN.md` is absent: "This feature looks user-facing but `DESIGN.md` is missing. Run `/design` first, or confirm to proceed without a design system." STOP and wait for confirmation.

## Step 2: Check dependencies

From roadmap, verify each dependency has a track (in any checkout) with status "In Progress" or "Complete".
Warn if unmet, but allow override. Also note which dependencies are **not yet merged into `main`**: specifying, planning and tasking can proceed in parallel, but `/build` will refuse to start until they are merged.

## Step 3: Create the feature worktree and track

**Number**: `{NNN}` is the numeric part of the roadmap id (`F-003` → `003`), never "the next free number" — parallel worktrees would collide. A feature with no roadmap entry gets the next number free across all checkouts and `feat/*` branches.

**Isolation**: each feature lives in its own git worktree, so several features can be specified, planned and built at the same time in separate sessions without touching each other's files.

1. **Foundations must be committed.** A new worktree starts from `main`, so `PRD.md`, `CLAUDE.md`, `DESIGN.md`, `specs/constitution.md` and `specs/roadmap.md` must be committed there. Run `git status --porcelain -- PRD.md CLAUDE.md DESIGN.md specs/` in the main checkout: if any of those is untracked or modified → STOP: "Commit the foundation artifacts to main first (suggested: `docs: add project foundations`)." and offer to do it (ask before committing).
2. **Create the worktree** from the main checkout root (use `git rev-parse --git-common-dir` to find it if you are already inside another worktree):
   `git worktree add .claude/worktrees/{NNN}-$ARGUMENTS -b feat/{NNN}-$ARGUMENTS main`
   If that worktree already exists, reuse it. If `.claude/worktrees/` is not git-ignored (`git check-ignore .claude/worktrees`), propose adding it to `.gitignore`.
3. **Enter it** with the `EnterWorktree` tool, using the path `.claude/worktrees/{NNN}-$ARGUMENTS`. All following steps, and every later command for this feature (`/clarify`, `/plan`, `/tasks`, `/build`, `/ship`), run **inside** this worktree.
4. Create `specs/{NNN}-$ARGUMENTS/` inside the worktree.

**Fallback**: not in a git repository, or no commit yet → skip the worktree, create the directory only, and WARN: "No git worktree isolation: initialize git and make a first commit to enable parallel features."

## Step 4: Write spec.md

Create `specs/{NNN}-$ARGUMENTS/spec.md`:

```markdown
# Spec: {Feature Name}

**Track ID**: {NNN}-{feature-name}
**Roadmap ref**: F-{NNN}
**Status**: Draft
**Created**: {today's date}
**Branch**: feat/{NNN}-{feature-name}
**Worktree**: .claude/worktrees/{NNN}-{feature-name}
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

## Design References (if applicable)
| Surface | Components used | New components needed |
|---------|-----------------|-----------------------|
{From DESIGN.md. List each surface this feature touches and which inventoried components it uses. If a needed component is NOT in the inventory, flag it here — `/design update` must run before `/implement`. Remove this section entirely if the feature has no user-facing surface.}

## Error Scenarios
{How errors should be handled — reference the PRD's error handling section if it exists}

## Acceptance Criteria
Each criterion is an executable scenario (Given/When/Then, or EARS: "When <trigger>, the system shall <response>"). It must be falsifiable by a test: observable inputs, observable outputs, no vague adjectives ("fast", "user-friendly", "robust").
- [ ] AC-1 (FR-1): **Given** {precondition} **When** {action} **Then** {observable outcome}
- [ ] AC-2 (FR-1, error): **Given** {precondition} **When** {invalid action} **Then** {specific error behavior}

Cover the happy path AND every scenario listed under "Error Scenarios". Every AC references the FR it verifies. `/tasks` links tasks to ACs and `/review` verifies each one.

## Out of Scope
- {Explicit exclusions}

## Open Questions
- [NEEDS CLARIFICATION: {question}] {Unresolved items needing a human decision. Never guess: mark the gap with this exact marker, in the section where the answer will land (a requirement, an AC, an error scenario) and list it here. `/clarify` resolves them; `/plan` refuses to run while any marker remains.}
```

## Step 5: Roadmap status

Do **not** edit `specs/roadmap.md`. Feature statuses are derived from the tracks (`/status` does this), and several features developing in parallel would otherwise all edit the same lines and conflict at merge time. `Not started` in the roadmap file only means "no track yet".

## Step 6: Present for review

1. User stories (one line each)
2. Acceptance criteria
3. Open questions requiring input (count of `[NEEDS CLARIFICATION]` markers)
4. Dependencies and their status
5. **If markers remain: "Run `/clarify $ARGUMENTS` to resolve them." Otherwise: "Review this spec. Once approved, run `/plan $ARGUMENTS`."** (Running `/clarify` is also worthwhile when the spec looks ambiguous even without markers.)
