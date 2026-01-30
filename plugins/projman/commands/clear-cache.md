---
description: Clear plugin cache to force fresh configuration reload after marketplace updates
---

# Clear Cache

## Purpose

Clear plugin cache to force fresh configuration reload after marketplace updates.

## When to Use

- After updating the marketplace (`git pull` or reinstall)
- When MCP servers show stale configuration
- When plugin changes don't take effect

## Workflow

Execute cache clear:

```bash
rm -rf ~/.claude/plugins/cache/leo-claude-mktplace/
```

Then inform user: "Cache cleared. Restart Claude Code for changes to take effect."

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  Clear Cache                                                     ║
╚══════════════════════════════════════════════════════════════════╝
```
