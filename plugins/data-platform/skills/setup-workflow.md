# Setup Workflow

## Important Context

- **This workflow uses Bash, Read, Write, AskUserQuestion tools** - NOT MCP tools
- **MCP tools won't work until after setup + session restart**
- **PostgreSQL and dbt are optional** - pandas tools work without them

## Phase 1: Environment Validation

### Check Python Version
```bash
python3 --version
```
Requires Python 3.10+. If below, stop and inform user.

## Phase 2: MCP Server Setup

### Locate MCP Server
Check both paths:
```bash
# Installed marketplace
ls -la ~/.claude/plugins/marketplaces/leo-claude-mktplace/mcp-servers/data-platform/

# Source
ls -la ~/claude-plugins-work/mcp-servers/data-platform/
```

### Check/Create Virtual Environment
```bash
# Check
ls -la /path/to/mcp-servers/data-platform/.venv/bin/python

# Create if missing
cd /path/to/mcp-servers/data-platform
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
```

## Phase 3: PostgreSQL Configuration (Optional)

### Config Location
`~/.config/claude/postgres.env`

### Config Format
```bash
# PostgreSQL Configuration
POSTGRES_URL=postgresql://user:pass@host:5432/db
```

Set permissions: `chmod 600 ~/.config/claude/postgres.env`

### Test Connection
```bash
source ~/.config/claude/postgres.env && python3 -c "
import asyncio, asyncpg
async def test():
    conn = await asyncpg.connect('$POSTGRES_URL', timeout=5)
    ver = await conn.fetchval('SELECT version()')
    await conn.close()
    print(f'SUCCESS: {ver.split(\",\")[0]}')
asyncio.run(test())
"
```

## Phase 4: dbt Configuration (Optional)

dbt is **project-level** (auto-detected via `dbt_project.yml`).

For subdirectory projects, set in `.env`:
```
DBT_PROJECT_DIR=./transform
DBT_PROFILES_DIR=~/.dbt
```

### Check dbt Installation
```bash
dbt --version
```

## Phase 5: Validation

### Verify MCP Server
```bash
cd /path/to/mcp-servers/data-platform
.venv/bin/python -c "from mcp_server.server import DataPlatformMCPServer; print('OK')"
```

## Memory Limits

Default: 100,000 rows per DataFrame

Override in project `.env`:
```
DATA_PLATFORM_MAX_ROWS=500000
```

For larger datasets:
- Use chunked processing (`chunk_size` parameter)
- Filter data before loading
- Store to Parquet for efficient re-loading

## Session Restart

After setup, restart Claude Code session for MCP tools to become available.
