# Viz-Platform MCP Tools Reference

## Tool Categories

| Category | Tools |
|----------|-------|
| DMC Validation | `list_components`, `get_component_props`, `validate_component` |
| Charts | `chart_create`, `chart_configure_interaction`, `chart_export` |
| Layouts | `layout_create`, `layout_add_filter`, `layout_set_grid`, `layout_set_breakpoints` |
| Themes | `theme_create`, `theme_extend`, `theme_validate`, `theme_export_css`, `theme_list`, `theme_activate` |
| Pages | `page_create`, `page_add_navbar`, `page_set_auth` |
| Accessibility | `accessibility_validate_colors`, `accessibility_validate_theme`, `accessibility_suggest_alternative` |

## DMC Validation Tools

### list_components
```python
list_components(category=None)  # All components
list_components(category="inputs")  # Filter by category
```

### get_component_props
```python
get_component_props(component="Button")
```

### validate_component
```python
validate_component(
    component="Button",
    props={"variant": "filled", "color": "blue"}
)
```

## Chart Tools

### chart_create
```python
chart_create(
    chart_type="line",
    data_ref="df_sales",
    x="date",
    y="revenue",
    color=None,
    title="Sales Over Time",
    theme=None
)
```

### chart_export
```python
chart_export(
    figure=figure_json,
    format="png",  # png, svg, pdf
    width=1200,
    height=800,
    scale=2,
    output_path=None
)
```

## Layout Tools

### layout_create
```python
layout_create(
    name="my-dashboard",
    template="sidebar"  # basic, sidebar, tabs, split
)
```

### layout_add_filter
```python
layout_add_filter(
    layout_ref="my-dashboard",
    filter_type="dropdown",  # dropdown, date_range, slider, checkbox, search
    options={}
)
```

### layout_set_grid
```python
layout_set_grid(
    layout_ref="my-dashboard",
    cols=12,
    spacing="md"
)
```

### layout_set_breakpoints
```python
layout_set_breakpoints(
    layout_ref="my-dashboard",
    breakpoints={
        "xs": {"cols": 1, "spacing": "xs"},
        "sm": {"cols": 2, "spacing": "sm"},
        "md": {"cols": 6, "spacing": "md"},
        "lg": {"cols": 12, "spacing": "md"},
        "xl": {"cols": 12, "spacing": "lg"}
    },
    mobile_first=True
)
```

## Theme Tools

### theme_create
```python
theme_create(
    name="corporate",
    primary_color="indigo",
    color_scheme="light",
    font_family="Inter, sans-serif",
    heading_font_family=None,
    border_radius="md",
    spacing_scale=1.0,
    colors=None
)
```

### theme_extend
```python
theme_extend(
    base_theme="dark",
    name="dark-corporate",
    overrides={"primary_color": "indigo"}
)
```

### theme_validate
```python
theme_validate(theme_name="corporate")
```

### theme_export_css
```python
theme_export_css(theme_name="corporate")
```

### theme_activate
```python
theme_activate(theme_name="dark")
```

## Accessibility Tools

### accessibility_validate_colors
```python
accessibility_validate_colors(
    colors=["#228be6", "#40c057", "#fa5252"],
    check_types=["deuteranopia", "protanopia", "tritanopia"],
    min_contrast_ratio=4.5
)
```

### accessibility_validate_theme
```python
accessibility_validate_theme(theme_name="corporate")
```
