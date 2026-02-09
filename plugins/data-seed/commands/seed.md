---
name: seed
description: Test data generation — type /seed <action> for commands
---

# /seed

Test data generation and database seeding with reproducible profiles.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|-------------|-------------|
| `/seed setup` | Setup wizard for data-seed configuration |
| `/seed generate` | Generate seed data from schema or models |
| `/seed apply` | Apply seed data to database or create fixture files |
| `/seed profile` | Define reusable data profiles (small, medium, large) |
| `/seed validate` | Validate seed data against schema constraints |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
