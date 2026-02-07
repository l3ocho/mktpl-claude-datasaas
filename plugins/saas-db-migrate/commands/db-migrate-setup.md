---
name: db-migrate setup
description: Setup wizard for migration tool detection and configuration
agent: migration-planner
---

# /db-migrate setup - Migration Platform Setup Wizard

## Skills to Load

- skills/orm-detection.md
- skills/visual-header.md

## Visual Output

Display header: `DB-MIGRATE - Setup Wizard`

## Usage

```
/db-migrate setup
```

## Workflow

### Phase 1: Migration Tool Detection

Scan the project for migration tool indicators:

| File / Pattern | Tool | Confidence |
|----------------|------|------------|
| `alembic.ini` in project root | Alembic | High |
| `alembic/` directory | Alembic | High |
| `sqlalchemy` in requirements | Alembic (likely) | Medium |
| `prisma/schema.prisma` | Prisma | High |
| `@prisma/client` in package.json | Prisma | High |
| `migrations/` with numbered `.sql` files | Raw SQL | Medium |
| `flyway.conf` | Flyway (raw SQL) | High |
| `knexfile.js` or `knexfile.ts` | Knex | High |

If no tool detected, ask user to select one.

### Phase 2: Configuration Mapping

Identify existing migration configuration:

- **Migration directory**: Where migration files live
- **Model directory**: Where ORM models are defined (for auto-generation)
- **Database URL**: Connection string location (env var, config file)
- **Naming convention**: How migration files are named
- **Current state**: Latest applied migration

### Phase 3: Database Connection Test

Attempt to verify database connectivity:

- Read connection string from detected location
- Test connection (read-only)
- Report database type (PostgreSQL, MySQL, SQLite)
- Report current schema version if detectable

### Phase 4: Validation

Display detected configuration summary and ask for confirmation.

## Output Format

```
+----------------------------------------------------------------------+
|  DB-MIGRATE - Setup Wizard                                           |
+----------------------------------------------------------------------+

Migration Tool:  Alembic 1.13.1
ORM:            SQLAlchemy 2.0.25
Database:       PostgreSQL 16.1
Migration Dir:  ./alembic/versions/
Model Dir:      ./app/models/
DB URL Source:   DATABASE_URL env var

Current State:
  Latest Migration: 2024_01_15_add_orders_table (applied)
  Pending:          0 migrations

Configuration saved to .db-migrate.json
```

## Important Notes

- This command does NOT run any migrations; it only detects and configures
- Database connection test is read-only (SELECT 1)
- If `.db-migrate.json` already exists, offer to update or keep
- All subsequent commands rely on this configuration
