---
name: debug-mcp scaffold
description: Generate a new MCP server skeleton project with standard structure
---

# /debug-mcp scaffold

Generate a new MCP server project with the standard directory structure, entry point, and configuration.

## Skills to Load

- `skills/visual-header.md`
- `skills/server-patterns.md`
- `skills/mcp-protocol.md`

## Agent

Delegate to `agents/mcp-debugger.md`.

## Usage

```
/debug-mcp scaffold <server_name> [--tools=<tool1,tool2,...>] [--location=<path>]
```

**Arguments:**
- `server_name` - Name for the new MCP server (lowercase, hyphens)

**Options:**
- `--tools` - Comma-separated list of initial tool names to generate stubs
- `--location` - Where to create the server (default: `mcp-servers/<server_name>`)

## Instructions

Execute `skills/visual-header.md` with context "Server Scaffold".

### Phase 1: Gather Requirements

1. Ask user for:
   - Server purpose (one sentence)
   - External service it integrates with (if any)
   - Authentication type (API key, OAuth, none)
   - Initial tools to register (at least one)

### Phase 2: Generate Project Structure

Apply patterns from `skills/server-patterns.md`:

```
mcp-servers/<server_name>/
├── mcp_server/
│   ├── __init__.py
│   ├── config.py          # Configuration loader (env files)
│   ├── server.py           # MCP server entry point
│   └── tools/
│       ├── __init__.py
│       └── <category>.py   # Tool implementations
├── tests/
│   ├── __init__.py
│   └── test_tools.py       # Tool unit tests
├── requirements.txt        # Python dependencies
└── README.md               # Server documentation
```

### Phase 3: Generate Files

#### server.py
- Import FastMCP or raw MCP protocol handler
- Register tools from tools/ directory
- Configure stdio transport
- Add startup logging with tool count

#### config.py
- Load from `~/.config/claude/<server_name>.env`
- Fall back to project-level `.env`
- Validate required variables on startup
- Mask sensitive values in logs

#### tools/<category>.py
- For each tool name provided in `--tools`:
  - Generate a stub function with `@mcp.tool` decorator
  - Include docstring with description
  - Define inputSchema with parameter types
  - Return placeholder response

#### requirements.txt
```
mcp>=1.0.0
httpx>=0.24.0
python-dotenv>=1.0.0
```

#### README.md
- Server name and description
- Installation instructions (venv setup)
- Configuration (env variables)
- Available tools table
- Architecture diagram

### Phase 4: Register in .mcp.json

1. Read the project's `.mcp.json`
2. Add the new server entry:
   ```json
   "<server_name>": {
     "command": "mcp-servers/<server_name>/.venv/bin/python",
     "args": ["-m", "mcp_server.server"],
     "cwd": "mcp-servers/<server_name>"
   }
   ```

   **Note:** Use `mcp_server.server` for new servers being scaffolded.
   Exception: gitea uses `gitea_mcp.server` (pip-installed package).
3. Show the change and ask user to confirm before writing

### Phase 5: Completion

```
## Scaffold Complete

### Created Files
- mcp-servers/<name>/mcp_server/server.py
- mcp-servers/<name>/mcp_server/config.py
- mcp-servers/<name>/mcp_server/tools/<category>.py
- mcp-servers/<name>/requirements.txt
- mcp-servers/<name>/README.md

### Next Steps
1. Create virtual environment:
   cd mcp-servers/<name> && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
2. Add credentials:
   Edit ~/.config/claude/<name>.env
3. Implement tool logic:
   Edit mcp-servers/<name>/mcp_server/tools/<category>.py
4. Restart Claude Code session to load the new server
5. Test: /debug-mcp test <name> <tool_name>
```

## User Request

$ARGUMENTS
