# Configuration Guide

Centralized configuration documentation for all plugins and MCP servers in the lm-claude-plugins marketplace.

## Overview

This marketplace uses a **hybrid configuration** approach:
- **System-level:** Credentials and service configuration (stored once per machine)
- **Project-level:** Repository-specific settings (stored per project)

**Benefits:**
- Single token per service (update once, use everywhere)
- Easy multi-project setup (just add `.env` per project)
- Security (tokens never committed to git)
- Project isolation (each project has its own scope)

## Prerequisites

Before configuring any plugin:

1. **Python 3.10+** installed
   ```bash
   python3 --version  # Should be 3.10.0 or higher
   ```

2. **Git repository** initialized
   ```bash
   git status  # Should show initialized repository
   ```

3. **Claude Code** installed and working

---

## System-Level Configuration

Configuration files stored in `~/.config/claude/`:

```bash
mkdir -p ~/.config/claude
```

### Gitea Configuration

Required by: `projman`, `pr-review`

```bash
cat > ~/.config/claude/gitea.env << 'EOF'
# Gitea API Configuration
GITEA_URL=https://gitea.example.com
GITEA_TOKEN=your_gitea_token_here
GITEA_ORG=your_organization
EOF

# Secure the file
chmod 600 ~/.config/claude/gitea.env
```

**Variables:**
| Variable | Description | Example |
|----------|-------------|---------|
| `GITEA_URL` | Gitea base URL (no `/api/v1`) | `https://gitea.example.com` |
| `GITEA_TOKEN` | Personal access token | `glpat-xxx...` |
| `GITEA_ORG` | Organization name | `bandit` |

**Generating Gitea Token:**
1. Log into Gitea → **User Icon** → **Settings**
2. **Applications** tab → **Manage Access Tokens**
3. **Generate New Token** with permissions:
   - `repo` (all sub-permissions)
   - `read:org`
   - `read:user`
   - `write:repo` (for wiki)
4. Copy token immediately (shown only once)

### NetBox Configuration

Required by: `cmdb-assistant`

```bash
cat > ~/.config/claude/netbox.env << 'EOF'
# NetBox API Configuration
NETBOX_URL=https://netbox.example.com
NETBOX_TOKEN=your_netbox_token_here
EOF

chmod 600 ~/.config/claude/netbox.env
```

**Variables:**
| Variable | Description | Example |
|----------|-------------|---------|
| `NETBOX_URL` | NetBox base URL | `https://netbox.example.com` |
| `NETBOX_TOKEN` | API token | `abc123...` |

### Git-Flow Configuration

Optional system defaults for: `git-flow`

```bash
cat > ~/.config/claude/git-flow.env << 'EOF'
# Git-Flow Default Configuration
GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=development
GIT_AUTO_DELETE_MERGED=true
GIT_AUTO_PUSH=false
GIT_PROTECTED_BRANCHES=main,master,development,staging,production
GIT_COMMIT_STYLE=conventional
GIT_CO_AUTHOR=true
EOF
```

---

## Project-Level Configuration

Create `.env` in each project root:

### Gitea Repository (projman, pr-review)

```bash
# .env in project root
GITEA_REPO=your-repo-name
```

### Git-Flow (project overrides)

```bash
# .env in project root
GIT_WORKFLOW_STYLE=pr-required
GIT_DEFAULT_BASE=main
```

### PR Review

```bash
# .env in project root
PR_REVIEW_CONFIDENCE_THRESHOLD=0.5
PR_REVIEW_AUTO_SUBMIT=false
```

---

## MCP Server Installation

MCP servers are located at repository root: `mcp-servers/`

### Gitea MCP Server

```bash
cd mcp-servers/gitea

# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python -c "from mcp_server import server; print('OK')"

deactivate
```

### NetBox MCP Server

```bash
cd mcp-servers/netbox

# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python -c "from mcp_server import server; print('OK')"

deactivate
```

---

## Plugin Configuration Reference

### projman

| Level | Variable | Default | Description |
|-------|----------|---------|-------------|
| System | `GITEA_URL` | (required) | Gitea API base URL |
| System | `GITEA_TOKEN` | (required) | API token |
| System | `GITEA_ORG` | (required) | Organization name |
| Project | `GITEA_REPO` | (required) | Repository name |

**Commands:** `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close`, `/labels-sync`, `/initial-setup`, `/review`, `/test-check`, `/test-gen`

### pr-review

| Level | Variable | Default | Description |
|-------|----------|---------|-------------|
| System | `GITEA_URL` | (required) | Gitea API base URL |
| System | `GITEA_TOKEN` | (required) | API token |
| Project | `GITEA_REPO` | (required) | Repository name |
| Project | `PR_REVIEW_CONFIDENCE_THRESHOLD` | `0.5` | Minimum confidence |
| Project | `PR_REVIEW_AUTO_SUBMIT` | `false` | Auto-submit reviews |

**Commands:** `/pr-review`, `/pr-summary`, `/pr-findings`

### git-flow

| Level | Variable | Default | Description |
|-------|----------|---------|-------------|
| System/Project | `GIT_WORKFLOW_STYLE` | `feature-branch` | Branching strategy |
| System/Project | `GIT_DEFAULT_BASE` | `development` | Default base branch |
| System/Project | `GIT_AUTO_DELETE_MERGED` | `true` | Delete merged branches |
| System/Project | `GIT_AUTO_PUSH` | `false` | Auto-push after commit |
| System/Project | `GIT_PROTECTED_BRANCHES` | `main,master,...` | Protected branches |
| System/Project | `GIT_COMMIT_STYLE` | `conventional` | Commit message style |
| System/Project | `GIT_CO_AUTHOR` | `true` | Include Claude co-author |

**Commands:** `/commit`, `/commit-push`, `/commit-merge`, `/commit-sync`, `/branch-start`, `/branch-cleanup`, `/git-status`, `/git-config`

### clarity-assist

No configuration required. Uses sensible defaults.

**Commands:** `/clarify`, `/quick-clarify`

### cmdb-assistant

| Level | Variable | Default | Description |
|-------|----------|---------|-------------|
| System | `NETBOX_URL` | (required) | NetBox API base URL |
| System | `NETBOX_TOKEN` | (required) | API token |

### doc-guardian

No configuration required. Hook-based plugin.

### code-sentinel

No configuration required. Hook-based plugin.

### project-hygiene

No configuration required. Hook-based plugin.

### claude-config-maintainer

No configuration required.

---

## Multi-Project Setup

1. **System config:** Set up once (credentials)
2. **Project config:** Create `.env` in each project root

**Example:**
```bash
# ~/projects/my-app/.env
GITEA_REPO=my-app

# ~/projects/another-app/.env
GITEA_REPO=another-app
GIT_WORKFLOW_STYLE=trunk-based
```

---

## Verification

### Test Gitea Connection

```bash
curl -H "Authorization: token YOUR_TOKEN" \
  https://gitea.example.com/api/v1/user
```

### Test MCP Server

```bash
cd mcp-servers/gitea
source .venv/bin/activate
python -c "from mcp_server import server; print('OK')"
```

### Run Plugin Setup

```bash
# For projman
/initial-setup
/labels-sync
```

---

## Troubleshooting

### Configuration not found

```bash
# Check system config exists
ls -la ~/.config/claude/gitea.env

# Check permissions (should be 600)
stat ~/.config/claude/gitea.env
```

### Authentication failed

```bash
# Test token directly
curl -H "Authorization: token YOUR_TOKEN" \
  https://gitea.example.com/api/v1/user

# Regenerate if invalid
```

### MCP server not starting

```bash
# Check venv exists
ls mcp-servers/gitea/.venv

# Reinstall if missing
cd mcp-servers/gitea
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Wrong repository

```bash
# Check project .env
cat .env

# Verify GITEA_REPO matches exactly
```

---

## Security Best Practices

1. **Never commit tokens**
   - Keep credentials in `~/.config/claude/` only
   - Add `.env` to `.gitignore`

2. **Secure configuration files**
   ```bash
   chmod 600 ~/.config/claude/*.env
   ```

3. **Rotate tokens periodically**
   - Every 6-12 months
   - Immediately if compromised

4. **Minimum permissions**
   - Only grant required token permissions
   - Use separate tokens for different environments

---

## Quick Setup Checklist

- [ ] Python 3.10+ installed
- [ ] `~/.config/claude/` directory created
- [ ] Service credentials configured (gitea.env, netbox.env)
- [ ] Configuration files secured (chmod 600)
- [ ] MCP servers installed with venv
- [ ] Project `.env` created with repository settings
- [ ] Connections tested
- [ ] Plugin commands verified
