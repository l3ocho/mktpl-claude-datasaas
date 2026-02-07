---
name: viz theme-css
description: Export a theme as CSS custom properties
---

# /viz theme-css

## Skills to Load
- skills/mcp-tools-reference.md
- skills/theming-system.md

## Visual Output

```
+------------------------------------------------------------------+
|  VIZ-PLATFORM - Theme CSS Export                                 |
+------------------------------------------------------------------+
```

Export a theme's design tokens as CSS custom properties.

## Usage

```
/viz theme-css {name}
```

## Arguments

- `name` (required): Theme name to export

## Tool Mapping

```python
theme_export_css(theme_name="corporate")
```

Use cases: external CSS, design handoff, documentation, other frameworks.

## Related Commands

- `/viz theme {name}` - Apply a theme
- `/viz theme-new {name}` - Create a new theme
