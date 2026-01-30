---
description: Export a theme as CSS custom properties
---

# Export Theme as CSS

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
/theme-css {name}
```

## Arguments

- `name` (required): Theme name to export

## Tool Mapping

```python
theme_export_css(theme_name="corporate")
```

Use cases: external CSS, design handoff, documentation, other frameworks.

## Related Commands

- `/theme {name}` - Apply a theme
- `/theme-new {name}` - Create a new theme
