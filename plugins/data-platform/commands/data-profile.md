# /data-profile - Data Profiling

## Skills to Load
- skills/data-profiling.md
- skills/mcp-tools-reference.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-PLATFORM - Data Profile`

## Usage

```
/data-profile <data_ref>
```

## Workflow

Execute `skills/data-profiling.md` profiling workflow:

1. **Get data reference**: Use `list_data` if none provided
2. **Generate profile**: Use `describe` for statistics
3. **Quality assessment**: Identify null columns, potential issues
4. **Report**: Statistics, types, memory usage, quality score

## Examples

```
/data-profile sales_data
/data-profile df_a1b2c3d4
```

## Required MCP Tools

- `describe` - Get statistical summary
- `head` - Preview first rows
- `list_data` - List available DataFrames
