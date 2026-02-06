---
name: projman setup
description: Configure projman - full setup, quick project init, or sync after repo move
---

# Projman Setup

## Skills Required

- skills/mcp-tools-reference.md
- skills/repo-validation.md
- skills/setup-workflows.md

## Purpose

Unified setup command for all configuration needs.

**Important:**
- Uses Bash, Read, Write, AskUserQuestion - NOT MCP tools
- MCP tools won't work until after setup + session restart
- Tokens must be entered manually for security

## Invocation

```
/projman setup              # Auto-detect appropriate mode
/projman setup --full       # Full wizard (MCP + system + project)
/projman setup --quick      # Project-only setup
/projman setup --sync       # Update after repo move
/projman setup --clear-cache # Clear plugin cache (between sessions only)
```

## Mode Detection

If no argument provided, auto-detect:

1. Check `~/.config/claude/gitea.env`
   - Missing → **full** mode

2. Check project `.env`
   - Missing → **quick** mode

3. Compare `.env` with git remote
   - Mismatch → **sync** mode
   - Match → offer reconfigure or exit

## Mode: Full

Execute `skills/setup-workflows.md` → Full Setup Workflow

Phases:
1. Environment validation (Python 3.10+)
2. MCP server setup (venv + requirements)
3. System-level config (`~/.config/claude/gitea.env`)
4. Project-level config (`.env`)
5. Final validation

## Mode: Quick

Execute `skills/setup-workflows.md` → Quick Setup Workflow

Steps:
1. Verify system config exists
2. Verify git repository
3. Check existing `.env`
4. Detect org/repo from git remote
5. Validate via API
6. Create/update `.env`
7. Check `.gitignore`

## Mode: Sync

Execute `skills/setup-workflows.md` → Sync Workflow

Steps:
1. Read current config
2. Detect git remote
3. Compare values
4. Show changes
5. Validate new values
6. Update `.env`
7. Confirm

## Mode: Clear Cache (--clear-cache)

Clear plugin cache to force fresh configuration reload.

**WARNING:** Only run between sessions, never mid-session. Clearing cache mid-session destroys MCP tool venv paths and breaks all MCP operations.

Steps:
1. Execute: `rm -rf ~/.claude/plugins/cache/leo-claude-mktplace/`
2. Inform user: "Cache cleared. Restart Claude Code for changes to take effect."

When to use:
- After updating the marketplace (`git pull` or reinstall)
- When MCP servers show stale configuration
- When plugin changes don't take effect

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  ⚙️ SETUP                                                        ║
║  [Mode: Full | Quick | Sync]                                     ║
╚══════════════════════════════════════════════════════════════════╝
```
