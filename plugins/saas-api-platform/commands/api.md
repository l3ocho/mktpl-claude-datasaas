---
name: api
description: API development toolkit — type /api <action> for commands
---

# /api

REST and GraphQL API scaffolding, validation, and documentation for FastAPI and Express.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `setup` | `/saas-api-platform:api-setup` | Setup wizard for saas-api-platform |
| `scaffold` | `/saas-api-platform:api-scaffold` | Generate routes, models, and schemas |
| `validate` | `/saas-api-platform:api-validate` | Validate routes against OpenAPI spec |
| `docs` | `/saas-api-platform:api-docs` | Generate or update OpenAPI specification |
| `test-routes` | `/saas-api-platform:api-test-routes` | Generate test cases for API endpoints |
| `middleware` | `/saas-api-platform:api-middleware` | Add and configure middleware |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/api scaffold`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/saas-api-platform:api-scaffold`)
