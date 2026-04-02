---
description: Generate or update the project constitution from the PRD
allowed-tools: Bash(ls:*), Read, Write, Edit, Grep, Glob
---

# Constitution

You are creating `specs/constitution.md` — the non-negotiable principles for this project. These are things that should never be violated regardless of which feature is being built. Any PR that violates these must be rejected.

## Step 0: Detect current state

1. Check if `specs/constitution.md` exists
2. Check if `PRD.md` exists

### If constitution already exists:
- Show the current constitution
- Ask: "Want to **update** it based on PRD changes, or is it good?"
- Only update if the user asks for changes
- STOP and wait for user input

### If no PRD exists:
- "No PRD.md found. The constitution is derived from the PRD — create or add a PRD first." STOP.

### If no constitution exists:
- Proceed to Step 1

---

## Step 1: Load context

Read:
- `PRD.md` — Full product requirements. Focus on:
  - Problem statement and goals (project context)
  - Architecture and tech stack decisions
  - Configuration requirements (env vars, auth, integrations)
  - Error handling and safety guardrails
  - Risks and mitigations
- `CLAUDE.md` — Existing conventions and quality gates (if missing, WARN: "No CLAUDE.md found. Constitution will be derived from PRD only.")

## Step 2: Extract principles

From the PRD, identify:

1. **Non-negotiable principles** — Security rules, data constraints, architectural invariants. Look for:
   - Authentication and authorization requirements
   - Read/write constraints (e.g., read-only, idempotent operations)
   - Error handling patterns (structured errors, graceful degradation)
   - Rate limits, batch limits, response size bounds
   - Data privacy (no PII in logs, no secrets in code)

2. **Tech stack** — Locked vs flexible choices from the PRD's architecture section

3. **Coding standards** — Rules derived from the architecture and CLAUDE.md:
   - Patterns mandated by the tech stack
   - Architectural patterns (e.g., module organization, client structure)
   - Type safety requirements
   - Naming conventions

4. **Quality gates** — Checklist from CLAUDE.md quality gates + PRD error handling requirements

5. **Compliance & security** — Auth mechanisms, data persistence rules, dependency provenance, transport security

## Step 3: Create specs/ directory if needed

```bash
mkdir -p specs
```

## Step 4: Write specs/constitution.md

Keep it **under 100 lines**. Every line should be something you'd reject a PR for violating.

```markdown
# Project Constitution

> Non-negotiable principles for {Project Name}. Reject any PR that violates these.

## 1. Project Context

{2-3 sentences: what the project does, who it's for, key constraints}

## 2. Non-Negotiable Principles

{Numbered list of hard rules — security, data privacy, error handling, response bounds}

## 3. Tech Stack

| Component | Choice | Locked? |
|-----------|--------|---------|
{From the PRD's architecture section — mark each as Locked or Flexible}

## 4. Coding Standards

{Short, opinionated rules derived from CLAUDE.md and PRD — patterns, type safety, module structure}

## 5. Quality Gates

{Checklist — every PR must pass ALL of these before merge}

## 6. Compliance & Security

{Auth mechanisms, data persistence rules, dependency provenance, transport security}
```

Note: Read the project name from PRD.md or CLAUDE.md. If neither provides a clear name, ask the user.

## Step 5: Present for review

1. Show the constitution
2. Highlight any principles that were judgment calls (not explicitly in the PRD)
3. Ask: **"Review this constitution. Once approved, it will be referenced by `/review` and `/qa` to check compliance."**

## What NOT to include
- Implementation details (those go in feature specs)
- Anything that changes per feature
- Aspirational goals — only things that are true TODAY
- Brand identity (unless relevant to the project)
