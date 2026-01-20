# /commit-sync - Commit, Push, and Sync

## Purpose

Full sync operation: commit local changes, push to remote, and sync with upstream/base branch.

## Behavior

### Step 1: Run /commit

Execute the standard commit workflow.

### Step 2: Push to Remote

Push committed changes to remote branch.

### Step 3: Sync with Base

Pull latest from base branch and rebase/merge:

```bash
# Fetch all
git fetch --all

# Rebase on base branch
git rebase origin/<base-branch>

# Push again (if rebased)
git push --force-with-lease
```

### Step 4: Report Status

```
Sync complete:

Local:  feat/password-reset @ abc1234
Remote: origin/feat/password-reset @ abc1234
Base:   development @ xyz7890 (synced)

Your branch is up-to-date with development.
No conflicts detected.
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_DEFAULT_BASE` | `development` | Branch to sync with |
| `GIT_SYNC_STRATEGY` | `rebase` | How to incorporate upstream changes |

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
```
