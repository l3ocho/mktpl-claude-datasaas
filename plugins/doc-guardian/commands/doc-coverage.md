---
description: Calculate documentation coverage percentage for functions and classes
---

# Documentation Coverage

Analyze codebase to calculate documentation coverage metrics.

## Process

1. **Scan Source Files**
   Identify all documentable items:

   **Python:**
   - Functions (def)
   - Classes
   - Methods
   - Module-level docstrings

   **JavaScript/TypeScript:**
   - Functions (function, arrow functions)
   - Classes
   - Methods
   - JSDoc comments

   **Other Languages:**
   - Adapt patterns for Go, Rust, etc.

2. **Determine Documentation Status**
   For each item, check:
   - Has docstring/JSDoc comment
   - Docstring is non-empty and meaningful (not just `pass` or `TODO`)
   - Parameters are documented (for detailed mode)
   - Return type is documented (for detailed mode)

3. **Calculate Metrics**
   ```
   Coverage = (Documented Items / Total Items) * 100
   ```

   **Levels:**
   - Basic: Item has any docstring
   - Standard: Docstring describes purpose
   - Complete: All parameters and return documented

4. **Output Format**
```
## Documentation Coverage Report

### Summary
- Total documentable items: 156
- Documented: 142
- Coverage: 91.0%

### By Type
| Type | Total | Documented | Coverage |
|------|-------|------------|----------|
| Functions | 89 | 85 | 95.5% |
| Classes | 23 | 21 | 91.3% |
| Methods | 44 | 36 | 81.8% |

### By Directory
| Path | Total | Documented | Coverage |
|------|-------|------------|----------|
| src/api/ | 34 | 32 | 94.1% |
| src/utils/ | 28 | 28 | 100.0% |
| src/models/ | 45 | 38 | 84.4% |
| tests/ | 49 | 44 | 89.8% |

### Undocumented Items
- [ ] src/api/handlers.py:45 `create_order()`
- [ ] src/api/handlers.py:78 `update_order()`
- [ ] src/models/user.py:23 `UserModel.validate()`
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--path <dir>` | Scan specific directory | Project root |
| `--exclude <glob>` | Exclude files matching pattern | `**/test_*,**/*_test.*` |
| `--include-private` | Include private members (_prefixed) | false |
| `--include-tests` | Include test files | false |
| `--min-coverage <pct>` | Fail if below threshold | none |
| `--format <fmt>` | Output format (table, json, markdown) | table |
| `--detailed` | Check parameter/return docs | false |

## Thresholds

Common coverage targets:
| Level | Coverage | Description |
|-------|----------|-------------|
| Minimal | 60% | Basic documentation exists |
| Good | 80% | Most public APIs documented |
| Excellent | 95% | Comprehensive documentation |

## CI Integration

Use `--min-coverage` to enforce standards:
```bash
# Fail if coverage drops below 80%
claude /doc-coverage --min-coverage 80
```

Exit codes:
- 0: Coverage meets threshold (or no threshold set)
- 1: Coverage below threshold

## Example Usage

```
/doc-coverage
/doc-coverage --path src/
/doc-coverage --min-coverage 85 --exclude "**/generated/**"
/doc-coverage --detailed --include-private
```

## Language Detection

File extensions mapped to documentation patterns:
| Extension | Language | Doc Format |
|-----------|----------|------------|
| .py | Python | Docstrings (""") |
| .js, .ts | JavaScript/TypeScript | JSDoc (/** */) |
| .go | Go | // comments above |
| .rs | Rust | /// doc comments |
| .rb | Ruby | # comments, YARD |
| .java | Java | Javadoc (/** */) |
