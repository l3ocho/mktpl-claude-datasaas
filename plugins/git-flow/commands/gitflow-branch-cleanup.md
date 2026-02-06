---
name: gitflow branch-cleanup
description: Remove merged and stale branches locally and optionally on remote
agent: git-assistant
---

# /gitflow branch-cleanup - Clean Merged and Stale Branches

## Skills

- skills/visual-header.md
- skills/git-safety.md
- skills/sync-workflow.md
- skills/environment-variables.md

## Purpose

Remove branches that have been merged OR whose remote tracking branch no longer exists.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--dry-run` | Preview without deleting |
| `--remote` | Also delete remote branches |
| `--stale-only` | Only delete stale branches (upstream gone) |

## Workflow

1. **Display header** - Show GIT-FLOW Branch Cleanup header
2. **Prune remote refs** - `git fetch --prune`
3. **Find merged branches** - `git branch --merged <base-branch>`
4. **Find stale branches** - `git branch -vv | grep ': gone]'`
5. **Exclude protected** - Never delete protected branches (per git-safety.md)
6. **Present findings** - Show merged, stale, and protected lists
7. **Confirm deletion** - Options: all, merged only, stale only, pick, cancel
8. **Execute cleanup** - Delete selected branches
9. **Report** - Show deletion summary

## Output

```
Cleaned up:
  Local (merged): 3 branches deleted
  Local (stale): 2 branches deleted
  Remote: 2 branches deleted

Repository is tidy!
```
