---
mode: agent
description: "Generate or update the feature roadmap from the PRD — decompose into ordered, dependency-aware features"
tools: ['editFiles', 'runCommands', 'search', 'codebase']
---

# Roadmap

You are building the project roadmap. This defines WHAT features exist and in WHAT order they should be built. Do NOT write any implementation code.

## Step 0: Detect current state

1. Read `specs/roadmap.md` (if it doesn't exist, note that no roadmap exists yet)
2. Search for `specs/*/spec.md` to find all feature tracks
3. For each track found, read its `spec.md` and extract the **Status** field

### If a roadmap already exists:
- Show the current roadmap with the status of each feature (cross-reference with existing tracks)
- Ask: "Want to **add features**, **reorder**, **split**, or **merge**? Or is the roadmap good — run the specify prompt to start the next feature."
- Only update if the user asks for changes
- STOP and wait for user input

### If no roadmap exists:
- Check if `PRD.md` exists. If not: "No PRD.md found. The roadmap is derived from the PRD — create or add a PRD first." STOP.
- Proceed to Step 1

---

## Step 1: Load context

Read:
- `PRD.md` — Full product requirements (especially sections covering user stories, features, and any recommended implementation sequence)
- `CLAUDE.md` — Tech stack, architecture, conventions (if missing, WARN: "No CLAUDE.md found. Roadmap will be based on PRD only.")

## Step 2: Decompose the PRD into features

Break the PRD into features. Each feature must be:

1. **Self-contained**: Can be built, tested, and demoed independently
2. **Vertically sliced**: Includes all layers (models + logic + interface + tests) for a complete capability
3. **Ordered by dependency**: Feature N depends only on features before it
4. **Right-sized**: Each feature = 1-2 days of work

### Ordering guidelines
- Start with **project foundation** (project config, package structure, core configuration)
- Then **core infrastructure** (clients, services, data access layers)
- Then **feature modules** grouped by domain or capability
- Then **integration** (wiring modules together, end-to-end flows)
- End with **polish and hardening** (error handling, documentation, deployment config)

### Feature mapping from PRD
- If the PRD has an implementation sequence section, use it as the recommended build order
- Feature groupings in the PRD define natural feature boundaries
- Each major section or user story group maps to roughly one feature

## Step 3: Write specs/roadmap.md

```markdown
# {Project Name} — Feature Roadmap

**Generated from**: PRD.md
**Last updated**: {today's date}
**Status**: Draft

## Features

### F-001: {feature-name}
**Summary**: {One sentence — what capability is available after this is built}
**PRD sections**: {e.g., "Architecture, Project Structure, Configuration"}
**Depends on**: None
**Delivers**: {Concrete deliverable — e.g., "project config, core module structure"}
**Estimated size**: S / M / L
**Status**: Not started

### F-002: {feature-name}
**Summary**: ...
**PRD sections**: ...
**Depends on**: F-001
**Delivers**: ...
**Estimated size**: ...
**Status**: Not started

(Continue for all features)

## Dependency Graph

{ASCII diagram showing the dependency chain}

## Milestones

### M1: Foundation (F-001 through F-00X)
{After these, project scaffold and core infrastructure are ready}

### M2: Core Features (F-00X through F-00Y)
{After these, the main capabilities are implemented}

### M3: Integration & Ship (F-00Y through F-00Z)
{End-to-end flows tested, ready for deployment}
```

Note: Read the project name from PRD.md or CLAUDE.md. If neither provides a clear name, ask the user.

## Step 4: Present for review

1. Feature table:
   | # | Feature | Depends on | Size |
2. Milestones with included features
3. Dependency graph (ASCII)
4. Ask: **"Review this roadmap. Once approved, run the specify prompt to start the first feature."**
