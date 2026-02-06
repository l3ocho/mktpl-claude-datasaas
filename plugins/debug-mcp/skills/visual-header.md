# Visual Header Skill

Standard visual header for debug-mcp commands.

## Header Template

```
+----------------------------------------------------------------------+
|  DEBUG-MCP - [Context]                                                |
+----------------------------------------------------------------------+
```

## Context Values by Command

| Command | Context |
|---------|---------|
| `/debug-mcp status` | Server Status |
| `/debug-mcp test` | Tool Test |
| `/debug-mcp logs` | Log Analysis |
| `/debug-mcp inspect` | Server Inspection |
| `/debug-mcp scaffold` | Server Scaffold |
| Agent mode | MCP Debugging |

## Usage

Display header at the start of every command response before proceeding with the operation.
