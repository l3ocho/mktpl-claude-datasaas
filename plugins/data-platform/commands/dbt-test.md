# /dbt-test - Run dbt Tests

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  📊 DATA-PLATFORM · dbt Tests                                     │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the tests.

Execute dbt tests with formatted pass/fail results.

## Usage

```
/dbt-test [selection] [--warn-only]
```

## Workflow

1. **Pre-validation** (MANDATORY):
   - Use `dbt_parse` to validate project first
   - If validation fails, show errors and STOP

2. **Execute tests**:
   - Use `dbt_test` with provided selection
   - Capture all test results

3. **Format results**:
   - Group by test type (schema vs. data)
   - Show pass/fail status with counts
   - Display failure details

## Report Format

```
=== dbt Test Results ===
Project: my_project
Selection: tag:critical

--- Summary ---
Total: 24 tests
PASS:  22 (92%)
FAIL:  1  (4%)
WARN:  1  (4%)
SKIP:  0  (0%)

--- Schema Tests (18) ---
[PASS] unique_dim_customers_customer_id
[PASS] not_null_dim_customers_customer_id
[PASS] not_null_dim_customers_email
[PASS] accepted_values_dim_customers_status
[FAIL] relationships_fct_orders_customer_id

--- Data Tests (6) ---
[PASS] assert_positive_order_amounts
[PASS] assert_valid_dates
[WARN] assert_recent_orders (threshold: 7 days)

--- Failure Details ---
Test: relationships_fct_orders_customer_id
Type: schema (relationships)
Model: fct_orders
Message: 15 records failed referential integrity check
Query: SELECT * FROM fct_orders WHERE customer_id NOT IN (SELECT customer_id FROM dim_customers)

--- Warning Details ---
Test: assert_recent_orders
Type: data
Message: No orders in last 7 days (expected for dev environment)
Severity: warn
```

## Selection Syntax

| Pattern | Meaning |
|---------|---------|
| (none) | Run all tests |
| `model_name` | Tests for specific model |
| `+model_name` | Tests for model and upstream |
| `tag:critical` | Tests with tag |
| `test_type:schema` | Only schema tests |
| `test_type:data` | Only data tests |

## Options

| Flag | Description |
|------|-------------|
| `--warn-only` | Treat failures as warnings (don't fail CI) |

## Examples

```
/dbt-test                          # Run all tests
/dbt-test dim_customers            # Tests for specific model
/dbt-test tag:critical             # Run critical tests only
/dbt-test +fct_orders              # Test model and its upstream
```

## Test Types

### Schema Tests
Built-in tests defined in `schema.yml`:
- `unique` - No duplicate values
- `not_null` - No null values
- `accepted_values` - Value in allowed list
- `relationships` - Foreign key integrity

### Data Tests
Custom SQL tests in `tests/` directory:
- Return rows that fail the assertion
- Zero rows = pass, any rows = fail

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All tests passed |
| 1 | One or more tests failed |
| 2 | dbt error (parse failure, etc.) |

## Available Tools

Use these MCP tools:
- `dbt_parse` - Pre-validation (ALWAYS RUN FIRST)
- `dbt_test` - Execute tests (REQUIRED)
- `dbt_build` - Alternative: run + test together
