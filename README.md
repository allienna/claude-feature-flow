# claude-feature-flow

A reusable set of Claude Code slash commands that provide a structured feature development workflow — from product requirements to merged PR.

## Workflow

```
/prd → /constitution → /design → /roadmap → /specify → (/clarify) → /plan → /tasks → (/analyze) → /build → /ship → /merge
```

### Core workflow

| Command | Description |
|---------|-------------|
| `/prd` | Create or update the Product Requirements Document through guided discovery |
| `/constitution` | Generate or update the project constitution from the PRD |
| `/design` | Create or update `DESIGN.md` — the project design system (tokens, components, surfaces, states, a11y) |
| `/roadmap` | Generate or update the feature roadmap from the PRD |
| `/specify` | Create a feature specification with testable (Given/When/Then) acceptance criteria and `[NEEDS CLARIFICATION]` markers |
| `/clarify` | Resolve spec ambiguities one question at a time before planning |
| `/plan` | Create a technical implementation plan from a spec (auto-detects) |
| `/tasks` | Break a plan into atomic tasks with `Depends-on`, `Files`, `Covers` and computed parallel execution waves |
| `/analyze` | Read-only consistency check across PRD, spec, plan, tasks and DESIGN.md (parallel analysts) |
| `/implement` | Implement the next pending task (auto-detects) |
| `/review` | Independent review by two parallel agents (spec compliance + code quality), merged into `review.md` |
| `/qa` | Run project-wide quality audit (delegated to an isolated `qa-verifier` agent) |
| `/ship` | Create branch, commit, push and open a PR |

### Automation & maintenance

| Command | Description |
|---------|-------------|
| `/build` | Orchestrated pipeline: implement tasks in parallel waves, review, converge on gaps, qa, ship (`/build quick` skips review and ship) |
| `/merge` | Address PR comments, squash merge, and update local main |
| `/review-pr` | Fetch PR review comments, fix issues, reply to each comment |
| `/status` | Show project status and suggest the next action |

## How `/build` orchestrates

`/build` is an **orchestrator**: it dispatches workers, waits at a barrier, merges their structured reports, and is the only writer of `tasks.md`. Workers and reviewers run in fresh contexts, so the orchestrator's context stays small even on large features.

| Phase | Pattern | Agents |
|-------|---------|--------|
| Implement | per wave: fan-out N tasks in parallel (default 3, `--parallel=N`) → barrier → fan-in JSON reports → wave-level test/lint/format run | `implementer` × N |
| Review | fan-out two independent reviewers → merge into `review.md` | `spec-reviewer` ‖ `quality-reviewer` |
| Converge | each blocker/major issue becomes a corrective task; loop until the verdict clears, `--max-rounds` (default 2) is hit, or a round makes no progress | back to the waves |
| QA | one isolated verifier | `qa-verifier` |

Safety rules: tasks in the same wave have **disjoint `Files`** (validated by `/tasks` and again by `/build`); workers may only write inside their `Files`, which `/build` verifies via `git status` after each wave; reviewers are read-only and never saw the code being written; `/ship` still asks for human confirmation. A `tasks.md` without `Depends-on`/`Files` (older format) runs sequentially.

The agents live in `agents/` (`implementer`, `spec-reviewer`, `quality-reviewer`, `qa-verifier`) and are namespaced `claude-feature-flow:<name>` when installed as a plugin.

## Prerequisites

Commands auto-discover your project setup from:

- **`PRD.md`** — Product requirements (used by `/prd`, `/roadmap`, `/specify`, `/plan`)
- **`CLAUDE.md`** — Build commands, conventions, tech stack (used by `/build`, `/implement`, `/qa`, `/review`, `/ship`). `/constitution` can also create an `AGENTS.md` so other coding agents share the same context
- **`DESIGN.md`** — Design system: tokens, components, surfaces, states, a11y (used by `/specify`, `/plan`, `/implement`, `/review`)
- **`specs/`** — Feature tracks created by the workflow
- **`design/mockups/`** (optional) — Mockup files ingested by `/design` to reconcile visuals with the design system

No project-specific configuration needed. Commands detect your tech stack, test runner, linter, and formatter from `CLAUDE.md`.

## Install

### From the marketplace

Add the marketplace and install the plugin from within Claude Code:

```
/plugin marketplace add allienna/claude-feature-flow
/plugin install claude-feature-flow@claude-feature-flow
```

Or from the CLI:

```bash
claude plugin install claude-feature-flow@claude-feature-flow
```

### From a local clone

```bash
git clone git@github.com:allienna/claude-feature-flow.git ~/claude-feature-flow
claude --plugin-dir ~/claude-feature-flow
```

### Via symlinks (legacy)

The included `install.sh` script links commands (and the `agents/` used by `/build`, `/review` and `/qa`) into your Claude Code configuration:

```bash
git clone git@github.com:allienna/claude-feature-flow.git ~/claude-feature-flow

# Global (all projects)
~/claude-feature-flow/install.sh ~/.claude/commands

# Per-project (from your project root)
~/claude-feature-flow/install.sh
```

Symlinks propagate updates automatically — pull the latest and all projects get updated commands.

### Manual

Copy the `commands/*.md` files into your `.claude/commands/` directory and the `agents/*.md` files into `.claude/agents/`.

## Updating

**Marketplace install** — update via CLI or slash command:

```bash
claude plugin update claude-feature-flow@claude-feature-flow
# or from within Claude Code:
/plugin marketplace update
```

**Local clone or symlinks** — just pull:

```bash
cd ~/claude-feature-flow && git pull
```

Changes propagate immediately since Claude Code reads the files directly.

## Getting started

1. Run `/prd` to create your Product Requirements Document through a guided interview
2. Run `/constitution` to establish non-negotiable project principles
3. Run `/design` to produce `DESIGN.md` — the design system referenced by every downstream UI-touching command
4. Run `/roadmap` to break the PRD into ordered features
5. Run `/specify` to detail the first feature, `/clarify` if anything is ambiguous, then `/plan` and `/tasks`
6. Optionally run `/analyze` to cross-check the artifacts, then `/build` to run the full pipeline — or `/implement` to go task by task
7. Run `/status` at any time to see where you are and what to do next

## Versioning

The plugin version is bumped automatically by [`.github/workflows/version-bump.yml`](.github/workflows/version-bump.yml) on every push to `main`, based on the [Conventional Commit](https://www.conventionalcommits.org/) header of the merge commit:

| Commit type | Bump | Typical case |
|-------------|------|--------------|
| `feat:` | minor | a new command |
| `fix:`, `perf:`, `refactor:` | patch | fixing or reworking an existing command |
| `feat!:` or `BREAKING CHANGE` | major | incompatible change |
| anything else (`docs:`, `chore:`, `ci:`, …) | none | no release |

The header is read from the first matching line of the merge commit's full message — i.e. the subject of a **squash-merge** commit, or the first line of the body of a GitHub "merge commit". For predictable bumps, **squash-merge PRs with a Conventional Commit title** (e.g. `feat: add /foo command`).

When a bump occurs the workflow re-syncs to the tip of `main`, updates `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, commits as `chore(release): vX.Y.Z`, and pushes a matching `vX.Y.Z` tag. If `main` is protected, allow the `github-actions[bot]` actor to push (or bypass the rule for it).

## License

MIT
