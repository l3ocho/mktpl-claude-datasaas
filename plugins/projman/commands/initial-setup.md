---
description: Run initial setup for support-claude-mktplace
---

# Initial Setup

Run the installation script to set up the toolkit.

## What This Does

1. Creates Python virtual environments for MCP servers
2. Installs all dependencies
3. Creates configuration file templates
4. Validates existing configuration
5. Reports remaining manual steps

## Execution

```bash
cd ${PROJECT_ROOT}
./scripts/setup.sh
```

## After Running

Review the output for any manual steps required:
- Configure API credentials in `~/.config/claude/`
- Run `/labels-sync` to sync Gitea labels
- Verify Wiki.js directory structure

## Re-Running

This command is safe to run multiple times. It will skip already-completed steps.
