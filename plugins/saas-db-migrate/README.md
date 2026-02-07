# saas-db-migrate

Database migration management for Alembic, Prisma, and raw SQL.

## Overview

The saas-db-migrate plugin provides a complete database migration toolkit. It detects your migration tool, generates migration files from model diffs, validates migrations for safety before applying, plans execution with rollback strategies, and tracks migration history.

## Supported Migration Tools

- **Alembic** (Python/SQLAlchemy) - Revision-based migrations with auto-generation
- **Prisma** (Node.js/TypeScript) - Schema-first migrations with diff-based generation
- **Raw SQL** - Sequential numbered SQL files for any database

## Supported Databases

- PostgreSQL (primary, with lock analysis)
- MySQL (with engine-specific considerations)
- SQLite (with ALTER limitations noted)

## Commands

| Command | Description |
|---------|-------------|
| `/db-migrate setup` | Setup wizard - detect tool, map configuration |
| `/db-migrate generate <desc>` | Generate migration from model diff or empty template |
| `/db-migrate validate` | Check migration safety (data loss, locks, rollback) |
| `/db-migrate plan` | Show execution plan with rollback strategy |
| `/db-migrate history` | Display migration history and current state |
| `/db-migrate rollback` | Generate rollback migration or plan |

## Agents

| Agent | Model | Mode | Purpose |
|-------|-------|------|---------|
| `migration-planner` | sonnet | default | Migration generation, planning, rollback |
| `migration-auditor` | haiku | plan (read-only) | Safety validation and risk assessment |

## Installation

This plugin is part of the Leo Claude Marketplace. It is installed automatically when the marketplace is configured.

### Prerequisites

- A project with an existing database and migration tool
- Run `/db-migrate setup` before using other commands

## Configuration

The `/db-migrate setup` command creates `.db-migrate.json` in your project root with detected settings. All subsequent commands read this file for tool and path configuration.

## Safety Philosophy

This plugin prioritizes data safety above all else. Every migration is analyzed for:
- **Data loss risk**: DROP and ALTER operations are flagged prominently
- **Lock duration**: DDL operations are assessed for table lock impact
- **Rollback completeness**: Every upgrade must have a corresponding downgrade
- **Transaction safety**: All operations must be wrapped in transactions
