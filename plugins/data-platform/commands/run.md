# /run - Execute dbt Models

Run dbt models with automatic pre-validation.

## Usage

```
/run [model_selection] [--full-refresh]
```

## Workflow

1. **Pre-validation** (MANDATORY):
   - Use `dbt_parse` to validate project
   - Check for deprecated syntax (dbt 1.9+)
   - If validation fails, show errors and STOP

2. **Execute models**:
   - Use `dbt_run` with provided selection
   - Monitor progress and capture output

3. **Report results**:
   - Success/failure status per model
   - Execution time
   - Row counts where available
   - Any warnings or errors

## Examples

```
/run                           # Run all models
/run dim_customers             # Run specific model
/run +fct_orders               # Run model and its upstream
/run tag:daily                 # Run models with tag
/run --full-refresh            # Rebuild incremental models
```

## Selection Syntax

| Pattern | Meaning |
|---------|---------|
| `model_name` | Run single model |
| `+model_name` | Run model and upstream |
| `model_name+` | Run model and downstream |
| `+model_name+` | Run model with all deps |
| `tag:name` | Run by tag |
| `path:models/staging` | Run by path |

## Available Tools

Use these MCP tools:
- `dbt_parse` - Pre-validation (ALWAYS RUN FIRST)
- `dbt_run` - Execute models
- `dbt_build` - Run + test
- `dbt_test` - Run tests only
