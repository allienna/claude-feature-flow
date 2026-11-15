# `quality-reviewer`

**Role.** Read-only reviewer of code quality, independent of spec compliance.

**Launched by.** `/review` (and `/build` through it), in parallel with `spec-reviewer`.

**Scope.** The feature's diff only (against the merge base with `main`), not the whole repository.

**Checks.** The project's test, lint, format and type-check commands; correctness smells (unhandled errors, races, leaks); maintainability (duplication of existing utilities, dead code, debug leftovers); tests that can actually fail; security smells.

**Report.** `quality_gates[]` (Test/Lint/Format/Type check: PASS/FAIL/SKIP) and `issues[]` (severity, `file:line` location, description, fix). `blocker` = breaks behaviour, security or a gate; `major` = fix before merge; `minor` = nice to have.

Schema: [`quality-reviewer.schema.json`](../../schemas/quality-reviewer.schema.json). Source: [`agents/quality-reviewer.md`](../../agents/quality-reviewer.md).
