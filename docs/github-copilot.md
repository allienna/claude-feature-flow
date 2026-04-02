# Feature Flow for GitHub Copilot

Use Feature Flow in VS Code with GitHub Copilot Chat — as prompts, an orchestrator agent, and auto-loading instructions.

## Resources overview

| Type | File | Purpose |
|------|------|---------|
| **Agent** | `agents/feature-flow.agent.md` | Orchestrator that guides you through the workflow with handoffs |
| **Instruction** | `instructions/feature-flow.instructions.md` | Auto-loads artifact structure and conventions |
| **Prompts** (14) | `prompts/feature-flow-*.prompt.md` | One per workflow step — invocable from Copilot Chat |
| **Collection** | `collections/feature-flow.yml` | Bundles everything for ADEO CLI install |

## Install

### Option 1: Copy to your project

Copy the resource directories into your project's `.github/` folder:

```bash
git clone git@github.com:allienna/claude-feature-flow.git ~/feature-flow

# Copy all resources
cp -r ~/feature-flow/prompts/ .github/prompts/
cp -r ~/feature-flow/agents/ .github/agents/
cp -r ~/feature-flow/instructions/ .github/instructions/
```

The prompts will appear in VS Code's Copilot Chat prompt picker, and the instruction will auto-load when working in files matching its `applyTo` pattern.

### Option 2: ADEO CLI

If your organization uses the [ADEO CLI](https://github.com/adeo/copilot-prompts):

```bash
adeo add feature-flow
```

This installs all resources from the collection in one step.

### Option 3: Cherry-pick prompts

You can install individual prompts instead of the full collection. Copy only the prompts you need:

```bash
# Just the planning prompts
cp ~/feature-flow/prompts/feature-flow-prd.prompt.md .github/prompts/
cp ~/feature-flow/prompts/feature-flow-roadmap.prompt.md .github/prompts/
cp ~/feature-flow/prompts/feature-flow-specify.prompt.md .github/prompts/
```

## Usage

### Using the orchestrator agent

The **Feature Flow agent** is the easiest way to get started. It detects your project state and suggests the right next step with handoff buttons.

In VS Code Copilot Chat, invoke it with:
```
@feature-flow What should I work on next?
```

The agent provides clickable handoff buttons to delegate to each workflow step.

### Using prompts directly

Each prompt is available in the Copilot Chat prompt picker. Open it with `Ctrl+/` (or `Cmd+/` on macOS) and search for "feature-flow":

| Prompt | What it does |
|--------|-------------|
| `feature-flow-prd` | Create or update the Product Requirements Document |
| `feature-flow-constitution` | Generate project constitution from the PRD |
| `feature-flow-roadmap` | Decompose PRD into ordered features |
| `feature-flow-specify` | Create detailed feature specification |
| `feature-flow-plan` | Technical implementation plan |
| `feature-flow-tasks` | Break plan into atomic tasks |
| `feature-flow-implement` | Implement the next pending task |
| `feature-flow-review` | Review feature against spec |
| `feature-flow-qa` | Project-wide quality audit |
| `feature-flow-ship` | Create branch, commit, push, open PR |
| `feature-flow-merge` | Address PR comments, squash merge |
| `feature-flow-build` | Full automation pipeline |
| `feature-flow-review-pr` | Fix and reply to PR review comments |
| `feature-flow-status` | Show progress and next action |

### Typical session

1. Open Copilot Chat and select the **feature-flow-prd** prompt
2. Answer the guided interview questions
3. Select **feature-flow-constitution** to set project principles
4. Select **feature-flow-roadmap** to plan features
5. Select **feature-flow-specify** to detail the first feature
6. Continue through plan → tasks → implement → review → qa → ship

Or use the **feature-flow agent** and follow its handoff suggestions through each step.

## How it differs from the Claude Code version

The Copilot prompts are adapted from the Claude Code commands with these changes:

| Aspect | Claude Code | GitHub Copilot |
|--------|-------------|----------------|
| **Invocation** | Slash commands (`/prd`) | Prompt picker or `@feature-flow` agent |
| **Tool access** | Explicit tools (`Glob`, `Read`, `Write`) | Copilot tools (`codebase`, `editFiles`, `runCommands`) |
| **Arguments** | `$ARGUMENTS` positional args | User provides context in chat message |
| **State detection** | `Glob("specs/[0-9]*/spec.md")` | Natural language: "Search for `specs/*/spec.md`" |
| **Orchestration** | `/build` command loops | Agent with handoff buttons |
| **Distribution** | Claude plugin marketplace | ADEO CLI or manual copy |

### Copilot-specific features

- **Agent handoffs** — The orchestrator agent delegates to specialized prompts via clickable buttons
- **Instruction auto-loading** — `feature-flow.instructions.md` activates automatically when editing files in `specs/` or `PRD.md`
- **VS Code native** — Works directly in the editor without terminal switching
- **Copilot tools** — Uses `runTests`, `problems`, and `testFailure` for tighter IDE integration

## Build command discovery

Like the Claude Code version, prompts read `CLAUDE.md` for build commands. Add a section like this:

```markdown
## Build & Run Commands

- Test: `pytest`
- Lint: `ruff check`
- Format: `ruff format`
- Type check: `pyright`
```

If `CLAUDE.md` is missing, prompts still work but skip automated quality checks.

## File structure

```
prompts/
  feature-flow-prd.prompt.md
  feature-flow-constitution.prompt.md
  feature-flow-roadmap.prompt.md
  feature-flow-specify.prompt.md
  feature-flow-plan.prompt.md
  feature-flow-tasks.prompt.md
  feature-flow-implement.prompt.md
  feature-flow-review.prompt.md
  feature-flow-qa.prompt.md
  feature-flow-ship.prompt.md
  feature-flow-merge.prompt.md
  feature-flow-build.prompt.md
  feature-flow-review-pr.prompt.md
  feature-flow-status.prompt.md
agents/
  feature-flow.agent.md
instructions/
  feature-flow.instructions.md
collections/
  feature-flow.yml
```
