---
name: db-migrate validate
description: Check migration safety before applying
agent: migration-auditor
---

# /db-migrate validate - Migration Safety Validator

## Skills to Load

- skills/migration-safety.md
- skills/visual-header.md

## Visual Output

Display header: `DB-MIGRATE - Validate`

## Usage

```
/db-migrate validate [<migration-file>] [--all] [--strict]
```

**Arguments:**
- `<migration-file>`: Specific migration to validate (default: latest unapplied)
- `--all`: Validate all unapplied migrations
- `--strict`: Treat warnings as errors

## Prerequisites

Run `/db-migrate setup` first. Migration files must exist in the configured directory.

## Process

### 1. Identify Target Migrations

Determine which migrations to validate:
- Specific file if provided
- All unapplied migrations if `--all`
- Latest unapplied migration by default

### 2. Parse Migration Operations

Read each migration file and extract SQL operations:
- Table creation/deletion
- Column additions, modifications, removals
- Index operations
- Constraint changes
- Data manipulation (INSERT, UPDATE, DELETE)
- Custom SQL blocks

### 3. Safety Analysis

Apply safety rules from `skills/migration-safety.md`:

| Check | Severity | Description |
|-------|----------|-------------|
| DROP TABLE | FAIL | Permanent data loss; requires explicit acknowledgment |
| DROP COLUMN | FAIL | Data loss; must confirm column is unused |
| ALTER COLUMN type (narrowing) | FAIL | Data truncation risk (e.g., VARCHAR(255) to VARCHAR(50)) |
| ALTER COLUMN type (widening) | WARN | Safe but verify application handles new type |
| ALTER COLUMN NOT NULL (existing data) | FAIL | May fail if NULLs exist; needs DEFAULT or backfill |
| RENAME TABLE/COLUMN | WARN | Application code must be updated simultaneously |
| Large table ALTER | WARN | May lock table for extended time; consider batching |
| Missing transaction wrapper | FAIL | Partial migrations leave inconsistent state |
| Missing rollback/downgrade | WARN | Cannot undo if problems occur |
| Data migration in schema migration | WARN | Should be separate migration |
| No-op migration | INFO | Migration has no effect |

### 4. Lock Duration Estimation

For ALTER operations on existing tables, estimate lock impact:
- Table size (if database connection available)
- Operation type (ADD COLUMN is instant in PostgreSQL, ALTER TYPE is not)
- Concurrent operation risk

### 5. Generate Report

Group findings by severity with actionable recommendations.

## Output Format

```
+----------------------------------------------------------------------+
|  DB-MIGRATE - Validate                                               |
+----------------------------------------------------------------------+

Target: alembic/versions/b3c4d5e6_drop_legacy_columns.py
Tool: Alembic

FINDINGS

FAIL (2)
  1. DROP COLUMN users.legacy_email
     Risk: Permanent data loss for 12,450 rows with values
     Fix: Verify column is unused, add data backup step, or
          rename column first and drop in a future migration

  2. ALTER COLUMN orders.total VARCHAR(10) -> VARCHAR(5)
     Risk: Data truncation for values longer than 5 characters
     Fix: Check max actual length: SELECT MAX(LENGTH(total)) FROM orders
          If safe, document in migration comment

WARN (1)
  1. Missing downgrade for DROP COLUMN
     Risk: Cannot rollback this migration
     Fix: Add downgrade() that re-creates column (data will be lost)

INFO (1)
  1. Migration includes both schema and data changes
     Suggestion: Separate into two migrations for cleaner rollback

SUMMARY
  Operations:   4 (2 DDL, 2 DML)
  FAIL:         2 (must fix before applying)
  WARN:         1 (should fix)
  INFO:         1 (improve)

VERDICT: FAIL (2 blocking issues)
```

## Exit Guidance

- FAIL: Do not apply migration until issues are resolved
- WARN: Review carefully; proceed with caution
- INFO: Suggestions for improvement; safe to proceed
- `--strict`: All WARN become FAIL
