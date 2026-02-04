---
name: git-status
description: Show comprehensive git status with recommendations
agent: git-assistant
---

# /git-status - Enhanced Status

## Skills

- skills/visual-header.md
- skills/commit-conventions.md
- skills/environment-variables.md

## Purpose

Show comprehensive git status with recommendations and insights beyond standard `git status`.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--short` | Compact output format |

## Workflow

1. **Display header** - Show GIT-FLOW Status header
2. **Gather info** - Branch, base comparison, remote status
3. **Categorize changes** - Staged, unstaged, untracked, deleted, renamed
4. **Generate recommendations** - What to stage, commit, sync
5. **Show quick actions** - Relevant /commands for current state

## Output Format

```
Git Status: <repo-name>

Branch: feat/password-reset
Base: development (3 commits ahead, 0 behind)
Remote: origin/feat/password-reset (synced)

--- Changes ---
Staged (ready to commit):
  [x] src/auth/reset.ts (modified)

Unstaged:
  [ ] tests/auth.test.ts (modified)

--- Recommendations ---
1. Stage test file: git add tests/auth.test.ts
2. Ready to commit with 1 staged file

--- Quick Actions ---
/git-commit - Commit staged changes
/git-commit-push - Commit and push
```
