---
name: debug-mcp logs
description: View recent MCP server logs and error patterns
---

# /debug-mcp logs

View and analyze recent MCP server log output.

## Skills to Load

- `skills/visual-header.md`
- `skills/log-analysis.md`

## Agent

Delegate to `agents/mcp-debugger.md`.

## Usage

```
/debug-mcp logs [--server=<name>] [--lines=<count>] [--errors-only]
```

**Options:**
- `--server` - Filter to a specific server (default: all)
- `--lines` - Number of recent lines to show (default: 50)
- `--errors-only` - Show only error-level log entries

## Instructions

Execute `skills/visual-header.md` with context "Log Analysis".

### Phase 1: Locate Log Sources

MCP servers in Claude Code output to stderr. Log locations vary:

1. **Claude Code session logs** - Check `~/.claude/logs/` for recent session logs
2. **Server stderr** - If server runs as a subprocess, logs go to Claude Code's stderr
3. **Custom log files** - Some servers may write to files in their cwd

Search for log files:
```bash
# Claude Code logs
ls -la ~/.claude/logs/ 2>/dev/null

# Server-specific logs
ls -la <server_cwd>/*.log 2>/dev/null
ls -la <server_cwd>/logs/ 2>/dev/null
```

### Phase 2: Parse Logs

1. Read the most recent log entries (default 50 lines)
2. Filter by server name if `--server` specified
3. If `--errors-only`, filter for patterns:
   - Lines containing `ERROR`, `CRITICAL`, `FATAL`
   - Python tracebacks (`Traceback (most recent call last)`)
   - JSON-RPC error responses (`"error":`)

### Phase 3: Error Analysis

Apply patterns from `skills/log-analysis.md`:

1. **Categorize errors** by type (ImportError, ConnectionError, TimeoutError, etc.)
2. **Count occurrences** of each error pattern
3. **Identify root cause** using the common patterns from the skill
4. **Suggest fix** for each error category

### Phase 4: Report

```
## MCP Server Logs

### Server: gitea
Last 10 entries:
[2025-11-15 10:00:01] INFO  Initialized with 42 tools
[2025-11-15 10:00:05] INFO  Tool call: list_issues (245ms)
...

### Server: netbox
Last 10 entries:
[2025-11-15 09:58:00] ERROR ImportError: No module named 'pynetbox'

### Error Summary

| Server | Error Type | Count | Root Cause | Fix |
|--------|-----------|-------|------------|-----|
| netbox | ImportError | 3 | Missing dependency | pip install pynetbox |

### Recommendations
1. Fix netbox: Reinstall dependencies in venv
2. All other servers: No issues detected
```

## User Request

$ARGUMENTS
