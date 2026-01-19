# Configuration Guide - Projman Plugin v2.0.0

Complete setup and configuration instructions for the Projman project management plugin.

## Overview

The Projman plugin uses a **hybrid configuration** approach:
- **System-level:** Credentials for Gitea (stored once per machine)
- **Project-level:** Repository path (stored per project)

This design allows:
- Single token per service (update once, use everywhere)
- Easy multi-project setup (just add `.env` per project)
- Security (tokens never committed to git)
- Project isolation (each project has its own scope)

## Prerequisites

Before configuring the plugin, ensure you have:

1. **Python 3.10+** installed
   ```bash
   python3 --version  # Should be 3.10.0 or higher
   ```

2. **Git repository** initialized
   ```bash
   git status  # Should show initialized repository
   ```

3. **Gitea access** with an account and permissions to:
   - Create issues
   - Manage labels
   - Read organization information
   - Access repository wiki

4. **Claude Code** installed and working

## Step 1: Install MCP Server

The plugin bundles the Gitea MCP server at `mcp-servers/gitea/`:

```bash
# Navigate to MCP server directory (inside plugin)
cd plugins/projman/mcp-servers/gitea

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from mcp_server import server; print('Gitea MCP Server installed successfully')"

# Deactivate when done
deactivate
```

## Step 2: Generate Gitea API Token

1. Log into Gitea: https://gitea.example.com
2. Navigate to: **User Icon** (top right) → **Settings**
3. Click **Applications** tab
4. Scroll to **Manage Access Tokens**
5. Click **Generate New Token**
6. Configure token:
   - **Token Name:** `claude-code-projman`
   - **Permissions:**
     - `repo` (all sub-permissions) - Repository access
     - `read:org` - Read organization information and labels
     - `read:user` - Read user information
     - `write:repo` - Wiki access
7. Click **Generate Token**
8. **IMPORTANT:** Copy token immediately (shown only once!)
9. Save token securely - you'll need it in Step 3

**Token Permissions Explained:**
- `repo` - Create, read, update issues, labels, and wiki
- `read:org` - Access organization-level labels
- `read:user` - Associate issues with user account
- `write:repo` - Create wiki pages for lessons learned

## Step 3: System-Level Configuration

Create system-wide configuration file in `~/.config/claude/`:

### 3.1 Create Configuration Directory

```bash
mkdir -p ~/.config/claude
```

### 3.2 Configure Gitea

```bash
cat > ~/.config/claude/gitea.env << 'EOF'
# Gitea API Configuration
GITEA_URL=https://gitea.example.com
GITEA_TOKEN=your_gitea_token_here
GITEA_ORG=your_organization
EOF

# Secure the file (owner read/write only)
chmod 600 ~/.config/claude/gitea.env
```

**Replace placeholders:**
- `your_gitea_token_here` with the token from Step 2
- `your_organization` with your Gitea organization name

**Configuration Variables:**
- `GITEA_URL` - Gitea base URL (without `/api/v1`)
- `GITEA_TOKEN` - Personal access token from Step 2
- `GITEA_ORG` - Organization name (e.g., `bandit`)

### 3.3 Verify System Configuration

```bash
# Check file exists and has correct permissions
ls -la ~/.config/claude/gitea.env

# Should show:
# -rw------- gitea.env
```

**Security Note:** File should have `600` permissions (owner read/write only) to protect API tokens.

## Step 4: Project-Level Configuration

For each project where you'll use Projman, create a `.env` file:

### 4.1 Create Project .env File

```bash
# In your project root directory
cat > .env << 'EOF'
# Gitea Repository Configuration
GITEA_REPO=your-repo-name
EOF
```

**Example for MyProject:**
```bash
cat > .env << 'EOF'
GITEA_REPO=my-project
EOF
```

### 4.2 Verify Project Configuration

```bash
# Check .env exists
ls -la .env

# Check .env content
cat .env
```

**Note:** The `.env` file may already be in your `.gitignore`. If your project uses `.env` for other purposes, the Gitea configuration will merge with existing variables.

## Step 5: Configuration Verification

Test that everything is configured correctly:

### 5.1 Test Gitea Connection

```bash
# Test with curl
curl -H "Authorization: token YOUR_GITEA_TOKEN" \
  https://gitea.example.com/api/v1/user

# Should return your user information in JSON format
```

### 5.2 Test Wiki Access

```bash
# Test wiki API
curl -H "Authorization: token YOUR_GITEA_TOKEN" \
  https://gitea.example.com/api/v1/repos/YOUR_ORG/YOUR_REPO/wiki/pages

# Should return list of wiki pages (or empty array)
```

### 5.3 Test MCP Server Loading

```bash
# Navigate to plugin directory
cd plugins/projman

# Verify .mcp.json exists
cat .mcp.json

# Test loading (Claude Code will attempt to start MCP servers)
claude --debug
```

## Step 6: Initialize Plugin

### 6.1 Run Initial Setup

```bash
/initial-setup
```

This will:
- Validate Gitea MCP server connection
- Test credential configuration
- Sync label taxonomy
- Verify required directory structure

### 6.2 Sync Label Taxonomy

```bash
/labels-sync
```

This will:
- Fetch all labels from Gitea (organization + repository)
- Update `skills/label-taxonomy/labels-reference.md`
- Enable intelligent label suggestions

### 6.3 Verify Commands Available

```bash
# List available commands
/sprint-plan
/sprint-start
/sprint-status
/sprint-close
/labels-sync
/initial-setup
```

## Configuration Files Reference

### System-Level Files

**`~/.config/claude/gitea.env`:**
```bash
GITEA_URL=https://gitea.example.com
GITEA_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxxx
GITEA_ORG=your_organization
```

### Project-Level Files

**`.env` (in project root):**
```bash
GITEA_REPO=your-repo-name
```

### Plugin Configuration

**`projman/.mcp.json`:**
```json
{
  "mcpServers": {
    "gitea": {
      "command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/gitea/.venv/bin/python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/gitea",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/gitea"
      }
    }
  }
}
```

## Multi-Project Setup

To use Projman with multiple projects:

1. **System config:** Set up once (already done in Step 3)
2. **Project config:** Create `.env` in each project root:

**Project 1: Main App**
```bash
# ~/projects/my-app/.env
GITEA_REPO=my-app
```

**Project 2: App Site**
```bash
# ~/projects/my-app-site/.env
GITEA_REPO=my-app-site
```

**Project 3: Company Site**
```bash
# ~/projects/company-site/.env
GITEA_REPO=company-site
```

Each project operates independently with its own issues and lessons learned (stored in each repository's wiki).

## Troubleshooting

### Cannot find configuration files

**Problem:** MCP server reports "Configuration not found"

**Solution:**
```bash
# Check system config exists
ls -la ~/.config/claude/gitea.env

# If missing, recreate from Step 3
```

### Authentication failed

**Problem:** "401 Unauthorized" or "Invalid token"

**Solution:**
```bash
# Test Gitea token
curl -H "Authorization: token YOUR_TOKEN" \
  https://gitea.example.com/api/v1/user

# If fails, regenerate token (Step 2)
```

### MCP server not starting

**Problem:** "Failed to start MCP server"

**Solution:**
```bash
# Check Python virtual environment exists
ls plugins/projman/mcp-servers/gitea/.venv

# If missing, reinstall (Step 1)

# Check dependencies installed
cd plugins/projman/mcp-servers/gitea
source .venv/bin/activate
python -c "import requests; import mcp"

# If import fails, reinstall requirements
pip install -r requirements.txt
```

### Wrong repository

**Problem:** Issues created in wrong repo

**Solution:**
```bash
# Check project .env configuration
cat .env

# Verify GITEA_REPO matches Gitea repository name exactly

# Update if incorrect
```

### Permissions errors

**Problem:** "Permission denied" when creating issues or wiki pages

**Solution:**
- Verify token has `repo`, `read:org`, and `write:repo` permissions (Step 2)
- Regenerate token with correct permissions if needed

### Repository not in organization

**Problem:** "Repository must belong to configured organization"

**Solution:**
- Verify `GITEA_ORG` in system config matches the organization owning the repository
- Verify `GITEA_REPO` belongs to that organization
- Fork the repository to your organization if needed

## Security Best Practices

1. **Never commit tokens**
   - Keep credentials in `~/.config/claude/` only
   - Never hardcode tokens in code
   - Use system-level config for credentials

2. **Secure configuration files**
   - Set `600` permissions on `~/.config/claude/*.env`
   - Store in user home directory only
   - Don't share token files

3. **Rotate tokens periodically**
   - Regenerate tokens every 6-12 months
   - Immediately revoke if compromised
   - Use separate tokens for dev/prod if needed

4. **Minimum permissions**
   - Only grant required permissions
   - Gitea: `repo`, `read:org`, `read:user`, `write:repo`

5. **Monitor usage**
   - Review Gitea access logs periodically
   - Watch for unexpected API usage

## Next Steps

After configuration is complete:

1. Run `/initial-setup` to verify everything works
2. Run `/labels-sync` to fetch label taxonomy
3. Try `/sprint-plan` to start your first sprint
4. Read [README.md](./README.md) for usage guide

## Support

**Configuration Issues:**
- Check [README.md](./README.md) troubleshooting section
- Contact repository maintainer for support

**Questions:**
- Read command documentation: `commands/*.md`
- Check agent descriptions in `agents/`

---

**Configuration Status Checklist:**

- [ ] Python 3.10+ installed
- [ ] Gitea MCP server installed (in `mcp-servers/gitea/`)
- [ ] Gitea API token generated with correct permissions
- [ ] System config created (`~/.config/claude/gitea.env`)
- [ ] Project config created (`.env`)
- [ ] Gitea connection tested
- [ ] Wiki access tested
- [ ] `/initial-setup` completed successfully
- [ ] `/labels-sync` completed successfully
- [ ] Commands verified available

Once all items are checked, you're ready to use Projman!
