---
description: Clear plugin cache to force fresh configuration reload after marketplace updates
---

# Clear Cache

Clear plugin cache to force fresh configuration reload. Run this after marketplace updates.

## When to Use

- After updating the marketplace (`git pull` or reinstall)
- When MCP servers show stale configuration
- When plugin changes don't take effect

## What It Does

1. Clears `~/.claude/plugins/cache/leo-claude-mktplace/`
2. Forces Claude Code to re-read `.mcp.json` files on next session

## Instructions

Run this command, then **restart your Claude Code session** for changes to take effect.

```bash
rm -rf ~/.claude/plugins/cache/leo-claude-mktplace/
```

After clearing, inform the user: "Cache cleared. Restart Claude Code for changes to take effect."
