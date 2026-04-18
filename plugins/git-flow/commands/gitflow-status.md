---
name: gitflow status
description: Show comprehensive git status with recommendations
agent: git-assistant
---

# /gitflow status - Enhanced Git Status

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

### Step 0: Load Environment (MANDATORY — must run before any git or API operation)

**Imperative:** Before executing any subsequent step, read environment variables per `skills/environment-variables.md`. This step is non-skippable.

1. Read project `.env` if present. Parse all `GIT_*` and `GITEA_*` variables.
2. Read user `~/.config/claude/git-flow.env` if present. Project values override user values.
3. Apply defaults from `skills/environment-variables.md` for any unset variable.
4. Expose resolved values. Variables used by this command: `GIT_DEFAULT_BASE`, `GIT_PROTECTED_BRANCHES`, `GIT_AUTO_PRUNE`.
5. If any required variable has no value after resolution, halt and ask the user.

**Do not proceed to Step 1 until all environment variables above have been resolved.**

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
/gitflow commit - Commit staged changes
/gitflow commit --push - Commit and push
```
