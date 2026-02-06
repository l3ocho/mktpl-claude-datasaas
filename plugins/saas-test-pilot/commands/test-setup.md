---
name: test setup
description: Detect test framework, configure test runner, and initialize test structure
---

# /test setup

Setup wizard for test automation. Detects existing frameworks or helps choose one.

## Visual Output

```
+----------------------------------------------------------------------+
|  TEST-PILOT - Setup                                                   |
+----------------------------------------------------------------------+
```

## Skills to Load

- skills/framework-detection.md

## Process

1. **Project Detection**
   - Scan for existing test directories (`tests/`, `test/`, `__tests__/`, `spec/`)
   - Detect language from file extensions and config files
   - Identify existing test framework configuration

2. **Framework Detection**
   - Python: check for pytest.ini, setup.cfg [tool.pytest], pyproject.toml [tool.pytest], conftest.py, unittest patterns
   - JavaScript/TypeScript: check for jest.config.js/ts, vitest.config.ts, .mocharc.yml, karma.conf.js
   - E2E: check for playwright.config.ts, cypress.config.js, selenium configs

3. **Configuration Review**
   - Show detected framework and version
   - Show test directory structure
   - Show coverage configuration if present
   - Show CI/CD test integration if found

4. **Recommendations**
   - If no framework detected: recommend based on language and project type
   - If framework found but no coverage: suggest coverage setup
   - If no test directory structure: propose standard layout
   - If missing conftest/setup files: offer to create them

## Output Format

```
## Test Environment

### Detected Framework
- Language: Python 3.x
- Framework: pytest 8.x
- Config: pyproject.toml [tool.pytest.ini_options]

### Test Structure
tests/
  conftest.py
  unit/
  integration/

### Coverage
- Tool: pytest-cov
- Current: 72% line coverage

### Recommendations
- [ ] Add conftest.py fixtures for database connection
- [ ] Configure pytest-xdist for parallel execution
- [ ] Add coverage threshold to CI pipeline
```
