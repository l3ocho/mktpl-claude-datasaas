#!/bin/bash
# data-platform startup check hook
# Checks for common issues at session start
# All output MUST have [data-platform] prefix

PREFIX="[data-platform]"

# Check if MCP venv exists
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"
VENV_PATH="$PLUGIN_ROOT/mcp-servers/data-platform/.venv/bin/python"

if [[ ! -f "$VENV_PATH" ]]; then
    echo "$PREFIX MCP venv missing - run /initial-setup or setup.sh"
    exit 0
fi

# Check PostgreSQL configuration (optional - just warn if configured but failing)
POSTGRES_CONFIG="$HOME/.config/claude/postgres.env"
if [[ -f "$POSTGRES_CONFIG" ]]; then
    source "$POSTGRES_CONFIG"
    if [[ -n "${POSTGRES_URL:-}" ]]; then
        # Quick connection test (5 second timeout)
        RESULT=$("$VENV_PATH" -c "
import asyncio
import sys
async def test():
    try:
        import asyncpg
        conn = await asyncpg.connect('$POSTGRES_URL', timeout=5)
        await conn.close()
        return 'OK'
    except Exception as e:
        return f'FAIL: {e}'
print(asyncio.run(test()))
" 2>/dev/null || echo "FAIL: asyncpg not installed")

        if [[ "$RESULT" == "OK" ]]; then
            # PostgreSQL OK - say nothing
            :
        elif [[ "$RESULT" == *"FAIL"* ]]; then
            echo "$PREFIX PostgreSQL connection failed - check POSTGRES_URL"
        fi
    fi
fi

# Check dbt project (if in a project with dbt_project.yml)
if [[ -f "dbt_project.yml" ]] || [[ -f "transform/dbt_project.yml" ]]; then
    if ! command -v dbt &> /dev/null; then
        echo "$PREFIX dbt CLI not found - dbt tools unavailable"
    fi
fi

# All checks passed - say nothing
exit 0
