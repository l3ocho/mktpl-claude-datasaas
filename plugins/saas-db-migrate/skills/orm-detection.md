---
name: orm-detection
description: Detect Alembic, Prisma, or raw SQL migration tools and locate configuration files
---

# ORM Detection

## Purpose

Identify the database migration tool in use and map its configuration. This skill is loaded by the `migration-planner` agent during setup and migration generation to ensure tool-appropriate output.

---

## Detection Rules

### Alembic Detection

| Indicator | Location | Confidence |
|-----------|----------|------------|
| `alembic.ini` file | Project root | High |
| `alembic/` directory with `env.py` | Project root | High |
| `alembic/versions/` directory | Within alembic dir | High |
| `sqlalchemy` + `alembic` in requirements | `requirements.txt`, `pyproject.toml` | Medium |
| `from alembic import op` in Python files | `*.py` in versions dir | High |

**Alembic Configuration Files:**
- `alembic.ini` — Main config (database URL, migration directory)
- `alembic/env.py` — Migration environment (model imports, target metadata)
- `alembic/versions/` — Migration files directory

**Model Location:**
- Look for `Base = declarative_base()` or `class Base(DeclarativeBase)` in Python files
- Check `target_metadata` in `env.py` to find the models module
- Common locations: `app/models/`, `models/`, `src/models/`

### Prisma Detection

| Indicator | Location | Confidence |
|-----------|----------|------------|
| `prisma/schema.prisma` file | Project root | High |
| `@prisma/client` in package.json | `package.json` | High |
| `prisma/migrations/` directory | Within prisma dir | High |
| `npx prisma` in scripts | `package.json` scripts | Medium |

**Prisma Configuration Files:**
- `prisma/schema.prisma` — Schema definition (models, datasource, generator)
- `prisma/migrations/` — Migration directories (timestamp-named)
- `.env` — `DATABASE_URL` connection string

### Raw SQL Detection

| Indicator | Location | Confidence |
|-----------|----------|------------|
| `migrations/` dir with numbered `.sql` files | Project root | Medium |
| `flyway.conf` | Project root | High (Flyway) |
| `knexfile.js` or `knexfile.ts` | Project root | High (Knex) |
| `db/migrate/` directory | Project root | Medium (Rails-style) |

**Raw SQL Configuration:**
- Migration directory location
- Naming pattern (sequential numbers, timestamps)
- Tracking table name (if database-tracked)

---

## Database Connection Detection

Look for connection strings in this order:

1. `DATABASE_URL` environment variable
2. `.env` file in project root
3. `alembic.ini` `sqlalchemy.url` setting
4. `prisma/schema.prisma` `datasource` block
5. Application config files (`config.py`, `config.js`, `settings.py`)

**Database Type Detection:**
- `postgresql://` or `postgres://` — PostgreSQL
- `mysql://` — MySQL
- `sqlite:///` — SQLite
- `mongodb://` — MongoDB (not supported for SQL migrations)

---

## Version Detection

**Alembic**: Parse from `pip show alembic` or `requirements.txt` pin
**Prisma**: Parse from `package.json` `@prisma/client` version
**SQLAlchemy**: Parse from requirements; important for feature compatibility (1.4 vs 2.0 API)

---

## Ambiguous Projects

If multiple migration tools are detected (e.g., Alembic for backend + Prisma for a separate service), ask the user which one to target. Store selection in `.db-migrate.json`.
