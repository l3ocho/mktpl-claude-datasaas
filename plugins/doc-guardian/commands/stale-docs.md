---
description: Detect documentation files that are stale relative to their associated code
---

# Stale Documentation Detection

Identify documentation files that may be outdated based on commit history.

## Process

1. **Map Documentation to Code**
   Build relationships between docs and code:

   | Doc File | Related Code |
   |----------|--------------|
   | README.md | All files in same directory |
   | API.md | src/api/**/* |
   | CLAUDE.md | Configuration files, scripts |
   | docs/module.md | src/module/**/* |
   | Component.md | Component.tsx, Component.css |

2. **Analyze Commit History**
   For each doc file:
   - Find last commit that modified the doc
   - Find last commit that modified related code
   - Count commits to code since doc was updated

3. **Calculate Staleness**
   ```
   Commits Behind = Code Commits Since Doc Update
   Days Behind = Days Since Doc Update - Days Since Code Update
   ```

4. **Apply Threshold**
   Default: Flag if documentation is 10+ commits behind related code

   **Staleness Levels:**
   | Commits Behind | Level | Action |
   |----------------|-------|--------|
   | 0-5 | Fresh | No action needed |
   | 6-10 | Aging | Review recommended |
   | 11-20 | Stale | Update needed |
   | 20+ | Critical | Immediate attention |

5. **Output Format**
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

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--threshold <n>` | Commits behind to flag as stale | 10 |
| `--days` | Use days instead of commits | false |
| `--path <dir>` | Scan specific directory | Project root |
| `--doc-pattern <glob>` | Pattern for doc files | `**/*.md,**/README*` |
| `--ignore <glob>` | Ignore specific docs | `CHANGELOG.md,LICENSE` |
| `--show-fresh` | Include fresh docs in output | false |
| `--format <fmt>` | Output format (table, json) | table |

## Relationship Detection

How docs are mapped to code:

1. **Same Directory**
   - `src/api/README.md` relates to `src/api/**/*`

2. **Name Matching**
   - `docs/auth.md` relates to `**/auth.*`, `**/auth/**`

3. **Explicit Links**
   - Parse `[link](path)` in docs to find related files

4. **Import Analysis**
   - Track which modules are referenced in code examples

## Configuration

Create `.doc-guardian.yml` to customize mappings:
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

## Example Usage

```
/stale-docs
/stale-docs --threshold 5
/stale-docs --days --threshold 30
/stale-docs --path docs/ --show-fresh
```

## Integration with doc-audit

`/stale-docs` focuses specifically on commit-based staleness, while `/doc-audit` checks content accuracy. Use both for comprehensive documentation health:

```
/doc-audit      # Check for broken references and content drift
/stale-docs     # Check for files that may need review
```

## Exit Codes

- 0: No critical or stale documentation
- 1: Stale documentation found (useful for CI)
- 2: Critical documentation found
