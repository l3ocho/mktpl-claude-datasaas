---
name: git-commit-push
description: Create a commit and push to remote in one operation
agent: git-assistant
---

# /git-commit-push - Commit and Push

## Skills

- skills/visual-header.md
- skills/commit-conventions.md
- skills/sync-workflow.md
- skills/git-safety.md
- skills/environment-variables.md

## Purpose

Create a commit and push to the remote repository in one operation.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--message`, `-m` | Override auto-generated message |
| `--force` | Force push (requires confirmation) |

## Workflow

1. **Display header** - Show GIT-FLOW Commit & Push header
2. **Run /git-commit** - Execute standard commit workflow
3. **Check upstream** - Set up tracking if needed (`git push -u`)
4. **Push** - Push to remote
5. **Handle conflicts** - Offer rebase/merge/force if push fails (per sync-workflow.md)
6. **Verify safety** - Warn before push to protected branches (per git-safety.md)
7. **Report** - Show push result

## Output

```
Committed: abc1234
feat(auth): add password reset functionality

Pushed to: origin/feat/password-reset
Remote URL: https://github.com/user/repo
```
