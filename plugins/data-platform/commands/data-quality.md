---
name: data quality
---

# /data quality - Data Quality Assessment

## Skills to Load
- skills/data-profiling.md
- skills/mcp-tools-reference.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-PLATFORM - Data Quality`

## Usage

```
/data quality <data_ref> [--strict]
```

## Workflow

Execute `skills/data-profiling.md` quality assessment:

1. **Get data reference**: Use `list_data` if none provided
2. **Run quality checks**: Nulls, duplicates, types, outliers
3. **Calculate score**: Apply weighted scoring formula
4. **Generate report**: Issues and recommendations

## Options

| Flag | Description |
|------|-------------|
| `--strict` | Stricter thresholds (WARN at 1%, FAIL at 5% nulls) |

## Examples

```
/data quality sales_data
/data quality df_customers --strict
```

## Quality Thresholds

See `skills/data-profiling.md` for detailed thresholds and scoring.

## Required MCP Tools

- `describe` - Get statistical summary
- `head` - Preview data
- `list_data` - List available DataFrames
