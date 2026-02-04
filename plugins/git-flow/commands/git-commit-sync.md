---
name: git-commit-sync
description: Commit, push, and sync with base branch
agent: git-assistant
---

# /git-commit-sync - Commit, Push, and Sync

## Skills

- skills/visual-header.md
- skills/commit-conventions.md
- skills/sync-workflow.md
- skills/merge-workflow.md
- skills/environment-variables.md

## Purpose

Full sync operation: commit local changes, push to remote, sync with upstream/base branch, and detect stale branches.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--base` | Override default base branch |
| `--no-rebase` | Use merge instead of rebase |

## Workflow

1. **Display header** - Show GIT-FLOW Commit Sync header
2. **Run /git-commit** - Execute standard commit workflow
3. **Push to remote** - Push committed changes
4. **Fetch with prune** - `git fetch --all --prune`
5. **Sync with base** - Rebase on base branch (per sync-workflow.md)
6. **Handle conflicts** - Guide resolution if conflicts occur (per merge-workflow.md)
7. **Push again** - `git push --force-with-lease` if rebased
8. **Detect stale** - Report stale local branches
9. **Report status** - Show sync summary

## Output

```
Committed: abc1234
Pushed to: origin/feat/password-reset
Synced with: development (xyz7890)

Status: Clean, up-to-date
Stale branches: 2 found - run /branch-cleanup
```
