#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Validating Marketplace ==="

# Check marketplace.json exists and is valid JSON
MARKETPLACE_JSON="$ROOT_DIR/.claude-plugin/marketplace.json"
if [[ ! -f "$MARKETPLACE_JSON" ]]; then
    echo "ERROR: Missing $MARKETPLACE_JSON"
    exit 1
fi

if ! jq empty "$MARKETPLACE_JSON" 2>/dev/null; then
    echo "ERROR: Invalid JSON in marketplace.json"
    exit 1
fi
echo "✓ marketplace.json is valid JSON"

# Check required fields
if ! jq -e '.name' "$MARKETPLACE_JSON" >/dev/null; then
    echo "ERROR: Missing 'name' field in marketplace.json"
    exit 1
fi

if ! jq -e '.owner.name' "$MARKETPLACE_JSON" >/dev/null; then
    echo "ERROR: Missing 'owner.name' field in marketplace.json"
    exit 1
fi

if ! jq -e '.owner.email' "$MARKETPLACE_JSON" >/dev/null; then
    echo "ERROR: Missing 'owner.email' field in marketplace.json"
    exit 1
fi
echo "✓ Required marketplace fields present"

# Check plugins array exists
if ! jq -e '.plugins | type == "array"' "$MARKETPLACE_JSON" >/dev/null; then
    echo "ERROR: Missing or invalid 'plugins' array in marketplace.json"
    exit 1
fi

# Check each plugin entry in marketplace.json
PLUGIN_COUNT=$(jq '.plugins | length' "$MARKETPLACE_JSON")
echo "Found $PLUGIN_COUNT plugins in marketplace.json"

for i in $(seq 0 $((PLUGIN_COUNT - 1))); do
    PLUGIN_NAME=$(jq -r ".plugins[$i].name" "$MARKETPLACE_JSON")
    echo "--- Checking marketplace entry: $PLUGIN_NAME ---"

    # Check required fields in marketplace entry
    for field in name source description version; do
        if ! jq -e ".plugins[$i].$field" "$MARKETPLACE_JSON" >/dev/null; then
            echo "ERROR: Missing '$field' in marketplace entry for $PLUGIN_NAME"
            exit 1
        fi
    done

    # Check author field
    if ! jq -e ".plugins[$i].author.name" "$MARKETPLACE_JSON" >/dev/null; then
        echo "ERROR: Missing 'author.name' in marketplace entry for $PLUGIN_NAME"
        exit 1
    fi

    # Check homepage and repository
    if ! jq -e ".plugins[$i].homepage" "$MARKETPLACE_JSON" >/dev/null; then
        echo "WARNING: Missing 'homepage' in marketplace entry for $PLUGIN_NAME"
    fi

    if ! jq -e ".plugins[$i].repository" "$MARKETPLACE_JSON" >/dev/null; then
        echo "WARNING: Missing 'repository' in marketplace entry for $PLUGIN_NAME"
    fi

    # v3.0.0: Check category, tags, license fields
    if ! jq -e ".plugins[$i].category" "$MARKETPLACE_JSON" >/dev/null; then
        echo "ERROR: Missing 'category' in marketplace entry for $PLUGIN_NAME (required v3.0.0+)"
        exit 1
    fi

    if ! jq -e ".plugins[$i].tags | type == \"array\"" "$MARKETPLACE_JSON" >/dev/null; then
        echo "ERROR: Missing or invalid 'tags' array in marketplace entry for $PLUGIN_NAME (required v3.0.0+)"
        exit 1
    fi

    if ! jq -e ".plugins[$i].license" "$MARKETPLACE_JSON" >/dev/null; then
        echo "ERROR: Missing 'license' in marketplace entry for $PLUGIN_NAME (required v3.0.0+)"
        exit 1
    fi

    echo "✓ Marketplace entry $PLUGIN_NAME valid"
done

# Validate each plugin directory
PLUGINS_DIR="$ROOT_DIR/plugins"
echo ""
echo "=== Validating Plugin Directories ==="

for plugin_dir in "$PLUGINS_DIR"/*/; do
    plugin_name=$(basename "$plugin_dir")
    echo "--- Checking plugin directory: $plugin_name ---"

    # Check plugin.json exists
    plugin_json="$plugin_dir.claude-plugin/plugin.json"
    if [[ ! -f "$plugin_json" ]]; then
        echo "WARNING: Missing plugin.json in $plugin_name/.claude-plugin/"
        continue
    fi

    # Validate JSON syntax
    if ! jq empty "$plugin_json" 2>/dev/null; then
        echo "ERROR: Invalid JSON in $plugin_name/plugin.json"
        exit 1
    fi

    # Check required plugin fields
    for field in name description version; do
        if ! jq -e ".$field" "$plugin_json" >/dev/null; then
            echo "ERROR: Missing '$field' in $plugin_name/plugin.json"
            exit 1
        fi
    done

    # Check recommended fields
    if ! jq -e '.author.name' "$plugin_json" >/dev/null; then
        echo "WARNING: Missing 'author.name' in $plugin_name/plugin.json"
    fi

    if ! jq -e '.homepage' "$plugin_json" >/dev/null; then
        echo "WARNING: Missing 'homepage' in $plugin_name/plugin.json"
    fi

    if ! jq -e '.repository' "$plugin_json" >/dev/null; then
        echo "WARNING: Missing 'repository' in $plugin_name/plugin.json"
    fi

    if ! jq -e '.license' "$plugin_json" >/dev/null; then
        echo "WARNING: Missing 'license' in $plugin_name/plugin.json"
    fi

    if ! jq -e '.keywords | type == "array"' "$plugin_json" >/dev/null; then
        echo "WARNING: Missing 'keywords' array in $plugin_name/plugin.json"
    fi

    # Check README exists
    if [[ ! -f "$plugin_dir/README.md" ]]; then
        echo "WARNING: Missing README.md in $plugin_name/"
    fi

    echo "✓ $plugin_name valid"
done

# v3.0.0: Validate MCP server symlinks
echo ""
echo "=== Validating MCP Server Symlinks (v3.0.0+) ==="

# Check shared MCP servers exist
if [[ ! -d "$ROOT_DIR/mcp-servers/gitea" ]]; then
    echo "ERROR: Shared gitea MCP server not found at mcp-servers/gitea/"
    exit 1
fi
echo "✓ Shared gitea MCP server exists"

if [[ ! -d "$ROOT_DIR/mcp-servers/netbox" ]]; then
    echo "ERROR: Shared netbox MCP server not found at mcp-servers/netbox/"
    exit 1
fi
echo "✓ Shared netbox MCP server exists"

if [[ ! -d "$ROOT_DIR/mcp-servers/data-platform" ]]; then
    echo "ERROR: Shared data-platform MCP server not found at mcp-servers/data-platform/"
    exit 1
fi
echo "✓ Shared data-platform MCP server exists"

# Check symlinks for plugins that use MCP servers
check_mcp_symlink() {
    local plugin_name="$1"
    local server_name="$2"
    local symlink_path="$ROOT_DIR/plugins/$plugin_name/mcp-servers/$server_name"

    if [[ -L "$symlink_path" ]]; then
        # Verify symlink resolves correctly
        if [[ -d "$symlink_path" ]]; then
            echo "✓ $plugin_name -> $server_name symlink valid"
        else
            echo "ERROR: $plugin_name -> $server_name symlink broken (does not resolve)"
            exit 1
        fi
    else
        echo "ERROR: Missing symlink at plugins/$plugin_name/mcp-servers/$server_name"
        exit 1
    fi
}

# Plugins with gitea MCP dependency
check_mcp_symlink "projman" "gitea"
check_mcp_symlink "pr-review" "gitea"

# Plugins with netbox MCP dependency
check_mcp_symlink "cmdb-assistant" "netbox"

# Plugins with data-platform MCP dependency
check_mcp_symlink "data-platform" "data-platform"

echo ""
echo "=== All validations passed ==="
