# Branch Naming

## Purpose

Defines branch naming conventions and validation rules for consistent repository organization.

## When to Use

- Creating new branches with `/branch-start`
- Validating branch names
- Converting descriptions to branch names

## Branch Name Format

```
<type>/<description>
```

## Branch Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat/user-authentication` |
| `fix` | Bug fix | `fix/login-timeout` |
| `chore` | Maintenance | `chore/update-deps` |
| `docs` | Documentation | `docs/api-reference` |
| `refactor` | Code restructure | `refactor/auth-module` |
| `test` | Test additions | `test/auth-coverage` |
| `perf` | Performance | `perf/query-optimization` |
| `debug` | Debugging work | `debug/memory-leak` |

## Naming Rules

1. **Lowercase only** - Never use uppercase
2. **Hyphens for spaces** - Use `-` not `_` or ` `
3. **No special characters** - Alphanumeric and hyphens only
4. **Descriptive** - 2-4 words recommended
5. **Max 50 characters** - Keep concise

## Conversion Algorithm

```
Input:  "Add User Authentication"
Output: "feat/add-user-authentication"

Steps:
1. Lowercase: "add user authentication"
2. Replace spaces: "add-user-authentication"
3. Remove special chars: (none to remove)
4. Add prefix: "feat/add-user-authentication"
5. Truncate if > 50: (not needed)
```

## Validation Checks

```
Branch name validation:
[x] Lowercase
[x] Valid prefix (feat/)
[x] Descriptive (3+ words recommended)
[ ] Too long (52 chars, max 50)

Suggested: feat/add-user-auth
```

## Examples

**Valid:**
```
feat/add-password-reset
fix/null-pointer-login
chore/upgrade-typescript-5
docs/update-readme
refactor/simplify-auth
```

**Invalid:**
```
Feature/Add_Password_Reset  (wrong case, underscores)
fix-bug                      (too vague, no prefix)
my-branch                    (no type prefix)
feat/add-new-super-amazing-feature-for-users  (too long)
```

## Issue-Linked Branches

When working on issues, include issue number:
```
feat/123-add-password-reset
fix/456-login-timeout
```

## Related Skills

- skills/commit-conventions.md
- skills/git-safety.md
- skills/workflow-patterns/branching-strategies.md
