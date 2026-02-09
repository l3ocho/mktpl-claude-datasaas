---
name: api
description: API development toolkit — type /api <action> for commands
---

# /api

REST and GraphQL API scaffolding, validation, and documentation for FastAPI and Express.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/api setup` | Setup wizard for saas-api-platform |
| `/api scaffold` | Generate routes, models, and schemas |
| `/api validate` | Validate routes against OpenAPI spec |
| `/api docs` | Generate or update OpenAPI specification |
| `/api test-routes` | Generate test cases for API endpoints |
| `/api middleware` | Add and configure middleware |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
