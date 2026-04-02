---
mode: agent
description: "Address PR comments, squash merge, and update local main"
tools: ['editFiles', 'runCommands', 'search', 'codebase', 'runTests', 'changes']
---

# Merge — PR comment resolution, squash merge

Takes a PR number as input. If none provided, list open PRs and ask which one to process.

## 0. Detect repo

Run:
```bash
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
```

Use `$REPO` in all `gh api` calls below.

## 1. Check PR status

```bash
gh pr view {PR_NUMBER} --json state,reviewDecision,statusCheckRollup,title,body
```

Verify:
- PR is open
- Checks are passing
- Review status (approved, changes requested, pending)

If changes are requested, proceed to step 2. If approved and checks pass, skip to step 3.

## 2. Address comments

```bash
gh pr view {PR_NUMBER} --comments
gh api repos/{REPO}/pulls/{PR_NUMBER}/comments --paginate
```

Analyze inline comments from reviewers:

For each comment:
- Display the file, line, and comment body
- Evaluate whether the comment is relevant
- If relevant: apply the fix, commit, push, and reply via API:
  ```bash
  gh api repos/{REPO}/pulls/{PR_NUMBER}/comments/{COMMENT_ID}/replies -f body="Fixed, thanks."
  ```
- If not relevant: explain why and ask for confirmation before replying

After all fixes:
```bash
git add {changed_files}
git commit -m "fix: address PR review feedback"
git push
```

## 3. Squash merge

Prepare a squash commit message:
- First line: PR title with number (e.g., `feat(001): project scaffold (#5)`)
- Body: concise summary of changes (2-3 lines max)
- **Do NOT include `Co-Authored-By`**

**Display the proposed commit message and ask for validation before merging.**

Once validated:
```bash
gh pr merge {PR_NUMBER} --squash --delete-branch --subject "{TITLE}" --body "{BODY}"
```

## 4. Local update

```bash
git checkout main
git pull
```

Confirm the merge is done and main is up to date.
