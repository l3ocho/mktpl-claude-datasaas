# Configuration Guide - Projman Plugin

Complete setup and configuration instructions for the Projman project management plugin.

## Overview

The Projman plugin uses a **hybrid configuration** approach:
- **System-level:** Credentials for Gitea and Wiki.js (stored once per machine)
- **Project-level:** Repository and project paths (stored per project)

This design allows:
- ✅ Single token per service (update once, use everywhere)
- ✅ Easy multi-project setup (just add `.env` per project)
- ✅ Security (tokens never committed to git)
- ✅ Project isolation (each project has its own scope)

## Prerequisites

Before configuring the plugin, ensure you have:

1. **Python 3.10+** installed
   ```bash
   python --version  # Should be 3.10.0 or higher
   ```

2. **Git repository** initialized
   ```bash
   git status  # Should show initialized repository
   ```

3. **Gitea access** with an account and permissions to:
   - Create issues
   - Manage labels
   - Read organization information

4. **Wiki.js access** with an account and permissions to:
   - Create and edit pages
   - Manage tags
   - Read and write content

5. **Claude Code** installed and working

## Step 1: Install MCP Servers

The plugin requires two MCP servers installed at `../mcp-servers/` relative to the plugin:

### 1.1 Install Gitea MCP Server

```bash
# Navigate to Gitea MCP server directory
cd ../mcp-servers/gitea

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from mcp_server import server; print('Gitea MCP Server installed successfully')"
```

### 1.2 Install Wiki.js MCP Server

```bash
# Navigate to Wiki.js MCP server directory
cd ../mcp-servers/wikijs

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from mcp_server import server; print('Wiki.js MCP Server installed successfully')"
```

## Step 2: Generate API Tokens

### 2.1 Generate Gitea API Token

1. Log into Gitea: https://gitea.hotserv.cloud
2. Navigate to: **User Icon** (top right) → **Settings**
3. Click **Applications** tab
4. Scroll to **Manage Access Tokens**
5. Click **Generate New Token**
6. Configure token:
   - **Token Name:** `claude-code-projman`
   - **Permissions:**
     - ✅ `repo` (all sub-permissions) - Repository access
     - ✅ `read:org` - Read organization information and labels
     - ✅ `read:user` - Read user information
7. Click **Generate Token**
8. **IMPORTANT:** Copy token immediately (shown only once!)
9. Save token securely - you'll need it in Step 3

**Token Permissions Explained:**
- `repo` - Create, read, update issues and labels
- `read:org` - Access organization-level labels
- `read:user` - Associate issues with user account

### 2.2 Generate Wiki.js API Token

1. Log into Wiki.js: https://wiki.hyperhivelabs.com
2. Navigate to: **Administration** (top right)
3. Click **API Access** in the left sidebar
4. Click **New API Key**
5. Configure API key:
   - **Name:** `claude-code-projman`
   - **Expiration:** None (or set to your security policy)
   - **Permissions:**
     - ✅ **Pages:** Read, Create, Update
     - ✅ **Search:** Read
6. Click **Create**
7. **IMPORTANT:** Copy the JWT token immediately (shown only once!)
8. Save token securely - you'll need it in Step 3

**Token Permissions Explained:**
- Pages (read/create/update) - Manage documentation and lessons learned
- Search (read) - Find relevant lessons from previous sprints

## Step 3: System-Level Configuration

Create system-wide configuration files in `~/.config/claude/`:

### 3.1 Create Configuration Directory

```bash
mkdir -p ~/.config/claude
```

### 3.2 Configure Gitea

```bash
cat > ~/.config/claude/gitea.env << 'EOF'
# Gitea API Configuration
GITEA_API_URL=https://gitea.hotserv.cloud/api/v1
GITEA_API_TOKEN=your_gitea_token_here
GITEA_OWNER=hhl-infra
EOF

# Secure the file (owner read/write only)
chmod 600 ~/.config/claude/gitea.env
```

**Replace `your_gitea_token_here` with the token from Step 2.1**

**Configuration Variables:**
- `GITEA_API_URL` - Gitea API endpoint (includes `/api/v1`)
- `GITEA_API_TOKEN` - Personal access token from Step 2.1
- `GITEA_OWNER` - Organization or user name (e.g., `hhl-infra`)

### 3.3 Configure Wiki.js

```bash
cat > ~/.config/claude/wikijs.env << 'EOF'
# Wiki.js API Configuration
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_wikijs_token_here
WIKIJS_BASE_PATH=/hyper-hive-labs
EOF

# Secure the file (owner read/write only)
chmod 600 ~/.config/claude/wikijs.env
```

**Replace `your_wikijs_token_here` with the JWT token from Step 2.2**

**Configuration Variables:**
- `WIKIJS_API_URL` - Wiki.js GraphQL endpoint (includes `/graphql`)
- `WIKIJS_API_TOKEN` - API key from Step 2.2 (JWT format)
- `WIKIJS_BASE_PATH` - Base path in Wiki.js (e.g., `/hyper-hive-labs`)

### 3.4 Verify System Configuration

```bash
# Check files exist and have correct permissions
ls -la ~/.config/claude/

# Should show:
# -rw------- gitea.env
# -rw------- wikijs.env
```

**Security Note:** Files should have `600` permissions (owner read/write only) to protect API tokens.

## Step 4: Project-Level Configuration

For each project where you'll use Projman, create a `.env` file:

### 4.1 Create Project .env File

```bash
# In your project root directory
cat > .env << 'EOF'
# Gitea Repository Configuration
GITEA_REPO=your-repo-name

# Wiki.js Project Configuration
WIKIJS_PROJECT=projects/your-project-name
EOF
```

**Example for CuisineFlow project:**
```bash
cat > .env << 'EOF'
GITEA_REPO=cuisineflow
WIKIJS_PROJECT=projects/cuisineflow
EOF
```

### 4.2 Add .env to .gitignore

**CRITICAL:** Never commit `.env` to git!

```bash
# Add to .gitignore
echo ".env" >> .gitignore

# Verify
git check-ignore .env  # Should output: .env
```

### 4.3 Verify Project Configuration

```bash
# Check .env exists
ls -la .env

# Check it's in .gitignore
cat .gitignore | grep "\.env"
```

## Step 5: Configuration Verification

Test that everything is configured correctly:

### 5.1 Test Gitea Connection

```bash
# Test with curl
curl -H "Authorization: token YOUR_GITEA_TOKEN" \
  https://gitea.hotserv.cloud/api/v1/user

# Should return your user information in JSON format
```

### 5.2 Test Wiki.js Connection

```bash
# Test GraphQL endpoint
curl -H "Authorization: Bearer YOUR_WIKIJS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ pages { list { id title } } }"}' \
  https://wiki.hyperhivelabs.com/graphql

# Should return pages data in JSON format
```

### 5.3 Test MCP Server Loading

```bash
# Navigate to plugin directory
cd projman

# Verify .mcp.json exists
cat .mcp.json

# Test loading (Claude Code will attempt to start MCP servers)
claude --debug
```

## Step 6: Initialize Plugin

### 6.1 Sync Label Taxonomy

First time setup - fetch labels from Gitea:

```bash
/labels-sync
```

This will:
- Fetch all labels from Gitea (organization + repository)
- Update `skills/label-taxonomy/labels-reference.md`
- Enable intelligent label suggestions

### 6.2 Verify Commands Available

```bash
# List available commands
/sprint-plan --help
/sprint-start --help
/sprint-status --help
/sprint-close --help
/labels-sync --help
```

## Configuration Files Reference

### System-Level Files

**`~/.config/claude/gitea.env`:**
```bash
GITEA_API_URL=https://gitea.hotserv.cloud/api/v1
GITEA_API_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxxx
GITEA_OWNER=hhl-infra
```

**`~/.config/claude/wikijs.env`:**
```bash
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
WIKIJS_BASE_PATH=/hyper-hive-labs
```

### Project-Level Files

**`.env` (in project root):**
```bash
GITEA_REPO=cuisineflow
WIKIJS_PROJECT=projects/cuisineflow
```

**`.gitignore` (must include):**
```
.env
```

### Plugin Configuration

**`projman/.mcp.json`:**
```json
{
  "mcpServers": {
    "gitea": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea"
      }
    },
    "wikijs": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs"
      }
    }
  }
}
```

## Multi-Project Setup

To use Projman with multiple projects:

1. **System config:** Set up once (already done in Step 3)
2. **Project config:** Create `.env` in each project root:

**Project 1: CuisineFlow**
```bash
# ~/projects/cuisineflow/.env
GITEA_REPO=cuisineflow
WIKIJS_PROJECT=projects/cuisineflow
```

**Project 2: CuisineFlow-Site**
```bash
# ~/projects/cuisineflow-site/.env
GITEA_REPO=cuisineflow-site
WIKIJS_PROJECT=projects/cuisineflow-site
```

**Project 3: HHL-Site**
```bash
# ~/projects/hhl-site/.env
GITEA_REPO=hhl-site
WIKIJS_PROJECT=projects/hhl-site
```

Each project operates independently with its own issues and lessons learned.

## Troubleshooting

### Cannot find configuration files

**Problem:** MCP server reports "Configuration not found"

**Solution:**
```bash
# Check system config exists
ls -la ~/.config/claude/gitea.env
ls -la ~/.config/claude/wikijs.env

# If missing, recreate from Step 3
```

### Authentication failed

**Problem:** "401 Unauthorized" or "Invalid token"

**Solution:**
```bash
# Test Gitea token
curl -H "Authorization: token YOUR_TOKEN" \
  https://gitea.hotserv.cloud/api/v1/user

# Test Wiki.js token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://wiki.hyperhivelabs.com/graphql

# If fails, regenerate token (Step 2)
```

### MCP server not starting

**Problem:** "Failed to start MCP server"

**Solution:**
```bash
# Check Python virtual environment exists
ls ../mcp-servers/gitea/.venv
ls ../mcp-servers/wikijs/.venv

# If missing, reinstall (Step 1)

# Check dependencies installed
cd ../mcp-servers/gitea
source .venv/bin/activate
python -c "import requests; import mcp"

# If import fails, reinstall requirements
pip install -r requirements.txt
```

### Wrong repository or project

**Problem:** Issues created in wrong repo or lessons saved to wrong project

**Solution:**
```bash
# Check project .env configuration
cat .env

# Verify GITEA_REPO matches Gitea repository name
# Verify WIKIJS_PROJECT matches Wiki.js project path

# Update if incorrect
nano .env
```

### Permissions errors

**Problem:** "Permission denied" when creating issues or pages

**Solution:**
- **Gitea:** Verify token has `repo` and `read:org` permissions (Step 2.1)
- **Wiki.js:** Verify token has Pages (create/update) permissions (Step 2.2)
- Regenerate tokens with correct permissions if needed

## Security Best Practices

1. **Never commit tokens**
   - Keep `.env` in `.gitignore`
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
   - Gitea: `repo`, `read:org`, `read:user`
   - Wiki.js: Pages (read/create/update), Search (read)

5. **Monitor usage**
   - Review Gitea access logs periodically
   - Check Wiki.js audit logs
   - Watch for unexpected API usage

## Next Steps

After configuration is complete:

1. ✅ Run `/labels-sync` to fetch label taxonomy
2. ✅ Try `/sprint-plan` to start your first sprint
3. ✅ Read [README.md](./README.md) for usage guide
4. ✅ Review command documentation in `commands/`

## Support

**Configuration Issues:**
- Check [README.md](./README.md) troubleshooting section
- Review MCP server documentation:
  - [Gitea MCP](../mcp-servers/gitea/README.md)
  - [Wiki.js MCP](../mcp-servers/wikijs/README.md)
- Open issue: https://gitea.hotserv.cloud/hhl-infra/claude-code-hhl-toolkit/issues

**Questions:**
- Read command documentation: `commands/*.md`
- Check agent descriptions in `agents/` (Phase 3)
- Review skills: `skills/label-taxonomy/`

---

**Configuration Status Checklist:**

- [ ] Python 3.10+ installed
- [ ] Gitea MCP server installed
- [ ] Wiki.js MCP server installed
- [ ] Gitea API token generated
- [ ] Wiki.js API token generated
- [ ] System config created (`~/.config/claude/*.env`)
- [ ] Project config created (`.env`)
- [ ] `.env` added to `.gitignore`
- [ ] Gitea connection tested
- [ ] Wiki.js connection tested
- [ ] `/labels-sync` completed successfully
- [ ] Commands verified available

Once all items are checked, you're ready to use Projman!
