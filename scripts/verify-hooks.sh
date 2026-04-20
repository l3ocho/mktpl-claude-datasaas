#!/bin/bash
# verify-hooks.sh — Verify marketplace hook inventory (v12.0.0)
#
# Expected inventory (2 hooks, 1 plugin):
#   git-guardrails : PreToolUse → branch-check.sh     (Bash)
#   git-guardrails : PreToolUse → commit-msg-check.sh (Bash)
#
# FAIL conditions:
#   - Any SessionStart hook
#   - Any PostToolUse hook
#   - Any UserPromptSubmit hook
#   - Any hook of type "prompt"
#   - Any hooks.json outside the 1 expected plugin
#   - Hook count mismatch

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
PLUGINS_DIR="$ROOT_DIR/plugins"

echo "=== HOOK VERIFICATION (v12.0.0) ==="
echo ""

FAILED=0
HOOK_COUNT=0

ALLOWED_PLUGINS="git-guardrails"

# 1. Fail on any unexpected hooks.json
while IFS= read -r -d '' hooks_file; do
    plugin_name=$(basename "$(dirname "$(dirname "$hooks_file")")")
    if ! echo "$ALLOWED_PLUGINS" | grep -qw "$plugin_name"; then
        echo "FAIL: unexpected hooks.json in plugin: $plugin_name"
        echo "   File: $hooks_file"
        echo "   As of v12.0.0, only git-guardrails may have hooks."
        FAILED=1
    fi
done < <(find "$PLUGINS_DIR" -path "*/hooks/hooks.json" -print0 2>/dev/null)

# 2. Fail on forbidden hook types
while IFS= read -r -d '' hooks_file; do
    plugin_name=$(basename "$(dirname "$(dirname "$hooks_file")")")

    if jq -e '.hooks.SessionStart' "$hooks_file" > /dev/null 2>&1; then
        echo "FAIL: SessionStart hook in $plugin_name (forbidden)"
        FAILED=1
    fi

    if jq -e '.hooks.PostToolUse' "$hooks_file" > /dev/null 2>&1; then
        echo "FAIL: PostToolUse hook in $plugin_name (forbidden)"
        FAILED=1
    fi

    if jq -e '.hooks.UserPromptSubmit' "$hooks_file" > /dev/null 2>&1; then
        echo "FAIL: UserPromptSubmit hook in $plugin_name (forbidden)"
        FAILED=1
    fi

    if grep -q '"type"[[:space:]]*:[[:space:]]*"prompt"' "$hooks_file"; then
        echo "FAIL: prompt-type hook in $plugin_name (forbidden)"
        FAILED=1
    fi

    pre_count=$(jq '[.hooks.PreToolUse[]? | .hooks[]?] | length' "$hooks_file" 2>/dev/null || echo 0)
    HOOK_COUNT=$((HOOK_COUNT + pre_count))
done < <(find "$PLUGINS_DIR" -path "*/hooks/hooks.json" -print0 2>/dev/null)

# 3. Verify expected plugin has its hooks.json
for expected in $ALLOWED_PLUGINS; do
    if [[ ! -f "$PLUGINS_DIR/$expected/hooks/hooks.json" ]]; then
        echo "FAIL: missing expected hooks.json in $expected"
        FAILED=1
    else
        echo "✓ $expected: hooks.json present"
    fi
done

# 4. Summary
echo ""
echo "Total PreToolUse hooks: $HOOK_COUNT (expected: 2)"
if [[ "$HOOK_COUNT" -ne 2 ]]; then
    echo "FAIL: hook count mismatch"
    FAILED=1
fi

echo ""
if [[ $FAILED -eq 0 ]]; then
    echo "✓ All hooks verified — 2 PreToolUse safety hooks in git-guardrails"
else
    echo "FAIL: hook verification failed"
    exit 1
fi
