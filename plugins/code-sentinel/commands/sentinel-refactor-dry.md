---
name: sentinel refactor-dry
description: Preview refactoring changes without applying them
---

# /sentinel refactor-dry

Analyze and preview refactoring opportunities without making changes.

## Visual Output

```
+----------------------------------------------------------------------+
|  CODE-SENTINEL - Refactor Preview                                    |
+----------------------------------------------------------------------+
```

## Usage
```
/sentinel refactor-dry <target> [--all]
```

**Target:** File path, function name, or "." for current file
**--all:** Show all opportunities, not just recommended

## Skills to Load

- skills/refactoring-patterns.md
- skills/dry-run-workflow.md

## Process

1. **Scan Target** - Analyze code using patterns from skill
2. **Score Opportunities** - Rate by Impact/Risk/Effort (see dry-run-workflow skill)
3. **Output** - Group by recommended vs optional

## Output Format

```
## Refactoring Opportunities: <target>

### Recommended (High Impact, Low Risk)
1. **pattern** at lines X-Y
   - Impact: High | Risk: Low
   - Run: `/sentinel refactor <target> --pattern=<pattern>`

### Optional
- Lower priority items

### Summary
- X recommended, Y optional
- Estimated complexity reduction: Z%
```
