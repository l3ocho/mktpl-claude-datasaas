# dbt Workflow

## Pre-Validation (MANDATORY)

**Always run `dbt_parse` before any dbt operation.**

This validates:
- dbt_project.yml syntax
- Model SQL syntax
- schema.yml definitions
- Deprecated syntax (dbt 1.9+)

If validation fails, show errors and STOP.

## Model Selection Syntax

| Pattern | Meaning |
|---------|---------|
| `model_name` | Single model |
| `+model_name` | Model and upstream dependencies |
| `model_name+` | Model and downstream dependents |
| `+model_name+` | Model with all dependencies |
| `tag:name` | Models with specific tag |
| `path:models/staging` | Models in path |
| `test_type:schema` | Schema tests only |
| `test_type:data` | Data tests only |

## Execution Workflow

1. **Parse**: `dbt_parse` - Validate project
2. **Run**: `dbt_run` - Execute models
3. **Test**: `dbt_test` - Run tests
4. **Build**: `dbt_build` - Run + test together

## Test Types

### Schema Tests
Defined in `schema.yml`:
- `unique` - No duplicate values
- `not_null` - No null values
- `accepted_values` - Value in allowed list
- `relationships` - Foreign key integrity

### Data Tests
Custom SQL in `tests/` directory:
- Return rows that fail assertion
- Zero rows = pass, any rows = fail

## Materialization Types

| Type | Description |
|------|-------------|
| `view` | Virtual table, always fresh |
| `table` | Physical table, full rebuild |
| `incremental` | Append/merge new rows only |
| `ephemeral` | CTE, no physical object |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Test/run failure |
| 2 | dbt error (parse failure) |

## Result Formatting

```
=== dbt [Operation] Results ===
Project: [project_name]
Selection: [selection_pattern]

--- Summary ---
Total: X models/tests
PASS:  X (%)
FAIL:  X (%)
WARN:  X (%)
SKIP:  X (%)

--- Details ---
[Model/Test details with status]

--- Failure Details ---
[Error messages and remediation]
```
