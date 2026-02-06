# Design: saas-test-pilot

**Domain:** `saas`
**Target Version:** v9.5.0

## Purpose

Test automation toolkit supporting unit, integration, and end-to-end testing. Generates test cases from code analysis, manages test fixtures, and provides coverage analysis with gap detection.

## Target Users

- Developers writing tests for Python or JavaScript/TypeScript projects
- Teams enforcing test coverage requirements
- Projects needing test generation from existing code

## Commands

| Command | Description |
|---------|-------------|
| `/test setup` | Setup wizard — detect test framework, configure paths |
| `/test generate` | Generate test cases for functions/classes/modules |
| `/test coverage` | Analyze test coverage and identify untested code paths |
| `/test fixtures` | Generate or manage test fixtures and mocks |
| `/test e2e` | Generate end-to-end test scenarios from user stories |
| `/test run` | Run tests with formatted output and failure analysis |

## Agent Architecture

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| `test-architect` | sonnet | acceptEdits | Test generation, fixture creation, e2e scenarios |
| `coverage-analyst` | haiku | plan | Read-only coverage analysis and gap detection |

## Skills

| Skill | Purpose |
|-------|---------|
| `framework-detection` | Detect pytest/Jest/Vitest/Playwright, identify config |
| `test-patterns` | Unit/integration/e2e test patterns and best practices |
| `mock-patterns` | Mocking strategies for different dependency types |
| `coverage-analysis` | Coverage gap detection and prioritization |
| `fixture-management` | Fixture organization, factories, builders |
| `visual-header` | Standard command output headers |

## MCP Server

**Not required.** Test generation is file-based. Test execution uses the project's own test runner via Bash.

## Integration Points

| Plugin | Integration |
|--------|-------------|
| projman | `/sprint test` delegates to test-pilot when installed |
| saas-api-platform | API route tests generated from `/api test-routes` |
| saas-react-platform | Component tests generated alongside components |
| data-seed | Test fixtures use seed data profiles |
| code-sentinel | Security test patterns included in generation |

## Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| `claude-md-integration.md` | ~700 |
| Dispatch file (`test.md`) | ~200 |
| 6 commands (avg) | ~3,600 |
| 2 agents | ~1,200 |
| 6 skills | ~2,500 |
| **Total** | **~8,200** |

## Open Questions

- Should `/test run` replace projman's `/sprint test run` or supplement it?
- Support for property-based testing (Hypothesis, fast-check)?
