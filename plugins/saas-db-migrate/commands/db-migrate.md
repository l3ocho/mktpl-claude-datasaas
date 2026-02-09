---
name: db-migrate
description: Database migration toolkit — type /db-migrate <action> for commands
---

# /db-migrate

Database migration management for Alembic, Prisma, and raw SQL.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `setup` | `/saas-db-migrate:db-migrate-setup` | Setup wizard for migration tool detection |
| `generate` | `/saas-db-migrate:db-migrate-generate` | Generate migration from model diff |
| `validate` | `/saas-db-migrate:db-migrate-validate` | Check migration safety |
| `plan` | `/saas-db-migrate:db-migrate-plan` | Show execution plan with rollback strategy |
| `history` | `/saas-db-migrate:db-migrate-history` | Display migration history |
| `rollback` | `/saas-db-migrate:db-migrate-rollback` | Generate rollback migration |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/db-migrate generate`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/saas-db-migrate:db-migrate-generate`)
