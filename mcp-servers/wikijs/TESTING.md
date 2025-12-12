# Testing Guide - Wiki.js MCP Server

This document provides comprehensive testing instructions for the Wiki.js MCP Server.

## Test Suite Overview

The test suite includes:
- **18 unit tests** with mocks (fast, no external dependencies)
- **Integration tests** with real Wiki.js instance (requires live Wiki.js)
- **Configuration validation** tests
- **Mode detection** tests
- **GraphQL client** tests
- **Error handling** tests

## Prerequisites

### For Unit Tests (Mocked)
- Python 3.10+
- Virtual environment with dependencies installed
- No external services required

### For Integration Tests
- Everything from unit tests, plus:
- Running Wiki.js instance
- Valid API token with permissions
- System configuration file (`~/.config/claude/wikijs.env`)

## Quick Start

### Run All Unit Tests

```bash
cd mcp-servers/wikijs
source .venv/bin/activate
pytest -v
```

**Expected Output:**
```
==================== test session starts ====================
tests/test_config.py::test_load_system_config PASSED   [  5%]
tests/test_config.py::test_project_config_override PASSED [ 11%]
...
==================== 18 passed in 0.40s ====================
```

### Run Integration Tests

```bash
# Set up system configuration first
mkdir -p ~/.config/claude
cat > ~/.config/claude/wikijs.env << 'EOF'
WIKIJS_API_URL=http://wikijs.hotport/graphql
WIKIJS_API_TOKEN=your_real_token_here
WIKIJS_BASE_PATH=/your-org
EOF

# Run integration tests
pytest -v -m integration
```

## Test Categories

### 1. Configuration Tests (`test_config.py`)

Tests the hybrid configuration system and mode detection.

**Tests:**
- `test_load_system_config`: System-level config loading
- `test_project_config_override`: Project overrides system
- `test_missing_system_config`: Error when config missing
- `test_missing_required_config`: Validation of required vars
- `test_mode_detection_project`: Project mode detection
- `test_mode_detection_company`: Company mode detection

**Run:**
```bash
pytest tests/test_config.py -v
```

### 2. Wiki.js Client Tests (`test_wikijs_client.py`)

Tests the GraphQL client and all Wiki.js operations.

**Tests:**
- `test_client_initialization`: Client setup
- `test_company_mode_initialization`: Company mode setup
- `test_get_full_path_project_mode`: Path construction (project)
- `test_get_full_path_company_mode`: Path construction (company)
- `test_search_pages`: Page search
- `test_get_page`: Single page retrieval
- `test_create_page`: Page creation
- `test_update_page`: Page updates
- `test_list_pages`: List pages with filtering
- `test_create_lesson`: Lessons learned creation
- `test_search_lessons`: Lesson search
- `test_graphql_error_handling`: Error handling

**Run:**
```bash
pytest tests/test_wikijs_client.py -v
```

## Integration Testing

### Setup Integration Environment

**Step 1: Configure Wiki.js**

Create a test namespace in Wiki.js:
```
/test-integration/
├── projects/
│   └── test-project/
│       ├── documentation/
│       └── lessons-learned/
└── shared/
```

**Step 2: Configure System**

```bash
cat > ~/.config/claude/wikijs.env << 'EOF'
WIKIJS_API_URL=http://wikijs.hotport/graphql
WIKIJS_API_TOKEN=your_token_here
WIKIJS_BASE_PATH=/test-integration
EOF
```

**Step 3: Configure Project**

```bash
# In test directory
cat > .env << 'EOF'
WIKIJS_PROJECT=projects/test-project
EOF
```

### Run Integration Tests

```bash
# Mark tests for integration
pytest -v -m integration

# Run specific integration test
pytest tests/test_wikijs_client.py::test_create_page -v -m integration
```

### Integration Test Scenarios

**Scenario 1: Page Lifecycle**
1. Create page with `create_page`
2. Retrieve with `get_page`
3. Update with `update_page`
4. Search for page with `search_pages`
5. Cleanup (manual via Wiki.js UI)

**Scenario 2: Lessons Learned Workflow**
1. Create lesson with `create_lesson`
2. Search lessons with `search_lessons`
3. Add tags with `tag_lesson`
4. Verify searchability

**Scenario 3: Mode Detection**
1. Test in project mode (with `WIKIJS_PROJECT`)
2. Test in company mode (without `WIKIJS_PROJECT`)
3. Verify path scoping

## Manual Testing

### Test 1: Create and Retrieve Page

```bash
# Start MCP server
python -m mcp_server.server

# In another terminal, send MCP request
echo '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "create_page",
    "arguments": {
      "path": "documentation/test-api",
      "title": "Test API Documentation",
      "content": "# Test API\\n\\nThis is a test page.",
      "tags": "api,testing",
      "publish": true
    }
  }
}' | python -m mcp_server.server
```

**Expected Result:**
```json
{
  "success": true,
  "page": {
    "id": 123,
    "path": "/your-org/projects/test-project/documentation/test-api",
    "title": "Test API Documentation"
  }
}
```

### Test 2: Search Lessons

```bash
echo '{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "search_lessons",
    "arguments": {
      "query": "validation",
      "tags": "testing,claude-code",
      "limit": 10
    }
  }
}' | python -m mcp_server.server
```

**Expected Result:**
```json
{
  "success": true,
  "count": 2,
  "lessons": [...]
}
```

### Test 3: Mode Detection

**Project Mode:**
```bash
# Create .env with WIKIJS_PROJECT
echo "WIKIJS_PROJECT=projects/test-project" > .env

# Start server and check logs
python -m mcp_server.server 2>&1 | grep "mode"
```

**Expected Log:**
```
INFO:Running in project mode: projects/test-project
```

**Company Mode:**
```bash
# Remove .env
rm .env

# Start server and check logs
python -m mcp_server.server 2>&1 | grep "mode"
```

**Expected Log:**
```
INFO:Running in company-wide mode (PMO)
```

## Test Data Management

### Cleanup Test Data

After integration tests, clean up test pages in Wiki.js:

```bash
# Via Wiki.js UI
1. Navigate to /test-integration/
2. Select test pages
3. Delete

# Or via GraphQL (advanced)
curl -X POST http://wikijs.hotport/graphql \
  -H "Authorization: Bearer $WIKIJS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { pages { delete(id: 123) { responseResult { succeeded } } } }"
  }'
```

### Test Data Fixtures

For repeatable testing, create fixtures:

```python
# tests/conftest.py
import pytest

@pytest.fixture
async def test_page():
    """Create a test page and clean up after"""
    client = WikiJSClient(...)
    page = await client.create_page(
        path="test/fixture-page",
        title="Test Fixture",
        content="# Test"
    )
    yield page
    # Cleanup after test
    await client.delete_page(page['id'])
```

## Continuous Integration

### GitHub Actions / Gitea Actions

```yaml
name: Test Wiki.js MCP Server

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        working-directory: mcp-servers/wikijs
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt

      - name: Run unit tests
        working-directory: mcp-servers/wikijs
        run: |
          source .venv/bin/activate
          pytest -v

      # Integration tests (optional, requires Wiki.js instance)
      - name: Run integration tests
        if: env.WIKIJS_API_TOKEN != ''
        working-directory: mcp-servers/wikijs
        env:
          WIKIJS_API_URL: ${{ secrets.WIKIJS_API_URL }}
          WIKIJS_API_TOKEN: ${{ secrets.WIKIJS_API_TOKEN }}
          WIKIJS_BASE_PATH: /test-integration
        run: |
          source .venv/bin/activate
          pytest -v -m integration
```

## Debugging Tests

### Enable Verbose Logging

```bash
# Set log level to DEBUG
export PYTHONLOG=DEBUG
pytest -v -s
```

### Run Single Test with Debugging

```bash
# Run specific test with print statements visible
pytest tests/test_config.py::test_load_system_config -v -s

# Use pytest debugger
pytest tests/test_config.py::test_load_system_config --pdb
```

### Inspect GraphQL Queries

Add logging to see actual GraphQL queries:

```python
# In wikijs_client.py
async def _execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None):
    logger.info(f"GraphQL Query: {query}")
    logger.info(f"Variables: {variables}")
    # ... rest of method
```

## Test Coverage

### Generate Coverage Report

```bash
pip install pytest-cov

# Run with coverage
pytest --cov=mcp_server --cov-report=html

# Open report
open htmlcov/index.html
```

**Target Coverage:** 90%+ for all modules

## Performance Testing

### Benchmark GraphQL Operations

```python
import time

async def benchmark_search():
    client = WikiJSClient(...)
    start = time.time()
    results = await client.search_pages("test")
    elapsed = time.time() - start
    print(f"Search took {elapsed:.3f}s")
```

**Expected Performance:**
- Search: < 500ms
- Get page: < 200ms
- Create page: < 1s
- Update page: < 500ms

## Common Test Failures

### 1. Configuration Not Found

**Error:**
```
FileNotFoundError: System config not found: ~/.config/claude/wikijs.env
```

**Solution:**
```bash
mkdir -p ~/.config/claude
cat > ~/.config/claude/wikijs.env << 'EOF'
WIKIJS_API_URL=http://wikijs.hotport/graphql
WIKIJS_API_TOKEN=test_token
WIKIJS_BASE_PATH=/test
EOF
```

### 2. GraphQL Connection Error

**Error:**
```
httpx.ConnectError: Connection refused
```

**Solution:**
- Verify Wiki.js is running
- Check `WIKIJS_API_URL` is correct
- Ensure `/graphql` endpoint is accessible

### 3. Permission Denied

**Error:**
```
ValueError: Failed to create page: Permission denied
```

**Solution:**
- Regenerate API token with write permissions
- Check Wiki.js user/group permissions
- Verify base path exists and is accessible

### 4. Environment Variable Pollution

**Error:**
```
AssertionError: assert 'project' == 'company'
```

**Solution:**
```python
# In test, clear environment
monkeypatch.delenv('WIKIJS_PROJECT', raising=False)
```

## Best Practices

1. **Isolate Tests**: Each test should be independent
2. **Mock External Calls**: Use mocks for unit tests
3. **Clean Up Resources**: Delete test pages after integration tests
4. **Use Fixtures**: Reuse common setup/teardown
5. **Test Error Cases**: Not just happy paths
6. **Document Assumptions**: Comment what tests expect
7. **Consistent Naming**: Follow `test_<what>_<scenario>` pattern

## Next Steps

After testing passes:
1. Review code coverage report
2. Add integration tests for edge cases
3. Document any new test scenarios
4. Update CI/CD pipeline
5. Create test data fixtures for common scenarios

## Support

For testing issues:
- Check test logs: `pytest -v -s`
- Review Wiki.js logs
- Verify configuration files
- See main README.md troubleshooting section
