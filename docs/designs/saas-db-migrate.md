# Design: saas-db-migrate

**Domain:** `saas`
**Target Version:** v9.2.0

## Purpose

Database migration management for SQL databases. Supports Alembic (Python/SQLAlchemy), Prisma (Node.js), and raw SQL migrations. Provides migration generation, validation, rollback planning, and drift detection.

## Target Users

- Backend developers managing database schemas
- Teams using SQLAlchemy/Alembic or Prisma
- Projects needing migration safety checks before deployment

## Commands

| Command | Description |
|---------|-------------|
| `/db-migrate setup` | Setup wizard — detect ORM/migration tool, configure paths |
| `/db-migrate generate` | Generate migration from model diff or description |
| `/db-migrate validate` | Check migration safety (destructive ops, data loss risk, locking) |
| `/db-migrate plan` | Show migration execution plan with rollback strategy |
| `/db-migrate history` | Display migration history and current state |
| `/db-migrate rollback` | Generate rollback migration for a given migration |

## Agent Architecture

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| `migration-planner` | sonnet | default | Migration generation, rollback planning |
| `migration-auditor` | haiku | plan | Read-only safety validation (destructive op detection) |

## Skills

| Skill | Purpose |
|-------|---------|
| `orm-detection` | Detect Alembic vs Prisma vs raw SQL, identify config |
| `migration-safety` | Rules for detecting destructive operations (DROP, ALTER, data loss) |
| `rollback-patterns` | Standard rollback generation patterns per tool |
| `naming-conventions` | Migration file naming and ordering conventions |
| `visual-header` | Standard command output headers |

## MCP Server

**Not required.** Migrations are file-based. Database connectivity is handled by the ORM tool itself, not by Claude.

## Integration Points

| Plugin | Integration |
|--------|-------------|
| projman | Issue labels: `Component/Database`, `Tech/SQLAlchemy`, `Tech/Prisma` |
| saas-api-platform | Schema models shared between API and migration layers |
| code-sentinel | Migration validation as part of security scan |
| data-platform | PostgreSQL tools can inspect live schema for drift detection |

## Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| `claude-md-integration.md` | ~600 |
| Dispatch file (`db-migrate.md`) | ~200 |
| 6 commands (avg) | ~3,600 |
| 2 agents | ~1,200 |
| 5 skills | ~2,000 |
| **Total** | **~7,600** |

## Open Questions

- Should this integrate with data-platform's PostgreSQL MCP server for live schema comparison?
- Support for NoSQL migration tools (Mongoose, etc.)?
