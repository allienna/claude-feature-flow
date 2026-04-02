---
mode: agent
description: "Run a project-wide quality audit — tests, linting, type checking, security scanning, and spec compliance"
tools: ['runCommands', 'search', 'codebase', 'runTests', 'problems', 'editFiles']
---

# QA — Quality Audit

Run a project-wide health check: tests, linting, type checking, security scanning, and spec compliance.

**Modes**: Full audit (steps 0-6) or quick mode (steps 0-2 only). Determine from user input: if "quick" is mentioned, run quick mode.

## Step 0 — Detect Environment

### Discover project structure

1. Look for config files to identify the tech stack:
   - `pyproject.toml`, `setup.py`, `setup.cfg` → Python
   - `package.json` → JavaScript/TypeScript
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `pom.xml`, `build.gradle` → Java
   - Other config files as applicable

2. Discover source and test directories:
   - Try `src/**/*`, `lib/**/*`, `app/**/*`, `pkg/**/*` or identify from config files
   - Try `tests/**/*`, `test/**/*`, `__tests__/**/*`, `spec/**/*`

3. Assign the discovered paths:
   - Set `source_dir` to the primary source directory (e.g., `src` or `lib`)
   - Set `test_dir` to the primary test directory (e.g., `tests` or `__tests__`)

4. If no source files exist: "No source code to audit yet. Build some features first." STOP.

### Discover build commands

Read `CLAUDE.md` and extract:
- **Test command**: (e.g., `pytest`, `jest`, `go test`, `cargo test`)
- **Lint command**: (e.g., `ruff check`, `eslint`, `golangci-lint`)
- **Format command**: (e.g., `ruff format`, `prettier`, `gofmt`)
- **Type check command**: (e.g., `pyright`, `tsc --noEmit`, `mypy`)

If `CLAUDE.md` is missing: WARN "No CLAUDE.md found — cannot discover build commands. Add a CLAUDE.md with a '## Build & Run Commands' section. Skipping automated checks."

If `CLAUDE.md` exists but doesn't define some commands: WARN for each missing command and skip that check.

## Step 1 — Automated Quality Checks

Run each discovered command in sequence. Record results for each:

- **Lint**: Run lint command → record issues count
- **Format**: Run format check command → record violations count
- **Type check**: Run type check command → record errors count
- **Test**: Run test command → record pass/fail count

Skip any check whose command was not discovered, and note it as SKIP.

## Step 2 — Test Coverage Gap Audit

Identify untested areas:

**Source modules**: List all source files in the discovered source directory. Check which have corresponding test files in the test directory.

Produce a dynamically generated coverage gap table:

```
| Module | Has Tests | Notes |
|--------|-----------|-------|
| {source_file_1} | Yes/No | ... |
| {source_file_2} | Yes/No | ... |
```

**If quick mode was invoked, STOP HERE. Skip steps 3-5 and jump to step 6.**

## Step 3 — Security Scan

Run search-based checks. Each check is PASS or FAIL:

### 3.1 No Hardcoded Secrets
Search for potential API keys, tokens, or passwords in source files using pattern:
`(api_key|api_token|password|secret|bearer|private_key)\s*=\s*['"]`

PASS if no matches (or only references to env vars). FAIL if hardcoded values found.

### 3.2 .env.example Validation
Search for env var references in source code using patterns like:
`os.environ|os.getenv|env\(|process\.env|std::env|viper\.`

Cross-reference discovered env vars with `.env.example` (if it exists). PASS if all vars documented. WARN if `.env.example` is missing.

### 3.3 No Sensitive Data in Responses
Search for env var names (discovered in 3.2) appearing in response/output code. PASS if no matches. FAIL if credentials referenced in response code.

## Step 4 — Spec Compliance Checks

### 4.1 Constitution compliance
If `specs/constitution.md` exists, check each principle against the codebase.
If it doesn't exist: WARN "No constitution found — run the constitution prompt to create one. Skipping compliance checks."

### 4.2 Feature spec compliance
If feature specs exist (`specs/*/spec.md`), verify acceptance criteria are met for completed features.
If no specs exist: SKIP this check.

### 4.3 Codebase patterns
If `CLAUDE.md` defines key patterns or architectural conventions, verify adherence across the codebase.
If not defined: SKIP this check.

## Step 5 — Dependency Discipline

Check dependency count based on the detected package manager:

```bash
# Python: pip list | wc -l
# Node: npm ls --depth=0 | wc -l
# Go: go list -m all | wc -l
# Rust: cargo tree --depth 1 | wc -l
```

Report count. WARN if it seems unusually high for the project scope.

## Step 6 — Generate QA Report

Write `qa-report.md` in the **project root** with this structure:

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
- **PASS**: "QA passed. Run the ship prompt to create the PR."
- **WARN**: "QA passed with warnings. Review above, then run the ship prompt."
- **FAIL**: "QA failed. Fix the issues listed above, then re-run the QA prompt."
