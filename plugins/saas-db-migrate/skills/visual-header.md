---
name: visual-header
description: Standard header format for db-migrate commands and agents
---

# Visual Header

## Standard Format

Display at the start of every command execution:

```
+----------------------------------------------------------------------+
|  DB-MIGRATE - [Command Name]                                         |
+----------------------------------------------------------------------+
```

## Command Headers

| Command | Header Text |
|---------|-------------|
| db-migrate-setup | Setup Wizard |
| db-migrate-generate | Generate |
| db-migrate-validate | Validate |
| db-migrate-plan | Plan |
| db-migrate-history | History |
| db-migrate-rollback | Rollback |

## Summary Box Format

For completion summaries:

```
+============================================================+
|            DB-MIGRATE [OPERATION] COMPLETE                  |
+============================================================+
| Component:         [Status]                                |
| Component:         [Status]                                |
+============================================================+
```

## Status Indicators

- Success: `[check]` or `Ready`
- Warning: `[!]` or `Partial`
- Failure: `[X]` or `Failed`
- New file: `[+]`
- Modified file: `[~]`
- Deleted file: `[-]`

## Risk Level Indicators

- LOW: Safe operation, no data loss risk
- MEDIUM: Reversible but requires attention
- HIGH: Potential data loss, backup required
- CRITICAL: Irreversible data loss, explicit approval required
