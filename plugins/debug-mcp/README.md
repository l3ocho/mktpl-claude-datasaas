# debug-mcp

MCP server debugging, inspection, and development toolkit.

## Overview

This plugin provides tools for diagnosing MCP server issues, testing tool invocations, analyzing server logs, inspecting configurations and dependencies, and scaffolding new MCP servers. It is essential for maintaining and developing MCP integrations in the Leo Claude Marketplace.

## Commands

| Command | Description |
|---------|-------------|
| `/debug-mcp status` | Show all MCP servers with health status |
| `/debug-mcp test` | Test a specific MCP tool call |
| `/debug-mcp logs` | View recent MCP server logs and errors |
| `/debug-mcp inspect` | Inspect MCP server config and dependencies |
| `/debug-mcp scaffold` | Generate MCP server skeleton project |

## Agent

| Agent | Model | Mode | Purpose |
|-------|-------|------|---------|
| mcp-debugger | sonnet | default | All debug-mcp operations: inspection, testing, log analysis, scaffolding |

## Skills

| Skill | Description |
|-------|-------------|
| mcp-protocol | MCP stdio protocol specification, JSON-RPC messages, tool/resource/prompt definitions |
| server-patterns | Python MCP server directory structure, FastMCP pattern, config loader, entry points |
| venv-diagnostics | Virtual environment health checks: existence, Python binary, packages, imports |
| log-analysis | Common MCP error patterns with root causes and fixes |
| visual-header | Standard command output header |

## Architecture

```
plugins/debug-mcp/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── debug-mcp.md            # Dispatch file
│   ├── debug-mcp-status.md
│   ├── debug-mcp-test.md
│   ├── debug-mcp-logs.md
│   ├── debug-mcp-inspect.md
│   └── debug-mcp-scaffold.md
├── agents/
│   └── mcp-debugger.md
├── skills/
│   ├── mcp-protocol.md
│   ├── server-patterns.md
│   ├── venv-diagnostics.md
│   ├── log-analysis.md
│   └── visual-header.md
├── claude-md-integration.md
└── README.md
```

## License

MIT License - Part of the Leo Claude Marketplace.
