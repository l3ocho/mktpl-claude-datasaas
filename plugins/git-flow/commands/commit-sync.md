# /commit-sync - Commit, Push, and Sync

## Purpose

Full sync operation: commit local changes, push to remote, sync with upstream/base branch, and clean up stale remote-tracking branches.

## Behavior

### Step 1: Run /commit

Execute the standard commit workflow.

### Step 2: Push to Remote

Push committed changes to remote branch.

### Step 3: Sync with Base

Pull latest from base branch and rebase/merge:

```bash
# Fetch all with prune (removes stale remote-tracking refs)
git fetch --all --prune

# Rebase on base branch
git rebase origin/<base-branch>

# Push again (if rebased)
git push --force-with-lease
```

### Step 4: Detect Stale Local Branches

Check for local branches tracking deleted remotes:

```bash
# Find local branches with gone upstreams
git branch -vv | grep ': gone]'
```

If stale branches found, report them:

```
Stale local branches (remote deleted):
  - feat/old-feature (was tracking origin/feat/old-feature)
  - fix/merged-bugfix (was tracking origin/fix/merged-bugfix)

Run /branch-cleanup to remove these branches.
```

### Step 5: Report Status

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

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_DEFAULT_BASE` | `development` | Branch to sync with |
| `GIT_SYNC_STRATEGY` | `rebase` | How to incorporate upstream changes |
| `GIT_AUTO_PRUNE` | `true` | Auto-prune stale remote refs on sync |

## Conflict Handling

If conflicts occur during rebase:

```
Conflicts detected while syncing with development.

Conflicting files:
- src/auth/login.ts
- src/auth/types.ts

Options:
1. Open conflict resolution (I'll guide you)
2. Abort sync (keep local state)
3. Accept all theirs (⚠️ loses your changes in conflicts)
4. Accept all ours (⚠️ ignores upstream in conflicts)
```

## Output

On success:
```
Committed: abc1234
Pushed to: origin/feat/password-reset
Synced with: development (xyz7890)

Status: Clean, up-to-date
Stale branches: None (or N found - run /branch-cleanup)
```
