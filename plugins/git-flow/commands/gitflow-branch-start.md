---
name: gitflow branch-start
description: Create a new feature/fix/chore branch with consistent naming
agent: git-assistant
---

# /gitflow branch-start - Start New Branch

## Skills

- skills/visual-header.md
- skills/branch-naming.md
- skills/git-safety.md
- skills/environment-variables.md

## Purpose

Create a new branch with consistent naming conventions, based on the configured base branch.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<description>` | Brief description for branch name |
| `--type` | Branch type: feat, fix, chore, docs, refactor |
| `--issue` | Issue number to include in branch name |

## Workflow

1. **Display header** - Show GIT-FLOW Branch Start header
2. **Determine type** - Prompt for branch type if not provided
3. **Get description** - Prompt for description if not provided
4. **Generate name** - Convert to kebab-case (per branch-naming.md)
5. **Validate** - Check naming rules, truncate if needed
6. **Update base** - Checkout and pull base branch
7. **Create branch** - `git checkout -b <new-branch>`
8. **Confirm** - Display created branch info

## Output

```
Branch: feat/add-user-authentication
Base: development @ abc1234
Status: Ready for development
```
