---
name: api test-routes
description: Generate request/response test cases for API endpoints
agent: api-architect
---

# /api test-routes - API Test Generator

## Skills to Load

- skills/route-patterns.md
- skills/visual-header.md

## Visual Output

Display header: `API-PLATFORM - Test Routes`

## Usage

```
/api test-routes [<resource>] [--coverage=basic|full] [--runner=pytest|jest|vitest]
```

**Arguments:**
- `<resource>`: Specific resource to generate tests for (default: all)
- `--coverage`: `basic` generates happy-path only; `full` includes edge cases (default: `full`)
- `--runner`: Test runner to target (auto-detected from project)

## Prerequisites

Run `/api setup` first. Route files must exist (either manually written or via `/api scaffold`).

## Process

### 1. Detect Test Runner

Auto-detect based on framework:
- **FastAPI**: `pytest` with `httpx` (TestClient)
- **Express**: `jest` or `vitest` with `supertest`

Check for existing test config (`pytest.ini`, `jest.config.*`, `vitest.config.*`).

### 2. Scan Endpoints

For each route file, extract:
- HTTP method and path
- Required and optional parameters
- Request body schema with field types and constraints
- Expected response status codes
- Authentication requirements

### 3. Generate Test Cases

For each endpoint, generate test cases in categories:

**Happy Path (basic coverage):**
- Valid request returns expected status code
- Response body matches expected schema
- List endpoints return paginated results
- Create endpoint returns created resource with ID

**Validation (full coverage):**
- Missing required fields returns 422/400
- Invalid field types return 422/400
- String fields exceeding max length return 422/400
- Invalid enum values return 422/400

**Authentication (full coverage):**
- Request without auth token returns 401
- Request with expired token returns 401
- Request with insufficient permissions returns 403

**Edge Cases (full coverage):**
- GET non-existent resource returns 404
- DELETE already-deleted resource returns 404
- PUT with partial body returns 422/400
- Concurrent creation of duplicate resources

**Pagination (full coverage for list endpoints):**
- Default pagination returns correct page size
- Custom page size works correctly
- Out-of-range page returns empty results
- Sort parameters produce correct ordering

### 4. Write Test Files

Create test files in the project test directory:
- One test file per resource
- Test fixtures for common setup (auth tokens, sample data)
- Helper functions for repetitive assertions

## Output Format

```
+----------------------------------------------------------------------+
|  API-PLATFORM - Test Routes                                          |
+----------------------------------------------------------------------+

Coverage: full
Runner: pytest + httpx
Resource: orders

Files Created:
  [+] tests/test_orders.py      (18 test cases)
  [+] tests/conftest.py         (fixtures updated)

Test Cases Generated:
  Happy Path:    6 tests
  Validation:    5 tests
  Auth:          3 tests
  Edge Cases:    4 tests

  Total:         18 test cases for 6 endpoints

Next Steps:
  - Review generated tests and adjust sample data
  - Add database fixtures for integration tests
  - Run: pytest tests/test_orders.py -v
```

## Important Notes

- Generated tests use placeholder sample data; review and adjust for your domain
- Auth tests require a fixture that provides valid/invalid tokens
- Integration tests may need database setup/teardown fixtures
- Tests follow Arrange-Act-Assert pattern
