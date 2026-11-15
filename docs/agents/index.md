# Agents

Four subagents ship in `agents/`. Installed as a plugin they are named `feature-flow:<name>`; with `install.sh` they are linked into `.claude/agents/` and keep their bare names.

| Agent | Used by | Writes code? | Tools | Output |
|---|---|---|---|---|
| [`implementer`](implementer.md) | `/build` | yes, inside its task's `Files` only | Read, Write, Edit, Grep, Glob, Bash | JSON report |
| [`spec-reviewer`](spec-reviewer.md) | `/review`, `/build` | no | Read, Grep, Glob, Bash | JSON report |
| [`quality-reviewer`](quality-reviewer.md) | `/review`, `/build` | no | Read, Grep, Glob, Bash | JSON report |
| [`qa-verifier`](qa-verifier.md) | `/qa`, `/build` | no | Read, Grep, Glob, Bash | JSON report |

## Contracts

Every agent ends its reply with **exactly one fenced `json` block** and nothing after it. The block is validated against a JSON Schema in [`schemas/`](../../schemas):

| Agent | Schema |
|---|---|
| implementer | [`implementer.schema.json`](../../schemas/implementer.schema.json) |
| spec-reviewer | [`spec-reviewer.schema.json`](../../schemas/spec-reviewer.schema.json) |
| quality-reviewer | [`quality-reviewer.schema.json`](../../schemas/quality-reviewer.schema.json) |
| qa-verifier | [`qa-verifier.schema.json`](../../schemas/qa-verifier.schema.json) |

A missing or malformed block is never interpreted: an implementer's task counts as failed, a reviewer is relaunched once, and the review records "reviewer returned no valid report" rather than guessing.

## Design rules

- **Least privilege.** Reviewers and the QA verifier are read-only; `Bash` is for running the project's own commands and read-only git.
- **Fresh context.** A worker receives paths and one task, not a transcript.
- **Evidence over assertion.** Reviewers cite `file:line`, test names or command output; no evidence means `WARN`, never `PASS`.
- **Models.** Agents inherit your session model by default. `implementer` declares `sonnet`; you can override any agent's `model` in its frontmatter, for example a faster model for `qa-verifier` and your strongest for `spec-reviewer`. See [Tuning and cost](../guides/tuning-and-cost.md).

## Without the agents

If an agent type is unavailable, `/build`, `/review` and `/qa` fall back to a `general-purpose` agent given the content of the matching `agents/*.md` as its role and output contract.
