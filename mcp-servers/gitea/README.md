# Gitea MCP Server (Marketplace Wrapper)

This directory provides the virtual environment for the `gitea-mcp` package.

## Package

**Source:** [gitea-mcp](https://gitea.hotserv.cloud/personal-projects/gitea-mcp)
**Registry:** Gitea PyPI at gitea.hotserv.cloud
**Version:** >=1.0.0

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or use the marketplace setup script:

```bash
./scripts/setup-venvs.sh gitea
```

## Configuration

See `~/.config/claude/gitea.env` for system-level config (API URL, token).
See project `.env` for project-level config (GITEA_ORG, GITEA_REPO).

## Updating

```bash
source .venv/bin/activate
pip install --upgrade gitea-mcp \
  --extra-index-url https://gitea.hotserv.cloud/api/packages/personal-projects/pypi/simple
```

## Features

The `gitea-mcp` package provides MCP tools for:

- **Issues**: CRUD, comments, dependencies, execution order
- **Labels**: Get, suggest, create (org + repo level)
- **Milestones**: CRUD operations
- **Pull Requests**: List, get, diff, comments, reviews, create
- **Wiki**: Pages, lessons learned, RFC allocation
- **Validation**: Repository org check, branch protection
