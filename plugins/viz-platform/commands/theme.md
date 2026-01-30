---
description: Apply an existing theme to the current context
---

# Apply Theme

## Skills to Load
- skills/mcp-tools-reference.md
- skills/theming-system.md

## Visual Output

```
+------------------------------------------------------------------+
|  VIZ-PLATFORM - Apply Theme                                      |
+------------------------------------------------------------------+
```

Apply an existing theme to activate its design tokens.

## Usage

```
/theme {name}
```

## Arguments

- `name` (required): Theme name to activate

## Tool Mapping

```python
theme_activate(theme_name="dark")
theme_list()  # List available themes
```

## Theme Effects

When activated, new charts/layouts automatically use theme tokens.

## Related Commands

- `/theme-new {name}` - Create a new theme
- `/theme-css {name}` - Export theme as CSS
