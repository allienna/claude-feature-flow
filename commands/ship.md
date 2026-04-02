---
description: Create branch, commit, push and open a PR
argument-hint: "[feature-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# /ship — Create branch, commit, push and open a PR

## Step 1: Check status

```bash
git status
git branch --show-current
```

Verify there are changes to commit or commits to push. If no changes and branch is up to date, notify and stop.

## Step 2: Verify quality (if feature track exists)

If a feature track exists for this branch:
1. Read `specs/{NNN}-$ARGUMENTS/review.md` — verify verdict is "Ready to merge" or "Pass with notes"
2. If no review exists, warn: "No review found. Run `/review $ARGUMENTS` first, or confirm to ship without review."

### Discover and run quality gates

Read `CLAUDE.md` and extract build commands:
- **Test command**: Look for a command containing "test" (e.g., `pytest`, `jest`, `go test`, `cargo test`)
- **Lint command**: Look for a command containing "lint" or "check" (e.g., `ruff check`, `eslint`, `golangci-lint`)
- **Format command**: Look for a command containing "format" or "fmt" (e.g., `ruff format`, `prettier`, `gofmt`)
- **Type check command**: Look for a command containing "typecheck", "type" (e.g., `pyright`, `tsc --noEmit`, `mypy`)

If `CLAUDE.md` is missing or doesn't define build commands: WARN "No build commands found in CLAUDE.md — cannot run quality gates. Add a '## Build & Run Commands' section, or confirm to ship without checks."

Run each discovered command. If any gate fails, STOP and report the failure.

## Step 3: Create branch

If on `main`, create a new branch with a descriptive name based on the changes:
- `docs/...` for documentation
- `feat/{NNN}-...` for features (use track number if available)
- `fix/...` for fixes

If already on a feature branch, stay on it.

## Step 4: Commit

- Stage relevant files (no `git add .`, specific files only)
- Propose a concise commit message using conventional commits format:
  - `feat({NNN}): {description}` for feature tracks
  - `fix: {description}` for bug fixes
  - `chore: {description}` for maintenance
- **Do NOT include `Co-Authored-By`**
- **Ask for validation before committing**

## Step 5: Push and PR

```bash
git push -u origin {BRANCH}
```

Open a PR with `gh pr create`:
- Short title (< 70 characters)
- Body with:
  - `## Summary` — bullets from spec.md overview (if feature track exists) or from diff analysis
  - `## Acceptance Criteria` — checklist from spec.md (if feature track exists)
  - `## Test Results` — summary of test output
  - `## Test plan` — checklist of manual verification steps

## Step 6: Request review

Capture the PR number from the `gh pr create` output.

Ask the user: "Request a review on this PR? If so, provide a reviewer login (e.g., `@copilot`, `@username`)."

If yes:
```bash
gh pr edit {PR_NUMBER} --add-reviewer "{REVIEWER}"
```

Confirm the created PR URL.
