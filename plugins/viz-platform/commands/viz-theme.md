---
name: viz theme
description: Theme management — apply, create, or export CSS for a viz-platform theme
---

# /viz theme

Manage themes for the viz-platform. Routes to action based on first argument.

## Usage

```
/viz theme apply {name}       — Activate an existing theme
/viz theme create {name}      — Create a new theme with design tokens
/viz theme export-css {name}  — Export theme as CSS custom properties
```

## Action: apply

Activate an existing theme so charts and layouts use its tokens.

```python
theme_activate(theme_name="corporate")
theme_list()  # List available themes
```

## Action: create

Create a new theme. Prompts for primary color, font, spacing, and radius preferences.

```python
theme_create(name="corporate", tokens={
    "primary_color": "indigo",
    "font_family": "Inter, sans-serif",
    "color_scheme": "light"
})
theme_validate(theme_name="corporate")
```

## Action: export-css

Export a theme as CSS custom properties for use outside Mantine.

```python
theme_export_css(theme_name="corporate")
```

Output is written to `assets/theme.css` by default.

## Routing

If `$ARGUMENTS` starts with `apply`, `create`, or `export-css`, execute that action.
If no action is given, display usage above and ask which action to run.
