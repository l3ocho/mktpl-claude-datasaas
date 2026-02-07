#!/bin/bash
# verify-hooks.sh — Verify marketplace hook inventory
# Post-Decision #29: Only PreToolUse safety hooks and UserPromptSubmit quality hooks may exist
#
# Expected inventory:
#   code-sentinel  : PreToolUse → security-check.sh (Write|Edit|MultiEdit)
#   git-flow       : PreToolUse → branch-check.sh (Bash)
#   git-flow       : PreToolUse → commit-msg-check.sh (Bash)
#   cmdb-assistant : PreToolUse → validate-input.sh (MCP create/update)
#   clarity-assist : UserPromptSubmit → vagueness-check.sh (prompt quality)
#
# FAIL conditions:
#   - Any SessionStart hook
#   - Any PostToolUse hook
#   - Any hook of type "prompt"
#   - Any hooks.json outside the 4 expected plugins
#   - Missing expected hooks

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
PLUGINS_DIR="$ROOT_DIR/plugins"

echo "=== HOOK VERIFICATION (Post-Decision #29) ==="
echo ""

FAILED=0
HOOK_COUNT=0

# Allowed plugins with hooks
ALLOWED_PLUGINS="code-sentinel git-flow cmdb-assistant clarity-assist"

# 1. Check for unexpected hooks.json files
while IFS= read -r -d '' hooks_file; do
    plugin_name=$(basename "$(dirname "$(dirname "$hooks_file")")")
    if ! echo "$ALLOWED_PLUGINS" | grep -qw "$plugin_name"; then
        echo "FAIL: UNEXPECTED hooks.json in: $plugin_name"
        echo "   File: $hooks_file"
        echo "   Only code-sentinel, git-flow, cmdb-assistant, and clarity-assist may have hooks"
        FAILED=1
    fi
done < <(find "$PLUGINS_DIR" -path "*/hooks/hooks.json" -print0 2>/dev/null)

# 2. Check for forbidden hook types
while IFS= read -r -d '' hooks_file; do
    plugin_name=$(basename "$(dirname "$(dirname "$hooks_file")")")

    # Check for SessionStart (FORBIDDEN)
    if jq -e '.hooks.SessionStart' "$hooks_file" > /dev/null 2>&1; then
        echo "FAIL: SessionStart hook found in $plugin_name (FORBIDDEN post-Decision #29)"
        FAILED=1
    fi

    # Check for PostToolUse (FORBIDDEN)
    if jq -e '.hooks.PostToolUse' "$hooks_file" > /dev/null 2>&1; then
        echo "FAIL: PostToolUse hook found in $plugin_name (FORBIDDEN post-Decision #29)"
        FAILED=1
    fi

    # Check for prompt type (FORBIDDEN)
    if grep -q '"type"[[:space:]]*:[[:space:]]*"prompt"' "$hooks_file"; then
        echo "FAIL: Prompt-type hook found in $plugin_name (FORBIDDEN)"
        FAILED=1
    fi

    # Count PreToolUse hooks
    pre_count=$(jq '[.hooks.PreToolUse[]? | .hooks[]?] | length' "$hooks_file" 2>/dev/null || echo 0)
    HOOK_COUNT=$((HOOK_COUNT + pre_count))

    # Count UserPromptSubmit hooks (allowed for quality checks)
    ups_count=$(jq '[.hooks.UserPromptSubmit[]? | .hooks[]?] | length' "$hooks_file" 2>/dev/null || echo 0)
    HOOK_COUNT=$((HOOK_COUNT + ups_count))

done < <(find "$PLUGINS_DIR" -path "*/hooks/hooks.json" -print0 2>/dev/null)

# 3. Verify expected hooks exist
for expected in code-sentinel git-flow cmdb-assistant clarity-assist; do
    if [[ ! -f "$PLUGINS_DIR/$expected/hooks/hooks.json" ]]; then
        echo "FAIL: Missing expected hooks.json in $expected"
        FAILED=1
    else
        echo "✓ $expected: hooks.json present"
    fi
done

# 4. Summary
echo ""
echo "Total hooks: $HOOK_COUNT (expected: 5 — 4 PreToolUse + 1 UserPromptSubmit)"
if [[ "$HOOK_COUNT" -ne 5 ]]; then
    echo "FAIL: Hook count mismatch"
    FAILED=1
fi

echo ""
if [[ $FAILED -eq 0 ]]; then
    echo "✓ All hooks verified OK — 4 PreToolUse safety hooks + 1 UserPromptSubmit quality hook"
else
    echo "FAIL: HOOK VERIFICATION FAILED"
    exit 1
fi
