# Decision records

Short records of the decisions behind 2.0.

## ADR-001: Orchestrator–worker with fresh contexts
**Decision.** `/build` orchestrates; `implementer` workers do the work in fresh contexts and return structured reports.
**Why.** A single context accumulates every task and degrades on large features; authors reviewing their own work are biased.
**Consequence.** More agents (cost), but small orchestrator context and independent review.

## ADR-002: Parallelism only on declared, disjoint `Files`
**Decision.** `tasks.md` carries `Depends-on` and `Files`; `/tasks` computes waves; overlapping tasks are serialized.
**Why.** Fan-out is safe only on independent work with disjoint writes; shared writable state is the failure mode of parallel agents.
**Consequence.** Task authoring is more demanding; `/analyze` and `/build` re-validate.

## ADR-003: Structured outputs with a single JSON block
**Decision.** Every agent ends with one fenced JSON block validated against `schemas/*.schema.json`; invalid = failed, never interpreted.
**Why.** Fan-in is where parallel pipelines break; prose can't be merged mechanically.

## ADR-004: Independent reviewers and a mechanical verdict
**Decision.** Two read-only agents review (spec compliance, code quality); the verdict is computed by rules.
**Why.** Separation of author and reviewer, and reproducible outcomes.

## ADR-005: Worktrees at two levels, `baseRef: head` guarded by `base_sha`
**Decision.** One worktree per feature; one per worker in waves of 2+ tasks. Worker worktrees must start from the feature branch; each report's `base_sha` is checked against the baseline `HEAD` instead of trusting configuration.
**Why.** Claude Code starts subagent worktrees from the default branch by default (verified in a spike with default settings: with the feature branch two commits ahead of the default branch, a subagent worktree started from the default branch's commit and contained none of the branch's work. A plugin cannot ship the `worktree.baseRef` setting, so the user sets it and `/build` verifies it). Disjoint `Files` do not stop test pollution between concurrent workers.
**Consequence.** Baseline commits before each parallel wave (squashed away at merge); a one-time `worktree.baseRef` setting; per-worktree dependency setup.

## ADR-006: Markdown orchestrator first, workflow script later
**Decision.** 2.0 ships the orchestrator as slash-command Markdown. A Claude Code *dynamic workflow* (`workflows/build.js`) is planned for 2.1 on the same schemas.
**Why.** Markdown is portable and is the readable specification of the behaviour. A script enforces barriers, rounds and no-progress rules in code, keeps intermediate results out of the context, validates schemas with automatic retries and resumes after interruptions; but it needs a recent Claude Code, can't take user input mid-run (human gates must be separate runs), has no file or shell access of its own (bookkeeping needs an agent), and is not portable to other agent hosts.
**Consequence.** The Markdown commands remain the reference; the workflow is an opt-in accelerator.

## ADR-007: Roadmap statuses are derived
**Decision.** Feature commands never edit `specs/roadmap.md`; `/status` derives status from tracks across worktrees.
**Why.** Parallel features editing the same lines would conflict at every merge.

## ADR-008: Feature numbers come from roadmap ids
**Decision.** `NNN` = the numeric part of `F-NNN`.
**Why.** "Next free number" computed independently in two worktrees collides.
