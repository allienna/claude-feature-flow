---
description: Resolve ambiguities in a feature spec before planning. Auto-detects the feature if no argument given.
argument-hint: "[feature-name]"
allowed-tools: Bash(git:*), Read, Edit, Grep, Glob, EnterWorktree
---

# Clarify

Close the gaps in a spec **before** `/plan` builds on them. Every unresolved ambiguity becomes a wrong architecture decision later, which is much more expensive to fix. This command only edits `spec.md` — it never plans or implements.

## Step 0: Detect current state

**Locate the track first.** Features in progress live in their own git worktrees (`.claude/worktrees/{NNN}-{name}`), so `specs/{NNN}-{name}/` may not exist in your current directory. If a feature name is given and its `spec.md` is not found here, run `git worktree list --porcelain` and look in each worktree. If it is found in another worktree, switch to it with the `EnterWorktree` tool (`path` = that worktree) and continue from there; if it exists nowhere, use the usual "run `/specify`" message. With no feature name, consider the tracks of all worktrees and prefer the one in your current worktree.

1. `Glob("specs/[0-9]*/spec.md")` to find all feature tracks
2. For each, read the **Status** and check for `plan.md`

### State routing

**No tracks exist →** "No specs found. Run `/specify` first." STOP.

**`$ARGUMENTS` is empty →** Find the first track whose spec is Draft and contains a `[NEEDS CLARIFICATION` marker (Grep). If none has a marker, take the first Draft spec without a plan. Propose: "Clarifying **{feature-name}** — {N} open marker(s). Proceed?" Wait for confirmation.

**`$ARGUMENTS` provided, no matching track →** "No spec for '$ARGUMENTS'. Run `/specify $ARGUMENTS` first." STOP.

**Track exists and has a `plan.md` →** "A plan already exists. Clarifying the spec may invalidate it. Continue, then re-run `/plan $ARGUMENTS` (overwrite) afterwards?" Wait for confirmation.

## Step 1: Scan for gaps

Read `specs/{NNN}-$ARGUMENTS/spec.md`, plus `PRD.md` (sections it references) and `DESIGN.md` if present. List every gap in these categories:

1. **Explicit markers** — each `[NEEDS CLARIFICATION: …]`.
2. **Untestable acceptance criteria** — not in Given/When/Then or EARS form, vague adjectives ("fast", "intuitive", "secure", "robust"), no observable outcome.
3. **Missing scenarios** — an Error Scenario with no matching AC; a functional requirement (FR) with no AC; no AC for the failure path of an external call.
4. **Contradictions** — spec vs PRD, spec vs `DESIGN.md` inventory, two FRs that cannot both hold.
5. **Undefined terms and data** — an entity, limit, format or permission mentioned but never defined (sizes, timeouts, roles, validation rules).
6. **Scope edges** — behavior that could be in or out of scope and is not listed under "Out of Scope".

Do NOT invent gaps to look thorough: a clean spec is a valid outcome.

If nothing is found: "Spec is clear — no ambiguity found. Run `/plan $ARGUMENTS`." STOP.

## Step 2: Ask, one question at a time

Rank the gaps by impact on architecture and testability, keep the **top 5**, and ask them **one at a time**, waiting for the answer each time. Each question:
- states the gap and where it is (section / `AC-n`)
- proposes 2–3 concrete options with your recommended default first ("Recommended: …")
- accepts "your call" as an answer (record the default as a decision, flagged as assumed)

Remaining gaps beyond 5 stay as `[NEEDS CLARIFICATION]` markers so the next `/clarify` run picks them up.

## Step 3: Update the spec in place

After each answer, edit `spec.md` immediately:
- Replace the marker (or the vague text) with the decided behavior, in the section where it belongs.
- Rewrite affected acceptance criteria as testable scenarios (Given/When/Then).
- Add the AC/FR that was missing, with the next free ids. Never renumber existing ids (tasks and reviews reference them).
- Remove the answered line from `## Open Questions`.
- Append to a `## Clarifications` section at the end of the spec:
  `- {today}: Q: {question} → A: {decision} {(assumed) if the user delegated}`

## Step 4: Present

1. Table: gap → resolution
2. Remaining `[NEEDS CLARIFICATION]` markers (count)
3. **If markers remain: "Run `/clarify $ARGUMENTS` again to continue." Otherwise: "Spec is clean. Review the updated criteria, then run `/plan $ARGUMENTS`."**
