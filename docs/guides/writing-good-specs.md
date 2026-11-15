# Writing good specs

The pipeline is only as good as the spec: acceptance criteria become tests, reviews and corrective tasks.

## Acceptance criteria

Write each criterion as a scenario that a test can fail:

```markdown
- [ ] AC-1 (FR-1): **Given** an unauthenticated visitor **When** they request /orders
      **Then** they receive 401 and the response body contains no order data
- [ ] AC-2 (FR-1, error): **Given** the payment provider times out **When** checkout is submitted
      **Then** the order stays `pending` and the user sees a retry message
```

EARS is an equally valid form: *When &lt;trigger&gt;, the system shall &lt;response&gt;.*

| Do | Don't |
|---|---|
| Observable inputs and outputs | "The system should be fast" |
| One behaviour per criterion | "…and also logs, caches and notifies" |
| Reference the requirement (`FR-n`) | Floating criteria with no requirement |
| Cover every Error Scenario | Only the happy path |

## Never guess: use the marker

When you don't know, write `[NEEDS CLARIFICATION: question]` where the answer belongs. This is the tool, not a failure. `/plan` and `/build` refuse to run while markers remain, so unknowns can't leak into the architecture.

## `/clarify`

Run it when the spec has markers, or when it just feels vague. It scans for: explicit markers, untestable criteria, missing scenarios (an error scenario with no AC, an FR with no AC), contradictions (spec vs PRD vs `DESIGN.md`), undefined terms (limits, roles, formats), and scope edges. It asks at most five questions, one at a time, with a recommended default for each, then rewrites the spec in place and logs the decision under `## Clarifications`. Existing ids are never renumbered.

## `/analyze`

Before building (or after changing the spec), `/analyze` cross-checks PRD ↔ spec, spec ↔ plan, plan ↔ tasks, spec ↔ tasks (AC coverage), and constitution/`DESIGN.md` ↔ spec/plan with parallel read-only analysts. It writes nothing; it prints findings and one recommended next command.

## Good task breakdowns

`/tasks` produces the best parallelism when the plan names, per phase, the files each piece creates or modifies, and lists *independent seams* and *shared files* under **Parallelism Notes**. Shared files (route tables, registries, barrel files) are serialization points: tasks touching them are placed in different waves.
