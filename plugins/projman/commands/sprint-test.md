---
name: sprint test
description: Run tests with coverage or generate tests for specified code
---

# Sprint Test

## Skills Required

- skills/test-standards.md

## Purpose

Unified testing command for running tests and generating new tests.

## Invocation

```
/sprint test                       # Default: run tests
/sprint test run                   # Run tests, check coverage
/sprint test run --coverage        # Run with coverage report
/sprint test run --verbose         # Verbose output
/sprint test gen <target>          # Generate tests for target
/sprint test gen <target> --type=unit      # Specific test type
/sprint test gen <target> --framework=jest # Specific framework
```

## Mode Selection

- No args or `run` → **Run Mode**
- `gen <target>` → **Generate Mode**

---

## Mode: Run

Run tests and verify coverage before sprint close.

### Workflow

1. **Detect Framework**
   Check for: pytest.ini, package.json, go.mod, Cargo.toml, etc.

2. **Run Tests**
   Execute appropriate test command for detected framework.

3. **Check Coverage** (if --coverage or available)
   Report coverage percentage.

4. **Sprint File Analysis**
   Identify sprint files without tests.

See `skills/test-standards.md` for framework detection and commands.

### DO NOT (Run Mode)

- Modify test files
- Skip failing tests to make run pass
- Run tests in production environments
- Install dependencies without asking

---

## Mode: Generate

Generate comprehensive tests for specified code.

### Arguments

- **Target:** File path, function name, class name, or module
- **--type:** unit (default), integration, e2e, snapshot
- **--framework:** Auto-detected or specified (pytest, jest, vitest, go test)

### Workflow

1. **Analyze Target Code**
   Parse signatures, identify dependencies, map types.

2. **Determine Test Strategy**
   Based on code pattern:
   - Pure function → unit tests with multiple inputs
   - Class → instance lifecycle tests
   - API endpoint → request/response tests
   - Component → render and interaction tests

3. **Generate Tests**
   - Happy path cases
   - Edge cases (empty, null, boundary)
   - Error cases (invalid input, exceptions)
   - Type variations (if applicable)

4. **Output File**
   Create test file with proper structure and naming.

See `skills/test-standards.md` for test patterns and structure.

### DO NOT (Generate Mode)

- Install dependencies without asking first
- Generate tests that import private/internal functions not meant for testing
- Overwrite existing test files without confirmation
- Generate tests with hardcoded values that should be environment-based

---

## Sprint Integration

The `/sprint test` command plays a critical role in the sprint close workflow:

1. After `/sprint review` identifies code quality issues
2. Before `/sprint close` finalizes the sprint
3. The code reviewer and orchestrator reference test results when deciding if a sprint is ready to close

### Pre-Close Verification

When running `/sprint test run` before sprint close:

1. **Identify sprint files** - Files changed in the current sprint (via git diff against development)
2. **Check test coverage** - Report which sprint files have tests and which don't
3. **Flag untested code** - Warn if new code has no corresponding tests
4. **Recommend action** - "READY FOR CLOSE" or "TESTS NEEDED: [list of untested files]"

---

## Examples

### Run all tests
```
/sprint test run
```
Detects framework, runs full test suite, reports results.

### Run with coverage
```
/sprint test run --coverage
```
Same as above plus coverage percentage per file.

### Generate tests for a specific file
```
/sprint test gen src/auth/jwt_service.py
```
Analyzes the file, generates a test file at `tests/test_jwt_service.py`.

### Generate specific test type
```
/sprint test gen src/api/routes/auth.py --type=integration
```
Generates integration tests (request/response patterns) instead of unit tests.

### Generate with specific framework
```
/sprint test gen src/components/Card.jsx --framework=vitest
```
Uses Vitest instead of auto-detected framework.

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No test framework detected | List what was checked, ask user to specify test command |
| Tests fail | Report failures clearly, recommend "TESTS MUST PASS before sprint close" |
| No tests exist for sprint files | Warn with file list, offer to generate with `/sprint test gen` |
| External services required | Ask for confirmation before running tests that need database/API |
| Mixed framework project | Detect all frameworks, ask which to run or run all |

---

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  🧪 TEST                                                         ║
║  [Mode: Run | Generate]                                          ║
╚══════════════════════════════════════════════════════════════════╝
```
