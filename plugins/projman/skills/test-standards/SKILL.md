---
name: test-standards
description: Testing requirements, framework detection, and patterns
---

# Test Standards

## Purpose

Defines testing requirements, framework detection, and test patterns.

## When to Use

- **Commands**: `/test-check`, `/test-gen`
- **Executor agent**: When writing tests during implementation

---

## Framework Detection

| Indicator | Framework | Command |
|-----------|-----------|---------|
| `pytest.ini`, `pyproject.toml` with pytest | pytest | `pytest` |
| `package.json` with jest | Jest | `npm test` or `npx jest` |
| `package.json` with vitest | Vitest | `npm test` or `npx vitest` |
| `go.mod` with `*_test.go` | Go test | `go test ./...` |
| `Cargo.toml` | Cargo test | `cargo test` |
| `Makefile` with test target | Make | `make test` |

---

## Coverage Commands

| Framework | Coverage Command |
|-----------|------------------|
| Python/pytest | `pytest --cov=src --cov-report=term-missing` |
| JavaScript/Jest | `npm test -- --coverage` |
| Go | `go test -cover ./...` |
| Rust | `cargo tarpaulin` or `cargo llvm-cov` |

---

## Test Structure Pattern

### Unit Tests

For each function:
- **Happy path**: Expected inputs → expected output
- **Edge cases**: Empty, null, boundary values
- **Error cases**: Invalid inputs → expected errors
- **Type variations**: If dynamic typing

### Example (Python/pytest)

```python
import pytest
from module import target_function

class TestTargetFunction:
    """Tests for target_function."""

    def test_happy_path(self):
        """Standard input produces expected output."""
        result = target_function(valid_input)
        assert result == expected_output

    def test_empty_input(self):
        """Empty input handled gracefully."""
        result = target_function("")
        assert result == default_value

    def test_invalid_input_raises(self):
        """Invalid input raises ValueError."""
        with pytest.raises(ValueError):
            target_function(invalid_input)

    @pytest.mark.parametrize("input,expected", [
        (case1_in, case1_out),
        (case2_in, case2_out),
    ])
    def test_variations(self, input, expected):
        """Multiple input variations."""
        assert target_function(input) == expected
```

---

## Test Strategy by Code Pattern

| Code Pattern | Test Approach |
|--------------|---------------|
| Pure function | Unit tests with varied inputs |
| Class with state | Setup/teardown, state transitions |
| External calls | Mocks/stubs for dependencies |
| Database ops | Integration tests with fixtures |
| API endpoints | Request/response tests |
| UI components | Snapshot + interaction tests |

---

## Test Check Output Format

```
## Test Check Summary

### Test Results
- Framework: pytest
- Status: PASS/FAIL
- Passed: 45 | Failed: 2 | Skipped: 3
- Duration: 12.5s

### Failed Tests
- test_auth.py::test_token_refresh: AssertionError (line 45)
- test_api.py::test_login_endpoint: TimeoutError (line 78)

### Coverage (if available)
- Overall: 78%
- Sprint files coverage:
  - auth/jwt_service.py: 92%
  - api/routes/auth.py: 65%
  - models/user.py: NO TESTS

### Recommendation
TESTS MUST PASS / READY FOR CLOSE / COVERAGE GAPS TO ADDRESS
```

---

## Test Generation Output Format

```
## Tests Generated

### Target: src/orders.py:calculate_total

### File Created: tests/test_orders.py

### Tests (6 total)
- test_calculate_total_happy_path
- test_calculate_total_empty_items
- test_calculate_total_negative_price_raises
- test_calculate_total_with_discount
- test_calculate_total_with_tax
- test_calculate_total_parametrized_cases

### Run Tests
pytest tests/test_orders.py -v
```

---

## Do NOT

- Modify test files during `/test-check` (only run and report)
- Skip failing tests to make the run pass
- Run tests in production environments
- Install dependencies without asking first
- Run tests requiring external services without confirmation

---

## Error Handling

**If tests fail:**
1. Report the failure clearly
2. List failed test names and error summaries
3. Recommend: "TESTS MUST PASS before sprint close"
4. Offer to help debug specific failures

**If framework not detected:**
1. List what was checked
2. Ask user to specify the test command
3. Offer common suggestions based on file types
