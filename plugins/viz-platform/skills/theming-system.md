# Theming System

## Design Tokens

Themes define design tokens for consistent styling across components.

### Theme Properties

| Category | Properties |
|----------|------------|
| Colors | `primary_color`, `color_scheme`, `colors` |
| Typography | `font_family`, `heading_font_family` |
| Spacing | `border_radius`, `spacing_scale` |

### Color Scheme
- `light` - Light background, dark text
- `dark` - Dark background, light text

### Border Radius Scale
| Size | Value |
|------|-------|
| xs | 0.125rem |
| sm | 0.25rem |
| md | 0.5rem |
| lg | 1rem |
| xl | 2rem |

## Mantine Color Palette

Available primary colors:
- blue, cyan, teal, green, lime
- yellow, orange, red, pink, grape
- violet, indigo, gray, dark

Each color has 10 shades (0-9), where 5 is the primary shade.

## Custom Color Definition

```python
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
```

## CSS Custom Properties

Exported themes use Mantine CSS variable naming:

```css
:root {
  /* Colors */
  --mantine-color-scheme: light;
  --mantine-primary-color: indigo;
  --mantine-color-primary-0: #edf2ff;
  --mantine-color-primary-5: #5c7cfa;
  --mantine-color-primary-9: #364fc7;

  /* Typography */
  --mantine-font-family: Inter, sans-serif;
  --mantine-font-size-xs: 0.75rem;
  --mantine-font-size-md: 1rem;

  /* Spacing */
  --mantine-spacing-xs: 0.625rem;
  --mantine-spacing-md: 1rem;

  /* Border Radius */
  --mantine-radius-sm: 0.25rem;
  --mantine-radius-md: 0.5rem;

  /* Shadows */
  --mantine-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --mantine-shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

## Theme Inheritance

Create themes based on existing ones:
```python
theme_extend(
    base_theme="dark",
    name="dark-corporate",
    overrides={"primary_color": "indigo"}
)
```

## Built-in Themes

| Theme | Description |
|-------|-------------|
| `light` | Mantine default light mode |
| `dark` | Mantine default dark mode |
