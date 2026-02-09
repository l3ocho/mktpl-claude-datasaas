---
name: db-migrate
description: Database migration toolkit — type /db-migrate <action> for commands
---

# /db-migrate

Database migration management for Alembic, Prisma, and raw SQL.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/db-migrate setup` | Setup wizard for migration tool detection |
| `/db-migrate generate` | Generate migration from model diff |
| `/db-migrate validate` | Check migration safety |
| `/db-migrate plan` | Show execution plan with rollback strategy |
| `/db-migrate history` | Display migration history |
| `/db-migrate rollback` | Generate rollback migration |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
