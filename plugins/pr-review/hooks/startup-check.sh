#!/bin/bash
# pr-review startup check hook
# Checks for common issues at session start
# All output MUST have [pr-review] prefix

PREFIX="[pr-review]"

# Check if MCP venv exists
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"
VENV_PATH="$PLUGIN_ROOT/mcp-servers/gitea/.venv/bin/python"

if [[ ! -f "$VENV_PATH" ]]; then
    echo "$PREFIX MCP venvs missing - run setup.sh from installed marketplace"
    exit 0
fi

# Check git remote vs .env config (only if .env exists)
if [[ -f ".env" ]]; then
    CONFIGURED_REPO=$(grep -E "^GITEA_REPO=" .env 2>/dev/null | cut -d'=' -f2 | tr -d '"' || true)
    if [[ -n "$CONFIGURED_REPO" ]]; then
        CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\/[^.]*\).*/\1/' || true)
        if [[ -n "$CURRENT_REMOTE" && "$CONFIGURED_REPO" != "$CURRENT_REMOTE" ]]; then
            echo "$PREFIX Git remote mismatch - run /pr-review:project-sync"
            exit 0
        fi
    fi
fi

# All checks passed - say nothing
exit 0
