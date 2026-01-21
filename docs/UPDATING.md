# Updating Leo Claude Marketplace

This guide covers how to update your local installation when new versions are released.

---

## Quick Update

```bash
# 1. Pull latest changes
cd /path/to/leo-claude-mktplace
git pull origin main

# 2. Run post-update script
./scripts/post-update.sh
```

**Then restart your Claude Code session** to load any changes.

---

## What the Post-Update Script Does

1. **Updates Python dependencies** for MCP servers (gitea, netbox)
2. **Shows recent changelog entries** so you know what changed
3. **Validates your configuration** is still compatible

---

## After Updating: Re-run Setup if Needed

### When to Re-run `/initial-setup`

You typically **don't need** to re-run setup after updates. However, re-run if:

- Changelog mentions **new required environment variables**
- Changelog mentions **breaking changes** to configuration
- MCP tools stop working after update

### For Existing Projects

If an update requires new project-level configuration:

```
/project-init
```

This will detect existing settings and only add what's missing.

---

## Manual Steps After Update

Some updates may require manual configuration changes:

### New Environment Variables

If the changelog mentions new environment variables:

1. Check the variable name and purpose in the changelog
2. Add it to the appropriate config file:
   - System variables → `~/.config/claude/gitea.env` or `netbox.env`
   - Project variables → `.env` in your project root

### New MCP Server Features

If a new MCP server tool is added:

1. The post-update script handles dependency installation
2. Check plugin documentation for usage
3. New tools are available immediately after session restart

### Breaking Changes

Breaking changes will be clearly marked in CHANGELOG.md with migration instructions.

### Setup Script and Configuration Workflow Changes

When updating, review if changes affect the setup workflow:

1. **Check for setup command changes:**
   ```bash
   git diff HEAD~1 plugins/*/commands/initial-setup.md
   git diff HEAD~1 plugins/*/commands/project-init.md
   git diff HEAD~1 plugins/*/commands/project-sync.md
   ```

2. **Check for hook changes:**
   ```bash
   git diff HEAD~1 plugins/*/hooks/hooks.json
   ```

3. **Check for configuration structure changes:**
   ```bash
   git diff HEAD~1 docs/CONFIGURATION.md
   ```

**If setup commands changed:**
- Review what's new (new validation steps, new prompts, etc.)
- Consider re-running `/initial-setup` or `/project-init` to benefit from improvements
- Existing configurations remain valid unless changelog notes breaking changes

**If hooks changed:**
- Restart your Claude Code session to load new hooks
- New hooks (like SessionStart validation) activate automatically

**If configuration structure changed:**
- Check if new variables are required
- Run `/project-sync` if repository detection logic improved

---

## Troubleshooting Updates

### Dependencies fail to install

```bash
# Rebuild virtual environment
cd mcp-servers/gitea
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Configuration no longer works

1. Check CHANGELOG.md for breaking changes
2. Run `/initial-setup` to re-validate and fix configuration
3. Compare your config files with documentation in `docs/CONFIGURATION.md`

### MCP server won't start after update

1. Check Python version: `python3 --version` (requires 3.10+)
2. Verify venv exists: `ls mcp-servers/gitea/.venv`
3. Restart Claude Code session
4. Check logs for specific errors

### New commands not available

1. Restart your Claude Code session
2. Verify the plugin is still installed
3. Check if the command requires additional setup

---

## Version Pinning

To stay on a specific version:

```bash
# List available tags
git tag

# Checkout specific version
git checkout v3.0.0

# Run post-update
./scripts/post-update.sh
```

---

## Checking Current Version

The version is displayed in the main README.md title and in `CHANGELOG.md`.

```bash
# Check version from changelog
head -20 CHANGELOG.md
```

---

## Getting Help

- Check `docs/CONFIGURATION.md` for setup guide
- Check `docs/COMMANDS-CHEATSHEET.md` for command reference
- Review `CHANGELOG.md` for recent changes
- Search existing issues in Gitea
