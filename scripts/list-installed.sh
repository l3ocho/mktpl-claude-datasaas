#!/usr/bin/env bash
# =============================================================================
# list-installed.sh - Show installed marketplace plugins in a project
# =============================================================================
#
# Usage: ./scripts/list-installed.sh <target-project-path>
#
# This script:
# 1. Checks .mcp.json for MCP server entries from this marketplace
# 2. Checks CLAUDE.md for plugin integration sections
# 3. Reports which plugins are installed
#
# Examples:
#   ./scripts/list-installed.sh ~/projects/personal-portfolio
#   ./scripts/list-installed.sh .
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
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# --- Usage ---
usage() {
    echo "Usage: $0 <target-project-path>"
    echo ""
    echo "Show which marketplace plugins are installed in a project."
    echo ""
    echo "Arguments:"
    echo "  target-project-path Path to the target project (absolute or relative)"
    echo ""
    echo "Examples:"
    echo "  $0 ~/projects/personal-portfolio"
    echo "  $0 ."
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

# --- Get Available Plugins ---
get_available_plugins() {
    for dir in "$REPO_ROOT"/plugins/*/; do
        if [[ -d "$dir" ]]; then
            basename "$dir"
        fi
    done
}

# --- Get Plugins with MCP Servers ---
get_mcp_plugins() {
    for dir in "$REPO_ROOT"/mcp-servers/*/; do
        if [[ -d "$dir" && -f "$dir/run.sh" ]]; then
            basename "$dir"
        fi
    done
}

# --- Check MCP Installation ---
check_mcp_installed() {
    local plugin_name="$1"
    local target_path="$2"
    local mcp_json="$target_path/.mcp.json"

    if [[ ! -f "$mcp_json" ]]; then
        return 1
    fi

    # Check if this plugin's MCP server is referenced
    if jq -e ".mcpServers[\"$plugin_name\"]" "$mcp_json" > /dev/null 2>&1; then
        return 0
    fi

    # Also check if any entry points to this marketplace's mcp-servers
    if grep -q "leo-claude-mktplace.*mcp-servers/$plugin_name" "$mcp_json" 2>/dev/null || \
       grep -q "claude-plugins-work.*mcp-servers/$plugin_name" "$mcp_json" 2>/dev/null; then
        return 0
    fi

    return 1
}

# --- Check CLAUDE.md Integration ---
check_claude_md_installed() {
    local plugin_name="$1"
    local target_path="$2"
    local target_claude_md="$target_path/CLAUDE.md"

    if [[ ! -f "$target_claude_md" ]]; then
        return 1
    fi

    # Look for plugin-specific headers that install-plugin.sh adds
    # Formats vary by plugin:
    #   "# {plugin-name} Plugin - CLAUDE.md Integration"
    #   "# {plugin-name} CLAUDE.md Integration"
    # Use regex to match both patterns
    if grep -qE "^# ${plugin_name}( Plugin)? -? ?CLAUDE\.md Integration" "$target_claude_md" 2>/dev/null; then
        return 0
    fi

    return 1
}

# --- Get Plugin Version ---
get_plugin_version() {
    local plugin_name="$1"
    local plugin_json="$REPO_ROOT/plugins/$plugin_name/.claude-plugin/plugin.json"

    if [[ -f "$plugin_json" ]]; then
        jq -r '.version // "unknown"' "$plugin_json"
    else
        echo "unknown"
    fi
}

# --- Get Plugin Description ---
get_plugin_description() {
    local plugin_name="$1"
    local plugin_json="$REPO_ROOT/plugins/$plugin_name/.claude-plugin/plugin.json"

    if [[ -f "$plugin_json" ]]; then
        jq -r '.description // "No description"' "$plugin_json" | cut -c1-60
    else
        echo "No description"
    fi
}

# =============================================================================
# Main Execution
# =============================================================================

# Check arguments
if [[ $# -lt 1 ]]; then
    usage
fi

TARGET_PATH="$1"

# Resolve target path to absolute
if [[ -d "$TARGET_PATH" ]]; then
    TARGET_PATH=$(cd "$TARGET_PATH" && pwd)
else
    log_error "Target project path does not exist: $TARGET_PATH"
    exit 1
fi

check_prerequisites

echo ""
echo "=============================================="
echo -e "${BLUE}Installed Plugins: $(basename "$TARGET_PATH")${NC}"
echo "=============================================="
echo -e "${CYAN}Target:${NC} $TARGET_PATH"
echo ""

# Collect results
declare -A INSTALLED_MCP
declare -A INSTALLED_CLAUDE_MD
INSTALLED_PLUGINS=()
PARTIAL_PLUGINS=()
NOT_INSTALLED=()

# Check each available plugin
for plugin in $(get_available_plugins); do
    mcp_installed=false
    claude_installed=false
    has_mcp_server=false

    # Check if plugin has MCP server
    if [[ -d "$REPO_ROOT/mcp-servers/$plugin" ]]; then
        has_mcp_server=true
    fi

    # Check MCP installation (only if plugin has MCP server)
    if $has_mcp_server && check_mcp_installed "$plugin" "$TARGET_PATH"; then
        mcp_installed=true
        INSTALLED_MCP[$plugin]=true
    fi

    # Check CLAUDE.md integration
    if check_claude_md_installed "$plugin" "$TARGET_PATH"; then
        claude_installed=true
        INSTALLED_CLAUDE_MD[$plugin]=true
    fi

    # Categorize
    if $mcp_installed || $claude_installed; then
        if $has_mcp_server; then
            if $mcp_installed && $claude_installed; then
                INSTALLED_PLUGINS+=("$plugin")
            else
                PARTIAL_PLUGINS+=("$plugin")
            fi
        else
            # Plugins without MCP servers just need CLAUDE.md
            if $claude_installed; then
                INSTALLED_PLUGINS+=("$plugin")
            fi
        fi
    else
        NOT_INSTALLED+=("$plugin")
    fi
done

# Print fully installed plugins
if [[ ${#INSTALLED_PLUGINS[@]} -gt 0 ]]; then
    echo -e "${GREEN}✓ Fully Installed:${NC}"
    echo ""
    printf "  %-24s %-10s %s\n" "PLUGIN" "VERSION" "DESCRIPTION"
    printf "  %-24s %-10s %s\n" "------" "-------" "-----------"
    for plugin in "${INSTALLED_PLUGINS[@]}"; do
        version=$(get_plugin_version "$plugin")
        desc=$(get_plugin_description "$plugin")
        printf "  %-24s %-10s %s\n" "$plugin" "$version" "$desc"
    done
    echo ""
fi

# Print partially installed plugins
if [[ ${#PARTIAL_PLUGINS[@]} -gt 0 ]]; then
    echo -e "${YELLOW}⚠ Partially Installed:${NC}"
    echo ""
    for plugin in "${PARTIAL_PLUGINS[@]}"; do
        version=$(get_plugin_version "$plugin")
        echo "  $plugin (v$version)"
        if [[ -v INSTALLED_MCP[$plugin] ]]; then
            echo "    ✓ MCP server configured in .mcp.json"
        else
            echo "    ✗ MCP server NOT in .mcp.json"
        fi
        if [[ -v INSTALLED_CLAUDE_MD[$plugin] ]]; then
            echo "    ✓ Integration in CLAUDE.md"
        else
            echo "    ✗ Integration NOT in CLAUDE.md"
        fi
        echo ""
    done
    echo "  Run install-plugin.sh to complete installation."
    echo ""
fi

# Print available but not installed
if [[ ${#NOT_INSTALLED[@]} -gt 0 ]]; then
    echo -e "${BLUE}○ Available (not installed):${NC}"
    echo ""
    for plugin in "${NOT_INSTALLED[@]}"; do
        version=$(get_plugin_version "$plugin")
        desc=$(get_plugin_description "$plugin")
        printf "  %-24s %-10s %s\n" "$plugin" "$version" "$desc"
    done
    echo ""
fi

# Summary
echo "----------------------------------------------"
total_available=$(get_available_plugins | wc -l)
total_installed=${#INSTALLED_PLUGINS[@]}
total_partial=${#PARTIAL_PLUGINS[@]}

echo -e "Total: ${GREEN}$total_installed installed${NC}"
if [[ $total_partial -gt 0 ]]; then
    echo -e "       ${YELLOW}$total_partial partial${NC}"
fi
echo "       $((total_available - total_installed - total_partial)) available"
echo ""

# Install hint
if [[ ${#NOT_INSTALLED[@]} -gt 0 ]]; then
    echo "To install a plugin:"
    echo "  $SCRIPT_DIR/install-plugin.sh <plugin-name> $TARGET_PATH"
    echo ""
fi
