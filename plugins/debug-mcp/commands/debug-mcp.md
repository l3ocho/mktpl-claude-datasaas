---
name: debug-mcp
description: MCP debugging — type /debug-mcp <action> for commands
---

# /debug-mcp

MCP server debugging, inspection, and development toolkit.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `status` | `/debug-mcp:debug-mcp-status` | Show all MCP servers with health status |
| `test` | `/debug-mcp:debug-mcp-test` | Test a specific MCP tool call |
| `logs` | `/debug-mcp:debug-mcp-logs` | View recent MCP server logs and errors |
| `inspect` | `/debug-mcp:debug-mcp-inspect` | Inspect MCP server config and dependencies |
| `scaffold` | `/debug-mcp:debug-mcp-scaffold` | Generate MCP server skeleton project |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/debug-mcp status`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/debug-mcp:debug-mcp-status`)
