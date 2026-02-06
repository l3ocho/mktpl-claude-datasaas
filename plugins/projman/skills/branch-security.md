---
name: branch-security
description: Branch detection, protection rules, and branch-aware authorization
---

# Branch Security

## Purpose

Defines branch detection, classification, and branch-aware authorization rules.

## When to Use

- **Planner agent**: Before planning any sprint work
- **Orchestrator agent**: Before executing any sprint tasks
- **Executor agent**: Before modifying any files
- **Commands**: `/sprint plan`, `/sprint start`, `/sprint close`

---

## Branch Detection

```bash
git branch --show-current
```

## Branch Classification

| Branch Pattern | Classification | Capabilities |
|----------------|----------------|--------------|
| `development`, `develop`, `feat/*`, `fix/*`, `dev/*` | Development | Full access |
| `staging`, `stage/*` | Staging | Read-only code, can create issues |
| `main`, `master`, `prod/*` | Production | READ-ONLY, no changes |

---

## Behavior by Classification

### Development Branches
- Full planning and execution capabilities
- Can create/modify issues, wiki, lessons
- Can execute tasks and modify code
- Normal operation

### Staging Branches
- Can create issues to document bugs
- CANNOT modify application code
- Can modify `.env` files only
- Warn user about limitations

### Production Branches
- READ-ONLY mode enforced
- Cannot create issues or modify anything
- MUST stop immediately and instruct user to switch

---

## Stop Messages

### Production Branch
```
BRANCH SECURITY: Production branch detected

You are on branch: [branch-name]
Planning and execution are NOT allowed on production branches.

Please switch to a development branch:
  git checkout development

Or create a feature branch:
  git checkout -b feat/[issue-number]-[description]
```

### Staging Branch Warning
```
STAGING BRANCH: Limited capabilities

Available: Create issues to document bugs
Not available: Sprint planning, code modifications

Switch to development for full capabilities:
  git checkout development
```

---

## Branch Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Features | `feat/<issue>-<desc>` | `feat/45-jwt-service` |
| Bug fixes | `fix/<issue>-<desc>` | `fix/46-login-timeout` |
| Debugging | `debug/<issue>-<desc>` | `debug/47-memory-leak` |

**Validation:**
- Issue number MUST be present
- Prefix MUST be `feat/`, `fix/`, or `debug/`
- Description: kebab-case (lowercase, hyphens)
