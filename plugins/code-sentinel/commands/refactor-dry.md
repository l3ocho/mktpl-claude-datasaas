---
description: Preview refactoring changes without applying them
---

# Refactor Dry Run

Analyze and preview refactoring opportunities without making changes.

## Usage
```
/refactor-dry <target> [--all]
```

**Target:** File path, function name, or "." for current file
**--all:** Show all opportunities, not just recommended

## Process

1. **Scan Target**
   Analyze code for refactoring opportunities.

2. **Score Opportunities**
   Each opportunity rated by:
   - Impact (how much it improves code)
   - Risk (likelihood of breaking something)
   - Effort (complexity of the refactoring)

3. **Output**
```
## Refactoring Opportunities: src/handlers.py

### Recommended (High Impact, Low Risk)

1. **extract-method** at lines 45-67
   - Extract order validation logic
   - Impact: High (reduces complexity from 12 to 4)
   - Risk: Low (pure function, no side effects)
   - Run: `/refactor src/handlers.py:45 --pattern=extract-method`

2. **use-dataclass** for OrderInput class
   - Convert to dataclass with validation
   - Impact: Medium (reduces boilerplate)
   - Risk: Low
   - Run: `/refactor src/models.py:OrderInput --pattern=use-dataclass`

### Optional (Consider Later)

3. **use-fstring** at 12 locations
   - Modernize string formatting
   - Impact: Low (readability only)
   - Risk: None

### Summary
- 2 recommended refactorings
- 1 optional improvement
- Estimated complexity reduction: 35%
```
