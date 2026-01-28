# /data-quality - Data Quality Assessment

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  📊 DATA-PLATFORM · Data Quality                                  │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the assessment.

Comprehensive data quality check for DataFrames with pass/warn/fail scoring.

## Usage

```
/data-quality <data_ref> [--strict]
```

## Workflow

1. **Get data reference**:
   - If no data_ref provided, use `list_data` to show available options
   - Validate the data_ref exists

2. **Null analysis**:
   - Calculate null percentage per column
   - **PASS**: < 5% nulls
   - **WARN**: 5-20% nulls
   - **FAIL**: > 20% nulls

3. **Duplicate detection**:
   - Check for fully duplicated rows
   - **PASS**: 0% duplicates
   - **WARN**: < 1% duplicates
   - **FAIL**: >= 1% duplicates

4. **Type consistency**:
   - Identify mixed-type columns (object columns with mixed content)
   - Flag columns that could be numeric but contain strings
   - **PASS**: All columns have consistent types
   - **FAIL**: Mixed types detected

5. **Outlier detection** (numeric columns):
   - Use IQR method (values beyond 1.5 * IQR)
   - Report percentage of outliers per column
   - **PASS**: < 1% outliers
   - **WARN**: 1-5% outliers
   - **FAIL**: > 5% outliers

6. **Generate quality report**:
   - Overall quality score (0-100)
   - Per-column breakdown
   - Recommendations for remediation

## Report Format

```
=== Data Quality Report ===
Dataset: sales_data
Rows: 10,000 | Columns: 15
Overall Score: 82/100 [PASS]

--- Column Analysis ---
| Column       | Nulls | Dups | Type     | Outliers | Status |
|--------------|-------|------|----------|----------|--------|
| customer_id  | 0.0%  | -    | int64    | 0.2%     | PASS   |
| email        | 2.3%  | -    | object   | -        | PASS   |
| amount       | 15.2% | -    | float64  | 3.1%     | WARN   |
| created_at   | 0.0%  | -    | datetime | -        | PASS   |

--- Issues Found ---
[WARN] Column 'amount': 15.2% null values (threshold: 5%)
[WARN] Column 'amount': 3.1% outliers detected
[FAIL] 1.2% duplicate rows detected (12 rows)

--- Recommendations ---
1. Investigate null values in 'amount' column
2. Review outliers in 'amount' - may be data entry errors
3. Remove or deduplicate 12 duplicate rows
```

## Options

| Flag | Description |
|------|-------------|
| `--strict` | Use stricter thresholds (WARN at 1% nulls, FAIL at 5%) |

## Examples

```
/data-quality sales_data
/data-quality df_customers --strict
```

## Scoring

| Component | Weight | Scoring |
|-----------|--------|---------|
| Nulls | 30% | 100 - (avg_null_pct * 2) |
| Duplicates | 20% | 100 - (dup_pct * 50) |
| Type consistency | 25% | 100 if clean, 0 if mixed |
| Outliers | 25% | 100 - (avg_outlier_pct * 10) |

Final score: Weighted average, capped at 0-100

## Available Tools

Use these MCP tools:
- `describe` - Get statistical summary (for outlier detection)
- `head` - Preview data
- `list_data` - List available DataFrames
