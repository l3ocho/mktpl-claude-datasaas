# Design: debug-mcp

**Domain:** `debug`
**Target Version:** v9.8.0

## Purpose

MCP server debugging and development toolkit. Provides tools for inspecting MCP server health, testing tool calls, viewing server logs, and developing new MCP servers. Essential for marketplace developers building or troubleshooting MCP integrations.

## Target Users

- Plugin developers building MCP servers
- Users troubleshooting MCP connectivity issues
- Marketplace maintainers validating MCP configurations

## Commands

| Command | Description |
|---------|-------------|
| `/debug-mcp status` | Show all MCP servers: running/failed, tool count, last error |
| `/debug-mcp test` | Test a specific MCP tool call with sample input |
| `/debug-mcp logs` | View recent MCP server stderr/stdout logs |
| `/debug-mcp inspect` | Inspect MCP server config (.mcp.json entry, venv, dependencies) |
| `/debug-mcp scaffold` | Generate MCP server skeleton (Python, stdio transport) |

## Agent Architecture

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| `mcp-debugger` | sonnet | default | Server inspection, log analysis, scaffold generation |

Single agent is sufficient — this plugin is primarily diagnostic with one generative command.

## Skills

| Skill | Purpose |
|-------|---------|
| `mcp-protocol` | MCP stdio protocol, tool/resource/prompt schemas |
| `server-patterns` | Python MCP server patterns (FastMCP, raw protocol) |
| `venv-diagnostics` | Virtual environment health checks, dependency validation |
| `log-analysis` | MCP server error pattern recognition |
| `visual-header` | Standard command output headers |

## MCP Server

**Not required.** This plugin inspects other MCP servers via file system (reading .mcp.json, checking venvs, reading logs). It does not need its own MCP server.

## Integration Points

| Plugin | Integration |
|--------|-------------|
| contract-validator | `/cv status` delegates to debug-mcp for detailed MCP diagnostics |
| projman | `/projman setup` can invoke `/debug-mcp status` for post-setup verification |
| All plugins with MCP | Debug-mcp can diagnose any MCP server in the marketplace |

## Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| `claude-md-integration.md` | ~500 |
| Dispatch file (`debug-mcp.md`) | ~200 |
| 5 commands (avg) | ~3,000 |
| 1 agent | ~600 |
| 5 skills | ~2,000 |
| **Total** | **~6,300** |

## Open Questions

- Should this plugin have a hook that auto-runs on MCP failure (SessionStart)?
- Should `/debug-mcp scaffold` generate both Python and TypeScript templates?
