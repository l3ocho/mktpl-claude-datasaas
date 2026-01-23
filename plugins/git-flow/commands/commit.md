# /commit - Smart Commit

## Purpose

Create a git commit with an auto-generated conventional commit message based on staged changes.

## Behavior

### Step 1: Check for Protected Branch

Before any commit operation, check if the current branch is protected:

1. Get current branch: `git branch --show-current`
2. Check against `GIT_PROTECTED_BRANCHES` (default: `main,master,development,staging,production`)

If on a protected branch, warn the user:

```
⚠️  You are on a protected branch: development

Protected branches typically have push restrictions that will prevent
direct commits from being pushed to the remote.

Options:
1. Create a feature branch and continue (Recommended)
2. Continue on this branch anyway (may fail on push)
3. Cancel
```

**If option 1 (create feature branch):**
- Prompt for branch type (feat/fix/chore/docs/refactor)
- Prompt for brief description
- Create branch using `/branch-start` naming conventions
- Continue with commit on the new branch

**If option 2 (continue anyway):**
- Proceed with commit (user accepts risk of push rejection)
- Display reminder: "Remember: push may be rejected by remote protection rules"

### Step 2: Analyze Changes

1. Run `git status` to see staged and unstaged changes
2. Run `git diff --staged` to examine staged changes
3. If nothing staged, prompt user to stage changes

### Step 3: Generate Commit Message

Analyze the changes and generate a conventional commit message:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `build`: Build system or external dependencies
- `ci`: CI configuration

**Scope:** Determined from changed files (e.g., `auth`, `api`, `ui`)

### Step 4: Confirm or Edit

Present the generated message:

```
Proposed commit message:
───────────────────────
feat(auth): add password reset functionality

Implement forgot password flow with email verification.
Includes rate limiting and token expiration.
───────────────────────

Options:
1. Use this message (Recommended)
2. Edit the message
3. Regenerate with different focus
4. Cancel
```

### Step 5: Execute Commit

If confirmed, run:

```bash
git commit -m "$(cat <<'EOF'
<message>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_PROTECTED_BRANCHES` | `main,master,development,staging,production` | Branches that trigger protection warning |
| `GIT_COMMIT_STYLE` | `conventional` | Message style (conventional, simple, detailed) |
| `GIT_SIGN_COMMITS` | `false` | Use GPG signing |
| `GIT_CO_AUTHOR` | `true` | Include Claude co-author footer |

## Edge Cases

### No Changes Staged

```
No changes staged for commit.

Would you like to:
1. Stage all changes (`git add -A`)
2. Stage specific files (I'll help you choose)
3. Cancel
```

### Untracked Files

```
Found 3 untracked files:
- src/new-feature.ts
- tests/new-feature.test.ts
- docs/new-feature.md

Include these in the commit?
1. Yes, stage all (Recommended)
2. Let me pick which ones
3. No, commit only tracked files
```

## Output

On success:
```
Committed: abc1234
feat(auth): add password reset functionality

Files: 3 changed, 45 insertions(+), 12 deletions(-)
```
