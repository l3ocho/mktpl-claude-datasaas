#!/usr/bin/env bash
#
# venv-repair.sh - Fast MCP venv auto-repair for SessionStart hooks
#
# This script is designed to run at session start. It:
# 1. Checks if venvs exist in external cache (~/.cache/claude-mcp-venvs/)
# 2. Creates symlinks from marketplace to cache (instant operation)
# 3. Only runs pip install if cache is missing (first install)
#
# Output format: All messages prefixed with [mcp-venv] for hook display
#
# Usage:
#   ./scripts/venv-repair.sh           # Auto-repair (default)
#   ./scripts/venv-repair.sh --silent  # Silent mode (no output unless error)
#

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

PREFIX="[mcp-venv]"
VENV_CACHE_DIR="${HOME}/.cache/claude-mcp-venvs/leo-claude-mktplace"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# MCP servers
MCP_SERVERS=(gitea netbox data-platform viz-platform contract-validator)

# Parse args
SILENT=false
[[ "${1:-}" == "--silent" ]] && SILENT=true

log() {
    [[ "$SILENT" == true ]] && return
    echo "$PREFIX $1"
}

log_error() {
    echo "$PREFIX ERROR: $1" >&2
}

# ============================================================================
# Check if all venvs exist in cache
# ============================================================================

cache_complete() {
    for server in "${MCP_SERVERS[@]}"; do
        local venv_python="$VENV_CACHE_DIR/$server/.venv/bin/python"
        [[ ! -f "$venv_python" ]] && return 1
    done
    return 0
}

# ============================================================================
# Create symlinks from marketplace to cache
# ============================================================================

create_symlink() {
    local server_name="$1"
    local server_path="$REPO_ROOT/mcp-servers/$server_name"
    local venv_cache="$VENV_CACHE_DIR/$server_name/.venv"
    local venv_link="$server_path/.venv"

    # Skip if server doesn't exist
    [[ ! -d "$server_path" ]] && return 0

    # Skip if cache doesn't exist
    [[ ! -d "$venv_cache" ]] && return 1

    # Already correct symlink?
    if [[ -L "$venv_link" ]]; then
        local target
        target=$(readlink "$venv_link")
        [[ "$target" == "$venv_cache" ]] && return 0
        rm "$venv_link"
    elif [[ -d "$venv_link" ]]; then
        # Old venv directory exists - back it up or remove
        rm -rf "$venv_link"
    fi

    # Create symlink
    ln -s "$venv_cache" "$venv_link"
    return 0
}

create_all_symlinks() {
    local created=0
    for server in "${MCP_SERVERS[@]}"; do
        if create_symlink "$server"; then
            ((created++)) || true
        fi
    done
    [[ $created -gt 0 ]] && log "Restored $created venv symlinks"
}

# ============================================================================
# Full setup (only if cache missing)
# ============================================================================

setup_server() {
    local server_name="$1"
    local server_path="$REPO_ROOT/mcp-servers/$server_name"
    local venv_path="$VENV_CACHE_DIR/$server_name/.venv"

    [[ ! -d "$server_path" ]] && return 0

    mkdir -p "$VENV_CACHE_DIR/$server_name"

    # Create venv
    if [[ ! -d "$venv_path" ]]; then
        python3 -m venv "$venv_path"
    fi

    # Install dependencies
    # shellcheck disable=SC1091
    source "$venv_path/bin/activate"
    pip install -q --upgrade pip

    if [[ -f "$server_path/requirements.txt" ]]; then
        pip install -q -r "$server_path/requirements.txt"
    fi

    if [[ -f "$server_path/pyproject.toml" ]]; then
        pip install -q -e "$server_path"
    fi

    deactivate

    # Save hash for future quick checks
    local hash_file="$VENV_CACHE_DIR/$server_name/.requirements_hash"
    {
        if [[ -f "$server_path/requirements.txt" ]]; then
            cat "$server_path/requirements.txt"
        fi
        if [[ -f "$server_path/pyproject.toml" ]]; then
            cat "$server_path/pyproject.toml"
        fi
        echo ""  # Ensure non-empty input for sha256sum
    } | sha256sum | cut -d' ' -f1 > "$hash_file"
}

full_setup() {
    log "First run - setting up MCP venvs (this only happens once)..."
    for server in "${MCP_SERVERS[@]}"; do
        log "  Setting up $server..."
        setup_server "$server"
    done
    log "Setup complete. Future sessions will be instant."
}

# ============================================================================
# Main
# ============================================================================

main() {
    # Fast path: cache exists, just ensure symlinks
    if cache_complete; then
        create_all_symlinks
        exit 0
    fi

    # Slow path: need to create venvs (first install)
    full_setup
    create_all_symlinks
}

main "$@"
