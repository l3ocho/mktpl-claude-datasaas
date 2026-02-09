---
name: debug-mcp
description: MCP debugging — type /debug-mcp <action> for commands
---

# /debug-mcp

MCP server debugging, inspection, and development toolkit.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|-------------|-------------|
| `/debug-mcp status` | Show all MCP servers with health status |
| `/debug-mcp test` | Test a specific MCP tool call |
| `/debug-mcp logs` | View recent MCP server logs and errors |
| `/debug-mcp inspect` | Inspect MCP server config and dependencies |
| `/debug-mcp scaffold` | Generate MCP server skeleton project |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
