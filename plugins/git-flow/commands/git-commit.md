---
name: commit
description: Create a git commit with auto-generated conventional commit message
agent: git-assistant
---

# /commit - Smart Commit

## Skills

- skills/visual-header.md
- skills/git-safety.md
- skills/commit-conventions.md
- skills/environment-variables.md

## Purpose

Create a git commit with an auto-generated conventional commit message based on staged changes.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--message`, `-m` | Override auto-generated message |
| `--all`, `-a` | Stage all changes before commit |

## Workflow

1. **Display header** - Show GIT-FLOW Smart Commit header
2. **Check protected branch** - Warn if on protected branch (per git-safety.md)
3. **Analyze changes** - Run `git status` and `git diff --staged`
4. **Handle unstaged** - Prompt to stage if nothing staged
5. **Generate message** - Create conventional commit message (per commit-conventions.md)
6. **Confirm or edit** - Present message with options to use, edit, regenerate, or cancel
7. **Execute commit** - Run `git commit` with message and co-author footer

## Output

```
Committed: abc1234
feat(auth): add password reset functionality

Files: 3 changed, 45 insertions(+), 12 deletions(-)
```
