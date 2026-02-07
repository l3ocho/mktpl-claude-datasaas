#!/usr/bin/env bash
#
# claude-launch.sh - Launch Claude Code with task-specific plugin profiles
#
# Usage: ./scripts/claude-launch.sh [profile] [extra-args...]
#
# Profiles:
#   sprint  - Project management, git, PR review, security, docs (default)
#   data    - Data engineering and visualization
#   saas    - SaaS development (API, frontend, DB, testing)
#   ops     - Operations and infrastructure (CMDB, releases, deploy)
#   review  - Code review only (lightweight)
#   debug   - MCP debugging tools
#   full    - All plugins via marketplace.json (~22K tokens)
#
# Examples:
#   ./scripts/claude-launch.sh                    # Default sprint profile
#   ./scripts/claude-launch.sh sprint             # Explicit sprint profile
#   ./scripts/claude-launch.sh data --model opus  # Data profile with Opus
#   ./scripts/claude-launch.sh full               # Load all plugins
#

set -euo pipefail

# Colors for output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory (for relative plugin paths)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PLUGINS_DIR="$REPO_ROOT/plugins"

# Default profile
PROFILE="${1:-sprint}"

# Shift profile arg if provided (to pass remaining args to claude)
if [[ $# -gt 0 ]]; then
    shift
fi

# Define plugin lists for each profile
declare -A PROFILES
PROFILES[sprint]="projman git-flow pr-review code-sentinel doc-guardian clarity-assist"
PROFILES[infra]="DEPRECATED"
PROFILES[data]="data-platform viz-platform data-seed"
PROFILES[saas]="saas-api-platform saas-react-platform saas-db-migrate saas-test-pilot"
PROFILES[ops]="cmdb-assistant ops-release-manager ops-deploy-pipeline"
PROFILES[review]="pr-review code-sentinel"
PROFILES[debug]="debug-mcp"
PROFILES[full]=""  # Empty = use marketplace.json

# Validate profile
if [[ ! ${PROFILES[$PROFILE]+_} ]]; then
    echo -e "${YELLOW}Unknown profile: $PROFILE${NC}"
    echo "Available profiles: sprint, data, saas, ops, review, debug, full"
    exit 1
fi

# Handle deprecated profiles
if [[ "$PROFILE" == "infra" ]]; then
    echo -e "${YELLOW}Warning: 'infra' profile is deprecated. Use 'ops' instead.${NC}"
    echo -e "${YELLOW}   The 'ops' profile includes cmdb-assistant plus future ops plugins.${NC}"
    PROFILE="ops"
fi

# Build --plugin-dir arguments
PLUGIN_ARGS=()
PLUGIN_LIST="${PROFILES[$PROFILE]}"

if [[ -n "$PLUGIN_LIST" ]]; then
    echo -e "${CYAN}Profile: $PROFILE${NC}"
    echo -e "${GREEN}Loading plugins:${NC}"

    for plugin in $PLUGIN_LIST; do
        plugin_path="$PLUGINS_DIR/$plugin"
        if [[ -d "$plugin_path" ]]; then
            echo "  • $plugin"
            PLUGIN_ARGS+=("--plugin-dir" "$plugin_path")
        else
            echo -e "${YELLOW}  ⚠ $plugin (not found at $plugin_path)${NC}"
        fi
    done
    echo ""
else
    echo -e "${CYAN}Profile: full${NC}"
    echo -e "${GREEN}Loading all plugins via marketplace.json${NC}"
    echo ""
fi

# Enable MCP Tool Search for deferred tool loading
export ENABLE_TOOL_SEARCH=true
echo -e "${GREEN}MCP Tool Search: enabled${NC}"
echo ""

# Launch claude with plugin args and any extra arguments
if [[ ${#PLUGIN_ARGS[@]} -gt 0 ]]; then
    exec claude "${PLUGIN_ARGS[@]}" "$@"
else
    exec claude "$@"
fi
