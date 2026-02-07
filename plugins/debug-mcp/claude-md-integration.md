# Debug MCP Integration

Add to your project's CLAUDE.md:

## MCP Server Debugging (debug-mcp)

This project uses the **debug-mcp** plugin for diagnosing and developing MCP server integrations.

### Available Commands

| Command | Description |
|---------|-------------|
| `/debug-mcp status` | Show health status of all configured MCP servers |
| `/debug-mcp test` | Test a specific MCP tool call with parameters |
| `/debug-mcp logs` | View and analyze recent MCP server error logs |
| `/debug-mcp inspect` | Deep inspection of server config, dependencies, and tools |
| `/debug-mcp scaffold` | Generate a new MCP server project skeleton |

### Usage Guidelines

- Run `/debug-mcp status` when Claude Code reports MCP server failures at session start
- Use `/debug-mcp inspect <server> --deps` to diagnose missing package issues
- Use `/debug-mcp test <server> <tool>` to verify individual tool functionality
- Use `/debug-mcp logs --errors-only` to quickly find error patterns
- Use `/debug-mcp scaffold` when creating a new MCP server integration

### Common Troubleshooting

| Symptom | Command |
|---------|---------|
| "X MCP servers failed" at startup | `/debug-mcp status` |
| Tool call returns error | `/debug-mcp test <server> <tool>` |
| ImportError in server | `/debug-mcp inspect <server> --deps` |
| Unknown server errors | `/debug-mcp logs --server=<name>` |
