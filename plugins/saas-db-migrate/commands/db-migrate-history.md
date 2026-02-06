---
name: db-migrate history
description: Display migration history and current state
agent: migration-planner
---

# /db-migrate history - Migration History

## Skills to Load

- skills/orm-detection.md
- skills/visual-header.md

## Visual Output

Display header: `DB-MIGRATE - History`

## Usage

```
/db-migrate history [--limit=<n>] [--status=applied|pending|all] [--verbose]
```

**Arguments:**
- `--limit`: Number of migrations to show (default: 20)
- `--status`: Filter by status (default: all)
- `--verbose`: Show full migration details including SQL operations

## Prerequisites

Run `/db-migrate setup` first. Reads `.db-migrate.json` for tool and configuration.

## Process

### 1. Read Migration Source

Depending on the detected tool:

**Alembic:**
- Read `alembic_version` table for applied migrations
- Scan `alembic/versions/` directory for all migration files
- Cross-reference to determine pending migrations

**Prisma:**
- Read `_prisma_migrations` table for applied migrations
- Scan `prisma/migrations/` directory for all migration directories
- Cross-reference applied vs available

**Raw SQL:**
- Read migration tracking table (if exists) for applied migrations
- Scan migration directory for numbered SQL files
- Determine state from sequence numbers

### 2. Build Timeline

For each migration, determine:
- Migration identifier (revision hash, timestamp, sequence number)
- Description (extracted from filename or metadata)
- Status: Applied, Pending, or Failed
- Applied timestamp (if available from tracking table)
- Author (if available from migration metadata)

### 3. Detect Anomalies

Flag unusual states:
- Out-of-order migrations (gap in sequence)
- Failed migrations that need manual intervention
- Migration files present in directory but not in tracking table
- Entries in tracking table without corresponding files (deleted migrations)

### 4. Display History

Present chronological list with status indicators.

## Output Format

```
+----------------------------------------------------------------------+
|  DB-MIGRATE - History                                                |
+----------------------------------------------------------------------+

Tool: Alembic
Database: PostgreSQL (myapp_production)
Total Migrations: 8 (6 applied, 2 pending)

MIGRATION HISTORY

  #  Status     Timestamp            Description
  -- --------   -------------------- ----------------------------------------
  1  [applied]  2024-01-05 10:30:00  initial_schema
  2  [applied]  2024-01-12 14:15:00  add_users_table
  3  [applied]  2024-01-20 09:45:00  add_products_table
  4  [applied]  2024-02-01 11:00:00  add_orders_table
  5  [applied]  2024-02-15 16:30:00  add_user_roles
  6  [applied]  2024-03-01 08:20:00  add_order_status_column
  7  [pending]  --                   add_order_items_table
  8  [pending]  --                   add_payment_tracking

Current Head: migration_006_add_order_status_column
Pending Count: 2

No anomalies detected.
```

### Verbose Mode

With `--verbose`, each migration expands to show:

```
  4  [applied]  2024-02-01 11:00:00  add_orders_table
     Operations:
       [+] CREATE TABLE orders (id, user_id, total, status, created_at)
       [+] CREATE INDEX ix_orders_user_id
       [+] ADD FOREIGN KEY orders.user_id -> users.id
     Rollback: Available (DROP TABLE orders)
```

## Important Notes

- History reads from both the database tracking table and the filesystem
- If database is unreachable, only filesystem state is shown (no applied timestamps)
- Anomalies like missing files or orphaned tracking entries should be resolved manually
