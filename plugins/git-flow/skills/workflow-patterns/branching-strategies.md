# Git Branching Strategies

## Supported Workflow Styles

### 1. Simple

```
main ─────●─────●─────●─────●─────●
          ↑     ↑     ↑     ↑     ↑
       commit commit commit commit commit
```

**Best for:**
- Solo projects
- Small scripts/utilities
- Documentation repos

**Rules:**
- Direct commits to main/development
- No feature branches required
- Linear history

### 2. Feature Branch (Default)

```
main ─────────────────●───────────●───────────
                      ↑           ↑
development ────●────●────●────●────●────●────
                ↑    ↑    ↑    ↑
feat/a ─────●───●────┘    │    │
                          │    │
feat/b ──────────●────●───┘    │
                               │
fix/c ────────────────●────●───┘
```

**Best for:**
- Small teams (2-5 developers)
- Projects without formal review process
- Rapid development cycles

**Rules:**
- Feature branches from development
- Merge when complete
- Delete branches after merge
- development → main for releases

### 3. PR Required

```
main ─────────────────────────────●───────────
                                  ↑
development ────●────●────●────●────●────●────
                ↑    ↑    ↑    ↑
                PR   PR   PR   PR
                ↑    ↑    ↑    ↑
feat/a ─────●───●    │    │    │
                     │    │    │
feat/b ──────────●───●    │    │
                          │    │
feat/c ───────────────●───●    │
                               │
fix/d ────────────────────●────●
```

**Best for:**
- Teams with code review requirements
- Open source projects
- Projects with CI/CD gates

**Rules:**
- All changes via pull request
- At least one approval required
- CI must pass before merge
- Squash commits on merge

### 4. Trunk-Based

```
main ────●────●────●────●────●────●────●────●
         ↑    ↑    ↑    ↑    ↑    ↑    ↑    ↑
         │    │    │    │    │    │    │    │
short branches (< 1 day)
```

**Best for:**
- CI/CD heavy workflows
- Experienced teams
- High deployment frequency

**Rules:**
- Very short-lived branches (hours, not days)
- Frequent integration to main
- Feature flags for incomplete work
- Continuous deployment

## Branch Naming Convention

```
<type>/<description>
```

### Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat/user-authentication` |
| `fix` | Bug fix | `fix/login-timeout` |
| `chore` | Maintenance | `chore/update-deps` |
| `docs` | Documentation | `docs/api-reference` |
| `refactor` | Code restructure | `refactor/auth-module` |
| `test` | Test additions | `test/auth-coverage` |
| `perf` | Performance | `perf/query-optimization` |

### Naming Rules

1. Lowercase only
2. Hyphens for word separation
3. No special characters
4. Descriptive (2-4 words)
5. Max 50 characters

### Examples

```
✓ feat/add-password-reset
✓ fix/null-pointer-login
✓ chore/upgrade-typescript-5

✗ Feature/Add_Password_Reset  (wrong case, underscores)
✗ fix-bug                      (too vague)
✗ my-branch                    (no type prefix)
```

## Protected Branches

Default protected branches:
- `main` / `master`
- `development` / `develop`
- `staging`
- `production`

Protection rules:
- No direct commits
- No force push
- Require PR for changes
- No deletion

## Commit Message Convention

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Examples

```
feat(auth): add password reset flow

Implement forgot password functionality with email verification.
Includes rate limiting (5 attempts/hour) and 24h token expiration.

Closes #123
```

```
fix(ui): resolve button alignment on mobile

The submit button was misaligned on screens < 768px.
Added responsive flex rules.
```

```
chore(deps): update dependencies

- typescript 5.3 → 5.4
- react 18.2 → 18.3
- node 18 → 20 (LTS)
```
