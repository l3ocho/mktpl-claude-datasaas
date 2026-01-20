---
name: test-check
description: Run tests and verify coverage before sprint close
---

# Test Check for Sprint Close

Verify test status and coverage before closing the sprint.

## Framework Detection

Detect the test framework by checking for:

| Indicator | Framework | Command |
|-----------|-----------|---------|
| `pytest.ini`, `pyproject.toml` with pytest, `tests/` with `test_*.py` | pytest | `pytest` |
| `package.json` with jest | Jest | `npm test` or `npx jest` |
| `package.json` with mocha | Mocha | `npm test` or `npx mocha` |
| `package.json` with vitest | Vitest | `npm test` or `npx vitest` |
| `go.mod` with `*_test.go` files | Go test | `go test ./...` |
| `Cargo.toml` with `tests/` or `#[test]` | Cargo test | `cargo test` |
| `Makefile` with test target | Make | `make test` |
| `tox.ini` | tox | `tox` |
| `setup.py` with test command | setuptools | `python setup.py test` |

## Execution Steps

### 1. Detect Framework

1. Check for framework indicators in project root
2. If multiple found, list them and ask which to run
3. If none found, report "No test framework detected"

### 2. Run Tests

1. Execute the appropriate test command
2. Capture stdout/stderr
3. Parse results for pass/fail counts
4. Note: Some frameworks may require dependencies to be installed first

### 3. Coverage Check (if available)

Coverage tools by framework:
- **Python**: `pytest --cov` or `coverage run`
- **JavaScript**: Jest has built-in coverage (`--coverage`)
- **Go**: `go test -cover`
- **Rust**: `cargo tarpaulin` or `cargo llvm-cov`

If coverage is configured:
- Report overall coverage percentage
- List files with 0% coverage that were changed in sprint

### 4. Sprint File Analysis

If sprint context is available:
- Identify which sprint files have tests
- Flag sprint files with no corresponding test coverage

## Output Format

```
## Test Check Summary

### Test Results
- Framework: {detected framework}
- Status: {PASS/FAIL}
- Passed: {n} | Failed: {n} | Skipped: {n}
- Duration: {time}

### Failed Tests
- test_name: error message (file:line)

### Coverage (if available)
- Overall: {n}%
- Sprint files coverage:
  - file.py: {n}%
  - file.py: NO TESTS

### Recommendation
{READY FOR CLOSE / TESTS MUST PASS / COVERAGE GAPS TO ADDRESS}
```

## Behavior Flags

The command accepts optional flags via natural language:

| Request | Behavior |
|---------|----------|
| "run tests with coverage" | Include coverage report |
| "run tests verbose" | Show full output |
| "just check, don't run" | Report framework detection only |
| "run specific tests for X" | Run tests matching pattern |

## Framework-Specific Notes

### Python (pytest)
```bash
# Basic run
pytest

# With coverage
pytest --cov=src --cov-report=term-missing

# Verbose
pytest -v

# Specific tests
pytest tests/test_specific.py -k "test_function_name"
```

### JavaScript (Jest/Vitest)
```bash
# Basic run
npm test

# With coverage
npm test -- --coverage

# Specific tests
npm test -- --testPathPattern="specific"
```

### Go
```bash
# Basic run
go test ./...

# With coverage
go test -cover ./...

# Verbose
go test -v ./...
```

### Rust
```bash
# Basic run
cargo test

# Verbose
cargo test -- --nocapture
```

## Do NOT

- Modify test files
- Skip failing tests to make the run pass
- Run tests in production environments (check for .env indicators)
- Install dependencies without asking first
- Run tests that require external services without confirmation

## Error Handling

If tests fail:
1. Report the failure clearly
2. List failed test names and error summaries
3. Recommend: "TESTS MUST PASS before sprint close"
4. Offer to help debug specific failures

If framework not detected:
1. List what was checked
2. Ask user to specify the test command
3. Offer common suggestions based on file types found
