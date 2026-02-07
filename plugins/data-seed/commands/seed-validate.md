---
name: seed validate
---

# /seed validate - Validate Seed Data

## Skills to Load
- skills/schema-inference.md
- skills/relationship-resolution.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-SEED - Validate`

## Usage

```
/seed validate [--profile <name>] [--strict]
```

## Workflow

### 1. Load Schema and Seed Data
- Parse schema from configured source using `skills/schema-inference.md`
- Load generated seed data from output directory
- If no seed data found, report error and suggest running `/seed generate`

### 2. Type Constraint Validation
- For each column in each table, verify generated values match declared type:
  - Integer columns contain only integers within range (INT, BIGINT, SMALLINT)
  - String columns respect max length constraints (VARCHAR(N))
  - Date/datetime columns contain parseable date values
  - Boolean columns contain only true/false/null
  - Decimal columns respect precision and scale
  - UUID columns contain valid UUID format
  - Enum columns contain only declared valid values

### 3. Referential Integrity Validation
- Use `skills/relationship-resolution.md` to build FK dependency graph
- For every foreign key value in child tables, verify parent row exists
- For self-referential keys, verify referenced row exists in same table
- For many-to-many through tables, verify both sides exist
- Report orphaned references as FAIL

### 4. Constraint Compliance
- NOT NULL: verify no null values in required columns
- UNIQUE: verify no duplicate values in unique columns or unique-together groups
- CHECK constraints: evaluate check expressions against generated data
- Default values: verify defaults are applied where column value is omitted

### 5. Statistical Validation (--strict mode)
- Verify null ratio matches profile configuration within tolerance
- Verify edge case ratio matches profile configuration
- Verify row counts match profile specification
- Verify distribution of enum/category values is not unrealistically uniform
- Verify date ranges are within reasonable bounds (not year 9999)

### 6. Report
- Display validation results grouped by severity:
  - **FAIL**: Type mismatch, FK violation, NOT NULL violation, UNIQUE violation
  - **WARN**: Unrealistic distributions, unexpected null ratios, date range issues
  - **INFO**: Statistics summary, coverage metrics

```
+----------------------------------------------------------------------+
|  DATA-SEED - Validate                                                |
|  Profile: medium                                                     |
+----------------------------------------------------------------------+

Tables Validated: 8
Rows Checked: 1,450
Constraints Verified: 42

FAIL (0)
  No blocking violations found.

WARN (2)
  1. [orders.created_at] Date range spans 200 years
     Suggestion: Constrain date generator to recent years

  2. [users.email] 3 duplicate values detected
     Suggestion: Increase faker uniqueness retry count

INFO (1)
  1. [order_items] Null ratio 0.12 (profile target: 0.10)
     Within acceptable tolerance.

VERDICT: PASS (0 blocking issues)
```

## Examples

```
/seed validate                           # Standard validation
/seed validate --profile large           # Validate large profile data
/seed validate --strict                  # Include statistical checks
```
