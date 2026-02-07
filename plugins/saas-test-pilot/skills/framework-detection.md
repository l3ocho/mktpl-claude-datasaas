---
description: Detect test frameworks, locate config files, and identify test runner
---

# Framework Detection Skill

## Overview

Detect the test framework and runner used by the current project based on configuration files, dependencies, and directory structure.

## Detection Matrix

### Python

| Indicator | Framework | Confidence |
|-----------|-----------|------------|
| `pytest.ini` | pytest | HIGH |
| `pyproject.toml` with `[tool.pytest]` | pytest | HIGH |
| `setup.cfg` with `[tool:pytest]` | pytest | HIGH |
| `conftest.py` in project root or tests/ | pytest | HIGH |
| `tests/test_*.py` with `import unittest` | unittest | MEDIUM |
| `tox.ini` with pytest commands | pytest | MEDIUM |

### JavaScript / TypeScript

| Indicator | Framework | Confidence |
|-----------|-----------|------------|
| `jest.config.js` or `jest.config.ts` | Jest | HIGH |
| `package.json` with `"jest"` config | Jest | HIGH |
| `vitest.config.ts` or `vitest.config.js` | Vitest | HIGH |
| `.mocharc.yml` or `.mocharc.json` | Mocha | HIGH |
| `karma.conf.js` | Karma | MEDIUM |

### E2E Frameworks

| Indicator | Framework | Confidence |
|-----------|-----------|------------|
| `playwright.config.ts` | Playwright | HIGH |
| `cypress.config.js` or `cypress.config.ts` | Cypress | HIGH |
| `cypress/` directory | Cypress | MEDIUM |

## Config File Locations

Search order for each framework:
1. Project root
2. `tests/` or `test/` directory
3. Inside `pyproject.toml`, `package.json`, or `setup.cfg` (inline config)

## Output

When detection completes, report:
- Detected framework name and version (from lock file or dependency list)
- Config file path
- Test directory path
- Coverage tool if configured (pytest-cov, istanbul, c8)
- CI integration if found (.github/workflows, .gitlab-ci.yml, Jenkinsfile)
