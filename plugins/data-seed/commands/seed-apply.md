---
name: seed apply
---

# /seed apply - Apply Seed Data

## Skills to Load
- skills/profile-management.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-SEED - Apply`

## Usage

```
/seed apply [--profile <name>] [--target <database|file>] [--clean] [--dry-run]
```

## Workflow

### 1. Locate Seed Data
- Look for generated seed files in configured output directory
- If no seed data found, prompt user to run `/seed generate` first
- Display available seed datasets with timestamps and profiles

### 2. Determine Target
- `--target database`: Apply directly to connected database via SQL execution
- `--target file` (default): Write fixture files for framework consumption
- Auto-detect framework for file output:
  - Django: `fixtures/` directory as JSON fixtures compatible with `loaddata`
  - SQLAlchemy: Python factory files or SQL insert scripts
  - Prisma: `prisma/seed.ts` compatible format
  - Generic: SQL insert statements or CSV files

### 3. Pre-Apply Validation
- If targeting database: verify connection, check table existence
- If `--clean` specified: generate TRUNCATE/DELETE statements for affected tables (respecting FK order)
- Display execution plan showing table order, row counts, and clean operations
- If `--dry-run`: display plan and exit without applying

### 4. Apply Data
- Execute in dependency order (parents before children)
- If targeting database: wrap in transaction, rollback on error
- If targeting files: write all files atomically
- Track progress: display per-table status during application

### 5. Post-Apply Summary
- Report rows inserted per table
- Report any errors or skipped rows
- Display total execution time
- If database target: verify row counts match expectations

## Examples

```
/seed apply                              # Write fixture files (default)
/seed apply --target database            # Insert directly into database
/seed apply --profile small --clean      # Clean + apply small dataset
/seed apply --dry-run                    # Preview without applying
/seed apply --target database --clean    # Truncate then seed database
```

## Safety

- Database operations always use transactions
- `--clean` requires explicit confirmation before executing TRUNCATE
- Never drops tables or modifies schema — seed data only
- `--dry-run` is always safe and produces no side effects
