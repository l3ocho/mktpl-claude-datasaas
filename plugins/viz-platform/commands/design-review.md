---
description: Audit codebase for design system compliance
arguments:
  - name: path
    description: File or directory to audit
    required: true
---

# /design-review

Scans target path for Dash Mantine Components usage and validates against design system standards.

## Usage

```
/design-review <path>
```

**Examples:**
```
/design-review ./app/pages/
/design-review ./app/components/dashboard.py
/design-review .
```

## What It Does

1. **Activates** the `design-reviewer` agent in review mode
2. **Loads** the `skills/design-system-audit.md` skill
3. **Scans** target path for:
   - Python files with DMC imports
   - Component instantiations and their props
   - Style dictionaries and color values
   - Accessibility attributes
4. **Validates** against:
   - DMC component registry (valid components and props)
   - Theme token usage (no hardcoded colors/sizes)
   - Accessibility standards (contrast, ARIA labels)
5. **Produces** detailed report grouped by severity

## Output

Generates a comprehensive audit report with:

- **FAIL**: Invalid props, deprecated components, missing required props
- **WARN**: Hardcoded colors/sizes, missing accessibility attributes
- **INFO**: Optimization suggestions, consistency recommendations

Each finding includes:
- File path and line number
- Description of the issue
- Recommended fix

## When to Use

- **Before PR review**: Catch design system violations early
- **On existing codebases**: Audit for compliance gaps
- **During refactoring**: Ensure changes maintain compliance
- **Learning**: Understand design system best practices

## Related Commands

- `/design-gate` - Binary pass/fail for sprint execution (no detailed report)
- `/viz-component` - Inspect individual DMC component props
- `/viz-theme` - Check active theme configuration

## Requirements

- viz-platform MCP server must be running
- Target path must contain Python files with DMC usage
