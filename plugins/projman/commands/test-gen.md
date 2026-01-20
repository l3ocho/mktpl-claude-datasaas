---
description: Generate tests for specified code - creates unit, integration, or e2e tests
---

# Test Generation

Generate comprehensive tests for specified code.

## Usage
```
/test-gen <target> [--type=<type>] [--framework=<framework>]
```

**Target:** File path, function name, class name, or module
**Type:** unit (default), integration, e2e, snapshot
**Framework:** Auto-detected or specify (pytest, jest, vitest, go test, etc.)

## Process

1. **Analyze Target Code**
   - Parse function/class signatures
   - Identify dependencies and side effects
   - Map input types and return types
   - Find edge cases from logic branches

2. **Determine Test Strategy**

   | Code Pattern | Test Approach |
   |--------------|---------------|
   | Pure function | Unit tests with varied inputs |
   | Class with state | Setup/teardown, state transitions |
   | External calls | Mocks/stubs for dependencies |
   | Database ops | Integration tests with fixtures |
   | API endpoints | Request/response tests |
   | UI components | Snapshot + interaction tests |

3. **Generate Tests**

   For each target function/method:
   - Happy path test (expected inputs → expected output)
   - Edge cases (empty, null, boundary values)
   - Error cases (invalid inputs → expected errors)
   - Type variations (if dynamic typing)

4. **Test Structure**
   ```python
   # Example output for Python/pytest

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

5. **Output**
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

### Coverage Estimate
- Line coverage: ~85%
- Branch coverage: ~70%

### Run Tests
pytest tests/test_orders.py -v
```

## Framework Detection

| Files Present | Framework Used |
|---------------|----------------|
| pytest.ini, conftest.py | pytest |
| jest.config.* | jest |
| vitest.config.* | vitest |
| *_test.go | go test |
| Cargo.toml | cargo test |
| mix.exs | ExUnit |

## Integration with /test-check

- `/test-gen` creates new tests
- `/test-check` verifies tests pass
- Typical flow: `/test-gen src/new_module.py` → `/test-check`
