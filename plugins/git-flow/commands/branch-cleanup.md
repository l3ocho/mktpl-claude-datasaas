# /branch-cleanup - Clean Merged and Stale Branches

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔀 GIT-FLOW · Branch Cleanup                                     │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the workflow.

## Purpose

Remove branches that have been merged OR whose remote tracking branch no longer exists, both locally and optionally on remote.

## Behavior

### Step 1: Prune Remote Refs

```bash
# Remove stale remote-tracking references
git fetch --prune
```

### Step 2: Identify Branches for Cleanup

```bash
# Find merged local branches
git branch --merged <base-branch>

# Find merged remote branches
git branch -r --merged <base-branch>

# Find local branches with deleted upstreams (stale)
git branch -vv | grep ': gone]'
```

### Step 3: Present Findings

```
Found branches for cleanup:

Merged (safe to delete):
  - feat/login-page (merged 3 days ago)
  - fix/typo-header (merged 1 week ago)
  - chore/deps-update (merged 2 weeks ago)

Stale (remote deleted):
  - feat/old-feature (upstream gone)
  - fix/already-merged (upstream gone)

Remote (merged into base):
  - origin/feat/login-page
  - origin/fix/typo-header

Protected (won't delete):
  - main
  - development
  - staging

Delete these branches?
1. Delete all (local merged + stale + remote)
2. Delete merged only (skip stale)
3. Delete stale only (upstream gone)
4. Let me pick which ones
5. Cancel
```

### Step 4: Execute Cleanup

```bash
# Delete merged local branches
git branch -d <branch-name>

# Delete stale local branches (force needed since no upstream)
git branch -D <stale-branch-name>

# Delete remote branches
git push origin --delete <branch-name>
```

### Step 5: Report

```
Cleanup complete:

Deleted local (merged): 3 branches
Deleted local (stale): 2 branches
Deleted remote: 2 branches
Skipped: 0 branches

Remaining local branches:
  - main
  - development
  - feat/current-work (not merged, has upstream)
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_DEFAULT_BASE` | `development` | Base branch for merge detection |
| `GIT_PROTECTED_BRANCHES` | `main,master,development,staging,production` | Never delete these |
| `GIT_AUTO_DELETE_REMOTE` | `false` | Auto-delete remote branches |
| `GIT_CLEANUP_STALE` | `true` | Include stale branches (upstream gone) in cleanup |

## Safety

- Never deletes protected branches
- Warns about unmerged branches that still have upstreams
- Confirms before deleting remote branches
- Uses `-d` (safe delete) for merged branches
- Uses `-D` (force delete) only for stale branches with confirmation
- Stale branches are highlighted separately for review

## Output

On success:
```
Cleaned up:
  Local (merged): 3 branches deleted
  Local (stale): 2 branches deleted
  Remote: 2 branches deleted

Repository is tidy!
```
