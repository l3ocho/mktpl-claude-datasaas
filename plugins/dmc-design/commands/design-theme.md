---
name: design theme
description: [dmc-design] Theme management — apply, create, or export CSS for a dmc-design theme
---

# /design theme

Manage themes for dmc-design. Routes to action based on first argument.

## Usage

```
/design theme apply {name}       — Activate an existing theme
/design theme create {name}      — Create a new theme with design tokens
/design theme export-css {name}  — Export theme as CSS custom properties
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
