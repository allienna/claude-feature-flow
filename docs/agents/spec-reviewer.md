# `spec-reviewer`

**Role.** Read-only reviewer: does the code satisfy the spec, plan, constitution and design system?

**Launched by.** `/review` (and `/build` through it), in parallel with `quality-reviewer`.

**Checks.** Each acceptance criterion with evidence and a test that can fail; traceability (every AC in some task's `Covers`); each architecture decision; each constitution principle; error handling and codebase patterns; design system (tokens, inventory, the five states, accessibility baseline); scope creep (behaviour no requirement asks for).

**Report.** `acceptance_criteria[]` (id, PASS/FAIL/WARN, evidence), `architecture[]`, `constitution[]`, `spec_compliance[]`, `issues[]` (severity `blocker|major|minor`, `ac`, description, concrete `fix`). Every FAIL AC has a matching issue with a fix; the orchestrator turns those into corrective tasks.

Schema: [`spec-reviewer.schema.json`](../../schemas/spec-reviewer.schema.json). Source: [`agents/spec-reviewer.md`](../../agents/spec-reviewer.md).
