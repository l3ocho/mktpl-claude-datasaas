---
name: seed setup
---

# /seed setup - Data Seed Setup Wizard

## Skills to Load
- skills/schema-inference.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-SEED - Setup Wizard`

## Usage

```
/seed setup
```

## Workflow

### Phase 1: Environment Detection
- Detect project type: Python (SQLAlchemy, Django ORM), Node.js (Prisma, TypeORM), or raw SQL
- Check for existing schema files: `schema.prisma`, `models.py`, `*.sql` DDL files
- Identify package manager and installed ORM libraries

### Phase 2: Schema Source Configuration
- Ask user to confirm detected schema source or specify manually
- Supported sources:
  - SQLAlchemy models (`models.py`, `models/` directory)
  - Prisma schema (`prisma/schema.prisma`)
  - Django models (`models.py` with Django imports)
  - Raw SQL DDL files (`*.sql` with CREATE TABLE statements)
  - JSON Schema definitions (`*.schema.json`)
- Store schema source path for future commands

### Phase 3: Output Configuration
- Ask preferred output format: SQL inserts, JSON fixtures, CSV files, or ORM factory objects
- Ask preferred output directory (default: `seeds/` or `fixtures/`)
- Ask default locale for faker data (default: `en_US`)

### Phase 4: Profile Initialization
- Create default profiles if none exist:
  - `small` — 10 rows per table, minimal relationships
  - `medium` — 100 rows per table, realistic relationships
  - `large` — 1000 rows per table, stress-test volume
- Store profiles in `seed-profiles.json` in output directory

### Phase 5: Validation
- Verify schema can be parsed from detected source
- Display summary with detected tables, column counts, and relationship map
- Inform user of available commands

## Important Notes

- Uses Bash, Read, Write, AskUserQuestion tools
- Does not require database connection (schema-first approach)
- Profile definitions are portable across environments
