---
description: Read-only consistency analysis across PRD, constitution, spec, plan, tasks and DESIGN.md. Auto-detects the feature if no argument given.
argument-hint: "[feature-name]"
allowed-tools: Bash(git:*), Read, Grep, Glob, Agent, EnterWorktree
---

# Analyze

Cross-check the artifacts of a feature for drift **before** implementation (or after a spec change). This command is **strictly read-only**: it writes no file and changes no status. It reports; you decide.

```
PRD ◄──► spec ◄──► plan ◄──► tasks        constitution ──► all
            ▲                  │              DESIGN.md ──► spec/plan
            └── AC coverage ───┘
```

## Step 0: Detect current state

**Locate the track first.** Features in progress live in their own git worktrees (`.claude/worktrees/{NNN}-{name}`), so `specs/{NNN}-{name}/` may not exist in your current directory. If a feature name is given and its `spec.md` is not found here, run `git worktree list --porcelain` and look in each worktree. If it is found in another worktree, switch to it with the `EnterWorktree` tool (`path` = that worktree) and continue from there; if it exists nowhere, use the usual "run `/specify`" message. With no feature name, consider the tracks of all worktrees and prefer the one in your current worktree.

1. `Glob("specs/[0-9]*/spec.md")` to find all feature tracks
2. `$ARGUMENTS` empty → the first track that has a spec and no `review.md` (prefer one with a plan or tasks). Propose and wait for confirmation. No match for `$ARGUMENTS` → "No spec for '$ARGUMENTS'." STOP.
3. Need at least a `spec.md` plus one more artifact (`plan.md` or `PRD.md`) to compare. Otherwise: "Nothing to cross-check yet." STOP.

## Step 1: Fan-out — one read-only analyst per artifact pair

Launch in **a single message**, in parallel, one `general-purpose` agent per applicable pair (skip a pair whose artifacts do not exist). (The built-in `Explore` agent only reads excerpts, which is not enough to compare documents.) Each agent gets only the paths of its artifacts, is told to use **only Read, Grep and Glob** (no Write/Edit/Bash), and must end with one fenced `json` block.

| # | Pair | Looks for |
|---|------|-----------|
| A | PRD ↔ spec | FR/AC contradicting or silently dropping a PRD requirement; scope the PRD never asked for |
| B | spec ↔ plan | Every FR/AC has an architecture decision or implementation phase; every `AD-n` traces to a requirement; plan contradicting the spec; unresolved `[NEEDS CLARIFICATION]` |
| C | plan ↔ tasks | Every file of the plan's "Affected Files" is in some task's `Files`; no task outside the plan; `Depends-on` consistent with plan phases; wave validity (acyclic, disjoint `Files` per wave) |
| D | spec ↔ tasks | **AC coverage**: every `AC-n` in the `Covers` of at least one task; tasks whose `Test` cannot verify the AC they claim |
| E | constitution + DESIGN.md ↔ spec/plan | Plan decisions violating a constitution principle; components/tokens used but absent from `DESIGN.md`; Design Mobilization inconsistent with Design References |

Prompt template for each analyst: "Compare {artifact X} and {artifact Y} for: {looks for}. Read-only: do not edit anything. End with ```json {\"pair\": \"A\", \"findings\": [{\"severity\": \"critical|major|minor\", \"ids\": [\"AC-3\", \"AD-2\"], \"where\": \"file:section\", \"description\": \"\", \"suggested_fix\": \"\"}]}```. Report only verifiable inconsistencies, each with the ids/lines involved; an empty list is fine."

## Step 2: Barrier and fan-in

Wait for all analysts. A missing/malformed block → note "pair {X}: no valid result" (do not infer findings). Merge, deduplicate findings pointing at the same ids (keep the highest severity), and sort `critical` > `major` > `minor`.

## Step 3: Report (printed, not written)

```
Analysis — {feature}
===============================
Artifacts compared: {list of pairs run}

| Sev | Where | Finding | Suggested fix |
|-----|-------|---------|---------------|

AC coverage: {covered}/{total} — uncovered: {AC ids}
Verdict: CLEAN | NEEDS ATTENTION ({n} critical, {m} major) 
```

Then ONE recommendation:
- critical/major on spec or AC → "`/clarify {name}`"
- critical/major on plan ↔ tasks or coverage → "`/tasks {name}` (overwrite) or edit `tasks.md`"
- spec ↔ plan mismatch → "`/plan {name}` (overwrite)"
- clean → "Artifacts are consistent. Next: {the normal next command from `/status`}"
