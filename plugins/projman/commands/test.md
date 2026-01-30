---
description: Run tests with coverage or generate tests for specified code
---

# Test

## Skills Required

- skills/test-standards.md

## Purpose

Unified testing command for running tests and generating new tests.

## Invocation

```
/test                       # Default: run tests
/test run                   # Run tests, check coverage
/test run --coverage        # Run with coverage report
/test run --verbose         # Verbose output
/test gen <target>          # Generate tests for target
/test gen <target> --type=unit      # Specific test type
/test gen <target> --framework=jest # Specific framework
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

---

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  🧪 TEST                                                         ║
║  [Mode: Run | Generate]                                          ║
╚══════════════════════════════════════════════════════════════════╝
```
