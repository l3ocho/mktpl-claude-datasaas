---
name: debug-mcp status
description: Show all configured MCP servers with health status, venv state, and tool counts
---

# /debug-mcp status

Display the health status of all MCP servers configured in the project.

## Skills to Load

- `skills/visual-header.md`
- `skills/venv-diagnostics.md`
- `skills/log-analysis.md`

## Agent

Delegate to `agents/mcp-debugger.md`.

## Usage

```
/debug-mcp status [--server=<name>] [--verbose]
```

**Options:**
- `--server` - Check a specific server only
- `--verbose` - Show detailed output including tool lists

## Instructions

Execute `skills/visual-header.md` with context "Server Status".

### Phase 1: Locate Configuration

1. Read `.mcp.json` from the project root
2. Parse the `mcpServers` object to extract all server definitions
3. For each server, extract:
   - Server name (key in mcpServers)
   - Command path (usually Python interpreter in .venv)
   - Arguments (module path)
   - Working directory (`cwd`)
   - Environment variables or env file references

### Phase 2: Check Each Server

For each configured MCP server:

1. **Executable check** - Does the command path exist?
   ```bash
   test -f <command_path> && echo "OK" || echo "MISSING"
   ```

2. **Virtual environment check** - Apply `skills/venv-diagnostics.md`:
   - Does `.venv/` directory exist in the server's cwd?
   - Is the Python binary intact (not broken symlink)?
   - Are requirements satisfied?

3. **Config file check** - Does the referenced env file exist?
   ```bash
   test -f <env_file_path> && echo "OK" || echo "MISSING"
   ```

4. **Module check** - Can the server module be imported?
   ```bash
   cd <cwd> && .venv/bin/python -c "import <module_name>" 2>&1
   ```

### Phase 3: Report

```
## MCP Server Status

| Server | Executable | Venv | Config | Import | Status |
|--------|-----------|------|--------|--------|--------|
| gitea | OK | OK | OK | OK | HEALTHY |
| netbox | OK | MISSING | OK | FAIL | ERROR |
| data-platform | OK | OK | OK | OK | HEALTHY |

### Errors

#### netbox
- Venv missing: /path/to/mcp-servers/netbox/.venv does not exist
- Import failed: ModuleNotFoundError: No module named 'pynetbox'
- Fix: cd /path/to/mcp-servers/netbox && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

### Summary
- Healthy: 4/5
- Errors: 1/5
```

### Phase 4: Verbose Mode

If `--verbose`, additionally show for each healthy server:
- Tool count (parse server source for `@mcp.tool` decorators or tool registration)
- Resource count
- Last modification time of server.py

## User Request

$ARGUMENTS
