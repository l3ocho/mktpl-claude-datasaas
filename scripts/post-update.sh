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

    if [[ ! -d "$server_path" ]]; then
        log_warn "$server_name directory not found at $server_path - skipping"
        return 0
    fi

    if [[ ! -f "$server_path/requirements.txt" ]]; then
        log_warn "$server_name has no requirements.txt - skipping"
        return 0
    fi

    cd "$server_path"

    # Create venv if missing
    if [[ ! -d ".venv" ]]; then
        log_info "Creating $server_name venv (was missing)..."
        python3 -m venv .venv
        log_success "$server_name venv created"
    else
        log_info "Updating $server_name dependencies..."
    fi

    # Install/update dependencies
    source .venv/bin/activate
    pip install -q --upgrade pip
    pip install -q -r requirements.txt

    # Install local package in editable mode if pyproject.toml exists
    if [[ -f "pyproject.toml" ]]; then
        pip install -q -e .
        log_success "$server_name package installed (editable mode)"
    fi

    deactivate
    cd "$REPO_ROOT"
    log_success "$server_name ready"
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

    # Shared MCP servers at repository root (v3.0.0+)
    update_mcp_server "gitea"
    update_mcp_server "netbox"
    update_mcp_server "data-platform"
    update_mcp_server "viz-platform"
    update_mcp_server "contract-validator"

    check_changelog

    echo ""
    log_success "Post-update complete!"
    echo ""
    echo "If you see new features in the changelog that require"
    echo "configuration changes, update your ~/.config/claude/*.env files."
}

main "$@"

# Clear plugin cache to ensure fresh hooks are loaded
echo "Clearing plugin cache..."
rm -rf ~/.claude/plugins/cache/leo-claude-mktplace/
echo "Cache cleared"
