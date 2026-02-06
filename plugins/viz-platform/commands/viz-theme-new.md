---
name: viz theme-new
description: Create a new custom theme with design tokens
---

# /viz theme-new

## Skills to Load
- skills/mcp-tools-reference.md
- skills/theming-system.md

## Visual Output

```
+------------------------------------------------------------------+
|  VIZ-PLATFORM - New Theme                                        |
+------------------------------------------------------------------+
```

Create a new custom theme with specified design tokens.

## Usage

```
/viz theme-new {name}
```

## Arguments

- `name` (required): Name for the new theme

## Tool Mapping

```python
theme_create(name="corporate", primary_color="indigo", color_scheme="light", font_family="Inter")
theme_validate(theme_name="corporate")
```

## Related Commands

- `/viz theme {name}` - Apply a theme
- `/viz theme-css {name}` - Export theme as CSS
