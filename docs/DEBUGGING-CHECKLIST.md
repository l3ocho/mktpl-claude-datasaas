# Debugging Checklist for Marketplace Troubleshooting

**Purpose:** Systematic approach to diagnose and fix plugin loading issues.

Last Updated: 2026-01-22

---

## Step 1: Identify the Loading Path

Claude Code loads plugins from different locations depending on context:

| Location | Path | When Used |
|----------|------|-----------|
| **Source** | `~/claude-plugins-work/` | When developing in this directory |
| **Installed** | `~/.claude/plugins/marketplaces/leo-claude-mktplace/` | After marketplace install |
| **Cache** | `~/.claude/` | Plugin metadata, settings |

**Determine which path Claude is using:**

```bash
# Check if installed marketplace exists
ls -la ~/.claude/plugins/marketplaces/leo-claude-mktplace/

# Check Claude's current plugin loading
cat ~/.claude/settings.local.json | grep -A5 "mcpServers"
```

**Key insight:** If you're editing source but Claude uses installed, your changes won't take effect.

---

## Step 2: Verify Files Exist at Runtime Location

Check the files Claude will actually load:

```bash
# For installed marketplace
RUNTIME=~/.claude/plugins/marketplaces/leo-claude-mktplace

# Check MCP server exists
ls -la $RUNTIME/mcp-servers/gitea/
ls -la $RUNTIME/mcp-servers/netbox/

# Check plugin manifests
ls -la $RUNTIME/plugins/projman/.claude-plugin/plugin.json
ls -la $RUNTIME/plugins/pr-review/.claude-plugin/plugin.json

# Check .mcp.json files
cat $RUNTIME/plugins/projman/.mcp.json
```

---

## Step 3: Verify Virtual Environments Exist

**This is the most common failure point after installation.**

MCP servers require Python venvs to exist at the INSTALLED location:

```bash
RUNTIME=~/.claude/plugins/marketplaces/leo-claude-mktplace

# Check venvs exist
ls -la $RUNTIME/mcp-servers/gitea/.venv/bin/python
ls -la $RUNTIME/mcp-servers/netbox/.venv/bin/python

# If missing, create them:
cd $RUNTIME && ./scripts/setup.sh
```

**Common error:** "X MCP servers failed to start" = venvs don't exist in installed path.

---

## Step 4: Verify Symlink Resolution

Plugins use symlinks to shared MCP servers. Verify they resolve correctly:

```bash
RUNTIME=~/.claude/plugins/marketplaces/leo-claude-mktplace

# Check symlinks exist and resolve
readlink -f $RUNTIME/plugins/projman/mcp-servers/gitea
readlink -f $RUNTIME/plugins/pr-review/mcp-servers/gitea
readlink -f $RUNTIME/plugins/cmdb-assistant/mcp-servers/netbox

# Should resolve to:
# $RUNTIME/mcp-servers/gitea
# $RUNTIME/mcp-servers/netbox
```

**If broken:** Symlinks are relative. If directory structure differs, they'll break.

---

## Step 5: Test MCP Server Startup

Manually test if the MCP server can start:

```bash
RUNTIME=~/.claude/plugins/marketplaces/leo-claude-mktplace

# Test Gitea MCP
cd $RUNTIME/mcp-servers/gitea
PYTHONPATH=. .venv/bin/python -c "from mcp_server.server import main; print('OK')"

# Test NetBox MCP
cd $RUNTIME/mcp-servers/netbox
PYTHONPATH=. .venv/bin/python -c "from mcp_server.server import main; print('OK')"
```

**If import fails:** Check requirements.txt installed, check Python version compatibility.

---

## Step 6: Verify Configuration Files

Check environment variables are set:

```bash
# System-level credentials (should exist)
cat ~/.config/claude/gitea.env
# Should contain: GITEA_API_URL, GITEA_API_TOKEN

cat ~/.config/claude/netbox.env
# Should contain: NETBOX_API_URL, NETBOX_API_TOKEN

# Project-level config (in target project)
cat /path/to/project/.env
# Should contain: GITEA_ORG, GITEA_REPO
```

---

## Step 7: Verify Hooks Configuration

Check hooks are valid:

```bash
RUNTIME=~/.claude/plugins/marketplaces/leo-claude-mktplace

# List all hooks.json files
find $RUNTIME/plugins -name "hooks.json" -exec echo "=== {} ===" \; -exec cat {} \;

# Verify hook events are valid
# Valid: PreToolUse, PostToolUse, UserPromptSubmit, SessionStart, SessionEnd,
#        Notification, Stop, SubagentStop, PreCompact
# INVALID: task-completed, file-changed, git-commit-msg-needed
```

---

## Quick Diagnostic Commands

Run these to quickly identify issues:

```bash
RUNTIME=~/.claude/plugins/marketplaces/leo-claude-mktplace

echo "=== Installation Status ==="
[ -d "$RUNTIME" ] && echo "Installed: YES" || echo "Installed: NO"

echo -e "\n=== Virtual Environments ==="
[ -f "$RUNTIME/mcp-servers/gitea/.venv/bin/python" ] && echo "Gitea venv: OK" || echo "Gitea venv: MISSING"
[ -f "$RUNTIME/mcp-servers/netbox/.venv/bin/python" ] && echo "NetBox venv: OK" || echo "NetBox venv: MISSING"

echo -e "\n=== Symlinks ==="
[ -L "$RUNTIME/plugins/projman/mcp-servers/gitea" ] && echo "projman->gitea: OK" || echo "projman->gitea: MISSING"
[ -L "$RUNTIME/plugins/pr-review/mcp-servers/gitea" ] && echo "pr-review->gitea: OK" || echo "pr-review->gitea: MISSING"
[ -L "$RUNTIME/plugins/cmdb-assistant/mcp-servers/netbox" ] && echo "cmdb-assistant->netbox: OK" || echo "cmdb-assistant->netbox: MISSING"

echo -e "\n=== Config Files ==="
[ -f ~/.config/claude/gitea.env ] && echo "gitea.env: OK" || echo "gitea.env: MISSING"
[ -f ~/.config/claude/netbox.env ] && echo "netbox.env: OK" || echo "netbox.env: MISSING"
```

---

## Common Issues and Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Missing venvs | "X MCP servers failed" | `cd ~/.claude/plugins/marketplaces/leo-claude-mktplace && ./scripts/setup.sh` |
| Broken symlinks | MCP tools not available | Reinstall marketplace or manually recreate symlinks |
| Wrong path edits | Changes don't take effect | Edit installed path or reinstall after source changes |
| Missing credentials | MCP connection errors | Create `~/.config/claude/gitea.env` with API credentials |
| Invalid hook events | Hooks don't fire | Use only valid event names (see Step 7) |

---

## After Fixing Issues

1. **Restart Claude Code** - Plugins are loaded at startup
2. **Verify fix works** - Run a simple command that uses the MCP
3. **Document the issue** - If it's a new failure mode, add to this checklist

---

## Cache Clearing: When It's Safe vs Destructive

**⚠️ CRITICAL: Never clear plugin cache mid-session.**

### Why Cache Clearing Breaks MCP Tools

When Claude Code starts a session:
1. MCP tools are loaded from the cache directory
2. Tool definitions include **absolute paths** to the venv (e.g., `~/.claude/plugins/cache/.../venv/`)
3. These paths are cached in the session memory
4. Deleting the cache removes the venv, but the session still references the old paths
5. Any MCP tool making HTTP requests fails with TLS certificate errors

### When Cache Clearing is SAFE

| Scenario | Safe? | Action |
|----------|-------|--------|
| Before starting Claude Code | ✅ Yes | Clear cache, then start session |
| Between sessions | ✅ Yes | Clear cache after `/exit`, before next session |
| During a session | ❌ NO | Never - will break MCP tools |
| After plugin source edits | ❌ NO | Restart session instead |

### Recovery: MCP Tools Broken Mid-Session

If you accidentally cleared cache during a session and MCP tools fail:

```
Error: Could not find a suitable TLS CA certificate bundle, invalid path:
/home/.../.claude/plugins/cache/.../certifi/cacert.pem
```

**Fix:**
1. Exit the current session (`/exit` or Ctrl+C)
2. Start a new Claude Code session
3. MCP tools will reload from the reinstalled cache

### Correct Workflow for Plugin Development

1. Make changes to plugin source files
2. Run `./scripts/verify-hooks.sh` (verifies hook types)
3. Tell user: "Please restart Claude Code for changes to take effect"
4. **Do NOT clear cache** - session restart handles reloading

---

## Automated Diagnostics

Use these commands for automated checking:

- `/debug-report` - Run full diagnostics, create issue if problems found
- `/debug-review` - Investigate existing diagnostic issues and propose fixes

---

## Related Documentation

- `CLAUDE.md` - Installation Paths and Troubleshooting sections
- `docs/CONFIGURATION.md` - Setup and configuration guide
- `docs/UPDATING.md` - Update procedures
