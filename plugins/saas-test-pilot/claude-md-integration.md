# Test Pilot Integration

Add to your project's CLAUDE.md:

## Test Automation

This project uses saas-test-pilot for test generation and coverage analysis.

### Commands
- `/test setup` - Detect framework and configure test environment
- `/test generate <target>` - Generate tests for a function, class, or module
- `/test coverage` - Analyze coverage gaps prioritized by risk
- `/test fixtures generate <model>` - Create fixtures and factories
- `/test e2e <feature>` - Generate E2E test scenarios
- `/test run` - Execute tests with formatted output

### Supported Frameworks
- Python: pytest, unittest
- JavaScript/TypeScript: Jest, Vitest
- E2E: Playwright, Cypress

### Test Organization
Tests follow the standard structure:
```
tests/
  conftest.py          # Shared fixtures
  unit/                # Unit tests (fast, isolated)
  integration/         # Integration tests (database, APIs)
  e2e/                 # End-to-end tests (browser, full stack)
  fixtures/            # Shared test data and response mocks
```

### Coverage Targets
- coverage-analyst provides risk-based gap analysis
- Focus on branch coverage, not just line coverage
- Critical modules (auth, payments) require higher thresholds
