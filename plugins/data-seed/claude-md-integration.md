# data-seed Plugin - CLAUDE.md Integration

Add this section to your project's CLAUDE.md to enable data-seed plugin features.

## Suggested CLAUDE.md Section

```markdown
## Test Data Generation (data-seed)

This project uses the data-seed plugin for test data generation and database seeding.

### Configuration

**Schema Source**: Auto-detected from project ORM (SQLAlchemy, Prisma, Django, raw SQL)
**Output Directory**: `seeds/` or `fixtures/` (configurable via `/seed setup`)
**Profiles**: `seed-profiles.json` in output directory

### Available Commands

| Command | Purpose |
|---------|---------|
| `/seed setup` | Configure schema source and output format |
| `/seed generate` | Generate test data from schema |
| `/seed apply` | Apply seed data to database or fixture files |
| `/seed profile` | Manage data profiles (small, medium, large) |
| `/seed validate` | Validate seed data against schema constraints |

### Data Profiles

| Profile | Rows/Table | Edge Cases | Use Case |
|---------|------------|------------|----------|
| `small` | 10 | None | Unit tests |
| `medium` | 100 | 10% | Development |
| `large` | 1000 | 5% | Performance testing |

### Typical Workflow

```
/seed setup                          # First-time configuration
/seed generate --profile medium      # Generate development data
/seed validate                       # Verify integrity
/seed apply --target file            # Write fixture files
```

### Custom Profiles

Create custom profiles for project-specific needs:
```
/seed profile create staging
```

Override row counts per table and set custom value pools for enum columns.
```

## Environment Variables

Add to project `.env` if needed:

```env
# Seed data configuration
SEED_OUTPUT_DIR=./seeds
SEED_DEFAULT_PROFILE=medium
SEED_DEFAULT_LOCALE=en_US
```

## Typical Workflows

### Initial Setup
```
/seed setup                          # Detect schema, configure output
/seed generate                       # Generate with default profile
/seed validate                       # Verify data integrity
```

### CI/CD Integration
```
/seed generate --profile small       # Fast, minimal data for tests
/seed apply --target file            # Write fixtures
# Run test suite with fixtures
```

### Development Environment
```
/seed generate --profile medium      # Realistic development data
/seed apply --target database --clean  # Clean and seed database
```

### Performance Testing
```
/seed generate --profile large       # High-volume data
/seed apply --target database        # Load into test database
# Run performance benchmarks
```
