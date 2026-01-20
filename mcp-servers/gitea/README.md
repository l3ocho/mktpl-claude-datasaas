# Gitea MCP Server

Model Context Protocol (MCP) server for Gitea integration with Claude Code.

## Overview

The Gitea MCP Server provides Claude Code with direct access to Gitea for issue management, label operations, and repository tracking. It supports both single-repository (project mode) and multi-repository (company/PMO mode) operations.

**Status**: ✅ Phase 1 Complete - Fully functional and tested

## Features

### Core Functionality

- **Issue Management**: CRUD operations for Gitea issues
- **Label Taxonomy**: Dynamic 44-label system with intelligent suggestions
- **Mode Detection**: Automatic project vs company-wide mode detection
- **Branch-Aware Security**: Prevents accidental changes on production branches
- **Hybrid Configuration**: System-level credentials + project-level paths
- **PMO Support**: Multi-repository aggregation for organization-wide views

### Tools Provided

| Tool | Description | Mode |
|------|-------------|------|
| `list_issues` | List issues from repository | Both |
| `get_issue` | Get specific issue details | Both |
| `create_issue` | Create new issue with labels | Both |
| `update_issue` | Update existing issue | Both |
| `add_comment` | Add comment to issue | Both |
| `get_labels` | Get all labels (org + repo) | Both |
| `suggest_labels` | Intelligent label suggestion | Both |
| `aggregate_issues` | Cross-repository issue aggregation | PMO Only |

## Architecture

### Directory Structure

```
mcp-servers/gitea/
├── .venv/                      # Python virtual environment
├── requirements.txt            # Python dependencies
├── mcp_server/
│   ├── __init__.py
│   ├── server.py              # MCP server entry point
│   ├── config.py              # Configuration loader
│   ├── gitea_client.py        # Gitea API client
│   └── tools/
│       ├── __init__.py
│       ├── issues.py          # Issue tools
│       └── labels.py          # Label tools
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_gitea_client.py
│   ├── test_issues.py
│   └── test_labels.py
├── README.md                   # This file
└── TESTING.md                  # Testing instructions
```

### Mode Detection

The server operates in two modes based on environment variables:

**Project Mode** (Single Repository):
- When `GITEA_REPO` is set
- Operates on single repository
- Used by `projman` plugin

**Company Mode** (Multi-Repository / PMO):
- When `GITEA_REPO` is NOT set
- Operates on all repositories in organization
- Used by `projman-pmo` plugin

### Branch-Aware Security

Operations are restricted based on the current Git branch:

| Branch | Read | Create Issue | Update/Comment |
|--------|------|--------------|----------------|
| `main`, `master`, `prod/*` | ✅ | ❌ | ❌ |
| `staging`, `stage/*` | ✅ | ✅ | ❌ |
| `development`, `develop`, `feat/*`, `dev/*` | ✅ | ✅ | ✅ |

## Installation

### Prerequisites

- Python 3.10 or higher
- Git repository (for branch detection)
- Access to Gitea instance with API token

### Step 1: Install Dependencies

```bash
cd mcp-servers/gitea
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Step 2: Configure System-Level Settings

Create `~/.config/claude/gitea.env`:

```bash
mkdir -p ~/.config/claude

cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.example.com/api/v1
GITEA_API_TOKEN=your_gitea_token_here
GITEA_OWNER=bandit
EOF

chmod 600 ~/.config/claude/gitea.env
```

### Step 3: Configure Project-Level Settings (Optional)

For project mode, create `.env` in your project root:

```bash
echo "GITEA_REPO=your-repo-name" > .env
echo ".env" >> .gitignore
```

For company/PMO mode, omit the `.env` file or don't set `GITEA_REPO`.

## Configuration

### System-Level Configuration

**File**: `~/.config/claude/gitea.env`

**Required Variables**:
- `GITEA_API_URL` - Gitea API endpoint (e.g., `https://gitea.example.com/api/v1`)
- `GITEA_API_TOKEN` - Personal access token with repo permissions
- `GITEA_OWNER` - Organization or user name (e.g., `bandit`)

### Project-Level Configuration

**File**: `<project-root>/.env`

**Optional Variables**:
- `GITEA_REPO` - Repository name (enables project mode)

### Generating Gitea API Token

1. Log into Gitea: https://gitea.example.com
2. Navigate to: **Settings** → **Applications** → **Manage Access Tokens**
3. Click **Generate New Token**
4. Configure token:
   - **Token Name**: `claude-code-mcp`
   - **Permissions**:
     - ✅ `repo` (all) - Read/write repositories, issues, labels
     - ✅ `read:org` - Read organization information and labels
     - ✅ `read:user` - Read user information
5. Click **Generate Token**
6. Copy token immediately (shown only once)
7. Add to `~/.config/claude/gitea.env`

## Usage

### Running the MCP Server

```bash
cd mcp-servers/gitea
source .venv/bin/activate
python -m mcp_server.server
```

The server communicates via JSON-RPC 2.0 over stdio.

### Integration with Claude Code Plugins

The MCP server is designed to be used by Claude Code plugins via `.mcp.json` configuration:

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
    }
  }
}
```

### Example Tool Calls

**List Issues**:
```python
from mcp_server.tools.issues import IssueTools
from mcp_server.gitea_client import GiteaClient

client = GiteaClient()
issue_tools = IssueTools(client)

issues = await issue_tools.list_issues(state='open', labels=['Type/Bug'])
```

**Suggest Labels**:
```python
from mcp_server.tools.labels import LabelTools

label_tools = LabelTools(client)

context = "Fix critical authentication bug in production API"
suggestions = await label_tools.suggest_labels(context)
# Returns: ['Type/Bug', 'Priority/Critical', 'Component/Auth', 'Component/API', ...]
```

## Testing

### Unit Tests

Run all 42 unit tests with mocks:

```bash
pytest tests/ -v
```

Expected: `42 passed in 0.57s`

### Integration Tests

Test with real Gitea instance:

```bash
python -c "
from mcp_server.gitea_client import GiteaClient

client = GiteaClient()
issues = client.list_issues(state='open')
print(f'Found {len(issues)} open issues')
"
```

### Full Testing Guide

See [TESTING.md](./TESTING.md) for comprehensive testing instructions.

## Label Taxonomy System

The system supports a dynamic 44-label taxonomy (28 org + 16 repo):

**Organization Labels (28)**:
- `Agent/*` (2) - Agent/Human, Agent/Claude
- `Complexity/*` (3) - Simple, Medium, Complex
- `Efforts/*` (5) - XS, S, M, L, XL
- `Priority/*` (4) - Low, Medium, High, Critical
- `Risk/*` (3) - Low, Medium, High
- `Source/*` (4) - Development, Staging, Production, Customer
- `Type/*` (6) - Bug, Feature, Refactor, Documentation, Test, Chore

**Repository Labels (16)**:
- `Component/*` (9) - Backend, Frontend, API, Database, Auth, Deploy, Testing, Docs, Infra
- `Tech/*` (7) - Python, JavaScript, Docker, PostgreSQL, Redis, Vue, FastAPI

Labels are fetched dynamically from Gitea and suggestions adapt to the current taxonomy.

## Security

### Token Storage

- Store tokens in `~/.config/claude/gitea.env`
- Set file permissions to `600` (read/write owner only)
- Never commit tokens to Git
- Use separate tokens for development and production

### Branch Detection

The MCP server implements defense-in-depth branch detection:

1. **MCP Tools**: Check branch before operations
2. **Agent Prompts**: Warn users about branch restrictions
3. **CLAUDE.md**: Provides additional context

### Input Validation

- All user input is validated before API calls
- Issue titles and descriptions are sanitized
- Label names are checked against taxonomy
- Repository names are validated

## Troubleshooting

### Common Issues

**Module not found**:
```bash
cd mcp-servers/gitea
source .venv/bin/activate
```

**Configuration not found**:
```bash
ls -la ~/.config/claude/gitea.env
# If missing, create it following installation steps
```

**Authentication failed**:
```bash
# Test token manually
curl -H "Authorization: token YOUR_TOKEN" \
  https://gitea.example.com/api/v1/user
```

**Permission denied on branch**:
```bash
# Check current branch
git branch --show-current

# Switch to development branch
git checkout development
```

See [TESTING.md](./TESTING.md#troubleshooting) for more details.

## Development

### Project Structure

- `config.py` - Hybrid configuration loader with mode detection
- `gitea_client.py` - Synchronous Gitea API client using requests
- `tools/issues.py` - Async wrappers with branch detection
- `tools/labels.py` - Label management and suggestion
- `server.py` - MCP server with JSON-RPC 2.0 over stdio

### Adding New Tools

1. Add method to `GiteaClient` (sync)
2. Add async wrapper to appropriate tool class
3. Register tool in `server.py` `setup_tools()`
4. Add unit tests
5. Update documentation

### Testing Philosophy

- **Unit tests**: Use mocks for fast feedback
- **Integration tests**: Use real Gitea API for validation
- **Branch detection**: Test all branch types
- **Mode detection**: Test both project and company modes

## Performance

### Caching

Labels are cached to reduce API calls:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_labels_cached(self, repo: str):
    return self.get_labels(repo)
```

### Retry Logic

API calls include automatic retry with exponential backoff:

```python
@retry_on_failure(max_retries=3, delay=1)
def list_issues(self, state='open', labels=None, repo=None):
    # Implementation
```

## Changelog

### v1.0.0 (2025-01-06) - Phase 1 Complete

✅ Initial implementation:
- Configuration management (hybrid system + project)
- Gitea API client with all CRUD operations
- MCP server with 8 tools
- Issue tools with branch detection
- Label tools with intelligent suggestions
- Mode detection (project vs company)
- Branch-aware security model
- 42 unit tests (100% passing)
- Comprehensive documentation

## License

MIT License - Part of the Claude Code Marketplace project.

## Related Documentation

- **Projman Documentation**: `plugins/projman/README.md`
- **Configuration Guide**: `plugins/projman/CONFIGURATION.md`
- **Testing Guide**: `TESTING.md`

## Support

For issues or questions:
1. Check [TESTING.md](./TESTING.md) troubleshooting section
2. Review [plugins/projman/README.md](../../README.md) for plugin documentation
3. Create an issue in the project repository

---

**Built for**: Claude Code Marketplace - Project Management Plugins
**Phase**: 1 (Complete)
**Status**: ✅ Production Ready
**Last Updated**: 2025-01-06
