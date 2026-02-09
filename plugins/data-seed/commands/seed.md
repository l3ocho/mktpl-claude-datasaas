---
name: seed
description: Test data generation — type /seed <action> for commands
---

# /seed

Test data generation and database seeding with reproducible profiles.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `setup` | `/data-seed:seed-setup` | Setup wizard for data-seed configuration |
| `generate` | `/data-seed:seed-generate` | Generate seed data from schema or models |
| `apply` | `/data-seed:seed-apply` | Apply seed data to database or create fixture files |
| `profile` | `/data-seed:seed-profile` | Define reusable data profiles (small, medium, large) |
| `validate` | `/data-seed:seed-validate` | Validate seed data against schema constraints |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/seed generate`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/data-seed:seed-generate`)
