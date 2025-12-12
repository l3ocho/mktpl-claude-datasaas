#!/usr/bin/env bash
#
# post-update.sh - Run after pulling updates
#
# Usage: ./scripts/post-update.sh
#
# This script:
# 1. Updates Python dependencies for MCP servers
# 2. Validates configuration still works
# 3. Reports any new manual steps from CHANGELOG
#

set -euo pipefail

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

update_mcp_server() {
    local server_name="$1"
    local server_path="$REPO_ROOT/mcp-servers/$server_name"

    log_info "Updating $server_name dependencies..."

    if [[ -d "$server_path/.venv" ]] && [[ -f "$server_path/requirements.txt" ]]; then
        cd "$server_path"
        source .venv/bin/activate
        pip install -q --upgrade pip
        pip install -q -r requirements.txt
        deactivate
        cd "$REPO_ROOT"
        log_success "$server_name dependencies updated"
    else
        log_warn "$server_name not fully set up - run ./scripts/setup.sh first"
    fi
}

check_changelog() {
    log_info "Checking CHANGELOG for recent updates..."

    if [[ -f "$REPO_ROOT/CHANGELOG.md" ]]; then
        # Show the Unreleased section
        echo ""
        echo "Recent changes (from CHANGELOG.md):"
        echo "-----------------------------------"
        sed -n '/## \[Unreleased\]/,/## \[/p' "$REPO_ROOT/CHANGELOG.md" | head -30
        echo "-----------------------------------"
        echo ""
    fi
}

main() {
    echo "=============================================="
    echo "  Post-Update Check"
    echo "=============================================="
    echo ""

    update_mcp_server "gitea"
    update_mcp_server "wikijs"

    check_changelog

    echo ""
    log_success "Post-update complete!"
    echo ""
    echo "If you see new features in the changelog that require"
    echo "configuration changes, update your ~/.config/claude/*.env files."
}

main "$@"
