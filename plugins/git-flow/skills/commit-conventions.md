# Commit Conventions

## Purpose

Defines conventional commit message format for consistent, parseable commit history.

## When to Use

- Generating commit messages in `/git-commit`
- Validating user-provided commit messages
- Explaining commit format to users

## Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Commit Types

| Type | Purpose | Example Scope |
|------|---------|---------------|
| `feat` | New feature | `auth`, `api`, `ui` |
| `fix` | Bug fix | `login`, `validation` |
| `docs` | Documentation only | `readme`, `api-docs` |
| `style` | Formatting, whitespace | `lint`, `format` |
| `refactor` | Code change (no bug fix, no feature) | `auth-module` |
| `perf` | Performance improvement | `query`, `cache` |
| `test` | Adding/updating tests | `unit`, `e2e` |
| `chore` | Maintenance tasks | `deps`, `build` |
| `build` | Build system or dependencies | `webpack`, `npm` |
| `ci` | CI configuration | `github-actions` |

## Scope Detection

Derive scope from changed files:
- `src/auth/*` -> `auth`
- `src/api/*` -> `api`
- `tests/*` -> `test`
- `docs/*` -> `docs`
- Multiple directories -> most significant or omit

## Examples

**Feature commit:**
```
feat(auth): add password reset flow

Implement forgot password with email verification.
Includes rate limiting (5 attempts/hour) and 24h token expiration.

Closes #123
```

**Bug fix:**
```
fix(ui): resolve button alignment on mobile

The submit button was misaligned on screens < 768px.
Added responsive flex rules.
```

**Maintenance:**
```
chore(deps): update dependencies

- typescript 5.3 -> 5.4
- react 18.2 -> 18.3
- node 18 -> 20 (LTS)
```

## Footer Conventions

| Footer | Purpose |
|--------|---------|
| `Closes #123` | Auto-close issue |
| `Refs #123` | Reference without closing |
| `BREAKING CHANGE:` | Breaking change description |
| `Co-Authored-By:` | Credit co-author |

## Co-Author Footer

When Claude assists with commits:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Related Skills

- skills/branch-naming.md
- skills/git-safety.md
