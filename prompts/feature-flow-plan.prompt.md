---
mode: agent
description: "Create a technical implementation plan from a feature spec — architecture decisions, affected files, and phases"
tools: ['editFiles', 'runCommands', 'search', 'codebase', 'problems']
---

# Plan

Create a technical implementation plan with architecture decisions, affected files, implementation phases, and test strategy.

## Step 0: Detect current state

1. Search for `specs/*/spec.md` to find all feature tracks
2. For each track found, read its `spec.md` and check for `plan.md`, `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md

### State routing

**No tracks exist →** "No feature specs found. Run the specify prompt first." STOP.

**No feature name provided →** Find the first track that has a spec but NO plan.md. Propose: "Ready to plan **{feature-name}**. Proceed?" Wait for confirmation.

**Feature name provided, no matching track →** "No spec found for '{feature-name}'. Run the specify prompt first." STOP.

**Feature name provided, track exists →** Check state:
- No spec → "No spec. Run the specify prompt first." STOP.
- Spec is Draft with open questions → "Spec has open questions. Resolve them first, then approve." STOP.
- Has plan + no tasks → "Plan already exists. Overwrite it, or move on with the tasks prompt?"
- Has plan + tasks with unchecked items → "Plan and tasks exist. Next step: run the implement prompt"
- Has plan + tasks all checked → "Everything done! Next step: run the review prompt"
→ STOP and suggest unless user confirms overwrite.

Only proceed to Step 1 if the track has a spec (Draft or Approved) and no plan, OR user confirms overwrite.

---

## Step 1: Read the spec and context

Read:
- `specs/{NNN}-{feature-name}/spec.md`
- `PRD.md` (sections referenced in the spec — if missing, WARN: "No PRD.md found. Plan will be based on spec only.")
- `CLAUDE.md` (if missing, WARN: "No CLAUDE.md found. Plan will not incorporate project conventions.")

## Step 2: Analyze existing codebase

Scan the codebase:

### Discover project structure
- Look for config files (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, etc.) to identify the tech stack
- Search for source files (try `src/**/*`, `lib/**/*`, `app/**/*`, or detect from config)
- Search for test files (try `tests/**/*`, `test/**/*`, `__tests__/**/*`, `*_test.*`)
- Read key files to understand current patterns (entry points, config, existing modules)

## Step 3: Write plan.md

Create `specs/{NNN}-{feature-name}/plan.md`:

```markdown
# Plan: {Feature Name}

**Spec**: specs/{NNN}-{feature-name}/spec.md

## Architecture Decisions

### AD-1: {Decision}
- **Choice**: {What}
- **Rationale**: {Why}
- **Alternatives considered**: {What else}

## Affected Files

### New Files
| File | Purpose |

### Modified Files
| File | Change |

## Implementation Phases

### Phase 1: {Name}
- Core data structures, interfaces, types
- Foundation that other phases depend on

### Phase 2: {Name}
- Business logic, service layer, integrations
- Builds on Phase 1 foundations

### Phase 3: {Name}
- Wiring, integration, end-to-end flows
- Tests and verification

(Add or remove phases as appropriate for the feature scope)

## Test Strategy
- **Mocking approach**: {Appropriate for the project's tech stack — detect from CLAUDE.md and existing tests}
- **Happy paths**: What to assert for each component
- **Error scenarios**: Common failure modes from the spec
- **Edge cases**: Boundary conditions specific to this feature

## Risk & Complexity
- **Estimated complexity**: Low / Medium / High
- **Key risks**: ...
- **New dependencies**: ...
```

## Step 4: Update spec status

Update spec.md status to "Approved".
Update specs/roadmap.md feature status to "Planning".

## Step 5: Present for review

1. Architecture decisions (one line each)
2. Phase breakdown with scope
3. Test strategy summary
4. **"Review this plan. Once approved, run the tasks prompt."**
