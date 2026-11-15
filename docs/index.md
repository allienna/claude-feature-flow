# feature-flow documentation

`feature-flow` is a Claude Code plugin that takes a product from **PRD to merged pull request** through a spec-driven pipeline. Version 2 adds an **orchestrator** that runs independent tasks in parallel with isolated subagents, reviews the result with agents that did not write the code, and loops until the spec is satisfied.

## Start here

| If you want to… | Read |
|---|---|
| Install it and run your first feature | [Getting started](getting-started.md) |
| Understand the pipeline and its artifacts | [Workflow](concepts/workflow.md), [Artifacts](concepts/artifacts.md) |
| Understand how `/build` parallelizes work | [Orchestration](concepts/orchestration.md) |
| Run several features at the same time | [Parallel features guide](guides/parallel-features.md) |
| Look up a command | [Command reference](commands/index.md) |
| Upgrade from 1.x | [Migration 1.x → 2.0](migration/1.x-to-2.0.md) |
| Fix something that broke | [Troubleshooting](guides/troubleshooting.md) |
| Contribute | [Contributing](contributing.md) |

## Map of the documentation

- **Concepts** — [workflow](concepts/workflow.md) · [artifacts](concepts/artifacts.md) · [state machine](concepts/state-machine.md) · [orchestration](concepts/orchestration.md) · [parallelism and worktrees](concepts/parallelism-and-worktrees.md)
- **Reference** — [commands](commands/index.md) · [agents](agents/index.md) · JSON contracts in [`schemas/`](../schemas)
- **Guides** — [parallel features](guides/parallel-features.md) · [writing good specs](guides/writing-good-specs.md) · [CLAUDE.md setup](guides/claude-md-setup.md) · [tuning and cost](guides/tuning-and-cost.md) · [troubleshooting](guides/troubleshooting.md)
- **Architecture** — [overview](architecture/overview.md) · [decision records](architecture/decisions.md)
- **Project** — [migration](migration/1.x-to-2.0.md) · [contributing](contributing.md) · [changelog](../CHANGELOG.md)

## Design principles

1. **Files are the memory.** Every phase reads and writes Markdown artifacts in the repository. Nothing important lives only in a chat context, so any phase can be resumed, reviewed or edited by a human.
2. **Humans keep the gates that matter.** The spec, the plan and the commit/PR are approved by you. Automation runs *between* those gates, never through them.
3. **Authors do not grade their own work.** Reviewers and QA run as separate, read-only agents in fresh contexts.
4. **Parallelism must be provably safe.** Tasks declare the files they write; only disjoint tasks run together, each in its own git worktree.
5. **Deterministic where possible.** Verdicts, wave computation and convergence rules are mechanical rules, not impressions.
