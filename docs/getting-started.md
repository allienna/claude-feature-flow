# Getting started

## Requirements

- Claude Code (a recent version; worktree isolation and subagents are required for parallel builds)
- A git repository with at least one commit (for worktrees; without git the pipeline still works, sequentially and without worktree isolation)
- The GitHub CLI `gh` for `/ship`, `/merge` and `/review-pr`
- A `CLAUDE.md` at the root of your project with a `## Build & Run Commands` section — see [CLAUDE.md setup](guides/claude-md-setup.md)

## Install

```
/plugin marketplace add allienna/claude-feature-flow
/plugin install claude-feature-flow@claude-feature-flow
```

Installed as a plugin, commands are namespaced (`/claude-feature-flow:build`) and agents are named `claude-feature-flow:implementer`, etc. Other install methods (local clone, `install.sh` symlinks, manual copy) are described in the [README](../README.md#install). With `install.sh`, agents are linked into `.claude/agents/` next to the commands.

## One-time Claude Code setting for parallel builds

Parallel workers run in their own git worktrees. Claude Code creates subagent worktrees from your repository's **default branch** unless told otherwise, which would hide the feature you are building. Set this once (user or project settings):

```json
{ "worktree": { "baseRef": "head" } }
```

`/build` checks this automatically on the first parallel wave and stops with a clear message if it is missing. Without it you can still build with `--isolate=none`. Details: [Parallelism and worktrees](concepts/parallelism-and-worktrees.md).

## Your first feature, end to end

**1. Foundations (once per project)** — run in the main checkout, then commit them to `main`:

```
/prd            # guided interview → PRD.md
/constitution   # non-negotiable principles → specs/constitution.md (+ optional AGENTS.md)
/design         # design system → DESIGN.md (UI projects)
/roadmap        # ordered features F-001… → specs/roadmap.md
```

Commit these files to `main` before specifying a feature: feature worktrees start from `main`, so anything uncommitted is invisible to them.

**2. Specify** — creates a git worktree `.claude/worktrees/001-<feature>` on branch `feat/001-<feature>`, enters it, and writes `spec.md`:

```
/specify
/clarify        # only if the spec has [NEEDS CLARIFICATION] markers or vague criteria
```

Review the spec: user stories, acceptance criteria written as Given/When/Then scenarios.

**3. Plan and tasks**

```
/plan           # architecture decisions, affected files, parallelism notes
/tasks          # atomic tasks with Depends-on / Files / Covers, grouped into execution waves
/analyze        # optional read-only cross-check of PRD ↔ spec ↔ plan ↔ tasks
```

**4. Build** — the orchestrator implements the tasks wave by wave, reviews, fixes gaps, runs QA, then hands over to `/ship`, which asks you to confirm the commit message before anything is pushed (`/build quick` stops after QA):

```
/build
```

Prefer to stay in control task by task? Use `/implement` repeatedly, then `/review` and `/qa`.

**5. Ship and merge**

```
/ship           # asks you to confirm the commit message, opens the PR
/merge <pr>     # answers review comments, squash merges, removes the worktree
```

`/status` tells you at any time where you are and what to run next.

## What gets created in your project

```
PRD.md  DESIGN.md  CLAUDE.md  AGENTS.md(optional)
specs/
  constitution.md
  roadmap.md
  001-feature-name/
    spec.md  plan.md  tasks.md  review.md
qa-report.md
.claude/worktrees/        # git-ignored; one directory per feature in progress
```

Next: [Workflow](concepts/workflow.md).
