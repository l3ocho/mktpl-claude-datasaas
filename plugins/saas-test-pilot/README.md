# saas-test-pilot

Test automation toolkit for unit, integration, and end-to-end testing.

## Overview

saas-test-pilot provides intelligent test generation, coverage analysis, fixture management, and E2E scenario creation. It detects your project's test framework automatically and generates tests following best practices for pytest, Jest, Vitest, Playwright, and Cypress.

## Commands

| Command | Description |
|---------|-------------|
| `/test setup` | Detect framework, configure test runner, initialize test structure |
| `/test generate` | Generate test cases for functions, classes, or modules |
| `/test coverage` | Analyze coverage and identify untested paths by risk |
| `/test fixtures` | Generate or manage test fixtures, factories, and mocks |
| `/test e2e` | Generate end-to-end test scenarios with page objects |
| `/test run` | Run tests with formatted output and failure analysis |

## Agents

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| test-architect | sonnet | acceptEdits | Test generation, fixtures, E2E design |
| coverage-analyst | haiku | plan (read-only) | Coverage analysis and gap detection |

## Skills

| Skill | Purpose |
|-------|---------|
| framework-detection | Auto-detect pytest/Jest/Vitest/Playwright and config files |
| test-patterns | AAA, BDD, page object model, and other test design patterns |
| mock-patterns | Mocking strategies: mock vs stub vs spy, DI patterns |
| coverage-analysis | Gap detection, risk scoring, prioritization |
| fixture-management | conftest.py patterns, factory_boy, shared fixtures |
| visual-header | Consistent command output headers |

## Supported Frameworks

### Unit / Integration
- **Python:** pytest, unittest
- **JavaScript/TypeScript:** Jest, Vitest, Mocha

### End-to-End
- **Playwright** (recommended)
- **Cypress**

### Coverage
- **Python:** pytest-cov (coverage.py)
- **JavaScript:** istanbul/nyc, c8, vitest built-in

## Installation

This plugin is part of the Leo Claude Marketplace. It is installed automatically when the marketplace is configured.

## License

MIT
