#!/usr/bin/env bash
# Switch between marketplace profiles
# Usage: ./scripts/switch-profile.sh [lean|full]

set -euo pipefail

echo "⚠️  DEPRECATED: use scripts/claude-launch.sh instead." >&2

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
MARKETPLACE_DIR="$ROOT_DIR/.claude-plugin"

case "${1:-lean}" in
  lean)
    cp "$MARKETPLACE_DIR/marketplace-lean.json" "$MARKETPLACE_DIR/marketplace.json"
    cp "$ROOT_DIR/.mcp-lean.json" "$ROOT_DIR/.mcp.json"
    rm -rf ~/.claude/plugins/cache/
    echo "Switched to LEAN profile (6 plugins, 1 MCP server)"
    echo "Plugin cache cleared."
    echo ""
    echo "Plugins: projman, git-flow, pr-review, clarity-assist, code-sentinel, doc-guardian"
    echo "MCP: gitea only"
    echo ""
    echo "Restart Claude Code session for changes to take effect."
    ;;
  full)
    cp "$MARKETPLACE_DIR/marketplace-full.json" "$MARKETPLACE_DIR/marketplace.json"
    cp "$ROOT_DIR/.mcp-full.json" "$ROOT_DIR/.mcp.json"
    rm -rf ~/.claude/plugins/cache/
    echo "Switched to FULL profile (12 plugins, 5 MCP servers)"
    echo "Plugin cache cleared."
    echo ""
    echo "Plugins: all"
    echo "MCP: gitea, netbox, data-platform, viz-platform, contract-validator"
    echo ""
    echo "Restart Claude Code session for changes to take effect."
    ;;
  status)
    # Check current profile by comparing files
    if diff -q "$MARKETPLACE_DIR/marketplace.json" "$MARKETPLACE_DIR/marketplace-lean.json" >/dev/null 2>&1; then
      echo "Current profile: LEAN (6 plugins, 1 MCP server)"
    elif diff -q "$MARKETPLACE_DIR/marketplace.json" "$MARKETPLACE_DIR/marketplace-full.json" >/dev/null 2>&1; then
      echo "Current profile: FULL (12 plugins, 5 MCP servers)"
    else
      echo "Current profile: CUSTOM (marketplace.json differs from both profiles)"
    fi
    ;;
  *)
    echo "Usage: $0 [lean|full|status]"
    echo ""
    echo "Profiles:"
    echo "  lean    — 6 core plugins (projman, git-flow, pr-review, clarity-assist, code-sentinel, doc-guardian)"
    echo "            1 MCP server (gitea only)"
    echo "  full    — All 12 plugins"
    echo "            5 MCP servers (gitea, netbox, data-platform, viz-platform, contract-validator)"
    echo "  status  — Show current profile"
    echo ""
    echo "Note: Restart Claude Code session after switching for changes to take effect."
    exit 1
    ;;
esac
