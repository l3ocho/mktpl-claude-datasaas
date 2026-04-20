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
| Design Contract | `contract_load`, `contract_validate`, `contract_resolve_component`, `contract_lock_component`, `contract_get_surface` |

## Design Contract Tools

| Tool | Purpose |
|------|---------|
| `contract_load` | Load `.claude/design-contract.json` from consumer project CWD |
| `contract_validate` | Validate contract against JSON schema; returns errors list |
| `contract_resolve_component` | Merge contract-enforced props with requested props; contract wins |
| `contract_lock_component` | Write a component lock entry to the contract file |
| `contract_get_surface` | Return surface spec (bg, border, variant) for a given scheme+level |

## Quick Reference

```python
# DMC
list_components(category="inputs")
get_component_props(component="Button")
validate_component(component="Button", props={"variant": "filled"})

# Charts
chart_create(chart_type="line", data={}, options={})
chart_export(figure={}, format="png", width=1200, height=800, scale=2)

# Layouts
layout_create(name="my-dashboard", template="sidebar")
layout_add_filter(layout_ref="my-dashboard", filter_type="dropdown", options={})
layout_set_grid(layout_ref="my-dashboard", grid={"cols": 12, "spacing": "md"})
layout_set_breakpoints(layout_ref="my-dashboard", breakpoints={})

# Themes
theme_create(name="corporate", tokens={"primary_color": "indigo"})
theme_extend(base_theme="dark", overrides={}, new_name="dark-corporate")
theme_validate(theme_name="corporate")
theme_export_css(theme_name="corporate")

# Design Contract
contract_load(project_root="/path/to/project")
contract_validate(contract_path="/path/to/.claude/design-contract.json")
contract_resolve_component(component="Card", scheme="light", surface_context="raised", requested_props={})
contract_lock_component(component="Modal", spec={"padding": "md"}, reference_file="app/pages/example.py", reference_line=42)
contract_get_surface(scheme="light", level="raised")
```
