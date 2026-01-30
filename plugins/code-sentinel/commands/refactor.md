---
description: Apply refactoring patterns to improve code structure and maintainability
---

# Refactor

Apply refactoring transformations to specified code.

## Visual Output

```
+----------------------------------------------------------------------+
|  CODE-SENTINEL - Refactor                                            |
+----------------------------------------------------------------------+
```

## Usage
```
/refactor <target> [--pattern=<pattern>]
```

**Target:** File path, function name, or "." for current context
**Pattern:** Specific refactoring pattern (optional)

## Skills to Load

- skills/refactoring-patterns.md

## Process

1. **Analyze Target** - Parse code, identify opportunities from skill, check dependencies
2. **Propose Changes** - Show before/after diff, explain improvement, list affected files
3. **Apply (with confirmation)** - Make changes, update references, run tests

## Output Format

```
## Refactoring: <pattern>

### Target
<file>:<function> (lines X-Y)

### Changes
- Change description

### Files Modified
- file1.py

### Metrics
- Cyclomatic complexity: X -> Y
- Function length: X -> Y lines
```
