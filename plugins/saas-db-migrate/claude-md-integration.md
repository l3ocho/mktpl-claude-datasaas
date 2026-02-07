# saas-db-migrate Plugin - CLAUDE.md Integration

Add this section to your project's CLAUDE.md to enable saas-db-migrate plugin features.

## Suggested CLAUDE.md Section

```markdown
## Database Migration Integration

This project uses the saas-db-migrate plugin for database migration workflows.

### Configuration

Run `/db-migrate setup` to auto-detect migration tool and configure paths.
Settings stored in `.db-migrate.json` in project root.

### Available Commands

| Command | Purpose |
|---------|---------|
| `/db-migrate setup` | Detect migration tool and configure |
| `/db-migrate generate <desc>` | Generate migration from model changes |
| `/db-migrate validate` | Check migration for safety issues |
| `/db-migrate plan` | Preview execution plan with rollback |
| `/db-migrate history` | Show migration history and state |
| `/db-migrate rollback` | Generate rollback migration |

### When to Use

- **After model changes**: `/db-migrate generate add_status_to_orders --auto` detects diffs
- **Before applying**: `/db-migrate validate` checks for data loss and lock risks
- **Before deploy**: `/db-migrate plan --include-rollback` shows full execution strategy
- **After issues**: `/db-migrate rollback --steps=1` generates rollback plan
- **Status check**: `/db-migrate history` shows what has been applied

### Safety Rules

- Never apply migrations without running `/db-migrate validate` first
- Always have a rollback plan for production migrations
- Separate schema changes from data migrations
- Use zero-downtime patterns for production (add nullable, backfill, constrain)
```

## Typical Workflows

### New Feature Migration
```
/db-migrate generate add_orders_table --auto
/db-migrate validate
/db-migrate plan
# Apply migration via your tool (alembic upgrade head, prisma migrate deploy)
```

### Pre-Deploy Check
```
/db-migrate validate --all --strict
/db-migrate plan --include-rollback
/db-migrate history --status=pending
```

### Emergency Rollback
```
/db-migrate history
/db-migrate rollback --steps=1 --dry-run
/db-migrate rollback --steps=1
```
