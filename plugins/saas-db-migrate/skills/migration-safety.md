---
name: migration-safety
description: Rules for detecting destructive operations, data loss risks, and long-running locks
---

# Migration Safety

## Purpose

Defines safety rules for analyzing database migrations. This skill is loaded by both the `migration-planner` (during generation) and `migration-auditor` (during validation) agents to ensure migrations do not cause data loss or operational issues.

---

## Destructive Operations

### FAIL-Level (Block Migration)

| Operation | Risk | Detection Pattern |
|-----------|------|-------------------|
| `DROP TABLE` | Complete data loss | `DROP TABLE` without preceding backup/export |
| `DROP COLUMN` | Column data loss | `DROP COLUMN` without verification step |
| `ALTER COLUMN` type narrowing | Data truncation | VARCHAR(N) to smaller N, INTEGER to SMALLINT |
| `ALTER COLUMN` SET NOT NULL | Failure if NULLs exist | `SET NOT NULL` without DEFAULT or backfill |
| `TRUNCATE TABLE` | All rows deleted | `TRUNCATE` in migration file |
| `DELETE FROM` without WHERE | All rows deleted | `DELETE FROM table` without WHERE clause |
| Missing transaction | Partial migration risk | DDL statements outside BEGIN/COMMIT |

### WARN-Level (Report, Continue)

| Operation | Risk | Detection Pattern |
|-----------|------|-------------------|
| `RENAME TABLE` | App code must update | `ALTER TABLE ... RENAME TO` |
| `RENAME COLUMN` | App code must update | `ALTER TABLE ... RENAME COLUMN` |
| `ALTER COLUMN` type widening | Usually safe but verify | INTEGER to BIGINT, VARCHAR to TEXT |
| `CREATE INDEX` (non-concurrent) | Table lock during build | `CREATE INDEX` without `CONCURRENTLY` |
| Large table ALTER | Extended lock time | Any ALTER on tables with 100K+ rows |
| Mixed schema + data migration | Complex rollback | DML and DDL in same migration file |
| Missing downgrade/rollback | Cannot undo | No downgrade function or DOWN section |

### INFO-Level (Suggestions)

| Operation | Suggestion | Detection Pattern |
|-----------|-----------|-------------------|
| No-op migration | Remove or document why | Empty upgrade function |
| Missing IF EXISTS/IF NOT EXISTS | Add for idempotency | `CREATE TABLE` without `IF NOT EXISTS` |
| Non-concurrent index on PostgreSQL | Use CONCURRENTLY | `CREATE INDEX` could be `CREATE INDEX CONCURRENTLY` |

---

## Lock Duration Rules

### PostgreSQL

| Operation | Lock Type | Duration |
|-----------|-----------|----------|
| ADD COLUMN (no default) | ACCESS EXCLUSIVE | Instant (metadata only) |
| ADD COLUMN with DEFAULT | ACCESS EXCLUSIVE | Instant (PG 11+) |
| ALTER COLUMN TYPE | ACCESS EXCLUSIVE | Full table rewrite |
| DROP COLUMN | ACCESS EXCLUSIVE | Instant (metadata only) |
| CREATE INDEX | SHARE | Proportional to table size |
| CREATE INDEX CONCURRENTLY | SHARE UPDATE EXCLUSIVE | Longer but non-blocking |
| ADD CONSTRAINT (CHECK) | ACCESS EXCLUSIVE | Scans entire table |
| ADD CONSTRAINT NOT VALID + VALIDATE | Split: instant + non-blocking | Recommended for large tables |

### MySQL

| Operation | Lock Type | Duration |
|-----------|-----------|----------|
| Most ALTER TABLE | Table copy | Proportional to table size |
| ADD COLUMN (last position) | Instant (8.0+ some cases) | Depends on engine |
| CREATE INDEX | Table copy or instant | Engine-dependent |

---

## Recommended Patterns

### Safe Column Addition
```sql
-- Good: nullable column, no lock
ALTER TABLE users ADD COLUMN middle_name VARCHAR(100);

-- Then backfill in batches (separate migration):
UPDATE users SET middle_name = '' WHERE middle_name IS NULL;

-- Then add constraint (separate migration):
ALTER TABLE users ALTER COLUMN middle_name SET NOT NULL;
```

### Safe Column Removal
```sql
-- Step 1: Remove from application code first
-- Step 2: Verify column is unused (no queries reference it)
-- Step 3: Drop in migration
ALTER TABLE users DROP COLUMN IF EXISTS legacy_field;
```

### Safe Type Change
```sql
-- Step 1: Add new column
ALTER TABLE orders ADD COLUMN amount_new NUMERIC(10,2);
-- Step 2: Backfill (separate migration)
UPDATE orders SET amount_new = amount::NUMERIC(10,2);
-- Step 3: Swap columns (separate migration)
ALTER TABLE orders DROP COLUMN amount;
ALTER TABLE orders RENAME COLUMN amount_new TO amount;
```

---

## Pre-Migration Checklist

Before applying any migration in production:

1. Database backup completed and verified
2. Migration validated with `/db-migrate validate`
3. Execution plan reviewed with `/db-migrate plan`
4. Rollback strategy documented and tested
5. Maintenance window scheduled (if required by lock analysis)
6. Application deployment coordinated (if schema change affects code)
