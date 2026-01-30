---
name: coverage-calculation
description: Documentation coverage metrics, language patterns, and thresholds
---

# Coverage Calculation

## Purpose

Defines how to calculate documentation coverage and thresholds.

## When to Use

- **doc-coverage**: Full coverage analysis
- **doc-audit**: Completeness checks

---

## Coverage Formula

```
Coverage = (Documented Items / Total Items) * 100
```

---

## Documentable Items by Language

### Python
- Functions (`def`)
- Classes
- Methods
- Module-level docstrings

### JavaScript/TypeScript
- Functions (`function`, arrow functions)
- Classes
- Methods
- JSDoc comments (`/** */`)

### Go
- Functions
- Types
- Methods
- Package comments (`//` above declaration)

### Rust
- Functions
- Structs/Enums
- Impl blocks
- Doc comments (`///`)

---

## Language Detection

| Extension | Language | Doc Format |
|-----------|----------|------------|
| .py | Python | Docstrings (`"""`) |
| .js, .ts | JavaScript/TypeScript | JSDoc (`/** */`) |
| .go | Go | `//` comments above |
| .rs | Rust | `///` doc comments |
| .rb | Ruby | `#` comments, YARD |
| .java | Java | Javadoc (`/** */`) |

---

## Coverage Levels

### Basic
- Item has any docstring/comment
- Not empty or placeholder

### Standard
- Docstring describes purpose
- Non-trivial content (not just `pass` or `TODO`)

### Complete
- All parameters documented
- Return type documented
- Raises/throws documented

---

## Coverage Thresholds

| Level | Coverage | Description |
|-------|----------|-------------|
| Minimal | 60% | Basic documentation exists |
| Good | 80% | Most public APIs documented |
| Excellent | 95% | Comprehensive documentation |

---

## Output Format

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

### Undocumented Items
- [ ] src/api/handlers.py:45 `create_order()`
- [ ] src/models/user.py:23 `UserModel.validate()`
```

---

## Exclusion Patterns

Default exclusions:
- `**/test_*` - Test files
- `**/*_test.*` - Test files
- Private members (`_prefixed`) unless `--include-private`
- Generated code (`**/generated/**`)
