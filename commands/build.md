---
description: "Orchestrated pipeline: implement tasks in parallel waves → review → converge → qa → ship. Use /build quick to skip review and ship."
argument-hint: "[quick] [--parallel=N] [--sequential] [--isolate=worktree|none] [--max-rounds=N] [feature-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
---

# Build — Orchestrated Feature Pipeline

You are the **orchestrator**. You do not write feature code yourself: you dispatch workers, wait at a barrier, merge their structured reports, and update state. This keeps your context small (reports, not source files) and keeps authors separate from reviewers.

```
tasks.md ──► waves ──► [fan-out: implementer × N] ──barrier──► [fan-in: reports → tasks.md]
                                                                    │
            wave checks (test/lint/format/typecheck, once) ◄────────┘
                                                                    ▼
         [fan-out: spec-reviewer ‖ quality-reviewer] ──► merge ──► review.md
                       │ issues? ──► corrective tasks ──► back to the waves (max rounds)
                       ▼
                 qa-verifier ──► qa-report.md ──► ship
```

**Modes**:
- `/build [feature]` — Full pipeline: implement → review (+ convergence) → qa → ship
- `/build quick [feature]` — Implement → qa quick (skip review, convergence and ship)

**Options** (parse them out of `$ARGUMENTS`, the remaining word is the feature name):
- `quick` → `QUICK_MODE=true`
- `--parallel=N` → max workers per wave (default **3**; ≥ 6 is rarely worth the token cost and merge risk)
- `--sequential` → same as `--parallel=1`
- `--max-rounds=N` → max convergence rounds (default **2**)
- `--isolate=worktree|none` → how parallel workers are isolated (default **`worktree`** for waves of 2+ tasks; a single-task wave always runs in place). `none` = shared working tree, protected only by disjoint `Files` and a `git status` scope check — use it when per-worktree setup is too heavy or tests share a fixed port/database

**Agents**: `implementer`, `spec-reviewer`, `quality-reviewer`, `qa-verifier`. Installed as a plugin their `subagent_type` is `claude-feature-flow:{name}`; installed with `install.sh` it is `{name}`. If a type is not available, launch a `general-purpose` agent and give it the content of the matching `agents/{name}.md` as its role and output contract.

---

## Step 0: Detect state

1. `Glob("specs/[0-9]*/spec.md")` to find all feature tracks
2. For each track, read its `spec.md` and check for `plan.md`, `tasks.md`, `review.md`
   - Extract the **Status** field from spec.md
   - If tasks.md exists, count `[x]` (done) and `[ ]` (pending) items
   - If review.md exists, read its **Verdict**

### Discover build commands

Read `CLAUDE.md` and extract test, lint, format, and type check commands. If `CLAUDE.md` is missing or doesn't define build commands: WARN "No build commands found in CLAUDE.md. Workers will implement tasks but cannot run automated checks. Add a '## Build & Run Commands' section to enable quality gates."

### State routing

**No tracks exist →** "No features found. Start with `/roadmap`." STOP.

**Feature name is empty →** Find the first track that has tasks.md with unchecked items. Propose: "Building **{feature-name}** — {pending} tasks remaining. Proceed?" Wait for confirmation.

**Feature name provided, no matching track →** "No spec for '{name}'. Run `/specify {name}` first." STOP.

**Feature name provided, track exists →** Check state:
- Spec contains `[NEEDS CLARIFICATION` → "Spec has unresolved questions. Run `/clarify {name}`." STOP.
- No plan → "No plan. Run `/plan {name}` first." STOP.
- No tasks → "No tasks. Run `/tasks {name}` first." STOP.
- All tasks checked + review verdict "Ready to merge" or "Pass with notes" → "Feature already reviewed. Run `/ship {name}` to create the PR." STOP.
- Has unchecked tasks → Proceed to Step 1.
- All tasks checked, no review (or review verdict "Needs work") → Skip to Step 2 (or Step 3 in quick mode).

### Preflight (git)

- **Branch**: `git branch --show-current` must equal the spec's **Branch** (`feat/{NNN}-{feature}`). If you are on `main` or another branch → STOP: "Not on the feature branch. Enter the feature worktree (`.claude/worktrees/{NNN}-{feature}`) or `git switch feat/{NNN}-{feature}`."
- **Dependencies**: every feature listed in the spec's **Depends on** must be merged into `main` (`git branch --merged main` / its spec is `Complete` on `main`). If not → STOP: "Feature {dep} is not merged yet — `/build` needs its code. Specs, plans and tasks can proceed in parallel; the build cannot."
- **Worktree isolation** (`--isolate=worktree`): needs a git repo with at least one commit, and Claude Code's `worktree.baseRef` set to `"head"` so worker worktrees start from this branch instead of the default branch. This is verified automatically on the first parallel wave (see 1b); you do not need to check the setting yourself.

Print: "**Build mode**: {full | quick} · parallel={N} · isolate={worktree|none} · max-rounds={R}" and proceed.

---

## Step 1: Implement by waves (fan-out / fan-in)

### 1a. Plan the waves

Read `specs/{NNN}-{feature}/tasks.md`. Build the task table: id, checked?, `Depends-on`, `Files`, `Covers`.

- Use the `## Execution Waves` table if present. Otherwise, or if any task lacks `Depends-on`/`Files`, treat the file as **sequential**: one task per wave, in file order (legacy format).
- Re-validate before launching: dependencies exist, no cycle, and within each wave the `Files` of tasks are pairwise disjoint. If two tasks of a wave overlap, move the later one to the next wave (never run them together).
- A task is **ready** when it is unchecked and all its dependencies are checked.

Print: "**Implementing {feature}** — {pending}/{total} tasks · {W} waves remaining".

### 1b. For each wave, in order

Let `ISOLATE` = `worktree` if `--isolate=worktree` (default) **and** the batch has 2+ tasks; otherwise `none` (the batch runs in place).

**Common to both modes**

1. **Select** the ready tasks of the wave, at most `--parallel` at a time (extra tasks form follow-up batches of the same wave).
2. **Prompt each worker** with only what it needs: the task block verbatim (`id`, title, **Do**, **Test**, **Files**, **Covers**); paths to `spec.md`, `plan.md`, `CLAUDE.md`, and `DESIGN.md` when the plan has a "Design Mobilization" section; the discovered build commands; the **Worktree Setup** commands from `CLAUDE.md` (worktree mode only); `mode: worktree|none`; for a retry, the previous report's `blockers`. Do NOT paste source code into the prompt and do NOT read source files yourself.
3. **Barrier**: continue only when every worker of the batch has returned. Never read a worker's partial output.
4. **Fan-in — parse** each worker's final fenced `json` block (contract: `schemas/implementer.schema.json`). Valid when it has `task_id`, `status`, `files_changed`, `tests_passed` (and, in worktree mode, `base_sha`, `head_sha`, `branch`). A missing or malformed block → the task is `failed` with blocker "no valid report".
5. **Wave checks** (once, by you, after integration): run the discovered test, lint, format and type check commands over the project. On failure, identify the offending task(s) from the output, relaunch **one** `implementer` (in place) with the failure as `blockers_from_previous_attempt`, and re-run the checks.
6. **Report**: one line per task — `T-X.Y — {title} — {done|failed|blocked}` — and `({done}/{total})`.
7. **Retry once**: a `failed` task is relaunched one time with its blockers (fresh worktree if in worktree mode). A task still failed, or `blocked` (needs a file outside its scope, missing design component, …), triggers the gate below.

**`ISOLATE = none` (shared working tree)**

- Before fan-out, snapshot `git status --porcelain`.
- Fan-out: launch ALL workers **in a single message**, one `implementer` Agent call per task, no `isolation` parameter.
- After the barrier — **scope check**: compare `git status --porcelain` with the snapshot. Any changed path outside the union of the batch's `Files` → STOP: "Out-of-scope edit by a worker: {paths}." (Reverting is the user's call; do not auto-revert.)
- `done` + `tests_passed: true` → **you** change `- [ ]` to `- [x]` in tasks.md. Workers never edit it.

**`ISOLATE = worktree` (one worktree + branch per worker)**

1. **Baseline**: the worktrees start from this branch's `HEAD`, so `HEAD` must contain everything done so far. If `git status --porcelain` is not empty: stage and commit **only** `specs/{NNN}-{feature}/` and the files declared in `Files` of already-checked tasks as `chore(build): wave {n} baseline`. Any other dirty path → STOP: "Uncommitted changes outside this track: {paths}. Commit or stash them, or use `--isolate=none`." Record `BASE=$(git rev-parse HEAD)`. (These checkpoint commits disappear in the squash merge of the PR.)
2. **Fan-out**: launch ALL workers **in a single message**, one `implementer` Agent call per task, each with `isolation: "worktree"`. Each worker works only in its own worktree, runs the Worktree Setup commands, implements its task, runs the task's **Test**, and **commits once** on its own branch.
3. **Barrier**, then for each worker read from the Agent result its `<worktree>` block (`worktreePath`, `worktreeBranch`) and from its JSON report `base_sha`, `head_sha`:
   - **Base guard**: `base_sha` must equal `BASE`. If not → STOP with: "Worker worktrees did not start from this branch (they started from {base_sha}, expected {BASE}). Set `worktree.baseRef` to `"head"` in your Claude Code settings (see docs/guides/troubleshooting.md), or re-run with `--isolate=none`." Do not merge anything.
   - **Scope check**: `git diff --name-only BASE..{branch}` must be a subset of that task's `Files`. Otherwise the task is `failed` (blocker "out-of-scope edit: {paths}") and its branch is not merged.
4. **Fan-in — merge** the accepted branches one at a time, in task-id order: `git merge --no-ff --no-edit {branch}`.
   - Conflict → `git merge --abort`; the task stays unchecked and is re-run **alone** in the next batch (it will then start from the merged `HEAD`). Print: "Merge conflict between {task} and earlier tasks of the wave: their `Files` overlap in practice. Fix `Files`/`Depends-on` in tasks.md." A conflict means the declared `Files` were wrong, not that the worker is at fault.
   - Success → **you** change `- [ ]` to `- [x]` for that task.
5. Run the **wave checks** on the integrated tree (common step 5).
6. **Cleanup**: for every worker branch, `git worktree remove --force {worktreePath}` then `git branch -D {branch}` (merged or discarded — a retry starts from a fresh worktree).

**Gate**: if any task is still failed or blocked after retries, finish the current batch's bookkeeping, then **STOP**: "Build stopped at {task ids} — {reasons}. Fix (or adjust `Files`/`Depends-on` in tasks.md) and re-run `/build {feature}` to resume." Do not start the next wave.

After all waves: "All {total} tasks implemented."

---

## Step 2: Review (full mode only) — fan-out / fan-in

**If `QUICK_MODE=true` → skip to Step 3.**

Execute the `/review` procedure (its Step 1–7): in parallel, in a single message, launch `spec-reviewer` and `quality-reviewer`; merge their JSON reports into `review.md`; derive the verdict. These agents did not write the code — that separation is the point.

### Gate and convergence

- **Verdict "Ready to merge" or "Pass with notes"** → Continue to Step 3.
- **Verdict "Needs work"** → enter the convergence loop (below). Without `--max-rounds` budget left, STOP: "Build stopped at review — see `specs/{NNN}-{feature}/review.md`. Fix and re-run `/build {feature}`."

### Convergence loop (`round = 1 … max-rounds`)

1. Turn every `issues` entry of severity `blocker` or `major` (and every `FAIL` AC) into a **corrective task**: append a `## Phase C{round}: Convergence round {round}` section to tasks.md with tasks `T-C{round}.{k}` using the normal format (`Covers: AC-n`, `Depends-on`, `Files`, **Do** = the reviewer's `fix`, **Test**). Recompute the `## Execution Waves` table for the new tasks (same rules as `/tasks`). `minor` issues stay in review.md as notes.
2. Run **Step 1** again (it only picks up the unchecked tasks).
3. Run **Step 2** again and record the round in review.md's `## Convergence History` (round, failing ACs, blocker+major count).
4. **Stop conditions**:
   - verdict is no longer "Needs work" → done, continue to Step 3;
   - **no progress**: the number of failing ACs plus blocker/major issues did not decrease compared with the previous round → STOP: "Convergence stalled after round {n}: {remaining issues}. Human decision needed.";
   - `max-rounds` reached → STOP with the remaining issues listed.

---

## Step 3: QA

Run the `/qa` procedure (it delegates the checks to a `qa-verifier` worker):
- **Full mode**: full QA
- **Quick mode**: `/qa quick` (automated checks only)

### Gate check
- **Verdict: FAIL** → STOP. "Build stopped at QA — see `qa-report.md` for details. Fix issues and re-run `/build {feature}`."
- **Verdict: PASS or WARN** → Continue to Step 4 (or STOP in quick mode).

**If `QUICK_MODE=true` → STOP here.** Print: "Quick build complete — {total} tasks implemented, QA {verdict}. Run `/review {feature}` then `/ship {feature}` when ready."

---

## Step 4: Ship (full mode only)

Run the `/ship` procedure (branch if needed, commit `feat({NNN}): {feature name}`, push, open PR). `/ship` keeps its own human confirmation of the commit message and reviewer — the pipeline never skips that gate.

---

## Resume behavior

`/build` is stateless between runs; everything it needs is on disk:
- Unchecked tasks → Step 1, ready tasks of the first incomplete wave (checked tasks are never redone)
- All tasks done, no review or "Needs work" → Step 2
- Review OK, no QA → Step 3
- QA done, not shipped → Step 4

An interrupted wave is safe to resume: workers that did not report leave their tasks unchecked, and the worker rule "write only inside `Files`" bounds any partial edits. After an interruption in worktree mode, leftover `worktree-agent-*` worktrees/branches (listed by `git worktree list`) can hold unmerged work: inspect, then remove them with `git worktree remove --force` and `git branch -D`; the tasks they covered are simply re-run.
