---
name: staleness-metrics
description: Documentation staleness levels, thresholds, and relationship detection
---

# Staleness Metrics

## Purpose

Defines how to measure documentation staleness relative to code changes.

## When to Use

- **doc stale-docs**: Commit-based staleness detection
- **doc audit**: Age-based analysis

---

## Staleness Calculation

```
Commits Behind = Code Commits Since Doc Update
Days Behind = Days Since Doc Update - Days Since Code Update
```

---

## Staleness Levels

| Commits Behind | Level | Action |
|----------------|-------|--------|
| 0-5 | Fresh | No action needed |
| 6-10 | Aging | Review recommended |
| 11-20 | Stale | Update needed |
| 20+ | Critical | Immediate attention |

---

## Relationship Detection

### 1. Same Directory
`src/api/README.md` relates to `src/api/**/*`

### 2. Name Matching
`docs/auth.md` relates to `**/auth.*`, `**/auth/**`

### 3. Explicit Links
Parse `[link](path)` in docs to find related files

### 4. Import Analysis
Track which modules are referenced in code examples

---

## Git Commands

```bash
# Last doc commit
git log -1 --format="%H %ai" -- docs/api.md

# Last code commit for related files
git log -1 --format="%H %ai" -- src/api/

# Commits to code since doc update
git rev-list <doc-commit>..HEAD -- src/api/ | wc -l
```

---

## Configuration

`.doc-guardian.yml`:
```yaml
stale-docs:
  threshold: 10
  mappings:
    - doc: docs/deployment.md
      code:
        - Dockerfile
        - docker-compose.yml
        - .github/workflows/deploy.yml
    - doc: ARCHITECTURE.md
      code:
        - src/**/*
  ignore:
    - CHANGELOG.md
    - LICENSE
    - vendor/**
```

---

## Output Format

```
## Stale Documentation Report

### Critical (20+ commits behind)
| File | Last Updated | Commits Behind | Related Code |
|------|--------------|----------------|--------------|
| docs/api.md | 2024-01-15 | 34 | src/api/**/* |

### Stale (11-20 commits behind)
| File | Last Updated | Commits Behind | Related Code |
|------|--------------|----------------|--------------|
| README.md | 2024-02-20 | 15 | package.json, src/index.ts |

### Aging (6-10 commits behind)
| File | Last Updated | Commits Behind | Related Code |
|------|--------------|----------------|--------------|
| CONTRIBUTING.md | 2024-03-01 | 8 | .github/*, scripts/* |

### Summary
- Critical: 1 file
- Stale: 1 file
- Aging: 1 file
- Fresh: 12 files
- Total documentation files: 15
```

---

## Exit Codes

- 0: No critical or stale documentation
- 1: Stale documentation found (for CI)
- 2: Critical documentation found
