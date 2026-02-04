---
name: git-commit-merge
description: Commit current changes and merge branch into target
agent: git-assistant
---

# /git-commit-merge - Commit and Merge

## Skills

- skills/visual-header.md
- skills/commit-conventions.md
- skills/merge-workflow.md
- skills/git-safety.md
- skills/environment-variables.md

## Purpose

Commit current changes, then merge the current branch into a target branch.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--target` | Target branch (default: GIT_DEFAULT_BASE) |
| `--squash` | Squash commits on merge |
| `--no-delete` | Keep branch after merge |

## Workflow

1. **Display header** - Show GIT-FLOW Commit & Merge header
2. **Run /git-commit** - Execute standard commit workflow
3. **Identify target** - Prompt for target branch if not specified
4. **Select strategy** - Merge commit, squash, or rebase (per merge-workflow.md)
5. **Execute merge** - Switch to target, pull, merge, push
6. **Handle conflicts** - Guide resolution if needed
7. **Cleanup** - Offer to delete merged branch (per git-safety.md)
8. **Report** - Show merge summary

## Output

```
Committed: abc1234
feat(auth): add password reset functionality

Merged feat/password-reset -> development
Deleted branch: feat/password-reset

development is now at: def5678
```
