#!/usr/bin/env python3
"""Generate docs/commands/*.md from commands/*.md.

Frontmatter (description, argument-hint, allowed-tools) and the step outline are
extracted from the real command files, so they cannot drift. The prose summary
per command lives in META below: update it when a command's contract changes.

Usage: python3 scripts/gen-command-docs.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CMD = ROOT / "commands"
OUT = ROOT / "docs" / "commands"

META = {
    "prd": dict(group="Foundations", summary="Guided discovery interview that produces the Product Requirements Document.",
        reads="existing `PRD.md` (update mode)", writes="`PRD.md` (after you approve)", gates="Five interview phases, each waits for your answers; the file is written only after approval.", next="`/constitution`"),
    "constitution": dict(group="Foundations", summary="Derives the non-negotiable project principles from the PRD, and offers a portable `AGENTS.md`.",
        reads="`PRD.md`, `CLAUDE.md`", writes="`specs/constitution.md`, optionally `AGENTS.md`", gates="You approve the principles; `AGENTS.md` is written only if you agree.", next="`/design` (UI projects) or `/roadmap`"),
    "design": dict(group="Foundations", summary="Creates or updates `DESIGN.md`: tokens, component inventory, surfaces, states and accessibility baseline. Reconciles mockups from `design/mockups/`.",
        reads="`PRD.md`, constitution, `design/mockups/`", writes="`DESIGN.md`", gates="Interview phases; confirms before writing. `/design update` changes an existing system without redoing it.", next="`/roadmap`"),
    "roadmap": dict(group="Foundations", summary="Breaks the PRD into ordered features `F-001…` with dependencies, sizes and milestones.",
        reads="`PRD.md`, `CLAUDE.md`, `DESIGN.md`", writes="`specs/roadmap.md`", gates="You approve scope and order. Statuses in this file are informational: they are derived by `/status`.", next="`/specify`"),
    "specify": dict(group="Feature", summary="Creates the feature's git worktree and branch, then writes its spec with testable acceptance criteria.",
        reads="roadmap, `PRD.md`, `CLAUDE.md`, `DESIGN.md`, every worktree's `specs/`", writes="worktree `.claude/worktrees/NNN-name`, branch `feat/NNN-name`, `spec.md`", gates="Stops if foundations are uncommitted on `main`; warns on unmet dependencies; you review the spec.", next="`/clarify` (if markers) or `/plan`"),
    "clarify": dict(group="Feature", summary="Resolves ambiguities in a spec, one question at a time, and edits the spec in place.",
        reads="`spec.md`, `PRD.md`, `DESIGN.md`", writes="`spec.md`", gates="At most five questions per run; recommended default offered for each.", next="`/plan`"),
    "plan": dict(group="Feature", summary="Writes the technical plan: architecture decisions, affected files, phases, parallelism notes, test strategy.",
        reads="`spec.md`, `PRD.md`, `CLAUDE.md`, `DESIGN.md`, the codebase", writes="`plan.md`; spec status → Approved", gates="Refuses while `[NEEDS CLARIFICATION]` markers remain or acceptance criteria are not testable.", next="`/tasks`"),
    "tasks": dict(group="Feature", summary="Breaks the plan into atomic tasks with dependencies, write scopes and AC coverage, and computes parallel execution waves.",
        reads="`spec.md`, `plan.md`, `CLAUDE.md`", writes="`tasks.md`; spec status → In Progress", gates="Every acceptance criterion must be covered by a task; dependency cycles are errors; asks before overwriting existing tasks.", next="`/analyze` (optional), then `/build` or `/implement`"),
    "analyze": dict(group="Feature", summary="Read-only consistency check across PRD, constitution, spec, plan, tasks and `DESIGN.md` using parallel analysts.",
        reads="all feature artifacts", writes="nothing (prints a report)", gates="None; it only reports.", next="the command its recommendation names"),
    "implement": dict(group="Feature", summary="Implements the next pending task in your own context (manual mode).",
        reads="`tasks.md`, `spec.md`, `plan.md`, `CLAUDE.md`, `DESIGN.md`, sources", writes="code; ticks the task in `tasks.md`", gates="Stops if a design component is missing from the inventory; honors the task's `Files` scope; one task per call.", next="`/implement` again, then `/review`"),
    "build": dict(group="Automation", summary="The orchestrator: implements tasks in parallel waves with isolated workers, reviews with independent agents, converges on gaps, runs QA, and hands over to `/ship`.",
        reads="`tasks.md`, `spec.md`, `plan.md`, `CLAUDE.md`, `DESIGN.md`", writes="code, `tasks.md` checkboxes, `review.md`, `qa-report.md`", gates="Stops on failed/blocked tasks, merge conflicts, out-of-scope edits, base-guard failure, stalled convergence, QA FAIL. The ship step keeps its own commit-message confirmation; `quick` mode skips review, convergence and ship.", next="`/ship`"),
    "review": dict(group="Feature", summary="Independent review by `spec-reviewer` and `quality-reviewer` in parallel, merged into `review.md` with a mechanical verdict.",
        reads="`spec.md`, `plan.md`, `tasks.md`, constitution, PRD, `DESIGN.md`", writes="`review.md`; spec status → Complete if OK", gates="Verdict: Ready to merge / Pass with notes / Needs work. On Needs work it can append corrective tasks.", next="`/qa` then `/ship`"),
    "qa": dict(group="Feature", summary="Project-wide quality audit delegated to the isolated `qa-verifier` agent.",
        reads="`CLAUDE.md`, config, constitution, specs", writes="`qa-report.md` (repository root)", gates="Verdict PASS / WARN / FAIL. `/qa quick` runs automated checks and the coverage-gap audit only.", next="`/ship`"),
    "ship": dict(group="Delivery", summary="Runs quality gates, commits, pushes and opens the pull request from the feature branch.",
        reads="`review.md`, `CLAUDE.md`, `spec.md`", writes="commit, push, PR", gates="You confirm the commit message; verifies you are on the feature branch; warns without a good review.", next="`/merge`"),
    "merge": dict(group="Delivery", summary="Answers PR review comments, squash merges, updates `main` and removes the feature worktree and branches.",
        reads="PR, comments (via `gh`)", writes="merge commit on `main`; removes worktree and branches", gates="You confirm the squash message and any reply to a comment you'd dismiss.", next="`/specify` (next feature)"),
    "review-pr": dict(group="Delivery", summary="Fetches PR review comments, fixes the issues and replies to each comment.",
        reads="PR comments (via `gh`)", writes="fixes, commits, replies", gates="You confirm before fixes are applied.", next="`/merge`"),
    "status": dict(group="Navigation", summary="Shows roadmap progress (derived from tracks), active worktrees and the single next action to take.",
        reads="roadmap, every worktree's `specs/`, `git worktree list`", writes="nothing", gates="Read-only.", next="the recommended command"),
}

def parse(path):
    text = path.read_text()
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    body = text
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
        body = text[m.end():]
    outline = [(len(h.group(1)), h.group(2).strip()) for h in re.finditer(r"^(#{2,3}) (.+)$", body, re.M)]
    return fm, outline

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    names = sorted(p.stem for p in CMD.glob("*.md"))
    missing = [n for n in names if n not in META]
    if missing:
        raise SystemExit(f"Add META entries for: {', '.join(missing)}")
    stale = [n for n in META if n not in names]
    if stale:
        raise SystemExit(f"META has no command file for: {', '.join(stale)}")
    for n in names:
        fm, outline = parse(CMD / f"{n}.md")
        meta = META[n]
        lines = [f"# `/{n}`", "", f"> {fm.get('description', meta['summary'])}", "",
                 "<!-- generated by scripts/gen-command-docs.py from commands/%s.md — do not edit -->" % n, "",
                 meta["summary"], "",
                 "| | |", "|---|---|",
                 f"| **Usage** | `/{n}" + (f" {fm['argument-hint']}" if fm.get("argument-hint") else "") + "` |",
                 f"| **Reads** | {meta['reads']} |",
                 f"| **Writes** | {meta['writes']} |",
                 f"| **Gates** | {meta['gates']} |",
                 f"| **Next** | {meta['next']} |",
                 f"| **Tools** | `{fm.get('allowed-tools', '—')}` |", ""]
        if outline:
            lines += ["## Procedure outline", "", "Extracted from the command source:", ""]
            for lvl, title in outline:
                lines.append(("  " * (lvl - 2)) + f"- {title}")
            lines.append("")
        lines += [f"Source: [`commands/{n}.md`](../../commands/{n}.md)", ""]
        (OUT / f"{n}.md").write_text("\n".join(lines))
    groups = {}
    for n in names:
        groups.setdefault(META[n]["group"], []).append(n)
    idx = ["# Command reference", "", "<!-- generated by scripts/gen-command-docs.py — do not edit -->", "",
           "Installed as a plugin, every command is also available namespaced: `/feature-flow:<command>`.", ""]
    for g in ["Foundations", "Feature", "Automation", "Delivery", "Navigation"]:
        if g not in groups:
            continue
        idx += [f"## {g}", "", "| Command | What it does |", "|---|---|"]
        for n in groups[g]:
            idx.append(f"| [`/{n}`]({n}.md) | {META[n]['summary']} |")
        idx.append("")
    (OUT / "index.md").write_text("\n".join(idx))
    print(f"generated {len(names)} command pages + index")

if __name__ == "__main__":
    main()
