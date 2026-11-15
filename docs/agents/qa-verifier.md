# `qa-verifier`

**Role.** Runs the project-wide health checks in an isolated context so large logs never reach the orchestrator.

**Launched by.** `/qa` (and `/build`).

**Modes.** `quick`: automated checks and coverage-gap audit. `full`: adds the security scan (hardcoded secrets, `.env.example`, sensitive data in responses), constitution/spec/pattern compliance, and dependency count.

**Report.** `categories[]` (Lint, Format, Type check, Test, Coverage gaps, Security, Spec compliance, Dependencies: PASS/WARN/FAIL/SKIP), `coverage_gaps[]`, `recommendations[]`. It does not write `qa-report.md` — the caller does, and computes the verdict (PASS/WARN/FAIL). No source code → `{"verdict": "NO_SOURCE"}`.

Schema: [`qa-verifier.schema.json`](../../schemas/qa-verifier.schema.json). Source: [`agents/qa-verifier.md`](../../agents/qa-verifier.md).
