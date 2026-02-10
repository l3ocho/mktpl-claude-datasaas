#!/usr/bin/env bash
#
# post-update.sh - Run after pulling updates or marketplace sync
#
# Usage: ./scripts/post-update.sh
#
# This script:
# 1. Clears Claude plugin cache (forces fresh .mcp.json reads)
# 2. Shows recent changelog updates
#
# NOTE: This script does NOT touch .venv directories.
# If venvs are missing, run ./scripts/setup.sh manually.
#

set -euo pipefail

CLAUDE_PLUGIN_CACHE="$HOME/.claude/plugins/cache/mktpl-claude-datasaas"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

check_changelog() {
    if [[ -f "$REPO_ROOT/CHANGELOG.md" ]]; then
        local unreleased
        unreleased=$(sed -n '/## \[Unreleased\]/,/## \[/p' "$REPO_ROOT/CHANGELOG.md" | grep -E '^### ' | head -1 || true)
        if [[ -n "$unreleased" ]]; then
            echo ""
            log_info "Recent changes (from CHANGELOG.md):"
            echo "-----------------------------------"
            sed -n '/## \[Unreleased\]/,/## \[/p' "$REPO_ROOT/CHANGELOG.md" | head -20
            echo "-----------------------------------"
        fi
    fi
}

main() {
    echo "=============================================="
    echo "  Post-Update Check"
    echo "=============================================="
    echo ""

    # Clear Claude plugin cache to force fresh .mcp.json reads
    # This cache holds versioned copies that become stale after updates
    # NOTE: This does NOT touch .venv directories
    if [[ -d "$CLAUDE_PLUGIN_CACHE" ]]; then
        log_info "Clearing Claude plugin cache..."
        rm -rf "$CLAUDE_PLUGIN_CACHE"
        log_success "Plugin cache cleared"
    fi

    check_changelog

    echo ""
    log_success "Post-update complete!"
    echo ""
    echo "IMPORTANT: Restart Claude Code for changes to take effect."
    echo ""
    echo "If MCP servers are not working, run: ./scripts/setup.sh"
}

main "$@"
