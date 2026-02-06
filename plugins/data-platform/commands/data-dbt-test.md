---
name: data dbt-test
---

# /data dbt-test - Run dbt Tests

## Skills to Load
- skills/dbt-workflow.md
- skills/mcp-tools-reference.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-PLATFORM - dbt Tests`

## Usage

```
/data dbt-test [selection] [--warn-only]
```

## Workflow

Execute `skills/dbt-workflow.md` test workflow:

1. **Pre-validation** (MANDATORY): Run `dbt_parse` first
2. **Execute tests**: Use `dbt_test` with selection
3. **Format results**: Group by test type, show pass/fail/warn counts

## Options

| Flag | Description |
|------|-------------|
| `--warn-only` | Treat failures as warnings |

## Examples

```
/data dbt-test                          # Run all tests
/data dbt-test dim_customers            # Tests for specific model
/data dbt-test tag:critical             # Run critical tests only
```

## Required MCP Tools

- `dbt_parse` - Pre-validation (ALWAYS RUN FIRST)
- `dbt_test` - Execute tests (REQUIRED)
