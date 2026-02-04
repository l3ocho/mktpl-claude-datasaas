# Sync Workflow

## Purpose

Defines push/pull patterns, rebase strategies, upstream tracking, and stale branch detection.

## When to Use

- Pushing commits in `/git-commit-push`
- Full sync operations in `/git-commit-sync`
- Detecting and reporting stale branches

## Push Workflow

### First Push (No Upstream)

```bash
git push -u origin <branch>
```

Sets upstream tracking for future pushes.

### Subsequent Pushes

```bash
git push
```

Pushes to tracked upstream.

### Push After Rebase

```bash
git push --force-with-lease
```

Safe force push - fails if remote has new commits.

## Sync with Base Branch

```bash
# 1. Fetch all with prune
git fetch --all --prune

# 2. Rebase on base branch
git rebase origin/<base-branch>

# 3. Push (force if rebased)
git push --force-with-lease
```

## Push Conflict Handling

When push fails due to diverged history:

```
Remote has changes not in your local branch.

Options:
1. Pull and rebase, then push (Recommended)
2. Pull and merge, then push
3. Force push (destructive - requires confirmation)
4. Cancel and review manually
```

### Rebase Resolution

```bash
git pull --rebase origin <branch>
git push
```

### Merge Resolution

```bash
git pull origin <branch>
git push
```

## Stale Branch Detection

Find local branches tracking deleted remotes:

```bash
git branch -vv | grep ': gone]'
```

### Report Format

```
Stale local branches (remote deleted):
  - feat/old-feature (was tracking origin/feat/old-feature)
  - fix/merged-bugfix (was tracking origin/fix/merged-bugfix)

Run /branch-cleanup to remove these branches.
```

## Remote Pruning

Remove stale remote-tracking references:

```bash
git fetch --prune
```

Or fetch all remotes:

```bash
git fetch --all --prune
```

## Sync Status Report

```
Sync complete:

Local:  feat/password-reset @ abc1234
Remote: origin/feat/password-reset @ abc1234
Base:   development @ xyz7890 (synced)

Your branch is up-to-date with development.
No conflicts detected.

Cleanup:
  Remote refs pruned: 2
  Stale local branches: 2 (run /branch-cleanup to remove)
```

## Tracking Setup

Check tracking status:

```bash
git branch -vv
```

Set upstream:

```bash
git branch --set-upstream-to=origin/<branch> <branch>
```

## Related Skills

- skills/git-safety.md
- skills/merge-workflow.md
