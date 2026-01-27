#!/usr/bin/env bash
#
# post-update.sh - Run after pulling updates or marketplace sync
#
# Usage: ./scripts/post-update.sh
#
# This script:
# 1. Restores MCP venv symlinks (instant if cache exists)
# 2. Creates venvs in external cache if missing (first run only)
# 3. Shows recent changelog updates
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

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

    # Run venv-repair.sh to restore symlinks to external cache
    # This is instant if cache exists, or does full setup on first run
    if [[ -x "$SCRIPT_DIR/venv-repair.sh" ]]; then
        log_info "Restoring MCP venv symlinks..."
        if "$SCRIPT_DIR/venv-repair.sh"; then
            log_success "MCP venvs ready"
        else
            log_error "MCP venv setup failed"
            log_warn "Run: $SCRIPT_DIR/setup-venvs.sh for full setup"
            exit 1
        fi
    else
        log_error "venv-repair.sh not found at $SCRIPT_DIR"
        exit 1
    fi

    check_changelog

    echo ""
    log_success "Post-update complete!"
    echo ""
    echo "MCP servers will work immediately on next session start."
}

main "$@"
