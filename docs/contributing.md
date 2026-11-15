# Contributing

## Repository layout

```
commands/    slash commands (the plugin's logic) — Markdown with frontmatter
agents/      subagent definitions and their output contracts
schemas/     JSON Schemas for agent reports
docs/        this documentation
scripts/     maintenance scripts (docs generation)
.claude-plugin/   plugin.json, marketplace.json
.github/workflows/version-bump.yml
```

## Developing a command

1. Edit the file in `commands/`. Keep the frontmatter (`description`, `argument-hint`, `allowed-tools`) accurate: list only the tools the command needs (`Bash(git:*)` rather than `Bash` where possible).
2. Test locally without installing: `claude --plugin-dir /path/to/claude-feature-flow` in a scratch project.
3. If you change a contract (task format, agent report, artifact layout) update, in the same PR: the command(s), the matching `agents/*.md` and `schemas/*.json`, and the docs pages.
4. Regenerate the command reference: `python3 scripts/gen-command-docs.py`.

## A scratch project for testing

Use a throwaway repository with a trivial stack, a `CLAUDE.md` with `Build & Run Commands`, and a roadmap of two independent features and one dependent one. Walk through `/specify` → `/build` → `/ship` for each and check: waves run in parallel for independent tasks, worker worktrees are cleaned up, `/merge` removes the feature worktree.

## Commits and versioning

Versions are **bumped automatically** — never edit `version` in `plugin.json` or `marketplace.json`.

On every push to `main`, the workflow reads the Conventional Commit header of the (squash) merge commit:

| Header | Bump |
|---|---|
| `feat!:` or `BREAKING CHANGE` in the message | major |
| `feat:` | minor |
| `fix:`, `perf:`, `refactor:` | patch |
| `docs:`, `chore:`, `ci:`, others | none |

Use a Conventional Commit PR title and **squash merge**. The workflow commits `chore(release): vX.Y.Z` and pushes the `vX.Y.Z` tag. If `main` is protected, allow `github-actions[bot]` to push.

## Documentation

- Update `CHANGELOG.md` (Keep a Changelog format) in every PR that changes behaviour.
- Command pages in `docs/commands/` are generated from `commands/*.md`; edit the source command or `scripts/gen-command-docs.py`, not the generated page.
- Every internal link must resolve (`python3 scripts/check-docs-links.py`).
