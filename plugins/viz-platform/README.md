# viz-platform

Visualization tools for Dash Mantine Components (DMC) dashboards — component validation, Plotly charts, layout scaffolding, and design-contract-driven surface consistency.

**Version:** 10.0.0

---

## Commands

| Command | Description |
|---------|-------------|
| `/viz setup` | Setup wizard — environment + design contract builder |
| `/viz chart {type}` | Create Plotly charts |
| `/viz chart-export {format}` | Export charts to PNG, SVG, PDF |
| `/viz dashboard {template}` | Scaffold a layout (basic, sidebar, tabs, split) |
| `/viz theme apply {name}` | Activate an existing theme |
| `/viz theme create {name}` | Create a custom theme |
| `/viz theme export-css {name}` | Export theme as CSS custom properties |
| `/viz breakpoints {layout}` | Configure responsive breakpoints |

---

## Agents

### layout-builder
Dashboard layout scaffolding specialist. Handles filtering, grid systems, and responsive design using `layout_create`, `layout_add_filter`, `layout_set_grid`, and `layout_set_breakpoints`.

---

## Skills

| Skill | Description |
|-------|-------------|
| `theming-system.md` | **Surface Contract Spec.** Surface hierarchy model, resolver merge rules, component lock protocol, density protocol |
| `mcp-tools-reference.md` | MCP tool signatures and call patterns including 5 new contract tools |
| `dmc-components.md` | DMC component registry and dynamic discovery |
| `accessibility-rules.md` | WCAG contrast requirements and accessibility validation patterns |
| `chart-types.md` | Supported Plotly chart types and configuration options |
| `layout-templates.md` | Available layout templates and configuration |
| `responsive-design.md` | Breakpoint patterns and mobile-first design rules |
| `color-scheme-validation.md` | Five auditable rules for dual-scheme CSS integrity |
| `analytical-chart-selection.md` | graph_objects trace type selection guide |
| `notebook-design-system.md` | Dark-theme design system for Plotly in Jupyter |
| `choropleth-map-patterns.md` | Tile-based map background control for go.Choroplethmap |

---

## Design Contract (v10.0.0)

### Contract-First Design Workflow

v10.0.0 introduces a surface hierarchy resolver that enforces design consistency project-wide. Instead of setting `bg`, `withBorder`, and `variant` on each component individually, you define a contract once and the resolver enforces it everywhere.

### Quick Start

1. Run `/viz setup` — complete Phase 3 (contract builder)
2. A `.claude/design-contract.json` is created in your project root
3. All component-generation MCP tools automatically apply contract enforcement

### Surface Levels

| Level | Components | Example bg (light) |
|-------|-----------|-------------------|
| `base` | AppShell, Container, Stack | `white` |
| `raised` | Card, Paper | `white` + border `gray.2` |
| `overlay` | Modal, Drawer, Popover | `gray.0` |
| `nested_in_overlay` | Card inside Modal | `white` |

### Contract MCP Tools

```python
# Load and inspect active contract
contract_load(project_root="/path/to/project")

# Validate contract against schema
contract_validate(project_root="/path/to/project")

# Resolve component props (contract wins over caller)
contract_resolve_component(
    component="Card",
    scheme="light",
    surface_context="raised",
    requested_props={"p": "md"}
)

# Lock a component's props
contract_lock_component(
    component="Modal",
    spec={"padding": "md", "radius": "md"},
    reference_file="app/pages/settings.py",
    reference_line=42
)

# Get surface tokens for a level
contract_get_surface(scheme="light", level="raised")
```

### Resolver Merge Order

```
component_locks  >  surface tokens  >  requested_props
```

---

## MCP Server

The `mcp-servers/viz-platform/` server provides DMC validation, chart, layout, theme, accessibility, and design contract tools. Requires Python 3.11+ with the viz-platform venv set up via `./scripts/setup.sh`.

New in v10.0.0:
- `resolver.py` — DesignContract class for surface resolution and component locking
- `schemas/design-contract.schema.json` — JSON Schema draft-07 for contract validation

---

## Consumer Project Requirements

Set `DMC_LLMS_JSON_URL` in `.env` to the llms.json URL for your DMC version:

```
DMC_LLMS_JSON_URL=https://www.dash-mantine-components.com/assets/llms.json
```

For dual-scheme projects, set an explicit CSS entry point:

```
CSS_ENTRY_POINT=assets/styles.css
```

---

## Integration

See `claude-md-integration.md` for the CLAUDE.md snippet to add to consumer projects.
