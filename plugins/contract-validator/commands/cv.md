---
name: cv
description: Cross-plugin compatibility validation — type /cv <action> for commands
---

# /cv

Cross-plugin compatibility validation and agent verification.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|-------------|-------------|
| `/cv validate` | Full marketplace compatibility validation |
| `/cv check-agent` | Validate single agent definition |
| `/cv list-interfaces` | Show all plugin interfaces |
| `/cv dependency-graph` | Mermaid visualization of plugin dependencies |
| `/cv setup` | Setup wizard for contract-validator MCP |
| `/cv status` | Marketplace-wide health check |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
