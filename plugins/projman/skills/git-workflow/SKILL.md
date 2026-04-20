---
name: git-workflow
description: Branch naming, merge process, and git operations
---

# Git Workflow

## Purpose

Defines branch naming conventions, merge protocols, and git operations.

## When to Use

- **Orchestrator agent**: When coordinating git operations
- **Executor agent**: When creating branches and commits
- **Commands**: `/sprint start`, `/sprint close`

---

## Branch Naming Convention (MANDATORY)

| Type | Pattern | Example |
|------|---------|---------|
| Features | `feat/<issue>-<desc>` | `feat/45-jwt-service` |
| Bug fixes | `fix/<issue>-<desc>` | `fix/46-login-timeout` |
| Debugging | `debug/<issue>-<desc>` | `debug/47-memory-leak` |

### Validation Rules

- Issue number MUST be present
- Prefix MUST be `feat/`, `fix/`, or `debug/`
- Description: kebab-case (lowercase, hyphens)
- No spaces or special characters

### Creating Feature Branch

```bash
git checkout development
git pull origin development
git checkout -b feat/45-jwt-service
```

---

## Branch Isolation

**Each task MUST have its own branch.**

```
Task #45 → feat/45-jwt-service (isolated)
Task #48 → feat/48-api-docs (isolated)
```

Never have two agents work on the same branch.

---

## Sequential Merge Protocol

After task completion, merge sequentially (never simultaneously):

```
1. Task #45 completes → merge feat/45-jwt-service to development
2. Task #48 completes → merge feat/48-api-docs to development
3. Never merge simultaneously - always sequential to detect conflicts
```

### Merge Steps

```bash
git checkout development
git pull origin development
git merge feat/45-jwt-service --no-ff
git push origin development
git branch -d feat/45-jwt-service
```

### If Merge Conflict Occurs

1. Stop second task
2. Resolve conflict manually or assign to human
3. Resume/restart second task with updated base

---

## Commit Message Format

```
<type>: <description>

[Optional body with details]

[Optional: Closes #XX]
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code refactoring |
| `docs` | Documentation |
| `test` | Test additions |
| `chore` | Maintenance |

### Auto-Close Keywords

Use in commit message to auto-close issues:
- `Closes #XX`
- `Fixes #XX`
- `Resolves #XX`

### Example

```
feat: implement JWT token generation

- Add generate_token(user_id, email) function
- Add verify_token(token) function
- Include refresh logic per Sprint 12 lesson

Closes #45
```

---

## Merge Request Template

When branch protection requires MR (check via `get_branch_protection`):

```markdown
## Summary
Brief description of changes made.

## Related Issues
Closes #45

## Testing
- Describe how changes were tested
- Include test commands if relevant
```

**NEVER include subtask checklists in MR body.** The issue already has them.

---

## Sprint Close Git Operations

Offer to handle:
1. Commit any remaining changes
2. Merge feature branches to development
3. Tag sprint completion (if release)
4. Clean up merged branches

```bash
# Tag sprint completion
git tag -a v0.18.0 -m "Sprint 18 release"
git push origin v0.18.0

# Clean up merged branches
git branch -d feat/45-jwt-service feat/46-login-endpoint
```
