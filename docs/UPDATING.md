# Updating Leo Claude Marketplace

This guide covers how to update your local installation when new versions are released.

## Quick Update

```bash
# 1. Pull latest changes
cd /path/to/leo-claude-mktplace
git pull origin main

# 2. Run post-update script
./scripts/post-update.sh
```

## What the Post-Update Script Does

1. **Updates Python dependencies** for MCP servers
2. **Shows recent changelog entries** so you know what changed
3. **Validates your configuration** is still compatible

## Manual Steps After Update

Some updates may require manual configuration changes:

### New Environment Variables

If the changelog mentions new environment variables:

1. Check the variable name and purpose in the changelog
2. Add it to the appropriate config file:
   - Gitea variables → `~/.config/claude/gitea.env`
   - Project variables → `.env` in your project root

### New MCP Server Features

If a new MCP server tool is added:

1. The post-update script handles dependency installation
2. Check `plugins/projman/README.md` for usage documentation
3. New tools are available immediately after update

### Breaking Changes

Breaking changes will be clearly marked in CHANGELOG.md with migration instructions.

## Troubleshooting

### Dependencies fail to install

```bash
# Rebuild virtual environment
cd plugins/projman/mcp-servers/gitea
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Configuration no longer works

1. Check CHANGELOG.md for breaking changes
2. Compare your config files with updated `.env.example` (if provided)
3. Run `./scripts/setup.sh` to validate configuration

### MCP server won't start

1. Check Python version: `python3 --version` (requires 3.10+)
2. Verify venv exists: `ls plugins/projman/mcp-servers/gitea/.venv`
3. Check logs for specific errors

## Version Pinning

To stay on a specific version:

```bash
# List available tags
git tag

# Checkout specific version
git checkout v2.2.0

# Run post-update
./scripts/post-update.sh
```

## Getting Help

- Check `plugins/projman/README.md` for projman documentation
- Check `plugins/projman/CONFIGURATION.md` for setup guide
- Review CHANGELOG.md for recent changes
- Search existing issues in Gitea
