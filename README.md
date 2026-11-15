# claude-feature-flow

A Claude Code plugin that takes a product **from PRD to merged pull request** through a spec-driven pipeline — now with an **orchestrator**: independent tasks run in parallel in isolated git worktrees, an independent pair of reviewers grades the result, and a convergence loop fixes the gaps until the spec is satisfied.

```
/prd → /constitution → /design → /roadmap
        per feature, in its own worktree:
/specify → (/clarify) → /plan → /tasks → (/analyze) → /build → /ship → /merge
```

## Highlights

- **Spec-driven, file-based.** Every phase reads and writes Markdown artifacts in your repo (`PRD.md`, `specs/NNN-feature/{spec,plan,tasks,review}.md`). Any step can be resumed, reviewed or edited by hand.
- **Orchestrated parallel builds.** `/build` computes execution *waves* from task dependencies and declared file scopes, fans out `implementer` subagents (each in its own worktree), merges their structured reports, and checks the integrated result.
- **Independent review.** `spec-reviewer` and `quality-reviewer` are read-only agents that did not write the code. The verdict is computed by rules, not impressions.
- **Convergence.** Review findings become corrective tasks; `/build` rebuilds until clean, out of rounds, or no longer progressing.
- **Several features at once.** `/specify` gives each feature its own worktree and branch, so two sessions never share a working tree.
- **Testable specs.** Acceptance criteria are Given/When/Then scenarios; unknowns are `[NEEDS CLARIFICATION]` markers resolved by `/clarify`; `/analyze` cross-checks the artifacts.
- **Human gates stay human.** Spec, plan, commit message and squash message are yours.

## Commands

| Group | Commands |
|---|---|
| Foundations | `/prd` `/constitution` `/design` `/roadmap` |
| Feature | `/specify` `/clarify` `/plan` `/tasks` `/analyze` `/implement` `/review` `/qa` |
| Automation | `/build` |
| Delivery | `/ship` `/merge` `/review-pr` |
| Navigation | `/status` |

Full reference: [docs/commands](docs/commands/index.md). Four agents ship with the plugin: [`implementer`, `spec-reviewer`, `quality-reviewer`, `qa-verifier`](docs/agents/index.md).

## Quick start

1. `/prd`, `/constitution`, `/design`, `/roadmap` — then **commit these to `main`**
2. `/specify` — creates the feature worktree and spec; `/clarify` if anything is vague
3. `/plan` → `/tasks` → `/build` — then `/ship` and `/merge`
4. `/status` at any time tells you the next command

Set `worktree.baseRef` to `"head"` in your Claude Code settings for parallel worker isolation, and give your project a `CLAUDE.md` with a `## Build & Run Commands` section. Details: [Getting started](docs/getting-started.md).

## Documentation

| | |
|---|---|
| [Getting started](docs/getting-started.md) | install, settings, first feature end to end |
| [Workflow](docs/concepts/workflow.md) · [Artifacts](docs/concepts/artifacts.md) · [State machine](docs/concepts/state-machine.md) | the pipeline and its files |
| [Orchestration](docs/concepts/orchestration.md) · [Parallelism and worktrees](docs/concepts/parallelism-and-worktrees.md) | how `/build` parallelizes safely |
| [Parallel features](docs/guides/parallel-features.md) · [Writing good specs](docs/guides/writing-good-specs.md) · [CLAUDE.md setup](docs/guides/claude-md-setup.md) · [Tuning and cost](docs/guides/tuning-and-cost.md) · [Troubleshooting](docs/guides/troubleshooting.md) | guides |
| [Architecture](docs/architecture/overview.md) · [Decisions](docs/architecture/decisions.md) | why it works this way |
| [Migration 1.x → 2.0](docs/migration/1.x-to-2.0.md) · [Changelog](CHANGELOG.md) · [Contributing](docs/contributing.md) | upgrading and contributing |

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
