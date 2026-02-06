# Design: data-seed

**Domain:** `data`
**Target Version:** v9.3.0

## Purpose

Test data generation and database seeding. Generates realistic fake data based on schema definitions, supports reproducible seeds, and manages seed files for development and testing environments.

## Target Users

- Developers needing test data for local development
- QA teams requiring reproducible datasets
- Projects with complex relational data models

## Commands

| Command | Description |
|---------|-------------|
| `/seed setup` | Setup wizard — detect schema source, configure output paths |
| `/seed generate` | Generate seed data from schema or model definitions |
| `/seed apply` | Apply seed data to database or create fixture files |
| `/seed profile` | Define reusable data profiles (small, medium, large, edge-cases) |
| `/seed validate` | Validate seed data against schema constraints and foreign keys |

## Agent Architecture

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| `seed-generator` | sonnet | acceptEdits | Data generation, profile management |
| `seed-validator` | haiku | plan | Read-only validation of seed data integrity |

## Skills

| Skill | Purpose |
|-------|---------|
| `schema-inference` | Infer data types and constraints from models/migrations |
| `faker-patterns` | Realistic data generation patterns (names, emails, addresses, etc.) |
| `relationship-resolution` | Foreign key and relationship-aware data generation |
| `profile-management` | Seed profile definitions and sizing |
| `visual-header` | Standard command output headers |

## MCP Server

**Not required.** Seed data is generated as files (JSON, SQL, CSV). Database insertion is handled by the application's own tooling.

## Integration Points

| Plugin | Integration |
|--------|-------------|
| saas-db-migrate | Schema models used as seed generation input |
| data-platform | Generated data can be loaded via `/data ingest` |
| saas-test-pilot | Seed data used in integration test fixtures |
| projman | Issue labels: `Component/Data`, `Tech/Faker` |

## Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| `claude-md-integration.md` | ~500 |
| Dispatch file (`seed.md`) | ~200 |
| 5 commands (avg) | ~3,000 |
| 2 agents | ~1,000 |
| 5 skills | ~2,000 |
| **Total** | **~6,700** |

## Open Questions

- Should we support database-specific seed formats (pg_dump, mysqldump)?
- Integration with Faker library or custom generation?
