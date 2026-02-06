# data-seed Plugin

Test data generation and database seeding with reproducible profiles for Claude Code.

## Overview

The data-seed plugin generates realistic test data from schema definitions. It supports multiple ORM dialects (SQLAlchemy, Prisma, Django ORM, raw SQL DDL), handles foreign key dependencies automatically, and produces output in SQL, JSON, or CSV formats.

Key features:
- **Schema-first**: Parses your existing schema — no manual configuration needed
- **Realistic data**: Locale-aware faker providers for names, emails, addresses, and more
- **Reproducible**: Deterministic generation from seed profiles
- **Dependency-aware**: Resolves FK relationships and generates in correct insertion order
- **Profile-based**: Reusable profiles for small (unit tests), medium (development), and large (stress tests)

## Installation

This plugin is part of the Leo Claude Marketplace. Install via the marketplace or copy the `plugins/data-seed/` directory to your Claude Code plugins path.

## Commands

| Command | Description |
|---------|-------------|
| `/seed setup` | Setup wizard — detect schema source, configure output format |
| `/seed generate` | Generate seed data from schema or models |
| `/seed apply` | Apply seed data to database or create fixture files |
| `/seed profile` | Define and manage reusable data profiles |
| `/seed validate` | Validate seed data against schema constraints |

## Quick Start

```
/seed setup                    # Detect schema, configure output
/seed generate                 # Generate data with medium profile
/seed validate                 # Verify generated data integrity
/seed apply                    # Write fixture files
```

## Agents

| Agent | Model | Role |
|-------|-------|------|
| `seed-generator` | Sonnet | Data generation, profile management, and seed application |
| `seed-validator` | Haiku | Read-only validation of seed data integrity |

## Skills

| Skill | Purpose |
|-------|---------|
| `schema-inference` | Parse ORM models and SQL DDL into normalized schema |
| `faker-patterns` | Map columns to realistic faker providers |
| `relationship-resolution` | FK dependency ordering and circular dependency handling |
| `profile-management` | Seed profile CRUD and configuration |
| `visual-header` | Standard visual output formatting |

## Supported Schema Sources

- SQLAlchemy models (2.0+ and legacy 1.x)
- Prisma schema
- Django ORM models
- Raw SQL DDL (CREATE TABLE statements)
- JSON Schema definitions

## Output Formats

- SQL INSERT statements
- JSON fixtures (Django-compatible)
- CSV files
- Prisma seed scripts
- Python factory objects

## License

MIT License — Part of the Leo Claude Marketplace.
