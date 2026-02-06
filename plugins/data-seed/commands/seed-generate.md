---
name: seed generate
---

# /seed generate - Generate Seed Data

## Skills to Load
- skills/schema-inference.md
- skills/faker-patterns.md
- skills/relationship-resolution.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-SEED - Generate`

## Usage

```
/seed generate [table_name] [--profile <name>] [--rows <count>] [--format <sql|json|csv>] [--locale <locale>]
```

## Workflow

### 1. Parse Schema
- Load schema from configured source (see `/seed setup`)
- Extract tables, columns, types, constraints, and relationships
- Use `skills/schema-inference.md` to normalize types across ORM dialects

### 2. Resolve Generation Order
- Build dependency graph from foreign key relationships
- Use `skills/relationship-resolution.md` to determine insertion order
- Handle circular dependencies via deferred constraint resolution
- If specific `table_name` provided, generate only that table plus its dependencies

### 3. Select Profile
- Load profile from `seed-profiles.json` (default: `medium`)
- Override row count if `--rows` specified
- Apply profile-specific edge case ratios and custom value overrides

### 4. Generate Data
- For each table in dependency order:
  - Map column types to faker providers using `skills/faker-patterns.md`
  - Respect NOT NULL constraints (never generate null for required fields)
  - Respect UNIQUE constraints (track generated values, retry on collision)
  - Generate foreign key values from previously generated parent rows
  - Apply locale-specific patterns for names, addresses, phone numbers
  - Handle enum/check constraints by selecting from valid values only
  - Include edge cases per profile settings (empty strings, boundary values, unicode)

### 5. Output Results
- Write generated data in requested format to configured output directory
- Display summary: tables generated, row counts, file paths
- Report any constraint violations or generation warnings

## Examples

```
/seed generate                          # All tables, medium profile
/seed generate users                    # Only users table + dependencies
/seed generate --profile large          # All tables, 1000 rows each
/seed generate orders --rows 50         # 50 order rows
/seed generate --format json            # Output as JSON fixtures
/seed generate --locale pt_BR           # Brazilian Portuguese data
```

## Edge Cases

- Self-referential foreign keys (e.g., `manager_id` on `employees`): generate root rows first, then assign managers from existing rows
- Many-to-many through tables: generate both sides first, then populate junction table
- Nullable foreign keys: generate null values at the profile's configured null ratio
