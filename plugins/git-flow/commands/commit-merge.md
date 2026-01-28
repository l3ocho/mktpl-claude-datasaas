# /commit-merge - Commit and Merge

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔀 GIT-FLOW · Commit & Merge                                     │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the workflow.

## Purpose

Commit current changes, then merge the current branch into a target branch.

## Behavior

### Step 1: Run /commit

Execute the standard commit workflow.

### Step 2: Identify Target Branch

Check environment or ask:

```
Merge into which branch?
1. development (Recommended - GIT_DEFAULT_BASE)
2. main
3. Other: ____
```

### Step 3: Merge Strategy

```
How should I merge?
1. Merge commit (preserves history)
2. Squash and merge (single commit)
3. Rebase (linear history)
```

### Step 4: Execute Merge

```bash
# Switch to target
git checkout <target>

# Pull latest
git pull origin <target>

# Merge feature branch
git merge <feature-branch> [--squash] [--no-ff]

# Push
git push origin <target>
```

### Step 5: Cleanup (Optional)

```
Merge complete. Delete the feature branch?
1. Yes, delete local and remote (Recommended)
2. Delete local only
3. Keep the branch
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_DEFAULT_BASE` | `development` | Default branch to merge into |
| `GIT_MERGE_STRATEGY` | `merge` | Default merge strategy |
| `GIT_AUTO_DELETE_MERGED` | `true` | Auto-delete merged branches |

## Safety Checks

- Verify target branch exists
- Check for uncommitted changes before switching
- Ensure merge doesn't conflict (preview first)

## Output

On success:
```
Committed: abc1234
feat(auth): add password reset functionality

Merged feat/password-reset → development
Deleted branch: feat/password-reset

development is now at: def5678
```
