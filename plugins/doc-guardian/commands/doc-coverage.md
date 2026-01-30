---
description: Calculate documentation coverage percentage for functions and classes
---

# Documentation Coverage

Analyze codebase to calculate documentation coverage metrics.

## Skills to Load

- skills/coverage-calculation.md
- skills/doc-patterns.md

## Visual Output

```
+------------------------------------------------------------------+
|  DOC-GUARDIAN - Documentation Coverage                           |
+------------------------------------------------------------------+
```

## Process

1. **Scan Source Files**
   Execute `skills/coverage-calculation.md` - identify documentable items

2. **Determine Documentation Status**
   Check each item has meaningful docstring/JSDoc

3. **Calculate Metrics**
   Use formula from skill: `Coverage = (Documented / Total) * 100`

4. **Output**
   Use format from `skills/coverage-calculation.md`

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--path <dir>` | Scan specific directory | Project root |
| `--exclude <glob>` | Exclude pattern | `**/test_*` |
| `--min-coverage <pct>` | Fail if below | none |
| `--detailed` | Check params/returns | false |

## Exit Codes

- 0: Coverage meets threshold
- 1: Coverage below threshold
