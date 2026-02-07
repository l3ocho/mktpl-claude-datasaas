---
name: test generate
description: Generate test cases for functions, classes, or modules with appropriate patterns
---

# /test generate

Generate comprehensive test cases for specified code targets.

## Visual Output

```
+----------------------------------------------------------------------+
|  TEST-PILOT - Generate Tests                                          |
+----------------------------------------------------------------------+
```

## Usage

```
/test generate <target> [--type=unit|integration] [--style=aaa|bdd]
```

**Target:** File path, class name, function name, or module path
**Type:** Test type — defaults to unit
**Style:** Test style — defaults to arrange-act-assert (aaa)

## Skills to Load

- skills/test-patterns.md
- skills/mock-patterns.md
- skills/framework-detection.md

## Process

1. **Analyze Target**
   - Read the target source code
   - Identify public functions, methods, and classes
   - Map input types, return types, and exceptions
   - Detect dependencies that need mocking

2. **Determine Test Strategy**
   - Pure functions: direct input/output tests
   - Functions with side effects: mock external calls
   - Class methods: test through public interface
   - Integration points: setup/teardown with real or fake dependencies

3. **Generate Test Cases**
   - Happy path: standard inputs produce expected outputs
   - Edge cases: empty inputs, None/null, boundary values
   - Error paths: invalid inputs, exceptions, error conditions
   - Type variations: different valid types if applicable

4. **Write Test File**
   - Follow project conventions for test file location
   - Use detected framework syntax (pytest/Jest/Vitest)
   - Include docstrings explaining each test case
   - Group related tests in classes or describe blocks

5. **Verify**
   - Check test file compiles/parses
   - Verify imports are correct
   - Confirm mock targets match actual module paths

## Output Format

```
## Generated Tests for `module.function_name`

### Test File: tests/unit/test_module.py

### Test Cases (7 total)
1. test_function_returns_expected_for_valid_input
2. test_function_handles_empty_input
3. test_function_raises_on_invalid_type
4. test_function_boundary_values
5. test_function_none_input
6. test_function_large_input
7. test_function_concurrent_calls (if applicable)

### Dependencies Mocked
- database.connection (unittest.mock.patch)
- external_api.client (fixture)
```
