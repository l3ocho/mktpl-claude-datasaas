# Wiki.js MCP Server

Model Context Protocol (MCP) server for Wiki.js integration with Claude Code.

## Overview

The Wiki.js MCP Server provides Claude Code with direct access to Wiki.js for documentation management, lessons learned capture, and knowledge base operations. It supports both single-project (project mode) and company-wide (PMO mode) operations.

**Status**: ✅ Phase 1.1b Complete - Fully functional and tested

## Features

### Core Functionality

- **Page Management**: CRUD operations for Wiki.js pages with markdown content
- **Lessons Learned**: Systematic capture and searchable repository of sprint insights
- **Mode Detection**: Automatic project vs company-wide mode detection
- **Hybrid Configuration**: System-level credentials + project-level paths
- **PMO Support**: Company-wide documentation and cross-project lesson search

### Tools Provided

| Tool | Description | Mode |
|------|-------------|------|
| `search_pages` | Search pages by keywords and tags | Both |
| `get_page` | Get specific page content | Both |
| `create_page` | Create new page with markdown content | Both |
| `update_page` | Update existing page | Both |
| `list_pages` | List pages under a path | Both |
| `create_lesson` | Create lessons learned entry | Both |
| `search_lessons` | Search lessons from previous sprints | Both |
| `tag_lesson` | Add/update tags on lessons | Both |

## Architecture

### Directory Structure

```
mcp-servers/wikijs/
├── .venv/                      # Python virtual environment
├── requirements.txt            # Python dependencies
├── mcp_server/
│   ├── __init__.py
│   ├── server.py              # MCP server entry point
│   ├── config.py              # Configuration loader
│   ├── wikijs_client.py       # Wiki.js GraphQL client
│   └── tools/
│       ├── __init__.py
│       ├── pages.py           # Page management tools
│       └── lessons_learned.py # Lessons learned tools
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_wikijs_client.py
├── README.md                   # This file
└── TESTING.md                  # Testing instructions
```

### Mode Detection

The server operates in two modes based on environment variables:

**Project Mode** (Single Project):
- When `WIKIJS_PROJECT` is set
- Operates on single project path
- Used by `projman` plugin
- Pages scoped to `/base_path/project/`

**Company Mode** (Multi-Project / PMO):
- When `WIKIJS_PROJECT` is NOT set
- Operates on all projects in organization
- Used by `projman-pmo` plugin
- Pages scoped to `/base_path/`

### GraphQL Integration

The server uses Wiki.js GraphQL API for all operations:
- **Pages API**: Create, read, update, list, search pages
- **Tags**: Categorize and filter content
- **Search**: Full-text search with tag filtering
- **Lessons Learned**: Specialized workflow for sprint insights

## Installation

### Prerequisites

- Python 3.10 or higher
- Access to Wiki.js instance with API token
- GraphQL API enabled on Wiki.js

### Step 1: Install Dependencies

```bash
cd mcp-servers/wikijs
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Step 2: System Configuration

Create system-level configuration with credentials:

```bash
mkdir -p ~/.config/claude

cat > ~/.config/claude/wikijs.env << 'EOF'
# Wiki.js API Configuration
WIKIJS_API_URL=http://wikijs.hotport/graphql
WIKIJS_API_TOKEN=your_api_token_here
WIKIJS_BASE_PATH=/hyper-hive-labs
EOF

chmod 600 ~/.config/claude/wikijs.env
```

**Obtaining Wiki.js API Token:**
1. Log in to Wiki.js as administrator
2. Navigate to Administration → API Access
3. Click "New API Key"
4. Set permissions: Pages (read/write), Search (read)
5. Copy the generated JWT token

### Step 3: Project Configuration (Optional)

For project-scoped operations, create `.env` in project root:

```bash
# In your project directory
cat > .env << 'EOF'
# Wiki.js project path
WIKIJS_PROJECT=projects/your-project-name
EOF

# Add to .gitignore
echo ".env" >> .gitignore
```

**Note:** Omit `.env` for company-wide (PMO) mode.

## Usage

### Running the MCP Server

```bash
cd mcp-servers/wikijs
source .venv/bin/activate
python -m mcp_server.server
```

The server runs as a stdio-based MCP server and communicates via JSON-RPC 2.0.

### Integration with Claude Code

The MCP server is referenced in plugin `.mcp.json`:

```json
{
  "mcpServers": {
    "wikijs": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
      "env": {}
    }
  }
}
```

### Example Tool Calls

**Search Pages:**
```json
{
  "name": "search_pages",
  "arguments": {
    "query": "API documentation",
    "tags": "backend,api",
    "limit": 10
  }
}
```

**Create Lesson Learned:**
```json
{
  "name": "create_lesson",
  "arguments": {
    "title": "Sprint 16 - Prevent Claude Code Infinite Loops",
    "content": "## Problem\\n\\nClaude Code entered infinite loop...\\n\\n## Solution\\n\\n...",
    "tags": "claude-code,testing,validation",
    "category": "sprints"
  }
}
```

**Search Lessons:**
```json
{
  "name": "search_lessons",
  "arguments": {
    "query": "validation",
    "tags": "testing,claude-code",
    "limit": 20
  }
}
```

## Configuration Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `WIKIJS_API_URL` | Wiki.js GraphQL endpoint | `http://wiki.example.com/graphql` |
| `WIKIJS_API_TOKEN` | API authentication token (JWT) | `eyJhbGciOiJSUzI1...` |
| `WIKIJS_BASE_PATH` | Base path in Wiki.js | `/hyper-hive-labs` |

### Optional Variables

| Variable | Description | Mode |
|----------|-------------|------|
| `WIKIJS_PROJECT` | Project-specific path | Project mode only |

### Configuration Priority

1. Project-level `.env` (overrides system)
2. System-level `~/.config/claude/wikijs.env`

## Wiki.js Structure

### Recommended Organization

```
/hyper-hive-labs/                  # Base path
├── projects/                      # Project-specific
│   ├── your-project/
│   │   ├── lessons-learned/
│   │   │   ├── sprints/
│   │   │   ├── patterns/
│   │   │   └── INDEX.md
│   │   └── documentation/
│   ├── another-project/
│   └── shared-library/
├── company/                       # Company-wide
│   ├── processes/
│   ├── standards/
│   └── tools/
└── shared/                        # Cross-project
    ├── architecture-patterns/
    ├── best-practices/
    └── tech-stack/
```

### Lessons Learned Categories

- **sprints/**: Sprint-specific lessons and retrospectives
- **patterns/**: Recurring patterns and solutions
- **architecture/**: Architectural decisions and outcomes
- **tools/**: Tool-specific tips and gotchas

## Testing

See [TESTING.md](./TESTING.md) for comprehensive testing instructions.

**Quick Test:**
```bash
source .venv/bin/activate
pytest -v
```

**Test Coverage:**
- 18 tests covering all major functionality
- Mock-based unit tests (fast)
- Integration tests with real Wiki.js instance
- Configuration validation
- Mode detection
- Error handling

## Lessons Learned System

### Why This Matters

After 15 sprints without systematic lesson capture, repeated mistakes occurred:
- Claude Code infinite loops on similar issues: 2-3 times
- Same architectural mistakes: Multiple occurrences
- Forgotten optimizations: Re-discovered each time

**Solution:** Mandatory lessons learned capture at sprint close, searchable at sprint start.

### Workflow

**Sprint Close (Orchestrator):**
1. Capture what went wrong
2. Document what went right
3. Note preventable repetitions
4. Tag for discoverability

**Sprint Start (Planner):**
1. Search relevant lessons by tags/keywords
2. Review applicable patterns
3. Apply preventive measures
4. Avoid known pitfalls

### Lesson Structure

```markdown
# Sprint X - [Lesson Title]

## Context
[What were you trying to do?]

## Problem
[What went wrong or what insight emerged?]

## Solution
[How did you solve it?]

## Prevention
[How can this be avoided or optimized in the future?]

## Tags
[Comma-separated tags for search]
```

## Troubleshooting

### Connection Errors

**Error:** `Failed to connect to Wiki.js GraphQL endpoint`

**Solutions:**
- Verify `WIKIJS_API_URL` is correct and includes `/graphql`
- Check Wiki.js is running and accessible
- Ensure GraphQL API is enabled in Wiki.js admin settings

### Authentication Errors

**Error:** `Unauthorized` or `Invalid token`

**Solutions:**
- Verify API token is correct and not expired
- Check token has required permissions (Pages: read/write, Search: read)
- Regenerate token in Wiki.js admin if needed

### Permission Errors

**Error:** `Page creation failed: Permission denied`

**Solutions:**
- Verify API key has write permissions
- Check user/group permissions in Wiki.js
- Ensure base path exists and is accessible

### Mode Detection Issues

**Error:** Operating in wrong mode

**Solutions:**
- Check `WIKIJS_PROJECT` environment variable
- Clear project `.env` for company mode
- Verify configuration loading order (project overrides system)

## Security Considerations

1. **Never commit tokens**: Keep `~/.config/claude/wikijs.env` and `.env` out of git
2. **Token scope**: Use minimum required permissions (Pages + Search)
3. **Token rotation**: Regenerate tokens periodically
4. **Access control**: Use Wiki.js groups/permissions for sensitive docs
5. **Audit logs**: Review Wiki.js audit logs for unexpected operations

## Performance

- **GraphQL queries**: Optimized for minimal data transfer
- **Search**: Indexed by Wiki.js for fast results
- **Pagination**: Configurable result limits (default: 20)
- **Caching**: Wiki.js handles internal caching

## Development

### Running Tests

```bash
# All tests
pytest -v

# Specific test file
pytest tests/test_config.py -v

# Integration tests only
pytest tests/test_wikijs_client.py -v -k integration
```

### Code Structure

- `config.py`: Configuration loading and validation
- `wikijs_client.py`: GraphQL client implementation
- `server.py`: MCP server setup and tool routing
- `tools/pages.py`: Page management MCP tools
- `tools/lessons_learned.py`: Lessons learned MCP tools

## License

MIT License - See repository root for details

## Support

For issues and questions:
- **Repository**: `ssh://git@hotserv.tailc9b278.ts.net:2222/bandit/support-claude-mktplace.git`
- **Issues**: Contact repository maintainer
- **Documentation**: `/docs/references/MCP-WIKIJS.md`
