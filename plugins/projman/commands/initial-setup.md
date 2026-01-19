---
description: Run initial setup for projman plugin
---

# Initial Setup

Run the installation script to set up the projman plugin.

## What This Does

1. Creates Python virtual environments for MCP servers
2. Installs all dependencies
3. Creates configuration file templates
4. Validates existing configuration
5. Validates repository organization
6. Syncs label taxonomy
7. Reports remaining manual steps

## Execution

```bash
cd ${PROJECT_ROOT}
./scripts/setup.sh
```

## Configuration Structure

The plugin uses a hybrid configuration approach:

**System-Level (credentials):**
```
~/.config/claude/gitea.env
```
Contains API credentials that work across all projects.

**Project-Level (repository/paths):**
```
project-root/.env
```
Contains project-specific settings like repository name.

## After Running

Review the output for any manual steps required:

1. **Configure API credentials** in `~/.config/claude/gitea.env`:
   ```
   GITEA_URL=https://gitea.your-company.com
   GITEA_TOKEN=your-api-token
   GITEA_ORG=your-organization
   ```

2. **Configure project settings** in `.env`:
   ```
   GITEA_REPO=your-repo-name
   WIKIJS_PROJECT=your-project
   ```

3. **Run `/labels-sync`** to sync Gitea labels

4. **Verify Gitea Wiki** is accessible and has proper structure

## Pre-Flight Checks

The setup script validates:

- Repository belongs to an organization (required)
- Required label categories exist
- API credentials are valid
- Network connectivity to Gitea

## Re-Running

This command is safe to run multiple times. It will skip already-completed steps.

## MCP Server Structure

The plugin bundles these MCP servers:

```
plugins/projman/mcp-servers/
└── gitea/
    ├── .venv/
    ├── requirements.txt
    └── mcp_server/
        ├── server.py
        ├── gitea_client.py
        └── tools/
            ├── issues.py
            ├── labels.py
            ├── wiki.py
            ├── milestones.py
            └── dependencies.py
```

## Troubleshooting

**Error: Repository not under organization**
- This plugin requires repositories to belong to a Gitea organization
- Transfer your repository to an organization or create one

**Error: Missing required labels**
- Run `/labels-sync` to create missing labels
- Or create them manually in Gitea

**Error: Cannot connect to Gitea**
- Verify `GITEA_URL` in `~/.config/claude/gitea.env`
- Check your API token has proper permissions
- Ensure network connectivity

**Error: Virtual environment creation failed**
- Ensure Python 3.8+ is installed
- Check disk space
- Try running `python -m venv .venv` manually in the MCP server directory
