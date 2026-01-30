# Data Profiling

## Profiling Workflow

1. **Get data reference** via `list_data`
2. **Generate statistics** via `describe`
3. **Analyze quality** (nulls, duplicates, types, outliers)
4. **Calculate score** and generate report

## Quality Checks

### Null Analysis
- Calculate null percentage per column
- **PASS**: < 5% nulls
- **WARN**: 5-20% nulls
- **FAIL**: > 20% nulls

### Duplicate Detection
- Check for fully duplicated rows
- **PASS**: 0% duplicates
- **WARN**: < 1% duplicates
- **FAIL**: >= 1% duplicates

### Type Consistency
- Identify mixed-type columns
- Flag numeric columns with string values
- **PASS**: Consistent types
- **FAIL**: Mixed types detected

### Outlier Detection (IQR Method)
- Calculate Q1, Q3, IQR = Q3 - Q1
- Outliers: values < Q1 - 1.5*IQR or > Q3 + 1.5*IQR
- **PASS**: < 1% outliers
- **WARN**: 1-5% outliers
- **FAIL**: > 5% outliers

## Quality Scoring

| Component | Weight | Formula |
|-----------|--------|---------|
| Nulls | 30% | 100 - (avg_null_pct * 2) |
| Duplicates | 20% | 100 - (dup_pct * 50) |
| Type consistency | 25% | 100 if clean, 0 if mixed |
| Outliers | 25% | 100 - (avg_outlier_pct * 10) |

Final score: Weighted average, capped at 0-100

## Report Format

```
=== Data Quality Report ===
Dataset: [data_ref]
Rows: X | Columns: Y
Overall Score: XX/100 [PASS/WARN/FAIL]

--- Column Analysis ---
| Column | Nulls | Dups | Type | Outliers | Status |
|--------|-------|------|------|----------|--------|
| col1   | X.X%  | -    | type | X.X%     | PASS   |

--- Issues Found ---
[WARN/FAIL] Column 'X': Issue description

--- Recommendations ---
1. Suggested remediation steps
```

## Strict Mode

With `--strict` flag:
- **WARN** at 1% nulls (vs 5%)
- **FAIL** at 5% nulls (vs 20%)
