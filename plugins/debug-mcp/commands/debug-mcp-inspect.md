---
name: debug-mcp inspect
description: Inspect MCP server configuration, dependencies, and tool definitions
---

# /debug-mcp inspect

Deep inspection of an MCP server's configuration, dependencies, and tool definitions.

## Skills to Load

- `skills/visual-header.md`
- `skills/venv-diagnostics.md`
- `skills/mcp-protocol.md`

## Agent

Delegate to `agents/mcp-debugger.md`.

## Usage

```
/debug-mcp inspect <server_name> [--tools] [--deps] [--config]
```

**Arguments:**
- `server_name` - Name of the MCP server from .mcp.json

**Options:**
- `--tools` - List all registered tools with their schemas
- `--deps` - Show dependency analysis (installed vs required)
- `--config` - Show configuration files and environment variables
- (no flags) - Show all sections

## Instructions

Execute `skills/visual-header.md` with context "Server Inspection".

### Phase 1: Configuration

1. Read `.mcp.json` and extract the server definition
2. Display:
   - Server name
   - Command and arguments
   - Working directory
   - Environment variable references

```
## Server: gitea

### Configuration (.mcp.json)
- Command: /path/to/mcp-servers/gitea/.venv/bin/python
- Args: ["-m", "mcp_server.server"]
- CWD: /path/to/mcp-servers/gitea
- Env file: ~/.config/claude/gitea.env

**Note:** The gitea server uses `gitea_mcp.server` (installed from package).
Other servers use `mcp_server.server` (local source).
```

### Phase 2: Dependencies (--deps)

Apply `skills/venv-diagnostics.md`:

1. Read `requirements.txt` from the server's cwd
2. Compare with installed packages:
   ```bash
   cd <cwd> && .venv/bin/pip freeze
   ```
3. Identify:
   - Missing packages (in requirements but not installed)
   - Version mismatches (installed version differs from required)
   - Extra packages (installed but not in requirements)

```
### Dependencies

| Package | Required | Installed | Status |
|---------|----------|-----------|--------|
| mcp | >=1.0.0 | 1.2.3 | OK |
| httpx | >=0.24 | 0.25.0 | OK |
| pynetbox | >=7.0 | — | MISSING |

- Missing: 1 package
- Mismatched: 0 packages
```

### Phase 3: Tools (--tools)

Parse the server source code to extract tool definitions:

1. Find Python files with `@mcp.tool` decorators or `server.add_tool()` calls
2. Extract tool name, description, and parameter schema
3. Group by module/category if applicable

```
### Tools (42 registered)

#### Issues (6 tools)
| Tool | Description | Params |
|------|-------------|--------|
| list_issues | List issues from repository | state?, labels?, repo? |
| get_issue | Get specific issue | issue_number (required) |
| create_issue | Create new issue | title (required), body (required) |
...
```

### Phase 4: Environment Configuration (--config)

1. Locate env file referenced in .mcp.json
2. Read the file (mask secret values)
3. Check for missing required variables

```
### Environment Configuration

File: ~/.config/claude/gitea.env
| Variable | Value | Status |
|----------|-------|--------|
| GITEA_API_URL | https://gitea.example.com/api/v1 | OK |
| GITEA_API_TOKEN | ****...a1b2 | OK |

File: .env (project level)
| Variable | Value | Status |
|----------|-------|--------|
| GITEA_ORG | personal-projects | OK |
| GITEA_REPO | mktpl-claude-datasaas | OK |
```

## User Request

$ARGUMENTS
