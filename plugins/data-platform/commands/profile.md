# /profile - Data Profiling

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  📊 DATA-PLATFORM · Data Profile                                  │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the profiling.

Generate statistical profile and quality report for a DataFrame.

## Usage

```
/profile <data_ref>
```

## Workflow

1. **Get data reference**:
   - If no data_ref provided, use `list_data` to show available options
   - Validate the data_ref exists

2. **Generate profile**:
   - Use `describe` for statistical summary
   - Analyze null counts, unique values, data types

3. **Quality assessment**:
   - Identify columns with high null percentage
   - Flag potential data quality issues
   - Suggest cleaning operations if needed

4. **Report**:
   - Summary statistics per column
   - Data type distribution
   - Memory usage
   - Quality score

## Examples

```
/profile sales_data
/profile df_a1b2c3d4
```

## Available Tools

Use these MCP tools:
- `describe` - Get statistical summary
- `head` - Preview first rows
- `list_data` - List available DataFrames
