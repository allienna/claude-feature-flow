---
description: Run project-wide quality audit
argument-hint: "[quick]"
allowed-tools: Bash, Read, Write, Grep, Glob, Agent
---

# QA — Quality Audit

Run a project-wide health check: tests, linting, type checking, security scanning, and spec compliance.

**Modes**: `/qa` = full audit, `/qa quick` = automated checks + coverage gap audit only

## Step 1 — Delegate the checks

The checks produce large outputs (test logs, lint dumps) that do not belong in your context. Launch ONE `qa-verifier` agent (`feature-flow:qa-verifier` when installed as a plugin, `qa-verifier` with the symlink install; otherwise a `general-purpose` agent given `${CLAUDE_PLUGIN_ROOT}/agents/qa-verifier.md` (or `.claude/agents/qa-verifier.md`) as its role) with `mode` = `full` or `quick`. It detects the stack, discovers the build commands from `CLAUDE.md`, runs the automated checks, the coverage gap audit and (full mode) the security scan, spec compliance and dependency checks, then returns one fenced `json` block.

- Returns `{"verdict": "NO_SOURCE"}` → "No source code to audit yet. Build some features first." STOP.
- No valid `json` block → relaunch once; if it still fails, report "QA verifier returned no valid result" and STOP (do not invent results).

## Step 2 — Generate QA Report

Using the verifier's `categories`, `coverage_gaps` and `recommendations`, you write `qa-report.md` in the **project root** with this structure:

```markdown
# QA Report

**Date**: YYYY-MM-DD HH:MM
**Mode**: Full / Quick
**Verdict**: PASS / WARN / FAIL

## Summary

| Category | Status | Details |
|----------|--------|---------|
| Lint | PASS/FAIL/SKIP | N issues |
| Format | PASS/FAIL/SKIP | N files |
| Type check | PASS/FAIL/SKIP | N errors |
| Test | PASS/FAIL/SKIP | X passed, Y failed |
| Coverage gaps | WARN | [list] |
| Security | PASS/WARN/FAIL | N/3 checks passed |
| Spec compliance | PASS/WARN/FAIL/SKIP | N checks passed |
| Dependencies | PASS/WARN | N packages |

## Details

[Per-category details with specific errors and recommendations]

## Recommendations

[Actionable items to fix any WARN or FAIL results]
```

**Verdict logic**:
- **PASS**: All categories PASS (SKIP is acceptable)
- **WARN**: Any category is WARN but none are FAIL
- **FAIL**: Any category is FAIL

Print the verdict and suggest next action:
- **PASS**: "QA passed. Run `/ship` to create the PR."
- **WARN**: "QA passed with warnings. Review above, then `/ship`."
- **FAIL**: "QA failed. Fix the issues listed above, then re-run `/qa`."
