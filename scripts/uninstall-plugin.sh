#!/usr/bin/env bash
# =============================================================================
# uninstall-plugin.sh - Remove marketplace plugin from a consumer project
# =============================================================================
#
# Usage: ./scripts/uninstall-plugin.sh <plugin-name> <target-project-path>
#
# This script:
# 1. Removes MCP server entry from target project's .mcp.json
# 2. Removes CLAUDE.md integration section for the plugin
# 3. Is idempotent (safe to run multiple times)
#
# Examples:
#   ./scripts/uninstall-plugin.sh data-platform ~/projects/personal-portfolio
#   ./scripts/uninstall-plugin.sh projman /home/user/my-project
#
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# --- Color Definitions ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- Logging Functions ---
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_skip() { echo -e "${YELLOW}[SKIP]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# --- Track Changes ---
CHANGES_MADE=()
SKIPPED=()

# --- Usage ---
usage() {
    echo "Usage: $0 <plugin-name> <target-project-path>"
    echo ""
    echo "Remove a marketplace plugin from a consumer project."
    echo ""
    echo "Arguments:"
    echo "  plugin-name         Name of the plugin (e.g., data-platform, viz-platform, projman)"
    echo "  target-project-path Path to the target project (absolute or relative)"
    echo ""
    echo "Examples:"
    echo "  $0 data-platform ~/projects/personal-portfolio"
    echo "  $0 projman /home/user/my-project"
    exit 1
}

# --- Prerequisite Check ---
check_prerequisites() {
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed."
        echo "Install with: sudo apt install jq"
        exit 1
    fi
}

# --- Validate Target Project ---
validate_target() {
    local target_path="$1"

    if [[ ! -d "$target_path" ]]; then
        log_error "Target project path does not exist: $target_path"
        exit 1
    fi

    log_success "Target project found: $target_path"
}

# --- Remove from .mcp.json ---
remove_from_mcp_json() {
    local plugin_name="$1"
    local target_path="$2"
    local mcp_json="$target_path/.mcp.json"

    # Check if .mcp.json exists
    if [[ ! -f "$mcp_json" ]]; then
        log_skip "No .mcp.json found - nothing to remove"
        SKIPPED+=(".mcp.json: File does not exist")
        return 0
    fi

    # Check if entry exists
    if ! jq -e ".mcpServers[\"$plugin_name\"]" "$mcp_json" > /dev/null 2>&1; then
        log_skip "MCP server '$plugin_name' not in .mcp.json"
        SKIPPED+=(".mcp.json: $plugin_name not present")
        return 0
    fi

    # Remove MCP server entry
    log_info "Removing MCP server '$plugin_name' from .mcp.json"
    local tmp_file=$(mktemp)
    jq "del(.mcpServers[\"$plugin_name\"])" "$mcp_json" > "$tmp_file"
    mv "$tmp_file" "$mcp_json"

    CHANGES_MADE+=("Removed $plugin_name from .mcp.json")
    log_success "Removed MCP server entry for '$plugin_name'"
}

# --- Remove from CLAUDE.md ---
remove_from_claude_md() {
    local plugin_name="$1"
    local target_path="$2"
    local target_claude_md="$target_path/CLAUDE.md"

    # Check if CLAUDE.md exists
    if [[ ! -f "$target_claude_md" ]]; then
        log_skip "No CLAUDE.md found - nothing to remove"
        SKIPPED+=("CLAUDE.md: File does not exist")
        return 0
    fi

    # Look for the plugin section header (handles multiple formats)
    # Formats: "# {plugin-name} Plugin - CLAUDE.md Integration" or "# {plugin-name} CLAUDE.md Integration"
    local section_header
    section_header=$(grep -E "^# ${plugin_name}( Plugin)? -? ?CLAUDE\.md Integration" "$target_claude_md" 2>/dev/null | head -1)

    if [[ -z "$section_header" ]]; then
        log_skip "Plugin '$plugin_name' section not found in CLAUDE.md"
        SKIPPED+=("CLAUDE.md: $plugin_name section not found")
        return 0
    fi

    log_info "Removing '$plugin_name' section from CLAUDE.md"

    # Create temp file and use awk to remove section
    # Remove from header to next "---" divider or next plugin header
    local tmp_file=$(mktemp)

    awk -v header="$section_header" '
    BEGIN { skip = 0; found = 0; in_code_block = 0 }
    {
        # Track code blocks (``` markers)
        if (/^```/) {
            in_code_block = !in_code_block
        }

        # Check if this is the section header we want to remove
        if ($0 == header) {
            skip = 1
            found = 1
            next
        }

        # Check if this is a horizontal rule (---) - only count if not in code block
        is_hr = /^---[[:space:]]*$/ && !in_code_block

        # Check if this is a new plugin section header (only outside code blocks)
        # Patterns: "# {name} Plugin - CLAUDE.md Integration" or "# {name} CLAUDE.md Integration"
        is_new_plugin_section = /^# [a-z-]+( Plugin)? -? ?CLAUDE\.md Integration/ && !in_code_block && $0 != header

        if (skip) {
            # Stop skipping when we hit --- (outside code block) or a new plugin section
            if (is_hr) {
                # This --- ends the section we are removing, skip it too
                skip = 0
                next
            }
            if (is_new_plugin_section) {
                # New plugin section starts, stop skipping and print it
                skip = 0
                print
            }
            next
        }

        # Not skipping - print the line
        print
    }
    END { if (!found) exit 1 }
    ' "$target_claude_md" > "$tmp_file" 2>/dev/null

    if [[ $? -eq 0 ]]; then
        # Clean up multiple consecutive blank lines
        awk 'NF{blank=0} !NF{blank++} blank<=2' "$tmp_file" > "${tmp_file}.clean"
        mv "${tmp_file}.clean" "$target_claude_md"
        rm -f "$tmp_file"
        CHANGES_MADE+=("Removed $plugin_name section from CLAUDE.md")
        log_success "Removed CLAUDE.md section for '$plugin_name'"
    else
        rm -f "$tmp_file"
        log_skip "Could not locate exact section boundaries in CLAUDE.md"
        log_warning "You may need to manually remove the $plugin_name section"
        SKIPPED+=("CLAUDE.md: Manual removal may be needed")
    fi
}

# --- Print Summary ---
print_summary() {
    local plugin_name="$1"
    local target_path="$2"

    echo ""
    echo "=============================================="
    echo -e "${GREEN}Uninstallation Summary${NC}"
    echo "=============================================="
    echo ""
    echo -e "${CYAN}Plugin:${NC} $plugin_name"
    echo -e "${CYAN}Target:${NC} $target_path"
    echo ""

    if [[ ${#CHANGES_MADE[@]} -gt 0 ]]; then
        echo -e "${GREEN}Changes Made:${NC}"
        for change in "${CHANGES_MADE[@]}"; do
            echo "  ✓ $change"
        done
        echo ""
    fi

    if [[ ${#SKIPPED[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Skipped (not present or N/A):${NC}"
        for skip in "${SKIPPED[@]}"; do
            echo "  - $skip"
        done
        echo ""
    fi

    if [[ ${#CHANGES_MADE[@]} -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  IMPORTANT:${NC}"
        echo "  Restart your Claude Code session for changes to take effect."
        echo ""
    fi
}

# =============================================================================
# Main Execution
# =============================================================================

# Check arguments
if [[ $# -lt 2 ]]; then
    usage
fi

PLUGIN_NAME="$1"
TARGET_PATH="$2"

# Resolve target path to absolute
TARGET_PATH=$(cd "$TARGET_PATH" 2>/dev/null && pwd || echo "$TARGET_PATH")

echo ""
echo "=============================================="
echo -e "${BLUE}Uninstalling Plugin: $PLUGIN_NAME${NC}"
echo "=============================================="
echo ""

# Run checks
check_prerequisites
validate_target "$TARGET_PATH"

echo ""

# Perform uninstallation
remove_from_mcp_json "$PLUGIN_NAME" "$TARGET_PATH"
remove_from_claude_md "$PLUGIN_NAME" "$TARGET_PATH"

# Print summary
print_summary "$PLUGIN_NAME" "$TARGET_PATH"
