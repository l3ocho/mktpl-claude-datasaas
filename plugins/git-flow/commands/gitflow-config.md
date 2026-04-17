---
name: gitflow config
description: Configure git-flow settings for the current project
agent: git-assistant
---

# /gitflow config - Configure Git-Flow

## Skills

- skills/visual-header.md
- skills/environment-variables.md
- skills/workflow-patterns/branching-strategies.md

## Purpose

Configure git-flow settings interactively or display current configuration.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--show` | Display current settings without prompting |
| `--reset` | Reset all settings to defaults |
| `<key>=<value>` | Set specific variable directly |

## Workflow

### Step 0: Load Environment (MANDATORY — must run before any git or API operation)

**Imperative:** Before executing any subsequent step, read environment variables per `skills/environment-variables.md`. This step is non-skippable.

1. Read project `.env` if present. Parse all `GIT_*` and `GITEA_*` variables.
2. Read user `~/.config/claude/git-flow.env` if present. Project values override user values.
3. Apply defaults from `skills/environment-variables.md` for any unset variable.
4. Expose resolved values. Variables used by this command: All `GIT_*` and `GITEA_*` variables (for display and editing).
5. If any required variable has no value after resolution, halt and ask the user.

**Do not proceed to Step 1 until all environment variables above have been resolved.**

1. **Display header** - Show GIT-FLOW Configuration header
2. **Load current settings** - Read from project and user config
3. **Present menu** - Show configuration options
4. **Handle selection** - Configure workflow style, base branch, protected branches, etc.
5. **Save settings** - Write to `.env` or `.claude/settings.json`
6. **Confirm** - Display saved configuration

## Configuration Menu

1. Workflow style (simple, feature-branch, pr-required, trunk-based)
2. Default base branch
3. Auto-delete merged branches
4. Auto-push after commit
5. Protected branches
6. View all settings
7. Reset to defaults
8. Re-run setup wizard (redirects to `/gitflow setup`)

## Output

```
Configuration saved!

GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=development
GIT_AUTO_DELETE_MERGED=true

These settings will be used for all git-flow commands.
```
