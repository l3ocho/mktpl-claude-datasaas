#!/usr/bin/env bash
# =============================================================================
# install-plugin.sh - Install marketplace plugin to a consumer project
# =============================================================================
#
# Usage: ./scripts/install-plugin.sh <plugin-name> <target-project-path> [--profile <profile-name>]
#
# This script:
# 1. Validates plugin exists in the marketplace
# 2. Updates target project's .mcp.json with MCP server entries (if applicable)
# 3. Appends CLAUDE.md integration snippet to target project
# 4. Is idempotent (safe to run multiple times)
#
# Examples:
#   ./scripts/install-plugin.sh data-platform ~/projects/personal-portfolio
#   ./scripts/install-plugin.sh data-platform ~/projects/webapp --profile readonly
#   ./scripts/install-plugin.sh projman /home/user/my-project
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
MCP_SERVERS_INSTALLED=()

# --- Usage ---
usage() {
    echo "Usage: $0 <plugin-name> <target-project-path> [--profile <profile-name>]"
    echo ""
    echo "Install a marketplace plugin to a consumer project."
    echo ""
    echo "Arguments:"
    echo "  plugin-name         Name of the plugin (e.g., data-platform, viz-platform, projman)"
    echo "  target-project-path Path to the target project (absolute or relative)"
    echo ""
    echo "Options:"
    echo "  --profile <name>    Integration profile to install (default: \"default\")"
    echo "                      Use \"readonly\" for read-only consumer projects (e.g., webapps)"
    echo "                      Available profiles depend on the plugin."
    echo ""
    echo "Available plugins:"
    for dir in "$REPO_ROOT"/plugins/*/; do
        if [[ -d "$dir" ]]; then
            basename "$dir"
        fi
    done
    echo ""
    echo "Examples:"
    echo "  $0 data-platform ~/projects/dataflow"
    echo "  $0 data-platform ~/projects/webapp --profile readonly"
    echo "  $0 viz-platform ~/projects/webapp"
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

# --- Validate Plugin Exists ---
validate_plugin() {
    local plugin_name="$1"
    local plugin_dir="$REPO_ROOT/plugins/$plugin_name"

    if [[ ! -d "$plugin_dir" ]]; then
        log_error "Plugin '$plugin_name' not found in $REPO_ROOT/plugins/"
        echo ""
        echo "Available plugins:"
        for dir in "$REPO_ROOT"/plugins/*/; do
            if [[ -d "$dir" ]]; then
                echo "  - $(basename "$dir")"
            fi
        done
        exit 1
    fi

    if [[ ! -f "$plugin_dir/.claude-plugin/plugin.json" ]]; then
        log_error "Plugin '$plugin_name' missing .claude-plugin/plugin.json"
        exit 1
    fi

    log_success "Plugin '$plugin_name' found"
}

# --- Validate Target Project ---
validate_target() {
    local target_path="$1"

    if [[ ! -d "$target_path" ]]; then
        log_error "Target project path does not exist: $target_path"
        exit 1
    fi

    log_success "Target project found: $target_path"

    # Warn if no CLAUDE.md
    if [[ ! -f "$target_path/CLAUDE.md" ]]; then
        log_warning "Target project has no CLAUDE.md - will create one"
    fi
}

# --- Get MCP Servers for Plugin ---
# Reads the mcp_servers array from metadata.json (separate from plugin.json to avoid schema validation issues)
# Returns newline-separated list of MCP server names, or empty if none
get_mcp_servers() {
    local plugin_name="$1"
    local metadata_json="$REPO_ROOT/plugins/$plugin_name/.claude-plugin/metadata.json"

    if [[ ! -f "$metadata_json" ]]; then
        return
    fi

    # Read mcp_servers array from metadata.json
    # Returns empty if field doesn't exist or is empty
    jq -r '.mcp_servers // [] | .[]' "$metadata_json" 2>/dev/null || true
}

# --- Check if plugin has any MCP servers ---
has_mcp_servers() {
    local plugin_name="$1"
    local servers
    servers=$(get_mcp_servers "$plugin_name")
    [[ -n "$servers" ]]
}

# --- Get Available Profiles for Plugin ---
# Returns space-separated list of profile names, or empty if plugin has no profiles
get_available_profiles() {
    local plugin_name="$1"
    local integration_file="$REPO_ROOT/plugins/$plugin_name/claude-md-integration.md"

    if [[ ! -f "$integration_file" ]]; then
        return
    fi

    # Extract profile names from <!-- BEGIN plugin_name:profile_name --> markers
    grep "<!-- BEGIN ${plugin_name}:" "$integration_file" 2>/dev/null \
        | sed "s|<!-- BEGIN ${plugin_name}:||;s| -->||" \
        | tr '\n' ' ' \
        | sed 's/ *$//'
}

# --- Update .mcp.json ---
update_mcp_json() {
    local plugin_name="$1"
    local target_path="$2"
    local mcp_json="$target_path/.mcp.json"

    # Get MCP servers for this plugin
    local mcp_servers
    mcp_servers=$(get_mcp_servers "$plugin_name")

    if [[ -z "$mcp_servers" ]]; then
        log_skip "Plugin '$plugin_name' has no MCP servers - skipping .mcp.json update"
        SKIPPED+=(".mcp.json: No MCP servers for $plugin_name")
        return 0
    fi

    # Create .mcp.json if it doesn't exist
    if [[ ! -f "$mcp_json" ]]; then
        log_info "Creating new .mcp.json"
        echo '{"mcpServers":{}}' > "$mcp_json"
        CHANGES_MADE+=("Created .mcp.json")
    fi

    # Add each MCP server
    local servers_added=0
    while IFS= read -r server_name; do
        [[ -z "$server_name" ]] && continue

        local mcp_server_path="$REPO_ROOT/mcp-servers/$server_name/run.sh"

        # Verify server exists
        if [[ ! -f "$mcp_server_path" ]]; then
            log_warning "MCP server '$server_name' not found at $mcp_server_path"
            continue
        fi

        # Check if entry already exists
        if jq -e ".mcpServers[\"$server_name\"]" "$mcp_json" > /dev/null 2>&1; then
            log_skip "MCP server '$server_name' already in .mcp.json"
            SKIPPED+=(".mcp.json: $server_name already present")
            continue
        fi

        # Add MCP server entry
        log_info "Adding MCP server '$server_name' to .mcp.json"
        local tmp_file=$(mktemp)
        jq ".mcpServers[\"$server_name\"] = {\"command\": \"$mcp_server_path\", \"args\": []}" "$mcp_json" > "$tmp_file"
        mv "$tmp_file" "$mcp_json"

        CHANGES_MADE+=("Added $server_name to .mcp.json")
        MCP_SERVERS_INSTALLED+=("$server_name")
        log_success "Added MCP server entry for '$server_name'"
        ((++servers_added))
    done <<< "$mcp_servers"
}

# --- Update CLAUDE.md ---
update_claude_md() {
    local plugin_name="$1"
    local target_path="$2"
    local target_claude_md="$target_path/CLAUDE.md"
    local integration_file="$REPO_ROOT/plugins/$plugin_name/claude-md-integration.md"

    # Check if integration file exists
    if [[ ! -f "$integration_file" ]]; then
        log_skip "No claude-md-integration.md for plugin '$plugin_name'"
        SKIPPED+=("CLAUDE.md: No integration snippet for $plugin_name")
        return 0
    fi

    # Create CLAUDE.md if it doesn't exist
    if [[ ! -f "$target_claude_md" ]]; then
        log_info "Creating new CLAUDE.md"
        cat > "$target_claude_md" << 'EOF'
# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

EOF
        CHANGES_MADE+=("Created CLAUDE.md")
    fi

    # Check if already integrated using HTML comment marker (preferred)
    local begin_marker="<!-- BEGIN marketplace-plugin: $plugin_name -->"
    if grep -qF "$begin_marker" "$target_claude_md" 2>/dev/null; then
        log_skip "Plugin '$plugin_name' integration already in CLAUDE.md"
        SKIPPED+=("CLAUDE.md: $plugin_name already present")
        return 0
    fi

    # Fallback: check for legacy header format (backward compatibility)
    if grep -qE "^# ${plugin_name}( Plugin)? -? ?CLAUDE\.md Integration" "$target_claude_md" 2>/dev/null; then
        log_skip "Plugin '$plugin_name' integration already in CLAUDE.md (legacy format)"
        SKIPPED+=("CLAUDE.md: $plugin_name already present")
        return 0
    fi

    # Determine integration content based on profile
    local profile_begin_marker="<!-- BEGIN ${plugin_name}:${PROFILE} -->"
    local profile_end_marker="<!-- END ${plugin_name}:${PROFILE} -->"
    local integration_content

    if grep -qF "$profile_begin_marker" "$integration_file" 2>/dev/null; then
        # Profile markers exist - extract content between them
        log_info "Extracting profile '${PROFILE}' from integration file"
        integration_content=$(awk -v begin="$profile_begin_marker" -v end="$profile_end_marker" \
            '{ if (found) {
                 if ($0 == end) exit
                 print
               } else if ($0 == begin) {
                 found = 1
               }
             }' "$integration_file")

        if [[ -z "$integration_content" ]]; then
            log_error "Profile '${PROFILE}' marker found but content is empty"
            exit 1
        fi
    elif [[ "$PROFILE" == "default" ]]; then
        # No profile markers and using default - inject entire file (backward compat)
        log_info "No profile markers found - injecting full integration file"
        integration_content=$(cat "$integration_file")
    else
        # Non-default profile requested but not found
        local available_profiles
        available_profiles=$(get_available_profiles "$plugin_name")
        log_error "Profile '${PROFILE}' not found in ${plugin_name}'s claude-md-integration.md."
        if [[ -n "$available_profiles" ]]; then
            echo "  Available profiles: $available_profiles"
        else
            echo "  This plugin has no profiles defined. Omit --profile to install the full integration."
        fi
        exit 1
    fi

    # Check for or create Marketplace Plugin Integration section
    local section_header="## Marketplace Plugin Integration"

    if ! grep -qF "$section_header" "$target_claude_md"; then
        log_info "Creating '$section_header' section"
        echo "" >> "$target_claude_md"
        echo "$section_header" >> "$target_claude_md"
        echo "" >> "$target_claude_md"
        echo "The following plugins are installed from the mktpl-claude-datasaas:" >> "$target_claude_md"
        echo "" >> "$target_claude_md"
    fi

    # Append integration content with HTML comment markers
    log_info "Adding '$plugin_name' integration to CLAUDE.md (profile: ${PROFILE})"
    local end_marker="<!-- END marketplace-plugin: $plugin_name -->"

    echo "" >> "$target_claude_md"
    echo "---" >> "$target_claude_md"
    echo "" >> "$target_claude_md"
    echo "$begin_marker" >> "$target_claude_md"
    echo "<!-- profile: ${PROFILE} -->" >> "$target_claude_md"
    echo "" >> "$target_claude_md"
    echo "$integration_content" >> "$target_claude_md"
    echo "" >> "$target_claude_md"
    echo "$end_marker" >> "$target_claude_md"

    CHANGES_MADE+=("Added $plugin_name integration to CLAUDE.md (profile: ${PROFILE})")
    log_success "Added CLAUDE.md integration for '$plugin_name' (profile: ${PROFILE})"
}

# --- Get Commands for Plugin ---
get_plugin_commands() {
    local plugin_name="$1"
    local commands_dir="$REPO_ROOT/plugins/$plugin_name/commands"

    if [[ ! -d "$commands_dir" ]]; then
        return
    fi

    for cmd_file in "$commands_dir"/*.md; do
        if [[ -f "$cmd_file" ]]; then
            local cmd_name
            cmd_name=$(basename "$cmd_file" .md)
            echo "  /$cmd_name"
        fi
    done
}

# --- Print Summary ---
print_summary() {
    local plugin_name="$1"
    local target_path="$2"

    echo ""
    echo "=============================================="
    echo -e "${GREEN}Installation Summary${NC}"
    echo "=============================================="
    echo ""
    echo -e "${CYAN}Plugin:${NC} $plugin_name"
    echo -e "${CYAN}Target:${NC} $target_path"

    # Show profile if non-default or if plugin has profiles defined
    local available_profiles
    available_profiles=$(get_available_profiles "$plugin_name")
    if [[ "$PROFILE" != "default" ]] || [[ -n "$available_profiles" ]]; then
        echo -e "${CYAN}Profile:${NC} $PROFILE"
    fi
    echo ""

    if [[ ${#CHANGES_MADE[@]} -gt 0 ]]; then
        echo -e "${GREEN}Changes Made:${NC}"
        for change in "${CHANGES_MADE[@]}"; do
            echo "  ✓ $change"
        done
        echo ""
    fi

    if [[ ${#SKIPPED[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Skipped (already present or N/A):${NC}"
        for skip in "${SKIPPED[@]}"; do
            echo "  - $skip"
        done
        echo ""
    fi

    # Show available commands
    echo -e "${CYAN}Commands Now Available:${NC}"
    local commands
    commands=$(get_plugin_commands "$plugin_name")
    if [[ -n "$commands" ]]; then
        echo "$commands"
    else
        echo "  (No commands - this plugin may be hooks-only)"
    fi
    echo ""

    # MCP servers info
    if [[ ${#MCP_SERVERS_INSTALLED[@]} -gt 0 ]]; then
        echo -e "${CYAN}MCP Servers Installed:${NC}"
        for server in "${MCP_SERVERS_INSTALLED[@]}"; do
            echo "  - $server"
        done
        echo ""
    elif has_mcp_servers "$plugin_name"; then
        echo -e "${CYAN}MCP Tools:${NC}"
        echo "  This plugin includes MCP server tools. Use ToolSearch to discover them."
        echo ""
    fi

    # Important reminder
    echo -e "${YELLOW}⚠️  IMPORTANT:${NC}"
    echo "  Restart your Claude Code session for changes to take effect."
    echo "  The .mcp.json changes require a session restart to load MCP servers."
    echo ""
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
PROFILE="default"

# Parse optional flags
shift 2
while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile)
            if [[ $# -lt 2 ]]; then
                log_error "--profile requires a value"
                usage
            fi
            PROFILE="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            ;;
    esac
done

# Resolve target path to absolute
TARGET_PATH=$(cd "$TARGET_PATH" 2>/dev/null && pwd || echo "$TARGET_PATH")

echo ""
echo "=============================================="
echo -e "${BLUE}Installing Plugin: $PLUGIN_NAME${NC}"
echo "=============================================="
echo ""

# Run checks
check_prerequisites
validate_plugin "$PLUGIN_NAME"
validate_target "$TARGET_PATH"

echo ""

# Perform installation
update_mcp_json "$PLUGIN_NAME" "$TARGET_PATH"
update_claude_md "$PLUGIN_NAME" "$TARGET_PATH"

# Print summary
print_summary "$PLUGIN_NAME" "$TARGET_PATH"
