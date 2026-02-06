---
name: rollback-patterns
description: Standard rollback generation patterns, reverse operations, and data backup strategies
---

# Rollback Patterns

## Purpose

Defines patterns for generating safe rollback migrations. This skill is loaded by the `migration-planner` agent when generating migrations (to include downgrade sections) and when creating explicit rollback plans.

---

## Reverse Operation Map

| Forward Operation | Reverse Operation | Data Preserved |
|-------------------|-------------------|----------------|
| CREATE TABLE | DROP TABLE | No (all data lost) |
| DROP TABLE | CREATE TABLE (empty) | No (must restore from backup) |
| ADD COLUMN | DROP COLUMN | No (column data lost) |
| DROP COLUMN | ADD COLUMN (nullable) | No (must restore from backup) |
| RENAME TABLE | RENAME TABLE (back) | Yes |
| RENAME COLUMN | RENAME COLUMN (back) | Yes |
| ADD INDEX | DROP INDEX | Yes (data unaffected) |
| DROP INDEX | CREATE INDEX | Yes (data unaffected) |
| ADD CONSTRAINT | DROP CONSTRAINT | Yes |
| DROP CONSTRAINT | ADD CONSTRAINT | Yes (if data still valid) |
| ALTER COLUMN TYPE | ALTER COLUMN TYPE (back) | Depends on conversion |
| INSERT rows | DELETE matching rows | Yes (if identifiable) |
| UPDATE rows | UPDATE with original values | Only if originals saved |
| DELETE rows | INSERT saved rows | Only if backed up |

---

## Rollback Classification

### Fully Reversible (Green)

Operations that can be undone with no data loss:
- RENAME operations (table, column)
- ADD/DROP INDEX
- ADD/DROP CONSTRAINT (when data satisfies constraint)
- ADD COLUMN (drop it in rollback)

### Partially Reversible (Yellow)

Operations where structure is restored but data is lost:
- CREATE TABLE (rollback = DROP TABLE; data lost)
- DROP COLUMN (rollback = ADD COLUMN; column data gone)
- ALTER COLUMN TYPE narrowing then widening (precision lost)

### Irreversible (Red)

Operations that cannot be meaningfully undone:
- DROP TABLE without backup (data permanently gone)
- TRUNCATE TABLE without backup
- DELETE without WHERE without backup
- Data transformation that loses information (e.g., hash, round)

---

## Backup Strategies

### Pre-Migration Table Backup

For migrations that will cause data loss, generate backup commands:

**PostgreSQL:**
```sql
-- Full table backup
CREATE TABLE _backup_users_20240115 AS SELECT * FROM users;

-- Column-only backup
CREATE TABLE _backup_users_email_20240115 AS
  SELECT id, legacy_email FROM users;
```

**Export to file:**
```bash
pg_dump --table=users --column-inserts dbname > users_backup_20240115.sql
```

### Restoration Commands

Include restoration commands in rollback section:

```sql
-- Restore from backup table
INSERT INTO users (id, legacy_email)
  SELECT id, legacy_email FROM _backup_users_email_20240115;

-- Clean up backup
DROP TABLE IF EXISTS _backup_users_email_20240115;
```

---

## Alembic Downgrade Patterns

```python
def downgrade():
    # Reverse of upgrade, in opposite order
    op.drop_index('ix_orders_user_id', table_name='orders')
    op.drop_table('orders')
```

For complex downgrades with data restoration:
```python
def downgrade():
    # Re-create dropped column
    op.add_column('users', sa.Column('legacy_email', sa.String(255), nullable=True))
    # Note: Data cannot be restored automatically
    # Restore from backup: _backup_users_email_YYYYMMDD
```

---

## Prisma Rollback Patterns

Prisma does not have native downgrade support. Generate a new migration that reverses the operations:

```sql
-- Rollback: undo add_orders_table
DROP TABLE IF EXISTS "order_items";
DROP TABLE IF EXISTS "orders";
```

---

## Raw SQL Rollback Patterns

Always include DOWN section in migration files:

```sql
-- UP
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10,2) NOT NULL
);

-- DOWN
DROP TABLE IF EXISTS orders;
```

---

## Point-of-No-Return Identification

Flag migrations that cross the point of no return:

1. **Data deletion without backup step**: Mark as irreversible
2. **Type narrowing that truncates data**: Data is permanently altered
3. **Hash/encrypt transformations**: Original values unrecoverable
4. **Aggregate/merge operations**: Individual records lost

When a migration includes irreversible operations, the rollback section must clearly state: "This migration cannot be fully rolled back. Data backup is required before applying."
