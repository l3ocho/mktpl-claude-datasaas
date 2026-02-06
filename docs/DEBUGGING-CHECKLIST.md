# Debugging Checklist for Marketplace Troubleshooting

**Purpose:** Systematic approach to diagnose and fix plugin loading issues.

Last Updated: 2026-01-28

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

## Step 4: Verify MCP Configuration

Check `.mcp.json` at marketplace root is correctly configured:

```bash
RUNTIME=~/.claude/plugins/marketplaces/leo-claude-mktplace

# Check .mcp.json exists and has valid content
cat $RUNTIME/.mcp.json | jq '.mcpServers | keys'

# Should list: gitea, netbox, data-platform, viz-platform, contract-validator
```

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
# Should contain: GITEA_REPO=owner/repo (e.g., my-org/my-repo)
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

echo -e "\n=== MCP Configuration ==="
[ -f "$RUNTIME/.mcp.json" ] && echo ".mcp.json: OK" || echo ".mcp.json: MISSING"

echo -e "\n=== Config Files ==="
[ -f ~/.config/claude/gitea.env ] && echo "gitea.env: OK" || echo "gitea.env: MISSING"
[ -f ~/.config/claude/netbox.env ] && echo "netbox.env: OK" || echo "netbox.env: MISSING"
```

---

## Common Issues and Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Missing venvs | "X MCP servers failed" | `cd ~/.claude/plugins/marketplaces/leo-claude-mktplace && ./scripts/setup.sh` |
| Missing .mcp.json | MCP tools not available | Check `.mcp.json` exists at marketplace root |
| Wrong path edits | Changes don't take effect | Edit installed path or reinstall after source changes |
| Missing credentials | MCP connection errors | Create `~/.config/claude/gitea.env` with API credentials |
| Invalid hook events | Hooks don't fire | Use only valid event names (see Step 7) |
| Gitea issues not closing | Merged to non-default branch | Manually close issues (see below) |
| MCP changes not taking effect | Session caching | Restart Claude Code session (see below) |

### Gitea Auto-Close Behavior

**Issue:** Using `Closes #XX` or `Fixes #XX` in commit/PR messages does NOT auto-close issues when merging to `development`.

**Root Cause:** Gitea only auto-closes issues when merging to the **default branch** (typically `main` or `master`). Merging to `development`, `staging`, or any other branch will NOT trigger auto-close.

**Workaround:**
1. Use the Gitea MCP tool to manually close issues after merging to development:
   ```
   mcp__plugin_projman_gitea__update_issue(issue_number=XX, state="closed")
   ```
2. Or close issues via the Gitea web UI
3. The auto-close keywords will still work when the changes are eventually merged to `main`

**Recommendation:** Include the `Closes #XX` keywords in commits anyway - they'll work when the final merge to `main` happens.

### MCP Session Restart Requirement

**Issue:** Changes to MCP servers, hooks, or plugin configuration don't take effect immediately.

**Root Cause:** Claude Code loads MCP tools and plugin configuration at session start. These are cached in session memory and not reloaded dynamically.

**What requires a session restart:**
- MCP server code changes (Python files in `mcp-servers/`)
- Changes to `.mcp.json` files
- Changes to `hooks/hooks.json`
- Changes to `plugin.json`
- Adding new MCP tools or modifying tool signatures

**What does NOT require a restart:**
- Command/skill markdown files (`.md`) - these are read on invocation
- Agent markdown files - read when agent is invoked

**Correct workflow after plugin changes:**
1. Make changes to source files
2. Run `./scripts/verify-hooks.sh` to validate
3. Inform user: "Please restart Claude Code for changes to take effect"
4. **Do NOT clear cache mid-session** - see "Cache Clearing" section

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

- `/cv status` - Marketplace-wide health check (installation, MCP, configuration)
- `/hygiene check` - Project file organization and cleanup check

---

## Related Documentation

- `CLAUDE.md` - Installation Paths and Troubleshooting sections
- `docs/CONFIGURATION.md` - Setup and configuration guide
- `docs/UPDATING.md` - Update procedures
