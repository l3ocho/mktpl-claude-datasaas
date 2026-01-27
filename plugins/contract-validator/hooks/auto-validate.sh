#!/bin/bash
# contract-validator SessionStart auto-validate hook
# Validates plugin contracts only when plugin files have changed since last check
# All output MUST have [contract-validator] prefix

PREFIX="[contract-validator]"

# ============================================================================
# Configuration
# ============================================================================

# Enable/disable auto-check (default: true)
AUTO_CHECK="${CONTRACT_VALIDATOR_AUTO_CHECK:-true}"

# Cache location for storing last check hash
CACHE_DIR="$HOME/.cache/claude-plugins/contract-validator"
HASH_FILE="$CACHE_DIR/last-check.hash"

# Marketplace location (installed plugins)
MARKETPLACE_PATH="$HOME/.claude/plugins/marketplaces/leo-claude-mktplace"

# ============================================================================
# Early exit if disabled
# ============================================================================

if [[ "$AUTO_CHECK" != "true" ]]; then
    exit 0
fi

# ============================================================================
# Smart mode: Check if plugin files have changed
# ============================================================================

# Function to compute hash of all plugin manifest files
compute_plugin_hash() {
    local hash_input=""

    if [[ -d "$MARKETPLACE_PATH/plugins" ]]; then
        # Hash all plugin.json, hooks.json, and agent files
        while IFS= read -r -d '' file; do
            if [[ -f "$file" ]]; then
                hash_input+="$(md5sum "$file" 2>/dev/null | cut -d' ' -f1)"
            fi
        done < <(find "$MARKETPLACE_PATH/plugins" \
            \( -name "plugin.json" -o -name "hooks.json" -o -name "*.md" -path "*/agents/*" \) \
            -print0 2>/dev/null | sort -z)
    fi

    # Also include marketplace.json
    if [[ -f "$MARKETPLACE_PATH/.claude-plugin/marketplace.json" ]]; then
        hash_input+="$(md5sum "$MARKETPLACE_PATH/.claude-plugin/marketplace.json" 2>/dev/null | cut -d' ' -f1)"
    fi

    # Compute final hash
    echo "$hash_input" | md5sum | cut -d' ' -f1
}

# Ensure cache directory exists
mkdir -p "$CACHE_DIR" 2>/dev/null

# Compute current hash
CURRENT_HASH=$(compute_plugin_hash)

# Check if we have a previous hash
if [[ -f "$HASH_FILE" ]]; then
    PREVIOUS_HASH=$(cat "$HASH_FILE" 2>/dev/null)

    # If hashes match, no changes - skip validation
    if [[ "$CURRENT_HASH" == "$PREVIOUS_HASH" ]]; then
        exit 0
    fi
fi

# ============================================================================
# Run validation (hashes differ or no cache)
# ============================================================================

ISSUES_FOUND=0
WARNINGS=""

# Function to add warning
add_warning() {
    WARNINGS+="  - $1"$'\n'
    ((ISSUES_FOUND++))
}

# 1. Check all installed plugins have valid plugin.json
if [[ -d "$MARKETPLACE_PATH/plugins" ]]; then
    for plugin_dir in "$MARKETPLACE_PATH/plugins"/*/; do
        if [[ -d "$plugin_dir" ]]; then
            plugin_name=$(basename "$plugin_dir")
            plugin_json="$plugin_dir/.claude-plugin/plugin.json"

            if [[ ! -f "$plugin_json" ]]; then
                add_warning "$plugin_name: missing .claude-plugin/plugin.json"
                continue
            fi

            # Basic JSON validation
            if ! python3 -c "import json; json.load(open('$plugin_json'))" 2>/dev/null; then
                add_warning "$plugin_name: invalid JSON in plugin.json"
                continue
            fi

            # Check required fields
            if ! python3 -c "
import json
with open('$plugin_json') as f:
    data = json.load(f)
required = ['name', 'version', 'description']
missing = [r for r in required if r not in data]
if missing:
    exit(1)
" 2>/dev/null; then
                add_warning "$plugin_name: plugin.json missing required fields"
            fi
        fi
    done
fi

# 2. Check hooks.json files are properly formatted
if [[ -d "$MARKETPLACE_PATH/plugins" ]]; then
    while IFS= read -r -d '' hooks_file; do
        plugin_name=$(basename "$(dirname "$(dirname "$hooks_file")")")

        # Validate JSON
        if ! python3 -c "import json; json.load(open('$hooks_file'))" 2>/dev/null; then
            add_warning "$plugin_name: invalid JSON in hooks/hooks.json"
            continue
        fi

        # Validate hook structure
        if ! python3 -c "
import json
with open('$hooks_file') as f:
    data = json.load(f)
if 'hooks' not in data:
    exit(1)
valid_events = ['PreToolUse', 'PostToolUse', 'UserPromptSubmit', 'SessionStart', 'SessionEnd', 'Notification', 'Stop', 'SubagentStop', 'PreCompact']
for event in data['hooks']:
    if event not in valid_events:
        exit(1)
    for hook in data['hooks'][event]:
        # Support both flat structure (type at top) and nested structure (matcher + hooks array)
        if 'type' in hook:
            # Flat structure: {type: 'command', command: '...'}
            pass
        elif 'matcher' in hook and 'hooks' in hook:
            # Nested structure: {matcher: '...', hooks: [{type: 'command', ...}]}
            for nested_hook in hook['hooks']:
                if 'type' not in nested_hook:
                    exit(1)
        else:
            exit(1)
" 2>/dev/null; then
            add_warning "$plugin_name: hooks.json has invalid structure or events"
        fi
    done < <(find "$MARKETPLACE_PATH/plugins" -path "*/hooks/hooks.json" -print0 2>/dev/null)
fi

# 3. Check agent references are valid (agent files exist and are markdown)
if [[ -d "$MARKETPLACE_PATH/plugins" ]]; then
    while IFS= read -r -d '' agent_file; do
        plugin_name=$(basename "$(dirname "$(dirname "$agent_file")")")
        agent_name=$(basename "$agent_file")

        # Check file is not empty
        if [[ ! -s "$agent_file" ]]; then
            add_warning "$plugin_name: empty agent file $agent_name"
            continue
        fi

        # Check file has markdown content (at least a header)
        if ! grep -q '^#' "$agent_file" 2>/dev/null; then
            add_warning "$plugin_name: agent $agent_name missing markdown header"
        fi
    done < <(find "$MARKETPLACE_PATH/plugins" -path "*/agents/*.md" -print0 2>/dev/null)
fi

# ============================================================================
# Store new hash and report results
# ============================================================================

# Always store the new hash (even if issues found - we don't want to recheck)
echo "$CURRENT_HASH" > "$HASH_FILE"

# Report any issues found (non-blocking warning)
if [[ $ISSUES_FOUND -gt 0 ]]; then
    echo "$PREFIX Plugin contract validation found $ISSUES_FOUND issue(s):"
    echo "$WARNINGS"
    echo "$PREFIX Run /validate-contracts for full details"
fi

# Always exit 0 (non-blocking)
exit 0
