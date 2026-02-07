---
description: Mocking, stubbing, and dependency injection strategies for tests
---

# Mock Patterns Skill

## Overview

Mocking strategies and best practices for isolating code under test from external dependencies.

## When to Mock

| Situation | Mock? | Reason |
|-----------|-------|--------|
| External API calls | Yes | Unreliable, slow, costs money |
| Database queries | Depends | Mock for unit, real for integration |
| File system | Depends | Mock for unit, tmpdir for integration |
| Time/date functions | Yes | Deterministic tests |
| Random/UUID generation | Yes | Reproducible tests |
| Pure utility functions | No | Fast, deterministic, no side effects |
| Internal business logic | No | Test the real thing |

## Python Mocking

### unittest.mock / pytest-mock

```
patch("module.path.to.dependency")     # Replaces at import location
patch.object(MyClass, "method")        # Replaces on specific class
MagicMock(return_value=expected)       # Creates callable mock
MagicMock(side_effect=Exception("e"))  # Raises on call
```

**Critical rule:** Patch where the dependency is USED, not where it is DEFINED.
- If `views.py` imports `from services import send_email`, patch `views.send_email`, NOT `services.send_email`.

### pytest-mock (preferred)

Use the `mocker` fixture for cleaner syntax:
- `mocker.patch("module.function")` — auto-cleanup after test
- `mocker.spy(obj, "method")` — record calls without replacing

## JavaScript Mocking

### Jest

```
jest.mock("./module")              // Auto-mock entire module
jest.spyOn(object, "method")       // Spy without replacing
jest.fn().mockReturnValue(value)   // Create mock function
```

### Vitest

```
vi.mock("./module")                // Same API as Jest
vi.spyOn(object, "method")
vi.fn().mockReturnValue(value)
```

## Mock vs Stub vs Spy

| Type | Behavior | Use When |
|------|----------|----------|
| **Mock** | Replace entirely, return fake data | Isolating from external service |
| **Stub** | Provide canned responses | Controlling specific return values |
| **Spy** | Record calls, keep real behavior | Verifying interactions without changing behavior |

## Dependency Injection Patterns

Prefer DI over mocking when possible:
- Constructor injection: pass dependencies as constructor args
- Function parameters: accept collaborators as arguments with defaults
- Context managers: swap implementations via context

DI makes tests simpler and avoids brittle mock paths.

## Anti-Patterns

- Mocking too deep (mock chains: `mock.return_value.method.return_value`)
- Asserting on mock call counts instead of outcomes
- Mocking the system under test
- Not resetting mocks between tests (use autouse fixtures or afterEach)
