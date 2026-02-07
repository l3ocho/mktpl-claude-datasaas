---
name: db-migrate rollback
description: Generate rollback migration for a previously applied migration
agent: migration-planner
---

# /db-migrate rollback - Rollback Generator

## Skills to Load

- skills/rollback-patterns.md
- skills/visual-header.md

## Visual Output

Display header: `DB-MIGRATE - Rollback`

## Usage

```
/db-migrate rollback [<migration>] [--steps=<n>] [--dry-run]
```

**Arguments:**
- `<migration>`: Specific migration to roll back to (exclusive — rolls back everything after it)
- `--steps`: Number of migrations to roll back from current head (default: 1)
- `--dry-run`: Show what would be rolled back without generating files

## Prerequisites

Run `/db-migrate setup` first. Target migrations must have rollback/downgrade operations defined.

## Process

### 1. Identify Rollback Target

Determine which migrations to reverse:
- If `<migration>` specified: roll back all migrations applied after it
- If `--steps=N`: roll back the last N applied migrations
- Default: roll back the single most recent migration

### 2. Check Rollback Feasibility

For each migration to roll back, verify:

| Check | Result | Action |
|-------|--------|--------|
| Downgrade function exists | Yes | Proceed |
| Downgrade function exists | No | FAIL: Cannot auto-rollback; manual intervention needed |
| Migration contains DROP TABLE | N/A | WARN: Data cannot be restored by rollback |
| Migration contains data changes | N/A | WARN: DML changes may not be fully reversible |
| Later migrations depend on this | Yes | Must roll back dependents first |

### 3. Generate Rollback

Depending on the tool:

**Alembic:**
- Generate `alembic downgrade <target_revision>` command
- Show the downgrade SQL that will execute
- If downgrade function is incomplete, generate supplementary migration

**Prisma:**
- Generate rollback migration SQL based on diff
- Create new migration directory with rollback operations

**Raw SQL:**
- Generate new numbered migration file with reverse operations
- Include transaction wrapping and safety checks

### 4. Data Recovery Plan

If rolled-back migrations included destructive operations:
- Recommend backup restoration for lost data
- Suggest data export before rollback
- Identify tables/columns that will be recreated empty

### 5. Present Rollback Plan

Show the complete rollback strategy with warnings.

## Output Format

```
+----------------------------------------------------------------------+
|  DB-MIGRATE - Rollback                                               |
+----------------------------------------------------------------------+

Mode: Roll back 2 steps
Tool: Alembic

ROLLBACK PLAN

Step 1: Undo migration_008_add_status_to_orders
  Operations:
    [-] DROP CONSTRAINT valid_status
    [-] DROP COLUMN orders.status
  Data Impact: Column data will be lost (12,450 rows)
  Reversible: Partially (column recreated empty on re-apply)

Step 2: Undo migration_007_add_order_items
  Operations:
    [-] DROP TABLE order_items
  Data Impact: Table and all data will be lost (3,200 rows)
  Reversible: Partially (table recreated empty on re-apply)

WARNINGS
  [!] 2 operations will cause data loss
  [!] Back up affected tables before proceeding

COMMANDS TO EXECUTE
  alembic downgrade -2
  # Or: alembic downgrade migration_006_add_orders_table

Generated Files:
  (No new files — Alembic uses existing downgrade functions)

RECOMMENDED PRE-ROLLBACK STEPS
  1. pg_dump --table=order_items myapp > order_items_backup.sql
  2. pg_dump --table=orders --column-inserts myapp > orders_status_backup.sql
  3. Review downgrade SQL with /db-migrate plan --include-rollback
```

## Important Notes

- Rollback does NOT execute migrations; it generates the plan and/or files
- Always back up data before rolling back destructive migrations
- Some migrations are irreversible (data-only changes without backup)
- Use `--dry-run` to preview without creating any files
- After rollback, verify application compatibility with the older schema
