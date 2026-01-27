#!/bin/bash
# Verify all hooks are command type (not prompt)
# Run this after any plugin update

echo "=== HOOK VERIFICATION ==="
echo ""

FAILED=0

# Check ALL hooks.json files in .claude directory
for f in $(find ~/.claude -name "hooks.json" 2>/dev/null); do
    if grep -q '"type": "prompt"' "$f" || grep -q '"type":"prompt"' "$f"; then
        echo "❌ PROMPT HOOK FOUND: $f"
        FAILED=1
    fi
done

# Note about cache (informational only - do NOT clear mid-session)
if [ -d ~/.claude/plugins/cache/leo-claude-mktplace ]; then
    echo "ℹ️  Cache exists: ~/.claude/plugins/cache/leo-claude-mktplace"
    echo "   (This is normal - do NOT clear mid-session or MCP tools will break)"
    echo "   To apply plugin changes: restart Claude Code session"
fi

# Verify installed hooks are command type
for plugin in doc-guardian code-sentinel projman pr-review project-hygiene data-platform cmdb-assistant; do
    HOOK_FILE=~/.claude/plugins/marketplaces/leo-claude-mktplace/plugins/$plugin/hooks/hooks.json
    if [ -f "$HOOK_FILE" ]; then
        if grep -q '"type": "command"' "$HOOK_FILE" || grep -q '"type":"command"' "$HOOK_FILE"; then
            echo "✓ $plugin: command type"
        else
            echo "❌ $plugin: NOT command type"
            FAILED=1
        fi
    fi
done

echo ""
if [ $FAILED -eq 0 ]; then
    echo "✓ All hooks verified OK"
else
    echo "❌ ISSUES FOUND - fix before using"
    exit 1
fi
