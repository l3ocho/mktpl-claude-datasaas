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

### Step 0: Load Environment (MANDATORY — must run before any git or API operation)

**Imperative:** Before executing any subsequent step, read environment variables per `skills/environment-variables.md`. This step is non-skippable.

1. Read project `.env` if present. Parse all `GIT_*` and `GITEA_*` variables.
2. Read user `~/.config/claude/git-flow.env` if present. Project values override user values.
3. Apply defaults from `skills/environment-variables.md` for any unset variable.
4. Expose resolved values. Variables used by this command: `GIT_DEFAULT_BASE`, `GIT_PROTECTED_BRANCHES`, `GIT_BRANCH_PREFIX`, `GIT_WORKFLOW_STYLE`.
5. If any required variable has no value after resolution, halt and ask the user.

**Do not proceed to Step 1 until all environment variables above have been resolved.**

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
