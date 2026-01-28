---
description: Create a new custom theme with design tokens
---

# Create New Theme

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🎨 VIZ-PLATFORM · New Theme                                      │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the theme creation.

Create a new custom theme with specified design tokens.

## Usage

```
/theme-new {name}
```

## Arguments

- `name` (required): Name for the new theme

## Examples

```
/theme-new corporate
/theme-new dark-blue
/theme-new brand-theme
```

## Tool Mapping

This command uses the `theme_create` MCP tool:

```python
theme_create(
    name="corporate",
    primary_color="indigo",
    color_scheme="light",
    font_family="Inter, sans-serif",
    heading_font_family=None,        # Optional: separate heading font
    border_radius="md",              # xs, sm, md, lg, xl
    spacing_scale=1.0,               # Multiplier for spacing
    colors=None                      # Optional: custom color palette
)
```

## Workflow

1. **User invokes**: `/theme-new corporate`
2. **Agent asks**: Primary color preference?
3. **Agent asks**: Light or dark color scheme?
4. **Agent asks**: Font family preference?
5. **Agent creates**: Theme with `theme_create`
6. **Agent validates**: Theme with `theme_validate`
7. **Agent activates**: New theme is ready to use

## Theme Properties

### Colors
- `primary_color`: Main accent color (blue, indigo, violet, etc.)
- `color_scheme`: "light" or "dark"
- `colors`: Custom color palette override

### Typography
- `font_family`: Body text font
- `heading_font_family`: Optional heading font

### Spacing
- `border_radius`: Component corner rounding
- `spacing_scale`: Multiply default spacing values

## Mantine Color Palette

Available primary colors:
- blue, cyan, teal, green, lime
- yellow, orange, red, pink, grape
- violet, indigo, gray, dark

## Custom Color Example

```python
theme_create(
    name="brand",
    primary_color="custom",
    colors={
        "custom": [
            "#e6f7ff",  # 0 - lightest
            "#bae7ff",  # 1
            "#91d5ff",  # 2
            "#69c0ff",  # 3
            "#40a9ff",  # 4
            "#1890ff",  # 5 - primary
            "#096dd9",  # 6
            "#0050b3",  # 7
            "#003a8c",  # 8
            "#002766"   # 9 - darkest
        ]
    }
)
```

## Extending Themes

To create a theme based on another:

```python
theme_extend(
    base_theme="dark",
    name="dark-corporate",
    overrides={
        "primary_color": "indigo",
        "font_family": "Roboto, sans-serif"
    }
)
```

## Related Commands

- `/theme {name}` - Apply a theme
- `/theme-css {name}` - Export theme as CSS
