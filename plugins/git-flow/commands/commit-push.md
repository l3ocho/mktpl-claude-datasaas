# /commit-push - Commit and Push

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔀 GIT-FLOW · Commit & Push                                      │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the workflow.

## Purpose

Create a commit and push to the remote repository in one operation.

## Behavior

### Step 1: Run /commit

Execute the standard commit workflow (see commit.md).

### Step 2: Push to Remote

After successful commit:

1. Check if branch has upstream tracking
2. If no upstream, set it: `git push -u origin <branch>`
3. If upstream exists: `git push`

### Step 3: Handle Conflicts

If push fails due to diverged history:

```
Remote has changes not in your local branch.

Options:
1. Pull and rebase, then push (Recommended)
2. Pull and merge, then push
3. Force push (⚠️ destructive)
4. Cancel and review manually
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_AUTO_PUSH` | `true` | Auto-push after commit |
| `GIT_PUSH_STRATEGY` | `rebase` | How to handle diverged branches |

## Safety Checks

- **Protected branches**: Warn before pushing to main/master/production
- **Force push**: Require explicit confirmation
- **No tracking**: Ask before creating new remote branch

## Output

On success:
```
Committed: abc1234
feat(auth): add password reset functionality

Pushed to: origin/feat/password-reset
Remote URL: https://github.com/user/repo
```
