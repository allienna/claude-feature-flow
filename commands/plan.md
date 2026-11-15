---
description: Create a technical implementation plan from a spec. Auto-detects the feature if no argument given.
argument-hint: "[feature-name]"
allowed-tools: Bash(ls:*), Read, Write, Edit, Grep, Glob
---

# Plan

## Step 0: Detect current state

Use your native tools to collect project state:

1. Use `Glob("specs/[0-9]*/spec.md")` to find all feature tracks
2. For each track found, read its `spec.md` and check for `plan.md`, `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md

### State routing

**No tracks exist →** "No feature specs found. Run `/specify` first." STOP.

**`$ARGUMENTS` is empty →** Find the first track that has a spec but NO plan.md. Propose: "Ready to plan **{feature-name}**. Proceed?" Wait for confirmation.

**`$ARGUMENTS` provided, no matching track →** "No spec found for '$ARGUMENTS'. Run `/specify $ARGUMENTS` first." STOP.

**`$ARGUMENTS` provided, track exists →** Check state:
- No spec → "No spec. Run `/specify $ARGUMENTS` first." STOP.
- Spec contains any `[NEEDS CLARIFICATION` marker (use Grep) → "Spec has {N} unresolved clarification marker(s). Run `/clarify $ARGUMENTS` first." STOP.
- Spec has acceptance criteria that are not testable scenarios (no Given/When/Then or EARS form, or vague adjectives) → "AC-{n} is not testable as written. Run `/clarify $ARGUMENTS` to tighten it." STOP.
- Has plan + no tasks → "Plan already exists. Overwrite it, or move on with `/tasks $ARGUMENTS`?"
- Has plan + tasks with unchecked items → "Plan and tasks exist. Next step: `/implement $ARGUMENTS`"
- Has plan + tasks all checked → "Everything done! Next step: `/review $ARGUMENTS`"
→ STOP and suggest unless user confirms overwrite.

Only proceed to Step 1 if the track has a spec (Draft or Approved) and no plan, OR user confirms overwrite.

---

## Step 1: Read the spec and context

Read:
- `specs/{NNN}-$ARGUMENTS/spec.md`
- `PRD.md` (sections referenced in the spec — if missing, WARN: "No PRD.md found. Plan will be based on spec only.")
- `CLAUDE.md` (if missing, WARN: "No CLAUDE.md found. Plan will not incorporate project conventions.")
- `DESIGN.md` (if the spec has a "Design References" section). Pull the named tokens, components, and surfaces — the plan will cite them by name.

## Step 2: Analyze existing codebase

Use your native tools to scan the codebase:

### Discover project structure
- Look for config files (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, etc.) to identify the tech stack
- Use Glob to find source files (try `src/**/*`, `lib/**/*`, `app/**/*`, or detect from config)
- Use Glob to find test files (try `tests/**/*`, `test/**/*`, `__tests__/**/*`, `*_test.*`)
- Read key files to understand current patterns (entry points, config, existing modules)

## Step 3: Write plan.md

Create `specs/{NNN}-$ARGUMENTS/plan.md`:

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
- Name the files each piece creates or modifies — `/tasks` copies them into each task's `Files` scope

### Phase 2: {Name}
- Business logic, service layer, integrations
- Builds on Phase 1 foundations

### Phase 3: {Name}
- Wiring, integration, end-to-end flows
- Tests and verification

(Add or remove phases as appropriate for the feature scope)

## Design Mobilization (if applicable)
- **Tokens used**: {comma-separated token names from DESIGN.md — colors, spacing, typography, radius, shadow, motion}
- **Components used**: {names from DESIGN.md inventory — flag any "new component required" items as a blocker that needs `/design update` before `/implement`}
- **Surfaces touched**: {from DESIGN.md}
- **States covered**: {which of loading / empty / error / success / offline this feature must implement}
- **A11y notes**: {anything beyond the baseline that this feature must honor}

{Remove this section entirely if the feature has no user-facing surface.}

## Parallelism Notes
- **Independent seams**: {Which parts of the work do not depend on each other (e.g. two services behind the same interface) — `/tasks` uses this to build parallel execution waves}
- **Shared files (serialization points)**: {Files several parts must touch (registries, routers, config, barrel files) — work on them is serialized}

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

Update spec.md status to "Approved". (Do not edit `specs/roadmap.md`: statuses are derived from tracks so parallel features never conflict.)

## Step 5: Present for review

1. Architecture decisions (one line each)
2. Phase breakdown with scope
3. Test strategy summary
4. **"Review this plan. Once approved, run `/tasks $ARGUMENTS`."**
