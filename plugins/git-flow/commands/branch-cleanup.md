# /branch-cleanup - Clean Merged Branches

## Purpose

Remove branches that have been merged, both locally and optionally on remote.

## Behavior

### Step 1: Identify Merged Branches

```bash
# Find merged local branches
git branch --merged <base-branch>

# Find merged remote branches
git branch -r --merged <base-branch>
```

### Step 2: Present Findings

```
Found 5 merged branches:

Local:
  - feat/login-page (merged 3 days ago)
  - fix/typo-header (merged 1 week ago)
  - chore/deps-update (merged 2 weeks ago)

Remote:
  - origin/feat/login-page
  - origin/fix/typo-header

Protected (won't delete):
  - main
  - development
  - staging

Delete these branches?
1. Delete all (local + remote)
2. Delete local only
3. Let me pick which ones
4. Cancel
```

### Step 3: Execute Cleanup

```bash
# Delete local
git branch -d <branch-name>

# Delete remote
git push origin --delete <branch-name>
```

### Step 4: Report

```
Cleanup complete:

Deleted local: 3 branches
Deleted remote: 2 branches
Skipped: 0 branches

Remaining local branches:
  - main
  - development
  - feat/current-work (not merged)
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_DEFAULT_BASE` | `development` | Base branch for merge detection |
| `GIT_PROTECTED_BRANCHES` | `main,master,development,staging,production` | Never delete these |
| `GIT_AUTO_DELETE_REMOTE` | `false` | Auto-delete remote branches |

## Safety

- Never deletes protected branches
- Warns about unmerged branches
- Confirms before deleting remote branches
- Uses `-d` (safe delete) not `-D` (force delete)

## Output

On success:
```
Cleaned up:
  Local: 3 branches deleted
  Remote: 2 branches deleted

Repository is tidy!
```
