# Merge Workflow

## Purpose

Defines merge strategies, conflict resolution approaches, and post-merge cleanup procedures.

## When to Use

- Merging feature branches in `/commit-merge`
- Resolving conflicts during sync operations
- Cleaning up after successful merges

## Merge Strategies

### 1. Merge Commit (Default)

```bash
git merge <branch> --no-ff
```

- **Preserves history** - All commits visible
- **Creates merge commit** - Clear merge point
- **Best for:** Feature branches, team workflows

### 2. Squash and Merge

```bash
git merge <branch> --squash
git commit -m "feat: complete feature"
```

- **Single commit** - Clean main branch history
- **Loses individual commits** - Combined into one
- **Best for:** PR workflows, many small commits

### 3. Rebase

```bash
git checkout <branch>
git rebase <target>
git checkout <target>
git merge <branch> --ff-only
```

- **Linear history** - No merge commits
- **Rewrites history** - Changes commit hashes
- **Best for:** Personal branches, clean history

## Standard Merge Procedure

```bash
# 1. Switch to target branch
git checkout <target>

# 2. Pull latest changes
git pull origin <target>

# 3. Merge feature branch
git merge <feature-branch> [--squash] [--no-ff]

# 4. Push merged result
git push origin <target>
```

## Conflict Resolution

When conflicts occur:

```
Conflicts detected while merging.

Conflicting files:
- src/auth/login.ts
- src/auth/types.ts

Options:
1. Open conflict resolution (guided)
2. Abort merge (keep local state)
3. Accept all theirs (loses your changes in conflicts)
4. Accept all ours (ignores upstream in conflicts)
```

### Manual Resolution Steps

1. Open conflicting file
2. Find conflict markers: `<<<<<<<`, `=======`, `>>>>>>>`
3. Edit to desired state
4. Remove markers
5. Stage resolved file: `git add <file>`
6. Continue: `git merge --continue` or `git rebase --continue`

## Post-Merge Cleanup

After successful merge:

```
Merge complete. Delete the feature branch?
1. Yes, delete local and remote (Recommended)
2. Delete local only
3. Keep the branch
```

### Cleanup Commands

```bash
# Delete local branch
git branch -d <branch>

# Delete remote branch
git push origin --delete <branch>
```

## Pre-Merge Checks

Before merging:
1. **Verify target exists** - `git branch -a | grep <target>`
2. **Check for uncommitted changes** - `git status`
3. **Preview conflicts** - `git merge --no-commit --no-ff <branch>`
4. **Abort preview** - `git merge --abort`

## Related Skills

- skills/git-safety.md
- skills/sync-workflow.md
