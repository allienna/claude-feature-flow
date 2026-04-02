---
mode: agent
description: "Create or update the Product Requirements Document through guided discovery"
tools: ['editFiles', 'runCommands', 'search', 'codebase', 'changes']
---

# PRD — Product Requirements Document

You are creating `PRD.md` — the single source of truth for what is being built, for whom, and why. Every other command in this workflow depends on it.

## Step 0: Detect current state

1. Check if `PRD.md` exists in the project root
2. Check if `CLAUDE.md` exists

### If PRD already exists:
- Read and display a summary of the current PRD (sections and key points)
- Ask: "Want to **update** a section, **add** new requirements, or **rewrite** from scratch?"
- If updating: ask which section, make targeted changes, show the diff
- STOP and wait for user input

### If no PRD exists:
- Proceed to Step 1

---

## Step 1: Discovery interview

Conduct a structured interview in 5 phases. For each phase:
- Present the questions clearly
- **Wait for the user's response before moving to the next phase**
- Take notes on their answers — you'll use them to generate the PRD
- If the user provides partial answers, ask follow-up questions to fill gaps
- If the user says "skip" or "not applicable", mark the section as N/A and move on

### Phase 1 — Vision & Context

Ask these questions (adapt wording naturally, don't read them robotically):

1. **What are you building?** Give me the elevator pitch — one paragraph.
2. **What problem does it solve?** What's the current pain or gap?
3. **Who are the target users?** Roles, personas, or user types.
4. **What does success look like?** Key metrics, goals, or outcomes.

After receiving answers, summarize what you understood and confirm before proceeding.

### Phase 2 — Features & User Stories

1. **What are the core things a user can DO with this?** List the main capabilities.
2. **Walk me through a typical user journey.** From first interaction to completing their goal.
3. **What's must-have vs nice-to-have?** Help me prioritize.
4. **Anything explicitly out of scope?** Things people might expect but you won't build.

Group the features into logical domains as you listen. These groups will become the roadmap features later.

### Phase 3 — Technical Foundation

1. **What's the tech stack?** Languages, frameworks, databases — or constraints/preferences if undecided.
2. **Any existing systems to integrate with?** APIs, databases, services, auth providers.
3. **Where will this run?** Cloud provider, on-prem, serverless, containers, etc.
4. **Architectural preferences?** Monolith, microservices, monorepo, specific patterns.

If `CLAUDE.md` exists, cross-reference its tech stack section and ask about discrepancies.

### Phase 4 — Quality & Security

1. **How do users authenticate?** OAuth, API keys, SSO, public access?
2. **Any sensitive data?** PII, financial data, health records — compliance requirements (GDPR, SOC2, HIPAA)?
3. **Performance expectations?** Latency targets, throughput, concurrent users, data volume.
4. **How should errors be handled?** Fail fast, graceful degradation, retry logic, user-facing error messages.

If the user is unsure about some of these, suggest sensible defaults based on the tech stack and project type.

### Phase 5 — Scope & Risks

1. **Known risks or unknowns?** Technical challenges, external dependencies, unproven approaches.
2. **Timeline or milestone constraints?** Deadlines, demo dates, release targets.
3. **Dependencies on external teams or services?** Anything that could block progress.

This phase is optional — if the user has nothing to add, skip it.

---

## Step 2: Generate PRD

After all phases are complete, generate `PRD.md` using the structure below. Every section maps to a downstream consumer:

```markdown
# {Project Name} — Product Requirements Document

**Last updated**: {today's date}
**Status**: Draft

## 1. Overview

### Problem Statement
{What pain or gap exists — from Phase 1}

### Goals & Success Metrics
{Measurable outcomes — from Phase 1}

### Target Users
| Persona | Description | Primary needs |
|---------|-------------|---------------|
{From Phase 1}

## 2. User Stories

### {Domain/Feature Group A}
- As a {persona}, I want to {action} so that {benefit}
- ...

### {Domain/Feature Group B}
- ...

{Grouped by domain — from Phase 2. These groups inform /roadmap feature decomposition.}

## 3. Functional Requirements

### {Feature Group A}
#### FR-1: {Requirement title}
{Detailed description}
**Acceptance criteria**:
- [ ] {Testable criterion}

### {Feature Group B}
#### FR-N: ...

{From Phase 2 — must-haves first, then nice-to-haves clearly separated.}

## 4. Non-Functional Requirements

### Performance
{Latency, throughput, scale targets — from Phase 4}

### Reliability
{Uptime targets, failover, data durability — from Phase 4}

### Scalability
{Growth expectations, horizontal/vertical scaling approach}

## 5. Architecture & Tech Stack

### System Architecture
{High-level architecture — components and their relationships. ASCII diagram if helpful.}

### Tech Stack
| Component | Choice | Rationale |
|-----------|--------|-----------|
{From Phase 3}

### Integrations
| System | Purpose | Interface |
|--------|---------|-----------|
{External systems — from Phase 3}

## 6. Error Handling

### User-Facing Errors
{How errors are communicated to users — from Phase 4}

### Internal Error Patterns
{Logging, monitoring, alerting approach — from Phase 4}

### Graceful Degradation
{What happens when dependencies fail — from Phase 4}

## 7. Security & Compliance

### Authentication & Authorization
{Auth model — from Phase 4}

### Data Privacy
{PII handling, encryption, retention policies — from Phase 4}

### Compliance
{Regulatory requirements — from Phase 4, or N/A}

## 8. Configuration

### Environment Variables
| Variable | Purpose | Required |
|----------|---------|----------|
{Derived from architecture and integrations}

### External Services
{Service dependencies and their configuration}

## 9. Implementation Sequence

{Recommended build order. This section is directly consumed by /roadmap.}

### Phase 1: Foundation
{What to build first — project setup, core infrastructure}

### Phase 2: Core Features
{Primary capabilities, in dependency order}

### Phase 3: Integration & Polish
{Wiring, end-to-end flows, hardening}

## 10. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
{From Phase 5}

## 11. Out of Scope

{Explicit exclusions — from Phase 2 and Phase 5. Prevents scope creep.}
- {Thing people might expect but we won't build}
```

### Writing guidelines

- **Be specific, not aspirational.** "API responses under 200ms at p95" not "fast API."
- **Include acceptance criteria** on every functional requirement — downstream commands use them.
- **Group features by domain** — these groups become the roadmap features.
- **Implementation sequence is critical** — the roadmap command uses it as the build order.
- **Mark nice-to-haves clearly** — separate them from must-haves in section 3.
- **Keep it under 300 lines** — long PRDs don't get read.

## Step 3: Present for review

1. Show a summary table:
   | Section | Content |
   |---------|---------|
   | Users | {count} personas |
   | Features | {count} requirements across {count} groups |
   | Tech stack | {key choices} |
   | Security | {auth model} |
   | Risks | {count} identified |

2. Highlight any sections marked N/A or where you made assumptions
3. Ask: **"Review this PRD. Once approved, run the constitution prompt to set the rules, then the roadmap prompt to plan the features."**

## Step 4: Save and suggest next steps

After the user approves (or asks for edits and approves the revision):

1. Write `PRD.md` to the project root
2. Suggest the workflow:
   ```
   constitution  → Set non-negotiable principles
   roadmap       → Break PRD into ordered features
   specify       → Detail the first feature
   ```
