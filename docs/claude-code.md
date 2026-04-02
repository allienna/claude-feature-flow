# Feature Flow for Claude Code

Use Feature Flow as a Claude Code plugin with slash commands (`/prd`, `/roadmap`, `/implement`, etc.).

## Install

### From the marketplace

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

**Marketplace install:**

```bash
claude plugin update claude-feature-flow@claude-feature-flow
# or from within Claude Code:
/plugin marketplace update
```

**Local clone or symlinks:**

```bash
cd ~/claude-feature-flow && git pull
```

Changes propagate immediately since Claude Code reads the files directly.

## Usage

All commands are available as slash commands. They auto-detect project state and suggest the next step.

### Foundation phase

```
/prd              → Guided interview to create PRD.md
/constitution     → Extract non-negotiable principles from the PRD
/roadmap          → Decompose PRD into ordered features
```

### Specification phase

```
/specify          → Create detailed spec for the next feature
/plan             → Technical implementation plan with architecture decisions
/tasks            → Break the plan into atomic, testable work items
```

### Implementation phase

```
/implement        → Implement one task at a time (auto-detects next task)
/build            → Full automation: implement all → review → QA → ship
/build quick      → Implement all → QA (skip review and ship)
```

### Quality & deployment

```
/review           → Review completed feature against its spec
/qa               → Project-wide quality audit (tests, lint, security, compliance)
/qa quick         → Automated checks only (skip security and compliance)
/ship             → Create branch, commit, push, open PR
/merge <pr>       → Address PR comments, squash merge, update main
/review-pr <pr>   → Fix and reply to PR review comments
```

### Status

```
/status           → Roadmap progress, active tracks, recommended next action
```

## Command arguments

Most commands auto-detect the current feature. You can also specify explicitly:

```
/specify auth-client
/plan auth-client
/tasks auth-client
/implement auth-client
/review auth-client
/build auth-client
/merge 42
/review-pr 42
```

## How commands discover your project

Commands read `CLAUDE.md` to find build commands. Add a section like this to your `CLAUDE.md`:

```markdown
## Build & Run Commands

- Test: `pytest`
- Lint: `ruff check`
- Format: `ruff format`
- Type check: `pyright`
```

If `CLAUDE.md` is missing, commands still work but skip automated quality checks.

## File structure

Feature Flow uses these source files:

```
commands/               # Claude Code slash commands
  prd.md
  constitution.md
  roadmap.md
  specify.md
  plan.md
  tasks.md
  implement.md
  review.md
  qa.md
  ship.md
  merge.md
  build.md
  review-pr.md
  status.md
.claude-plugin/
  plugin.json           # Plugin metadata
  marketplace.json      # Marketplace configuration
```
