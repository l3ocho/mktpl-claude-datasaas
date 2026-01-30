---
description: Detect documentation files that are stale relative to their associated code
---

# Stale Documentation Detection

Identify documentation files that may be outdated based on commit history.

## Skills to Load

- skills/staleness-metrics.md
- skills/drift-detection.md

## Visual Output

```
+------------------------------------------------------------------+
|  DOC-GUARDIAN - Stale Documentation Check                        |
+------------------------------------------------------------------+
```

## Process

1. **Map Documentation to Code**
   Execute `skills/staleness-metrics.md` - build relationships

2. **Analyze Commit History**
   For each doc file:
   - Find last commit that modified the doc
   - Find last commit that modified related code
   - Count commits to code since doc was updated

3. **Calculate Staleness**
   Use levels from skill (Fresh/Aging/Stale/Critical)

4. **Output**
   Use format from `skills/staleness-metrics.md`

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--threshold <n>` | Commits behind to flag | 10 |
| `--days` | Use days instead | false |
| `--path <dir>` | Scan directory | Project root |
| `--show-fresh` | Include fresh docs | false |

## Exit Codes

- 0: No critical or stale docs
- 1: Stale docs found
- 2: Critical docs found
