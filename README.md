# Feature Flow

A structured feature development workflow — from product requirements to merged PR. Available for both **Claude Code** and **GitHub Copilot**.

## Workflow

```
prd → constitution → roadmap → specify → plan → tasks → implement → review → qa → ship → merge
```

### Commands

| Command | Description |
|---------|-------------|
| `prd` | Create or update the Product Requirements Document through guided discovery |
| `constitution` | Generate or update the project constitution from the PRD |
| `roadmap` | Generate or update the feature roadmap from the PRD |
| `specify` | Create a feature specification (auto-detects the next feature) |
| `plan` | Create a technical implementation plan from a spec (auto-detects) |
| `tasks` | Break a plan into atomic tasks (auto-detects) |
| `implement` | Implement the next pending task (auto-detects) |
| `review` | Review a completed feature against its spec (auto-detects) |
| `qa` | Run project-wide quality audit |
| `ship` | Create branch, commit, push and open a PR |
| `build` | Full pipeline: implement all tasks, review, qa, ship (`build quick` to skip review) |
| `merge` | Address PR comments, squash merge, and update local main |
| `review-pr` | Fetch PR review comments, fix issues, reply to each comment |
| `status` | Show project status and suggest the next action |

## Choose your platform

| Platform | Guide | Install |
|----------|-------|---------|
| Claude Code | [docs/claude-code.md](docs/claude-code.md) | `claude plugin install claude-feature-flow@claude-feature-flow` |
| GitHub Copilot | [docs/github-copilot.md](docs/github-copilot.md) | Copy resources to `.github/` or use ADEO CLI |

## How it works

Feature Flow creates a chain of artifacts that each command reads and writes:

```
PRD.md                              # Product Requirements Document
specs/
  constitution.md                   # Non-negotiable project principles
  roadmap.md                        # Feature roadmap with dependencies
  {NNN}-{feature-name}/            # Feature track (e.g., 001-auth-client/)
    spec.md                         # Feature specification & acceptance criteria
    plan.md                         # Technical implementation plan
    tasks.md                        # Atomic task breakdown
    review.md                       # Spec compliance review
qa-report.md                        # Project-wide quality audit
```

Commands auto-discover your project setup from:

- **`PRD.md`** — Product requirements (used by prd, roadmap, specify, plan)
- **`CLAUDE.md`** — Build commands, conventions, tech stack (used by implement, qa, review, ship)
- **`specs/`** — Feature tracks created by the workflow

No project-specific configuration needed. Commands detect your tech stack, test runner, linter, and formatter automatically.

## Getting started

1. **Create your PRD** through a guided interview
2. **Set the constitution** — non-negotiable project principles
3. **Build the roadmap** — break the PRD into ordered features
4. **Specify** the first feature, then **plan** and **tasks**
5. **Implement** tasks one by one — or run **build** for full automation
6. Check **status** at any time to see where you are and what to do next

See the platform-specific guides for detailed installation and usage instructions.

## License

MIT
