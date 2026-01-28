---
description: Apply refactoring patterns to improve code structure and maintainability
---

# Refactor

Apply refactoring transformations to specified code.

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔒 CODE-SENTINEL · Refactor                                     │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the refactoring workflow.

## Usage
```
/refactor <target> [--pattern=<pattern>]
```

**Target:** File path, function name, or "." for current context
**Pattern:** Specific refactoring pattern (optional)

## Available Patterns

### Structure
| Pattern | Description |
|---------|-------------|
| `extract-method` | Extract code block into named function |
| `extract-class` | Move related methods to new class |
| `inline` | Inline trivial function/variable |
| `rename` | Rename with all references updated |
| `move` | Move function/class to different module |

### Simplification
| Pattern | Description |
|---------|-------------|
| `simplify-conditional` | Flatten nested if/else |
| `remove-dead-code` | Delete unreachable code |
| `consolidate-duplicate` | Merge duplicate code blocks |
| `decompose-conditional` | Break complex conditions into named parts |

### Modernization
| Pattern | Description |
|---------|-------------|
| `use-comprehension` | Convert loops to list/dict comprehensions |
| `use-pathlib` | Replace os.path with pathlib |
| `use-fstring` | Convert .format() to f-strings |
| `use-typing` | Add type hints |
| `use-dataclass` | Convert class to dataclass |

## Process

1. **Analyze Target**
   - Parse code structure
   - Identify refactoring opportunities
   - Check for side effects and dependencies

2. **Propose Changes**
   - Show before/after diff
   - Explain the improvement
   - List affected files/references

3. **Apply (with confirmation)**
   - Make changes
   - Update all references
   - Run existing tests if available

4. **Output**
```
## Refactoring: extract-method

### Target
src/handlers.py:create_order (lines 45-89)

### Changes
- Extracted validation logic → validate_order_input()
- Extracted pricing logic → calculate_order_total()
- Original function now 15 lines (was 44)

### Files Modified
- src/handlers.py
- tests/test_handlers.py (updated calls)

### Metrics
- Cyclomatic complexity: 12 → 4
- Function length: 44 → 15 lines
```
