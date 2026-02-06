---
name: viz accessibility-check
description: Validate color accessibility for color blind users
---

# /viz accessibility-check

## Skills to Load
- skills/mcp-tools-reference.md
- skills/accessibility-rules.md

## Visual Output

```
+------------------------------------------------------------------+
|  VIZ-PLATFORM - Accessibility Check                              |
+------------------------------------------------------------------+
```

Validate theme or chart colors for color blind accessibility.

## Usage

```
/viz accessibility-check {target}
```

## Arguments

- `target` (optional): "theme" or "chart" - defaults to active theme

## Tool Mapping

```python
accessibility_validate_colors(
    colors=["#228be6", "#40c057"],
    check_types=["deuteranopia", "protanopia", "tritanopia"],
    min_contrast_ratio=4.5
)
accessibility_validate_theme(theme_name="corporate")
```

## Related Commands

- `/viz theme-new {name}` - Create accessible theme
- `/viz chart {type}` - Create chart (check colors after)
