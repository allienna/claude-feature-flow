# Artifacts and identifiers

All artifacts are Markdown files versioned with your code. The pipeline never keeps hidden state.

## Project-level artifacts (live on `main`)

| File | Created by | Purpose |
|---|---|---|
| `PRD.md` | `/prd` | What you are building and why. Sections numbered 1–11. |
| `CLAUDE.md` | you | Build & Run Commands, conventions, key patterns. **Required by `/build`, `/review`, `/qa`.** |
| `AGENTS.md` | `/constitution` (optional) | The same context for other coding agents; avoids duplicating `CLAUDE.md`. |
| `specs/constitution.md` | `/constitution` | Principles that no feature may violate. |
| `DESIGN.md` | `/design` | Tokens, component inventory, surfaces, states, accessibility baseline. |
| `specs/roadmap.md` | `/roadmap` | Ordered features `F-001…` with dependencies, sizes, milestones. |
| `qa-report.md` | `/qa` | Last project-wide audit. Overwritten each run. |

## Feature-level artifacts (live in the feature's worktree until merged)

`specs/NNN-feature/`

| File | Created by | Purpose |
|---|---|---|
| `spec.md` | `/specify`, edited by `/clarify` | Context, user stories, requirements (FR), acceptance criteria (AC), error scenarios, out of scope, clarifications log. |
| `plan.md` | `/plan` | Architecture decisions (AD), affected files, phases, design mobilization, parallelism notes, test strategy, risks. |
| `tasks.md` | `/tasks`, checked off by `/build`/`/implement` | Atomic tasks and execution waves. |
| `review.md` | `/review` | Acceptance-criteria evidence, traceability, issues, verdict, convergence history. |

## Identifiers

Identifiers are stable and never renumbered; later artifacts and reviews reference them.

| Id | Meaning | Defined in |
|---|---|---|
| `F-NNN` | Roadmap feature. `NNN` is also the track number (`specs/NNN-…`), so parallel worktrees never collide. | roadmap |
| `FR-n` | Functional requirement | spec |
| `AC-n` | Acceptance criterion, a testable scenario | spec |
| `AD-n` | Architecture decision | plan |
| `T-x.y` | Task `y` of phase `x` | tasks |
| `T-Cn.k` | Corrective task `k` of convergence round `n` | tasks (added by `/build`/`/review`) |

## Acceptance criteria

Acceptance criteria are executable scenarios, falsifiable by a test:

```markdown
- [ ] AC-1 (FR-1): **Given** a registered user **When** they submit a wrong password
      **Then** the API returns 401 and no session is created
```

Rules: observable inputs and outputs, no vague adjectives, one `FR` reference, and every spec "Error Scenario" has an AC. `/plan` refuses a spec whose criteria are not testable. See [Writing good specs](../guides/writing-good-specs.md).

## `[NEEDS CLARIFICATION]` markers

Never guess. When information is missing the spec carries `[NEEDS CLARIFICATION: question]` at the place where the answer will land. `/clarify` resolves them; `/plan` and `/build` refuse to proceed while any remain.

## `tasks.md` format

```markdown
## Phase 1: Foundation

- [ ] **T-1.1**: Add the User model
  - **Covers**: AC-1, AC-2
  - **Depends-on**: none
  - **Files**: `src/models/user.py` (new), `src/models/__init__.py`
  - **Do**: …
  - **Test**: `pytest tests/test_user.py`

- [ ] **T-1.2** [P]: Add the search service
  - **Covers**: AC-3
  - **Depends-on**: T-1.1
  - **Files**: `src/services/search.py` (new)
  - …

## Execution Waves

| Wave | Tasks | Parallel? |
|------|-------|-----------|
| 1 | T-1.1 | no |
| 2 | T-1.2, T-1.3 | yes |
```

- `Files` is a **contract**: the exact paths a task may write. It is what makes parallel execution safe.
- `Covers` links tasks to acceptance criteria; `/tasks` refuses uncovered criteria and `/review` reports traceability.
- `[P]` marks tasks that share a wave with at least one other task.
- A file without `Depends-on`/`Files` (the 1.x format) is executed sequentially.
