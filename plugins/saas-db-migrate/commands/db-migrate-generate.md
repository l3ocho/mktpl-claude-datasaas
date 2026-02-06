---
name: db-migrate generate
description: Generate migration from model diff
agent: migration-planner
---

# /db-migrate generate - Migration Generator

## Skills to Load

- skills/orm-detection.md
- skills/naming-conventions.md
- skills/visual-header.md

## Visual Output

Display header: `DB-MIGRATE - Generate`

## Usage

```
/db-migrate generate <description> [--auto] [--empty]
```

**Arguments:**
- `<description>`: Short description of the change (e.g., "add_orders_table", "add_email_to_users")
- `--auto`: Auto-detect changes from model diff (Alembic/Prisma only)
- `--empty`: Generate empty migration file for manual editing

## Prerequisites

Run `/db-migrate setup` first. Reads `.db-migrate.json` for tool and configuration.

## Process

### 1. Read Configuration

Load `.db-migrate.json` to determine:
- Migration tool (Alembic, Prisma, raw SQL)
- Migration directory path
- Model directory path (for auto-detection)
- Naming convention

### 2. Detect Schema Changes (--auto mode)

**Alembic:**
- Compare current SQLAlchemy models against database schema
- Identify new tables, dropped tables, added/removed columns, type changes
- Detect index additions/removals, constraint changes
- Generate `upgrade()` and `downgrade()` functions

**Prisma:**
- Run `prisma migrate diff` to compare schema.prisma against database
- Identify model additions, field changes, relation updates
- Generate migration SQL and Prisma migration directory

**Raw SQL:**
- Auto-detection not available; create empty template
- Include commented sections for UP and DOWN operations

### 3. Generate Migration File

Create migration file following the naming convention:

| Tool | Format | Example |
|------|--------|---------|
| Alembic | `{revision}_{description}.py` | `a1b2c3d4_add_orders_table.py` |
| Prisma | `{timestamp}_{description}/migration.sql` | `20240115120000_add_orders_table/migration.sql` |
| Raw SQL | `{sequence}_{description}.sql` | `003_add_orders_table.sql` |

### 4. Include Safety Checks

Every generated migration includes:
- Transaction wrapping (BEGIN/COMMIT or framework equivalent)
- Data preservation warnings for destructive operations
- Rollback function/section (downgrade in Alembic, DOWN in raw SQL)
- Comments explaining each operation

### 5. Validate Generated Migration

Run safety checks from `skills/migration-safety.md` on the generated file before presenting to user.

## Output Format

```
+----------------------------------------------------------------------+
|  DB-MIGRATE - Generate                                               |
+----------------------------------------------------------------------+

Tool: Alembic
Mode: auto-detect
Description: add_orders_table

Changes Detected:
  [+] Table: orders (5 columns)
  [+] Column: orders.user_id (FK -> users.id)
  [+] Index: ix_orders_user_id

Files Created:
  [+] alembic/versions/a1b2c3d4_add_orders_table.py

Migration Preview:
  upgrade():
    - CREATE TABLE orders (id, user_id, total, status, created_at)
    - CREATE INDEX ix_orders_user_id ON orders(user_id)
    - ADD FOREIGN KEY orders.user_id -> users.id

  downgrade():
    - DROP INDEX ix_orders_user_id
    - DROP TABLE orders

Safety Check: PASS (no destructive operations)

Next Steps:
  - Review generated migration file
  - Run /db-migrate validate for safety analysis
  - Run /db-migrate plan to see execution plan
```

## Important Notes

- Auto-detection works best with Alembic and Prisma
- Always review generated migrations before applying
- Destructive operations (DROP, ALTER TYPE) are flagged with warnings
- The `--empty` flag is useful for data migrations that cannot be auto-detected
