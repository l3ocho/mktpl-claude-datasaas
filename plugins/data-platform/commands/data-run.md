# /data-run - Execute dbt Models

## Skills to Load
- skills/dbt-workflow.md
- skills/mcp-tools-reference.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-PLATFORM - dbt Run`

## Usage

```
/data-run [model_selection] [--full-refresh]
```

## Workflow

Execute `skills/dbt-workflow.md` run workflow:

1. **Pre-validation** (MANDATORY): Run `dbt_parse` first
2. **Execute models**: Use `dbt_run` with selection
3. **Report results**: Status, execution time, row counts

## Selection Syntax

See `skills/dbt-workflow.md` for full selection patterns.

## Examples

```
/data-run                           # Run all models
/data-run dim_customers             # Run specific model
/data-run +fct_orders               # Run model and upstream
/data-run tag:daily                 # Run models with tag
/data-run --full-refresh            # Rebuild incremental models
```

## Required MCP Tools

- `dbt_parse` - Pre-validation (ALWAYS RUN FIRST)
- `dbt_run` - Execute models
- `dbt_build` - Run + test
