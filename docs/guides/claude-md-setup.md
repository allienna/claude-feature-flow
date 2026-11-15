# CLAUDE.md setup

`/build`, `/implement`, `/review`, `/qa` and `/ship` discover how to build and test your project from `CLAUDE.md`. Nothing else is configured.

## Build & Run Commands (required)

```markdown
## Build & Run Commands

- Test: `pytest -q`
- Test single: `pytest -q tests/test_user.py::test_login`
- Lint: `ruff check .`
- Format: `ruff format --check .`
- Type check: `pyright`
```

A missing command is a `SKIP` with a warning, never an invented command. Without any, the pipeline still runs but no quality gate can fail.

## Worktree Setup (recommended for parallel builds)

A worker worktree is a fresh checkout. List what a worker must run before it can build and test:

```markdown
## Worktree Setup

- `npm ci --prefer-offline`
- `cp .env.example .env`
```

Each parallel worker runs these first. Keep them fast and idempotent; a slow install multiplies by the number of workers, in which case `--isolate=none` may be preferable.

For ignored files that must exist in every worktree (`.env`, local config) add a `.worktreeinclude` file at the repository root (gitignore syntax; only files that are also gitignored are copied).

## Key patterns

Describe conventions the reviewers can verify with `grep`: error-return shape, logging, module layout. `spec-reviewer` checks them against the diff.

## AGENTS.md

`/constitution` offers to create an `AGENTS.md` (build commands, conventions, pointer to the constitution) so other coding agents read the same context. If both files exist, keep one source of truth: let one import the other rather than duplicating.
