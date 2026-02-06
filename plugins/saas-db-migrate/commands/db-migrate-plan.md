---
name: db-migrate plan
description: Show execution plan with rollback strategy
agent: migration-planner
---

# /db-migrate plan - Migration Execution Plan

## Skills to Load

- skills/rollback-patterns.md
- skills/migration-safety.md
- skills/visual-header.md

## Visual Output

Display header: `DB-MIGRATE - Plan`

## Usage

```
/db-migrate plan [--target=<migration>] [--include-rollback]
```

**Arguments:**
- `--target`: Plan up to specific migration (default: all pending)
- `--include-rollback`: Show rollback plan alongside forward plan

## Prerequisites

Run `/db-migrate setup` first. Pending migrations must exist.

## Process

### 1. Determine Current State

Query the migration history to find:
- Latest applied migration
- All pending (unapplied) migrations in order
- Any out-of-order migrations (applied but not contiguous)

### 2. Build Forward Plan

For each pending migration, document:
- Migration identifier and description
- SQL operations that will execute (summarized)
- Estimated lock duration for ALTER operations
- Dependencies on previous migrations
- Expected outcome (tables/columns affected)

### 3. Build Rollback Plan (if --include-rollback)

For each migration in reverse order, document:
- Rollback/downgrade operations
- Data recovery strategy (if destructive operations present)
- Point-of-no-return warnings (migrations that cannot be fully rolled back)
- Recommended backup steps before applying

### 4. Risk Assessment

Evaluate the complete plan:
- Total number of operations
- Presence of destructive operations (DROP, ALTER TYPE)
- Estimated total lock time
- Data migration volume (if data changes included)
- Recommended maintenance window duration

### 5. Present Plan

Display ordered execution plan with risk indicators.

## Output Format

```
+----------------------------------------------------------------------+
|  DB-MIGRATE - Plan                                                   |
+----------------------------------------------------------------------+

Current State: migration_005_add_user_roles (applied)
Pending: 3 migrations

FORWARD PLAN

Step 1: migration_006_add_orders_table
  Operations:
    [+] CREATE TABLE orders (5 columns)
    [+] CREATE INDEX ix_orders_user_id
    [+] ADD FOREIGN KEY orders.user_id -> users.id
  Lock Impact: None (new table)
  Risk: LOW

Step 2: migration_007_add_order_items
  Operations:
    [+] CREATE TABLE order_items (4 columns)
    [+] CREATE INDEX ix_order_items_order_id
  Lock Impact: None (new table)
  Risk: LOW

Step 3: migration_008_add_status_to_orders
  Operations:
    [~] ADD COLUMN orders.status VARCHAR(20) DEFAULT 'pending'
    [~] ADD CHECK CONSTRAINT valid_status
  Lock Impact: ~2s (instant ADD COLUMN with DEFAULT in PostgreSQL 11+)
  Risk: LOW

ROLLBACK PLAN

Step 3 (reverse): Undo migration_008
  [~] DROP CONSTRAINT valid_status
  [~] DROP COLUMN orders.status
  Reversible: YES

Step 2 (reverse): Undo migration_007
  [-] DROP TABLE order_items
  Reversible: YES (but data is lost)

Step 1 (reverse): Undo migration_006
  [-] DROP TABLE orders
  Reversible: YES (but data is lost)

RISK SUMMARY
  Total Operations: 9
  Destructive:      0
  Lock Time:        ~2 seconds
  Risk Level:       LOW
  Maintenance Window: Not required

RECOMMENDATION: Safe to apply without maintenance window.
```

## Important Notes

- The plan is informational; it does not apply any migrations
- Lock time estimates are approximate and depend on table size
- Always back up the database before applying destructive migrations
- Out-of-order migrations are flagged as warnings
