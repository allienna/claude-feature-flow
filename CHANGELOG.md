# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/). Versions are bumped automatically from Conventional Commit headers on `main`.

## [2.0.0]

Orchestrated parallel pipeline. See the [migration guide](docs/migration/1.x-to-2.0.md).

### Added
- **Subagents**: `implementer`, `spec-reviewer`, `quality-reviewer`, `qa-verifier` in `agents/`, with JSON Schemas in `schemas/`.
- **`/clarify`**: resolves `[NEEDS CLARIFICATION]` markers and vague criteria one question at a time.
- **`/analyze`**: read-only consistency check across PRD, spec, plan, tasks and `DESIGN.md`, with parallel analysts.
- **Parallel execution waves**: `tasks.md` tasks declare `Depends-on`, `Files`, `Covers`; `/tasks` computes waves.
- **Feature worktrees**: `/specify` creates one git worktree per feature; `/status` lists active worktrees; `/merge` cleans up.
- **Worker worktrees**: `/build` isolates parallel workers in their own worktrees and merges them, with a `base_sha` guard.
- **Convergence loop**: review findings become corrective tasks until the verdict clears or `--max-rounds` is reached.
- **`/build` options**: `--parallel`, `--sequential`, `--isolate`, `--max-rounds`.
- Optional `AGENTS.md` generation from `/constitution`.
- Documentation site under `docs/`.

### Changed
- **BREAKING** `/build` is an orchestrator (workers and reviewers in separate contexts) instead of an inline loop.
- **BREAKING** `tasks.md` format extended; the 1.x format still runs, sequentially.
- **BREAKING** Acceptance criteria are Given/When/Then or EARS scenarios; `/plan` refuses untestable criteria and unresolved clarification markers.
- **BREAKING** `/review` is performed by two independent read-only agents and produces a merged `review.md` with evidence, traceability and convergence history.
- **BREAKING** `/specify` creates a git worktree instead of switching branch in place; foundations must be committed on `main` first.
- `/qa` runs in an isolated `qa-verifier` agent.
- Feature commands no longer edit `specs/roadmap.md`; status is derived from tracks.
- `install.sh` also links `agents/`.

### Fixed
- `/build` no longer drifts from `/implement` (it ignored `DESIGN.md`).

## [1.0.0]

Initial release: `/prd`, `/constitution`, `/design`, `/roadmap`, `/specify`, `/plan`, `/tasks`, `/implement`, `/review`, `/qa`, `/ship`, `/merge`, `/review-pr`, `/status`, `/build`; plugin manifest and marketplace; automatic version bump on `main`.
