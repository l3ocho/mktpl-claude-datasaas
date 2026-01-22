#!/usr/bin/env bash
#
# check-venv.sh - Check if MCP server venvs exist in installed marketplace
#
# Usage: ./scripts/check-venv.sh
#
# Exit codes:
#   0 - All venvs exist (or not installed via marketplace)
#   1 - Venvs missing, needs setup
#
# This script is designed to be called from SessionStart hooks
# to enable self-healing MCP server setup.

set -euo pipefail

# Installed marketplace location
MKTPLACE="$HOME/.claude/plugins/marketplaces/leo-claude-mktplace"

# If not installed via marketplace, exit silently
if [[ ! -d "$MKTPLACE" ]]; then
    exit 0
fi

# Check if gitea venv exists
if [[ ! -f "$MKTPLACE/mcp-servers/gitea/.venv/bin/python" ]]; then
    echo "SETUP_NEEDED"
    exit 1
fi

# Check if netbox venv exists
if [[ ! -f "$MKTPLACE/mcp-servers/netbox/.venv/bin/python" ]]; then
    echo "SETUP_NEEDED"
    exit 1
fi

# All good
exit 0
