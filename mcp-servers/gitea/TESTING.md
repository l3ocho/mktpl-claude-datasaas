# Gitea MCP Server - Testing Guide

This document provides comprehensive testing instructions for the Gitea MCP Server implementation.

## Table of Contents

1. [Unit Tests](#unit-tests)
2. [Manual MCP Server Testing](#manual-mcp-server-testing)
3. [Integration Testing](#integration-testing)
4. [Configuration Setup for Testing](#configuration-setup-for-testing)
5. [Troubleshooting](#troubleshooting)

---

## Unit Tests

Unit tests use mocks to test all modules without requiring a real Gitea instance.

### Prerequisites

Ensure the virtual environment is activated and dependencies are installed:

```bash
cd mcp-servers/gitea
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
```

### Running All Tests

Run all 42 unit tests:

```bash
pytest tests/ -v
```

Expected output:
```
============================== 42 passed in 0.57s ==============================
```

### Running Specific Test Files

Run tests for a specific module:

```bash
# Configuration tests
pytest tests/test_config.py -v

# Gitea client tests
pytest tests/test_gitea_client.py -v

# Issue tools tests
pytest tests/test_issues.py -v

# Label tools tests
pytest tests/test_labels.py -v
```

### Running Specific Tests

Run a single test:

```bash
pytest tests/test_config.py::test_load_system_config -v
```

### Test Coverage

Generate coverage report:

```bash
pytest --cov=mcp_server --cov-report=html tests/

# View coverage report
# Open htmlcov/index.html in your browser
```

Expected coverage: >80% for all modules

### Test Organization

**Configuration Tests** (`test_config.py`):
- System-level configuration loading
- Project-level configuration override
- Mode detection (project vs company)
- Missing configuration handling

**Gitea Client Tests** (`test_gitea_client.py`):
- API client initialization
- Issue CRUD operations
- Label retrieval
- PMO multi-repo operations

**Issue Tools Tests** (`test_issues.py`):
- Branch-aware security checks
- Async wrappers for sync client
- Permission enforcement
- PMO aggregation mode

**Label Tools Tests** (`test_labels.py`):
- Label retrieval (org + repo)
- Intelligent label suggestion
- Multi-category detection

---

## Manual MCP Server Testing

Test the MCP server manually using stdio communication.

### Step 1: Start the MCP Server

```bash
cd mcp-servers/gitea
source .venv/bin/activate
python -m mcp_server.server
```

The server will start and wait for JSON-RPC 2.0 messages on stdin.

### Step 2: Test Tool Listing

In another terminal, send a tool listing request:

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | python -m mcp_server.server
```

Expected response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {"name": "list_issues", "description": "List issues from Gitea repository", ...},
      {"name": "get_issue", "description": "Get specific issue details", ...},
      {"name": "create_issue", "description": "Create a new issue in Gitea", ...},
      ...
    ]
  }
}
```

### Step 3: Test Tool Invocation

**Note:** Manual tool invocation requires proper configuration. See [Configuration Setup](#configuration-setup-for-testing).

Example: List issues
```bash
echo '{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "list_issues",
    "arguments": {
      "state": "open"
    }
  }
}' | python -m mcp_server.server
```

---

## Integration Testing

Test the MCP server with a real Gitea instance.

### Prerequisites

1. **Gitea Instance**: Access to https://gitea.hotserv.cloud (or your Gitea instance)
2. **API Token**: Personal access token with required permissions
3. **Configuration**: Properly configured system and project configs

### Step 1: Configuration Setup

Create system-level configuration:

```bash
mkdir -p ~/.config/claude

cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.hotserv.cloud/api/v1
GITEA_API_TOKEN=your_gitea_token_here
GITEA_OWNER=hyperhivelabs
EOF

chmod 600 ~/.config/claude/gitea.env
```

Create project-level configuration (for project mode testing):

```bash
cd /path/to/test/project

cat > .env << EOF
GITEA_REPO=test-repo
EOF

# Add to .gitignore
echo ".env" >> .gitignore
```

### Step 2: Generate Gitea API Token

1. Log into Gitea: https://gitea.hotserv.cloud
2. Navigate to: **Settings** → **Applications** → **Manage Access Tokens**
3. Click **Generate New Token**
4. Token configuration:
   - **Token Name:** `mcp-integration-test`
   - **Required Permissions:**
     - ✅ `repo` (all) - Read/write access to repositories, issues, labels
     - ✅ `read:org` - Read organization information and labels
     - ✅ `read:user` - Read user information
5. Click **Generate Token**
6. Copy the token immediately (shown only once)
7. Add to `~/.config/claude/gitea.env`

### Step 3: Verify Configuration

Test configuration loading:

```bash
cd mcp-servers/gitea
source .venv/bin/activate
python -c "
from mcp_server.config import GiteaConfig
config = GiteaConfig()
result = config.load()
print(f'API URL: {result[\"api_url\"]}')
print(f'Owner: {result[\"owner\"]}')
print(f'Repo: {result[\"repo\"]}')
print(f'Mode: {result[\"mode\"]}')
"
```

Expected output:
```
API URL: https://gitea.hotserv.cloud/api/v1
Owner: hyperhivelabs
Repo: test-repo (or None for company mode)
Mode: project (or company)
```

### Step 4: Test Gitea Client

Test basic Gitea API operations:

```bash
python -c "
from mcp_server.gitea_client import GiteaClient

client = GiteaClient()

# Test listing issues
print('Testing list_issues...')
issues = client.list_issues(state='open')
print(f'Found {len(issues)} open issues')

# Test getting labels
print('\\nTesting get_labels...')
labels = client.get_labels()
print(f'Found {len(labels)} repository labels')

# Test getting org labels
print('\\nTesting get_org_labels...')
org_labels = client.get_org_labels()
print(f'Found {len(org_labels)} organization labels')

print('\\n✅ All integration tests passed!')
"
```

### Step 5: Test Issue Creation (Optional)

**Warning:** This creates a real issue in Gitea. Use a test repository.

```bash
python -c "
from mcp_server.gitea_client import GiteaClient

client = GiteaClient()

# Create test issue
print('Creating test issue...')
issue = client.create_issue(
    title='[TEST] MCP Server Integration Test',
    body='This is a test issue created by the Gitea MCP Server integration tests.',
    labels=['Type/Test']
)
print(f'Created issue #{issue[\"number\"]}: {issue[\"title\"]}')

# Clean up: Close the issue
print('\\nClosing test issue...')
client.update_issue(issue['number'], state='closed')
print('✅ Test issue closed')
"
```

### Step 6: Test MCP Server with Real API

Start the MCP server and test with real Gitea API:

```bash
cd mcp-servers/gitea
source .venv/bin/activate

# Run server with test script
python << 'EOF'
import asyncio
import json
from mcp_server.server import GiteaMCPServer

async def test_server():
    server = GiteaMCPServer()
    await server.initialize()

    # Test list_issues
    result = await server.issue_tools.list_issues(state='open')
    print(f'Found {len(result)} open issues')

    # Test get_labels
    labels = await server.label_tools.get_labels()
    print(f'Found {labels["total_count"]} total labels')

    # Test suggest_labels
    suggestions = await server.label_tools.suggest_labels(
        "Fix critical bug in authentication"
    )
    print(f'Suggested labels: {", ".join(suggestions)}')

    print('✅ All MCP server integration tests passed!')

asyncio.run(test_server())
EOF
```

### Step 7: Test PMO Mode (Optional)

Test company-wide mode (no GITEA_REPO):

```bash
# Temporarily remove GITEA_REPO
unset GITEA_REPO

python -c "
from mcp_server.gitea_client import GiteaClient

client = GiteaClient()

print(f'Running in {client.mode} mode')

# Test list_repos
print('\\nTesting list_repos...')
repos = client.list_repos()
print(f'Found {len(repos)} repositories')

# Test aggregate_issues
print('\\nTesting aggregate_issues...')
aggregated = client.aggregate_issues(state='open')
for repo_name, issues in aggregated.items():
    print(f'  {repo_name}: {len(issues)} open issues')

print('\\n✅ PMO mode tests passed!')
"
```

---

## Configuration Setup for Testing

### Minimal Configuration

**System-level** (`~/.config/claude/gitea.env`):
```bash
GITEA_API_URL=https://gitea.hotserv.cloud/api/v1
GITEA_API_TOKEN=your_token_here
GITEA_OWNER=hyperhivelabs
```

**Project-level** (`.env` in project root):
```bash
# For project mode
GITEA_REPO=test-repo

# For company mode (PMO), omit GITEA_REPO
```

### Verification

Verify configuration is correct:

```bash
# Check system config exists
ls -la ~/.config/claude/gitea.env

# Check permissions (should be 600)
stat -c "%a %n" ~/.config/claude/gitea.env

# Check content (without exposing token)
grep -v TOKEN ~/.config/claude/gitea.env

# Check project config (if using project mode)
cat .env
```

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'mcp_server'
```

**Solution:**
```bash
# Ensure you're in the correct directory
cd mcp-servers/gitea

# Activate virtual environment
source .venv/bin/activate

# Verify installation
pip list | grep mcp
```

#### 2. Configuration Not Found

**Error:**
```
FileNotFoundError: System config not found: /home/user/.config/claude/gitea.env
```

**Solution:**
```bash
# Create system config
mkdir -p ~/.config/claude
cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.hotserv.cloud/api/v1
GITEA_API_TOKEN=your_token_here
GITEA_OWNER=hyperhivelabs
EOF

chmod 600 ~/.config/claude/gitea.env
```

#### 3. Missing Required Configuration

**Error:**
```
ValueError: Missing required configuration: GITEA_API_TOKEN, GITEA_OWNER
```

**Solution:**
```bash
# Check configuration file
cat ~/.config/claude/gitea.env

# Ensure all required variables are present:
# - GITEA_API_URL
# - GITEA_API_TOKEN
# - GITEA_OWNER
```

#### 4. API Authentication Failed

**Error:**
```
requests.exceptions.HTTPError: 401 Client Error: Unauthorized
```

**Solution:**
```bash
# Test token manually
curl -H "Authorization: token YOUR_TOKEN" \
  https://gitea.hotserv.cloud/api/v1/user

# If fails, regenerate token in Gitea settings
```

#### 5. Permission Errors (Branch Detection)

**Error:**
```
PermissionError: Cannot create issues on branch 'main'
```

**Solution:**
```bash
# Check current branch
git branch --show-current

# Switch to development branch
git checkout development
# or
git checkout -b feat/test-feature
```

#### 6. Repository Not Specified

**Error:**
```
ValueError: Repository not specified
```

**Solution:**
```bash
# Add GITEA_REPO to project config
echo "GITEA_REPO=your-repo-name" >> .env

# Or specify repo in tool call
# (for PMO mode multi-repo operations)
```

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python -m mcp_server.server
```

### Test Summary

After completing all tests, verify:

- ✅ All 42 unit tests pass
- ✅ MCP server starts without errors
- ✅ Configuration loads correctly
- ✅ Gitea API client connects successfully
- ✅ Issues can be listed from Gitea
- ✅ Labels can be retrieved
- ✅ Label suggestions work correctly
- ✅ Branch detection blocks writes on main/staging
- ✅ Mode detection works (project vs company)

---

## Success Criteria

Phase 1 is complete when:

1. **All unit tests pass** (42/42)
2. **MCP server starts without errors**
3. **Can list issues from Gitea**
4. **Can create issues with labels** (in development mode)
5. **Mode detection works** (project vs company)
6. **Branch detection prevents writes on main/staging**
7. **Configuration properly merges** system + project levels

---

## Next Steps

After completing testing:

1. **Document any issues** found during testing
2. **Create integration with projman plugin** (Phase 2)
3. **Test in real project workflow** (Phase 5)
4. **Performance optimization** (if needed)
5. **Production hardening** (Phase 8)

---

## Additional Resources

- **MCP Documentation**: https://docs.anthropic.com/claude/docs/mcp
- **Gitea API Documentation**: https://docs.gitea.io/en-us/api-usage/
- **Project Documentation**: `docs/references/MCP-GITEA.md`
- **Implementation Plan**: `docs/references/PROJECT-SUMMARY.md`

---

**Last Updated**: 2025-01-06 (Phase 1 Implementation)
