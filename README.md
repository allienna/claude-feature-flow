# claude-feature-flow

A reusable set of Claude Code slash commands that provide a structured feature development workflow — from product requirements to merged PR.

## Workflow

```
/prd → /constitution → /design → /roadmap → /specify → /plan → /tasks → /implement → /review → /qa → /ship → /merge
```

### Core workflow

| Command | Description |
|---------|-------------|
| `/prd` | Create or update the Product Requirements Document through guided discovery |
| `/constitution` | Generate or update the project constitution from the PRD |
| `/design` | Create or update `DESIGN.md` — the project design system (tokens, components, surfaces, states, a11y) |
| `/roadmap` | Generate or update the feature roadmap from the PRD |
| `/specify` | Create a feature specification (auto-detects the next feature) |
| `/plan` | Create a technical implementation plan from a spec (auto-detects) |
| `/tasks` | Break a plan into atomic tasks (auto-detects) |
| `/implement` | Implement the next pending task (auto-detects) |
| `/review` | Review a completed feature against its spec (auto-detects) |
| `/qa` | Run project-wide quality audit |
| `/ship` | Create branch, commit, push and open a PR |

### Automation & maintenance

| Command | Description |
|---------|-------------|
| `/build` | Full pipeline: implement all tasks, review, qa, ship (use `/build quick` to skip review) |
| `/merge` | Address PR comments, squash merge, and update local main |
| `/review-pr` | Fetch PR review comments, fix issues, reply to each comment |
| `/status` | Show project status and suggest the next action |

## Prerequisites

Commands auto-discover your project setup from:

- **`PRD.md`** — Product requirements (used by `/prd`, `/roadmap`, `/specify`, `/plan`)
- **`CLAUDE.md`** — Build commands, conventions, tech stack (used by `/implement`, `/qa`, `/review`, `/ship`)
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

The included `install.sh` script links commands into your Claude Code configuration:

```bash
git clone git@github.com:allienna/claude-feature-flow.git ~/claude-feature-flow

# Global (all projects)
~/claude-feature-flow/install.sh ~/.claude/commands

# Per-project (from your project root)
~/claude-feature-flow/install.sh
```

Symlinks propagate updates automatically — pull the latest and all projects get updated commands.

### Manual

Copy the `commands/*.md` files into your `.claude/commands/` directory.

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
5. Run `/specify` to detail the first feature, then `/plan` and `/tasks`
6. Run `/implement` to start building — or `/build` to run the full pipeline
7. Run `/status` at any time to see where you are and what to do next

## Versioning

The plugin version is bumped automatically by [`.github/workflows/version-bump.yml`](.github/workflows/version-bump.yml) on every push to `main`, based on the [Conventional Commit](https://www.conventionalcommits.org/) type of the merge commit:

| Commit type | Bump | Typical case |
|-------------|------|--------------|
| `feat:` | minor | a new command |
| `fix:`, `perf:`, `refactor:` | patch | fixing or reworking an existing command |
| `feat!:` or `BREAKING CHANGE` | major | incompatible change |
| anything else (`docs:`, `chore:`, `ci:`, …) | none | no release |

When a bump occurs the workflow updates `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, commits as `chore(release): vX.Y.Z`, and pushes a matching `vX.Y.Z` tag. If `main` is protected, allow the `github-actions[bot]` actor to push (or bypass the rule for it).

## License

MIT
