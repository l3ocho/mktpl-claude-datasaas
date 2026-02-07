---
description: Test design patterns for unit, integration, and e2e tests
---

# Test Patterns Skill

## Overview

Standard test design patterns organized by test type. Use these as templates when generating tests.

## Unit Test Patterns

### Arrange-Act-Assert (AAA)

The default pattern for unit tests:

```
Arrange: Set up test data and dependencies
Act:     Call the function under test
Assert:  Verify the result matches expectations
```

- Keep Arrange minimal — only what this specific test needs
- Act should be a single function call
- Assert one logical concept (multiple assertions allowed if same concept)

### Parameterized Tests

Use when testing the same logic with different inputs:
- pytest: `@pytest.mark.parametrize("input,expected", [...])`
- Jest: `test.each([...])("description %s", (input, expected) => {...})`

Best for: validation functions, parsers, formatters, math operations.

### Exception Testing

Verify error conditions explicitly:
- pytest: `with pytest.raises(ValueError, match="expected message")`
- Jest: `expect(() => fn()).toThrow("expected message")`

Always assert the exception type AND message content.

## Integration Test Patterns

### Setup/Teardown

Use fixtures or beforeEach/afterEach for:
- Database connections and seeded data
- Temporary files and directories
- Mock server instances
- Environment variable overrides

### Transaction Rollback

For database integration tests, wrap each test in a transaction that rolls back:
- Ensures test isolation without slow re-seeding
- pytest: `@pytest.fixture(autouse=True)` with session-scoped DB and function-scoped transaction

## E2E Test Patterns

### Page Object Model

Encapsulate page interactions in reusable classes:
- One class per page or significant component
- Methods return page objects for chaining
- Selectors defined as class properties
- No assertions inside page objects

### User Flow Pattern

Structure E2E tests as user stories:
1. Setup — authenticate, navigate to starting point
2. Action — perform the user's workflow steps
3. Verification — check the final state
4. Cleanup — reset any created data

## Anti-Patterns to Avoid

- Testing implementation details instead of behavior
- Mocking the thing you are testing
- Tests that depend on execution order
- Assertions on exact error messages from third-party libraries
- Sleeping instead of waiting for conditions
