---
description: Export a theme as CSS custom properties
---

# Export Theme as CSS

Export a theme's design tokens as CSS custom properties for use outside Dash.

## Usage

```
/theme-css {name}
```

## Arguments

- `name` (required): Theme name to export

## Examples

```
/theme-css dark
/theme-css corporate
/theme-css my-brand
```

## Tool Mapping

This command uses the `theme_export_css` MCP tool:

```python
theme_export_css(theme_name="corporate")
```

## Output Example

```css
:root {
  /* Colors */
  --mantine-color-scheme: light;
  --mantine-primary-color: indigo;
  --mantine-color-primary-0: #edf2ff;
  --mantine-color-primary-1: #dbe4ff;
  --mantine-color-primary-2: #bac8ff;
  --mantine-color-primary-3: #91a7ff;
  --mantine-color-primary-4: #748ffc;
  --mantine-color-primary-5: #5c7cfa;
  --mantine-color-primary-6: #4c6ef5;
  --mantine-color-primary-7: #4263eb;
  --mantine-color-primary-8: #3b5bdb;
  --mantine-color-primary-9: #364fc7;

  /* Typography */
  --mantine-font-family: Inter, sans-serif;
  --mantine-heading-font-family: Inter, sans-serif;
  --mantine-font-size-xs: 0.75rem;
  --mantine-font-size-sm: 0.875rem;
  --mantine-font-size-md: 1rem;
  --mantine-font-size-lg: 1.125rem;
  --mantine-font-size-xl: 1.25rem;

  /* Spacing */
  --mantine-spacing-xs: 0.625rem;
  --mantine-spacing-sm: 0.75rem;
  --mantine-spacing-md: 1rem;
  --mantine-spacing-lg: 1.25rem;
  --mantine-spacing-xl: 2rem;

  /* Border Radius */
  --mantine-radius-xs: 0.125rem;
  --mantine-radius-sm: 0.25rem;
  --mantine-radius-md: 0.5rem;
  --mantine-radius-lg: 1rem;
  --mantine-radius-xl: 2rem;

  /* Shadows */
  --mantine-shadow-xs: 0 1px 3px rgba(0, 0, 0, 0.05);
  --mantine-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --mantine-shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --mantine-shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --mantine-shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);
}
```

## Use Cases

### External CSS Files
Include the exported CSS in non-Dash projects:
```html
<link rel="stylesheet" href="theme-tokens.css">
```

### Design Handoff
Share design tokens with designers or other teams.

### Documentation
Generate theme documentation for style guides.

### Other Frameworks
Use Mantine-compatible tokens in React, Vue, or other projects.

## Workflow

1. **User invokes**: `/theme-css corporate`
2. **Tool exports**: Theme tokens as CSS
3. **User can**: Save to file or copy to clipboard

## Related Commands

- `/theme {name}` - Apply a theme
- `/theme-new {name}` - Create a new theme
