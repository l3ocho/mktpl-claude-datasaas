---
description: Fixture organization, factories, shared test data, and conftest patterns
---

# Fixture Management Skill

## Overview

Patterns for organizing test fixtures, factories, and shared test data. Well-structured fixtures reduce test maintenance and improve readability.

## Python Fixtures (pytest)

### conftest.py Hierarchy

```
tests/
  conftest.py              # Shared across all tests (db connection, auth)
  unit/
    conftest.py            # Unit-specific fixtures (mocked services)
  integration/
    conftest.py            # Integration-specific (real db, test server)
```

Fixtures in parent conftest.py are available to all child directories. Keep fixtures at the narrowest scope possible.

### Fixture Scopes

| Scope | Lifetime | Use For |
|-------|----------|---------|
| `function` | Each test | Default. Mutable data, unique state |
| `class` | Each test class | Shared setup within a class |
| `module` | Each test file | Expensive setup shared across file |
| `session` | Entire test run | Database connection, compiled assets |

### Factory Pattern (factory_boy)

Use factories for complex model creation:
- Define a factory per model with sensible defaults
- Override only what the specific test needs
- Use `SubFactory` for relationships
- Use `LazyAttribute` for computed fields
- Use `Sequence` for unique values

## JavaScript Fixtures

### Factory Functions

```
function createUser(overrides = {}) {
  return {
    id: generateId(),
    name: "Test User",
    email: "test@example.com",
    ...overrides
  };
}
```

### Shared Test Data

- Place in `__tests__/fixtures/` or `test/fixtures/`
- Export factory functions, not static objects (avoid mutation between tests)
- Use builder pattern for complex objects with many optional fields

## Database Fixtures

### Seeding Strategies

| Strategy | Speed | Isolation | Complexity |
|----------|-------|-----------|------------|
| Transaction rollback | Fast | Good | Medium |
| Truncate + re-seed | Medium | Perfect | Low |
| Separate test database | Fast | Perfect | High |
| In-memory database | Fastest | Perfect | Medium |

### API Response Fixtures

- Store in `tests/fixtures/responses/` as JSON files
- Name by endpoint and scenario: `get_user_200.json`, `get_user_404.json`
- Update fixtures when API contracts change
- Use fixture loading helpers to avoid hardcoded paths

## Anti-Patterns

- Global mutable fixtures shared between tests
- Fixtures that depend on other fixtures in unpredictable order
- Overly specific fixtures that break when models change
- Fixtures with magic values whose meaning is unclear
