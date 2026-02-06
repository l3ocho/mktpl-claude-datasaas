#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# v8.0.0: Valid domain values
VALID_DOMAINS="core data saas ops debug"

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

    # v8.0.0: Check domain field
    PLUGIN_DOMAIN=$(jq -r ".plugins[$i].domain // empty" "$MARKETPLACE_JSON")
    if [[ -z "$PLUGIN_DOMAIN" ]]; then
        echo "ERROR: Missing 'domain' in marketplace entry for $PLUGIN_NAME (required v8.0.0+)"
        exit 1
    fi
    if ! echo "$VALID_DOMAINS" | grep -qw "$PLUGIN_DOMAIN"; then
        echo "ERROR: Invalid domain '$PLUGIN_DOMAIN' in marketplace entry for $PLUGIN_NAME (allowed: $VALID_DOMAINS)"
        exit 1
    fi
    echo "  ✓ domain: $PLUGIN_DOMAIN"

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

    # v8.0.0: Check domain field in plugin.json
    PLUGIN_DOMAIN_PJ=$(jq -r '.domain // empty' "$plugin_json")
    if [[ -z "$PLUGIN_DOMAIN_PJ" ]]; then
        echo "ERROR: Missing 'domain' in $plugin_name/plugin.json (required v8.0.0+)"
        exit 1
    fi
    if ! echo "$VALID_DOMAINS" | grep -qw "$PLUGIN_DOMAIN_PJ"; then
        echo "ERROR: Invalid domain '$PLUGIN_DOMAIN_PJ' in $plugin_name/plugin.json (allowed: $VALID_DOMAINS)"
        exit 1
    fi
    echo "  ✓ domain: $PLUGIN_DOMAIN_PJ"

    # Check README exists
    if [[ ! -f "$plugin_dir/README.md" ]]; then
        echo "WARNING: Missing README.md in $plugin_name/"
    fi

    # CRITICAL: Validate file references exist (mcpServers, hooks, commands)
    # This prevents broken references that silently break plugin loading

    # Check mcpServers references
    mcp_servers=$(jq -r '.mcpServers // [] | .[]' "$plugin_json" 2>/dev/null)
    for mcp_ref in $mcp_servers; do
        mcp_path="$plugin_dir/$mcp_ref"
        if [[ ! -f "$mcp_path" ]]; then
            echo "ERROR: BROKEN REFERENCE in $plugin_name/plugin.json"
            echo "       mcpServers references '$mcp_ref' but file does not exist at:"
            echo "       $mcp_path"
            echo ""
            echo "       FIX: Either create the file or remove the mcpServers entry"
            exit 1
        fi
        echo "  ✓ mcpServers reference: $mcp_ref exists"
    done

    # Check hooks references (can be array of file paths OR object with handlers)
    hooks_type=$(jq -r '.hooks | type' "$plugin_json" 2>/dev/null)
    if [[ "$hooks_type" == "array" ]]; then
        # Array format: ["./hooks/hooks.json"]
        hooks=$(jq -r '.hooks[]' "$plugin_json" 2>/dev/null)
        for hook_ref in $hooks; do
            hook_path="$plugin_dir/$hook_ref"
            if [[ ! -f "$hook_path" ]]; then
                echo "ERROR: BROKEN REFERENCE in $plugin_name/plugin.json"
                echo "       hooks references '$hook_ref' but file does not exist at:"
                echo "       $hook_path"
                echo ""
                echo "       FIX: Either create the file or remove the hooks entry"
                exit 1
            fi
            echo "  ✓ hooks reference: $hook_ref exists"
        done
    elif [[ "$hooks_type" == "object" ]]; then
        # Object format: { "PostToolUse": [...] } - inline hooks, no file reference to validate
        echo "  ✓ hooks: inline object format (no file references)"
    fi

    # Check commands directory references
    commands=$(jq -r '.commands // [] | .[]' "$plugin_json" 2>/dev/null)
    for cmd_ref in $commands; do
        cmd_path="$plugin_dir/$cmd_ref"
        if [[ ! -d "$cmd_path" ]] && [[ ! -f "$cmd_path" ]]; then
            echo "ERROR: BROKEN REFERENCE in $plugin_name/plugin.json"
            echo "       commands references '$cmd_ref' but path does not exist at:"
            echo "       $cmd_path"
            echo ""
            echo "       FIX: Either create the path or remove the commands entry"
            exit 1
        fi
        echo "  ✓ commands reference: $cmd_ref exists"
    done

    echo "✓ $plugin_name valid"
done

echo ""
echo "=== Validating Plugin Metadata (MCP Mappings) ==="

for plugin_dir in "$PLUGINS_DIR"/*/; do
    plugin_name=$(basename "$plugin_dir")
    metadata_json="$plugin_dir.claude-plugin/metadata.json"

    if jq -e '.mcp_servers' "$plugin_dir.claude-plugin/plugin.json" >/dev/null 2>&1; then
        echo "ERROR: $plugin_name/plugin.json contains 'mcp_servers' — move to metadata.json"
        exit 1
    fi

    if [[ -f "$metadata_json" ]]; then
        if ! jq empty "$metadata_json" 2>/dev/null; then
            echo "ERROR: Invalid JSON in $plugin_name/.claude-plugin/metadata.json"
            exit 1
        fi
        mcp_servers=$(jq -r '.mcp_servers // [] | .[]' "$metadata_json" 2>/dev/null)
        for server in $mcp_servers; do
            if [[ ! -d "$ROOT_DIR/mcp-servers/$server" ]]; then
                echo "ERROR: $plugin_name metadata.json references '$server' but mcp-servers/$server/ missing"
                exit 1
            fi
            echo "  ✓ $plugin_name → $server"
        done
    fi
done
echo "✓ Plugin metadata validation passed"

# CRITICAL: Validate marketplace.json file references
echo ""
echo "=== Validating Marketplace File References (CRITICAL) ==="

for i in $(seq 0 $((PLUGIN_COUNT - 1))); do
    PLUGIN_NAME=$(jq -r ".plugins[$i].name" "$MARKETPLACE_JSON")
    PLUGIN_SOURCE=$(jq -r ".plugins[$i].source" "$MARKETPLACE_JSON")
    PLUGIN_DIR="$ROOT_DIR/$PLUGIN_SOURCE"

    # Check mcpServers in marketplace.json
    mcp_servers=$(jq -r ".plugins[$i].mcpServers // [] | .[]" "$MARKETPLACE_JSON" 2>/dev/null)
    for mcp_ref in $mcp_servers; do
        mcp_path="$PLUGIN_DIR/$mcp_ref"
        if [[ ! -f "$mcp_path" ]]; then
            echo "ERROR: BROKEN REFERENCE in marketplace.json for $PLUGIN_NAME"
            echo "       mcpServers references '$mcp_ref' but file does not exist at:"
            echo "       $mcp_path"
            echo ""
            echo "       FIX: Either create the file or remove the mcpServers entry from marketplace.json"
            exit 1
        fi
        echo "✓ $PLUGIN_NAME: mcpServers reference $mcp_ref exists"
    done

    # Check hooks in marketplace.json
    hooks=$(jq -r ".plugins[$i].hooks // [] | .[]" "$MARKETPLACE_JSON" 2>/dev/null)
    for hook_ref in $hooks; do
        hook_path="$PLUGIN_DIR/$hook_ref"
        if [[ ! -f "$hook_path" ]]; then
            echo "ERROR: BROKEN REFERENCE in marketplace.json for $PLUGIN_NAME"
            echo "       hooks references '$hook_ref' but file does not exist at:"
            echo "       $hook_path"
            echo ""
            echo "       FIX: Either create the file or remove the hooks entry from marketplace.json"
            exit 1
        fi
        echo "✓ $PLUGIN_NAME: hooks reference $hook_ref exists"
    done
done

echo "✓ All file references validated"

# Validate MCP servers and configuration
echo ""
echo "=== Validating MCP Servers ==="

# Check shared MCP servers exist
for server in gitea netbox data-platform viz-platform contract-validator; do
    if [[ ! -d "$ROOT_DIR/mcp-servers/$server" ]]; then
        echo "ERROR: Shared $server MCP server not found at mcp-servers/$server/"
        exit 1
    fi
    echo "✓ Shared $server MCP server exists"
done

# Check .mcp.json exists at root
if [[ ! -f "$ROOT_DIR/.mcp.json" ]]; then
    echo "ERROR: .mcp.json not found at repository root"
    exit 1
fi
echo "✓ .mcp.json configuration exists"

# v8.0.0: Cross-validate domains match between marketplace.json and plugin.json
echo ""
echo "=== Cross-Validating Domain Fields ==="
for i in $(seq 0 $((PLUGIN_COUNT - 1))); do
    PLUGIN_NAME=$(jq -r ".plugins[$i].name" "$MARKETPLACE_JSON")
    MARKETPLACE_DOMAIN=$(jq -r ".plugins[$i].domain" "$MARKETPLACE_JSON")
    PLUGIN_JSON_PATH="$PLUGINS_DIR/$PLUGIN_NAME/.claude-plugin/plugin.json"
    if [[ -f "$PLUGIN_JSON_PATH" ]]; then
        PLUGIN_DOMAIN=$(jq -r '.domain' "$PLUGIN_JSON_PATH")
        if [[ "$MARKETPLACE_DOMAIN" != "$PLUGIN_DOMAIN" ]]; then
            echo "ERROR: Domain mismatch for $PLUGIN_NAME: marketplace.json='$MARKETPLACE_DOMAIN' vs plugin.json='$PLUGIN_DOMAIN'"
            exit 1
        fi
        echo "✓ $PLUGIN_NAME domain consistent: $MARKETPLACE_DOMAIN"
    fi
done

echo ""
echo "=== All validations passed ==="
