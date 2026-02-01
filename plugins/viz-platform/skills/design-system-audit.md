---
name: design-system-audit
description: Design system compliance rules and violation patterns for viz-platform audits
---

# Design System Audit

## Purpose

Defines what to check, how to classify violations, and common patterns for design system compliance auditing of Dash Mantine Components (DMC) code.

---

## What to Check

### 1. Component Prop Validity

| Check | Tool | Severity |
|-------|------|----------|
| Invalid prop names (typos) | `validate_component` | FAIL |
| Invalid prop values | `validate_component` | FAIL |
| Missing required props | `validate_component` | FAIL |
| Deprecated props | `get_component_props` | WARN |
| Unknown props | `validate_component` | WARN |

### 2. Theme Token Usage

| Check | Detection | Severity |
|-------|-----------|----------|
| Hardcoded hex colors | Regex `#[0-9a-fA-F]{3,6}` | WARN |
| Hardcoded RGB/RGBA | Regex `rgb\(` | WARN |
| Hardcoded font sizes | Regex `fontSize=\d+` | WARN |
| Hardcoded spacing | Regex `margin=\d+|padding=\d+` | INFO |
| Missing theme provider | AST analysis | FAIL |

**Allowed exceptions:**
- Colors in theme definition files
- Test/fixture files
- Comments and documentation

### 3. Accessibility Compliance

| Check | Tool | Severity |
|-------|------|----------|
| Color contrast ratio < 4.5:1 (AA) | `accessibility_validate_colors` | WARN |
| Color contrast ratio < 3:1 (large text) | `accessibility_validate_colors` | WARN |
| Missing aria-label on interactive | Manual scan | WARN |
| Color-only information | `accessibility_validate_theme` | WARN |
| Focus indicator missing | Manual scan | INFO |

### 4. Responsive Design

| Check | Detection | Severity |
|-------|-----------|----------|
| Fixed pixel widths > 600px | Regex `width=\d{3,}` | INFO |
| Missing breakpoint handling | No `visibleFrom`/`hiddenFrom` | INFO |
| Non-responsive layout | Fixed Grid columns | INFO |

---

## Common Violations

### FAIL-Level Violations

```python
# Invalid prop name (typo)
dmc.Button(colour="blue")  # Should be 'color'

# Invalid enum value
dmc.Button(size="large")   # Should be 'lg'

# Missing required prop
dmc.Select(data=[...])     # Missing 'id' for callbacks

# Invalid component name
dmc.Buttons(...)           # Should be 'Button'

# Wrong case
dmc.Button(fullwidth=True) # Should be 'fullWidth'

# React patterns in Dash
dmc.Button(onClick=fn)     # Should use 'id' + callback
```

### WARN-Level Violations

```python
# Hardcoded colors
dmc.Text(color="#ff0000")           # Use theme token
dmc.Button(style={"color": "red"})  # Use theme token

# Hardcoded font size
dmc.Text(style={"fontSize": "14px"})  # Use 'size' prop

# Poor contrast
dmc.Text(color="gray")  # Check contrast ratio

# Inline styles for colors
dmc.Container(style={"backgroundColor": "#f0f0f0"})

# Deprecated patterns
dmc.Button(variant="subtle")  # Check if still supported
```

### INFO-Level Violations

```python
# Fixed widths
dmc.Container(w=800)  # Consider responsive

# Missing responsive handling
dmc.Grid.Col(span=6)  # Consider span={{ base: 12, md: 6 }}

# Optimization opportunity
dmc.Stack([dmc.Text(...) for _ in range(100)])  # Consider virtualization
```

---

## Severity Classification

| Level | Icon | Meaning | Action |
|-------|------|---------|--------|
| **FAIL** | Red circle | Blocking issue, will cause runtime error | Must fix before completion |
| **WARN** | Orange circle | Quality issue, violates best practices | Should fix, may be waived |
| **INFO** | Yellow circle | Suggestion for improvement | Consider for future |

### Severity Decision Tree

```
Is it invalid syntax/props?
  YES -> FAIL
  NO -> Does it violate accessibility standards?
    YES -> WARN
    NO -> Does it use hardcoded styles?
      YES -> WARN
      NO -> Is it a best practice suggestion?
        YES -> INFO
        NO -> Not a violation
```

---

## Scanning Strategy

### File Types to Scan

| Extension | Priority | Check For |
|-----------|----------|-----------|
| `*.py` | High | DMC component usage |
| `*.dash.py` | High | Layout definitions |
| `theme*.py` | High | Theme configuration |
| `layout*.py` | High | Layout structure |
| `components/*.py` | High | Custom components |
| `callbacks/*.py` | Medium | Component references |

### Scan Process

1. **Find relevant files**
   ```
   glob: **/*.py
   filter: Contains 'dmc.' or 'dash_mantine_components'
   ```

2. **Extract component usages**
   - Parse Python AST
   - Find all `dmc.*` calls
   - Extract component name and kwargs

3. **Validate each component**
   - Call `validate_component(name, props)`
   - Record violations with file:line reference

4. **Scan for patterns**
   - Hardcoded colors (regex)
   - Inline styles (AST)
   - Fixed dimensions (regex)

5. **Run accessibility checks**
   - Extract color combinations
   - Call `accessibility_validate_colors`

---

## Report Template

```
Design System Audit Report
==========================
Path: <scanned-path>
Files Scanned: N
Timestamp: YYYY-MM-DD HH:MM:SS

Summary
-------
FAIL: N blocking violations
WARN: N quality warnings
INFO: N suggestions

Findings
--------

FAIL Violations (must fix)
--------------------------
[file.py:42] Invalid prop 'colour' on Button
  Found: colour="blue"
  Expected: color="blue"
  Docs: https://mantine.dev/core/button

[file.py:58] Invalid size value on Text
  Found: size="huge"
  Expected: One of ['xs', 'sm', 'md', 'lg', 'xl']

WARN Violations (should fix)
----------------------------
[theme.py:15] Hardcoded color detected
  Found: color="#ff0000"
  Suggestion: Use theme color token (e.g., color="red")

[layout.py:23] Low contrast ratio (3.2:1)
  Found: Text on background
  Required: 4.5:1 for WCAG AA
  Suggestion: Darken text or lighten background

INFO Suggestions
----------------
[dashboard.py:100] Consider responsive breakpoints
  Found: span=6 (fixed)
  Suggestion: span={{ base: 12, md: 6 }}

Files Scanned
-------------
- src/components/button.py (3 components)
- src/layouts/main.py (8 components)
- src/theme.py (1 theme config)

Gate Result: PASS | FAIL
```

---

## Integration with MCP Tools

### Required Tools

| Tool | Purpose | When Used |
|------|---------|-----------|
| `validate_component` | Check component props | Every component found |
| `get_component_props` | Get expected props | When suggesting fixes |
| `list_components` | Verify component exists | Unknown component names |
| `theme_validate` | Validate theme config | Theme files |
| `accessibility_validate_colors` | Check contrast | Color combinations |
| `accessibility_validate_theme` | Full a11y audit | Theme files |

### Tool Call Pattern

```
For each Python file:
  For each dmc.Component(...) found:
    result = validate_component(
      component_name="Component",
      props={extracted_props}
    )
    if result.errors:
      record FAIL violation
    if result.warnings:
      record WARN violation
```

---

## Skip Patterns

Do not flag violations in:

- `**/tests/**` - Test files may have intentional violations
- `**/__pycache__/**` - Compiled files
- `**/fixtures/**` - Test fixtures
- Files with `# noqa: design-audit` comment
- Theme definition files (colors are expected there)
