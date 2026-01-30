# Git Safety

## Purpose

Defines protected branches, destructive command warnings, and safety checks to prevent accidental data loss.

## When to Use

- Before any commit, push, or merge operation
- When user attempts to work on protected branches
- Before executing destructive commands

## Protected Branches

Default protected branches (configurable via `GIT_PROTECTED_BRANCHES`):
- `main`
- `master`
- `development`
- `staging`
- `production`

## Protection Rules

| Action | Behavior |
|--------|----------|
| Direct commit | Warn and offer to create feature branch |
| Force push | Require explicit confirmation |
| Deletion | Block completely |
| Merge into | Allow with standard workflow |

## Protected Branch Warning

When committing on protected branch:

```
You are on a protected branch: development

Protected branches typically have push restrictions that will prevent
direct commits from being pushed to the remote.

Options:
1. Create a feature branch and continue (Recommended)
2. Continue on this branch anyway (may fail on push)
3. Cancel
```

## Destructive Commands

Commands requiring extra confirmation:

| Command | Risk | Mitigation |
|---------|------|------------|
| `git push --force` | Overwrites remote history | Use `--force-with-lease` |
| `git reset --hard` | Loses uncommitted changes | Warn about unsaved work |
| `git branch -D` | Deletes unmerged branch | Confirm branch name |
| `git clean -fd` | Deletes untracked files | List files first |

## Safe Alternatives

| Risky | Safe Alternative |
|-------|------------------|
| `git push --force` | `git push --force-with-lease` |
| `git branch -D` | `git branch -d` (merged only) |
| `git reset --hard` | `git stash` first |
| `git checkout .` | Review changes first |

## Branch Deletion Safety

**Merged branches (`-d`):**
```bash
git branch -d feat/old-feature  # Safe: only deletes if merged
```

**Unmerged branches (`-D`):**
```bash
# Requires confirmation
git branch -D feat/abandoned  # Force: deletes regardless
```

## Push Rejection Handling

When push fails on protected branch:

```
Push rejected: Remote protection rules prevent direct push to development.

Options:
1. Create a pull request instead (Recommended)
2. Review branch protection settings
3. Cancel
```

## Stale Branch Detection

Branches with deleted remotes:
```bash
git branch -vv | grep ': gone]'
```

These are safe to delete locally with `-D` after confirmation.

## Related Skills

- skills/branch-naming.md
- skills/merge-workflow.md
