# /branch-start - Start New Branch

## Purpose

Create a new feature/fix/chore branch with consistent naming conventions.

## Usage

```
/branch-start [description]
```

## Behavior

### Step 1: Determine Branch Type

```
What type of change is this?
1. feat - New feature
2. fix - Bug fix
3. chore - Maintenance task
4. docs - Documentation
5. refactor - Code refactoring
```

### Step 2: Get Description

If not provided, ask:

```
Brief description (2-4 words):
> add user authentication
```

### Step 3: Generate Branch Name

Convert to kebab-case:
- `feat/add-user-authentication`
- `fix/login-timeout-error`
- `chore/update-dependencies`

### Step 4: Create Branch

```bash
# Ensure base branch is up-to-date
git checkout <base-branch>
git pull origin <base-branch>

# Create and switch to new branch
git checkout -b <new-branch>
```

### Step 5: Confirm

```
Created branch: feat/add-user-authentication
Based on: development (abc1234)

Ready to start coding!
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_DEFAULT_BASE` | `development` | Branch to create from |
| `GIT_BRANCH_PREFIX` | `true` | Use type/ prefix |

## Naming Rules

- Lowercase only
- Hyphens for spaces
- No special characters
- Max 50 characters

## Validation

```
Branch name validation:
✓ Lowercase
✓ Valid prefix (feat/)
✓ Descriptive (3+ words recommended)
✗ Too long (52 chars, max 50)

Suggested: feat/add-user-auth
Use this instead? (y/n)
```

## Output

On success:
```
Branch: feat/add-user-authentication
Base: development @ abc1234
Status: Ready for development
```
