---
description: Address PR comments, squash merge, and update local main
argument-hint: "<pr-number>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, ExitWorktree
---

# /merge — PR comment resolution, squash merge

Takes a PR number as argument (`$ARGUMENTS`). If no argument, list open PRs and ask which one to process.

## 0. Detect repo

```bash
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
```

Use `$REPO` in all `gh api` calls below.

## 1. Check PR status

```bash
gh pr view $ARGUMENTS --json state,reviewDecision,statusCheckRollup,title,body
```

Verify:
- PR is open
- Checks are passing
- Review status (approved, changes requested, pending)

If changes are requested, proceed to step 2. If approved and checks pass, skip to step 3.

## 2. Address comments

```bash
gh pr view $ARGUMENTS --comments
gh api repos/{REPO}/pulls/$ARGUMENTS/comments --paginate
```

Analyze inline comments from reviewers:

For each comment:
- Display the file, line, and comment body
- Evaluate whether the comment is relevant
- If relevant: apply the fix, commit, push, and reply via API:
  ```bash
  gh api repos/{REPO}/pulls/$ARGUMENTS/comments/{COMMENT_ID}/replies -f body="Fixed, thanks."
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
gh pr merge $ARGUMENTS --squash --subject "{TITLE}" --body "{BODY}"
```

Do **not** pass `--delete-branch` when the PR branch is checked out in a worktree: `gh` would try to switch the local checkout and fail. Branch and worktree cleanup is done explicitly in step 4.

## 4. Local update and cleanup

1. If the current session is inside the feature worktree (`.claude/worktrees/...`), leave it with the `ExitWorktree` tool so you are in the main checkout. If the feature has no worktree (a branch created by plugin 1.x), skip the worktree commands below and just delete the merged branch.
2. Update main and remove the feature's worktree and branches:

```bash
git checkout main
git pull
git worktree remove .claude/worktrees/{NNN}-{feature}     # refuses if there is uncommitted work: show it and ask
git branch -D feat/{NNN}-{feature}
git push origin --delete feat/{NNN}-{feature}             # ignore "remote ref does not exist" (auto-delete on merge)
git worktree prune
```

Never use `--force` on `git worktree remove` without showing the user what would be lost.

Confirm the merge is done, main is up to date and no stale worktree remains (`git worktree list`).
