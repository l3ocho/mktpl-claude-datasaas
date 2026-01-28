#!/bin/bash
# Capture original working directory before any cd operations
# This should be the user's project directory when launched by Claude Code
export CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_VENV="$HOME/.cache/claude-mcp-venvs/leo-claude-mktplace/viz-platform/.venv"
LOCAL_VENV="$SCRIPT_DIR/.venv"

if [[ -f "$CACHE_VENV/bin/python" ]]; then
    PYTHON="$CACHE_VENV/bin/python"
elif [[ -f "$LOCAL_VENV/bin/python" ]]; then
    PYTHON="$LOCAL_VENV/bin/python"
else
    echo "ERROR: No venv found. Run: ./scripts/setup-venvs.sh" >&2
    exit 1
fi

cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR"
exec "$PYTHON" -m mcp_server.server "$@"
