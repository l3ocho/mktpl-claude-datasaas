#!/usr/bin/env bash
#
# setup-venvs.sh - Smart MCP server venv management with external cache
#
# This script manages Python virtual environments for MCP servers in a
# PERSISTENT location outside the marketplace directory, so they survive
# marketplace updates.
#
# Features:
# - Stores venvs in ~/.cache/claude-mcp-venvs/ (survives updates)
# - Incremental installs (only missing packages)
# - Hash-based change detection (skip if requirements unchanged)
# - Can be called from SessionStart hooks safely
#
# Usage:
#   ./scripts/setup-venvs.sh              # Full setup
#   ./scripts/setup-venvs.sh --check      # Check only, no install
#   ./scripts/setup-venvs.sh --quick      # Skip if hash unchanged
#   ./scripts/setup-venvs.sh gitea        # Setup specific server only
#

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

# Persistent venv location (outside marketplace)
VENV_CACHE_DIR="${HOME}/.cache/claude-mcp-venvs/mktpl-claude-datasaas"

# Script and repo paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# MCP servers to manage
MCP_SERVERS=(gitea netbox data-platform viz-platform contract-validator)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Flags
CHECK_ONLY=false
QUICK_MODE=false
SPECIFIC_SERVER=""

# ============================================================================
# Argument Parsing
# ============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --check)
            CHECK_ONLY=true
            shift
            ;;
        --quick)
            QUICK_MODE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS] [SERVER]"
            echo ""
            echo "Options:"
            echo "  --check    Check venv status without installing"
            echo "  --quick    Skip servers with unchanged requirements"
            echo "  -h,--help  Show this help"
            echo ""
            echo "Servers: ${MCP_SERVERS[*]}"
            exit 0
            ;;
        *)
            SPECIFIC_SERVER="$1"
            shift
            ;;
    esac
done

# ============================================================================
# Helper Functions
# ============================================================================

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok() { echo -e "${GREEN}[OK]${NC} $1"; }
log_skip() { echo -e "${YELLOW}[SKIP]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Calculate hash of requirements file(s)
requirements_hash() {
    local server_path="$1"
    local hash_input=""

    if [[ -f "$server_path/requirements.txt" ]]; then
        hash_input+=$(cat "$server_path/requirements.txt")
    fi
    if [[ -f "$server_path/pyproject.toml" ]]; then
        hash_input+=$(cat "$server_path/pyproject.toml")
    fi

    echo "$hash_input" | sha256sum | cut -d' ' -f1
}

# Check if requirements changed since last install
requirements_changed() {
    local server_name="$1"
    local server_path="$2"
    local hash_file="$VENV_CACHE_DIR/$server_name/.requirements_hash"

    local current_hash
    current_hash=$(requirements_hash "$server_path")

    if [[ -f "$hash_file" ]]; then
        local stored_hash
        stored_hash=$(cat "$hash_file")
        if [[ "$current_hash" == "$stored_hash" ]]; then
            return 1  # Not changed
        fi
    fi
    return 0  # Changed or no hash file
}

# Save requirements hash after successful install
save_requirements_hash() {
    local server_name="$1"
    local server_path="$2"
    local hash_file="$VENV_CACHE_DIR/$server_name/.requirements_hash"

    requirements_hash "$server_path" > "$hash_file"
}

# ============================================================================
# Main Setup Function
# ============================================================================

setup_server() {
    local server_name="$1"
    local server_path="$REPO_ROOT/mcp-servers/$server_name"
    local venv_path="$VENV_CACHE_DIR/$server_name/.venv"

    # Verify server exists in repo
    if [[ ! -d "$server_path" ]]; then
        log_error "$server_name: source directory not found at $server_path"
        return 1
    fi

    # Check-only mode
    if [[ "$CHECK_ONLY" == true ]]; then
        if [[ -f "$venv_path/bin/python" ]]; then
            log_ok "$server_name: venv exists"
        else
            log_error "$server_name: venv MISSING"
            return 1
        fi
        return 0
    fi

    # Quick mode: skip if requirements unchanged
    if [[ "$QUICK_MODE" == true ]] && [[ -f "$venv_path/bin/python" ]]; then
        if ! requirements_changed "$server_name" "$server_path"; then
            log_skip "$server_name: requirements unchanged"
            return 0
        fi
    fi

    log_info "$server_name: setting up venv..."

    # Create cache directory
    mkdir -p "$VENV_CACHE_DIR/$server_name"

    # Create venv if missing
    if [[ ! -d "$venv_path" ]]; then
        python3 -m venv "$venv_path"
        log_ok "$server_name: venv created"
    fi

    # Activate and install
    # shellcheck disable=SC1091
    source "$venv_path/bin/activate"

    # Upgrade pip quietly
    pip install -q --upgrade pip

    # Install requirements (incremental - pip handles already-installed)
    if [[ -f "$server_path/requirements.txt" ]]; then
        pip install -q -r "$server_path/requirements.txt"
    fi

    # Install local package in editable mode if pyproject.toml exists
    if [[ -f "$server_path/pyproject.toml" ]]; then
        pip install -q -e "$server_path"
        log_ok "$server_name: package installed (editable)"
    fi

    deactivate

    # Save hash for quick mode
    save_requirements_hash "$server_name" "$server_path"

    log_ok "$server_name: ready"
}

# ============================================================================
# Create Symlinks (for backward compatibility)
# ============================================================================

create_symlinks() {
    log_info "Creating symlinks for backward compatibility..."

    for server_name in "${MCP_SERVERS[@]}"; do
        local server_path="$REPO_ROOT/mcp-servers/$server_name"
        local venv_path="$VENV_CACHE_DIR/$server_name/.venv"
        local link_path="$server_path/.venv"

        # Skip if source doesn't exist
        [[ ! -d "$server_path" ]] && continue

        # Skip if venv not in cache
        [[ ! -d "$venv_path" ]] && continue

        # Remove existing venv or symlink
        if [[ -L "$link_path" ]]; then
            rm "$link_path"
        elif [[ -d "$link_path" ]]; then
            log_warn "$server_name: removing old venv directory (now using cache)"
            rm -rf "$link_path"
        fi

        # Create symlink
        ln -s "$venv_path" "$link_path"
        log_ok "$server_name: symlink created"
    done
}

# ============================================================================
# Main
# ============================================================================

main() {
    echo "=============================================="
    echo "  MCP Server Venv Manager"
    echo "=============================================="
    echo "Cache: $VENV_CACHE_DIR"
    echo ""

    local failed=0

    if [[ -n "$SPECIFIC_SERVER" ]]; then
        # Setup specific server
        if setup_server "$SPECIFIC_SERVER"; then
            : # success
        else
            failed=1
        fi
    else
        # Setup all servers
        for server in "${MCP_SERVERS[@]}"; do
            if ! setup_server "$server"; then
                ((failed++)) || true
            fi
        done
    fi

    # Create symlinks for backward compatibility
    if [[ "$CHECK_ONLY" != true ]]; then
        create_symlinks
    fi

    echo ""
    if [[ $failed -eq 0 ]]; then
        log_ok "All MCP servers ready"
    else
        log_error "$failed server(s) failed"
        return 1
    fi
}

main "$@"
