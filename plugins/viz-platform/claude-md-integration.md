# viz-platform CLAUDE.md Integration

Add this snippet to your project's CLAUDE.md to enable viz-platform capabilities.

## Integration Snippet

```markdown
## Visualization (viz-platform)

This project uses viz-platform for Dash Mantine Components dashboards.

### Available Commands
- `/viz component {name}` - Inspect DMC component props
- `/viz chart {type}` - Create Plotly charts (line, bar, scatter, pie, area, histogram, box, heatmap, sunburst, treemap)
- `/viz dashboard {template}` - Create layouts (basic, sidebar, tabs, split)
- `/viz theme {name}` - Apply a theme
- `/viz theme-new {name}` - Create custom theme
- `/viz theme-css {name}` - Export theme as CSS

### MCP Tools Available
- **DMC**: list_components, get_component_props, validate_component
- **Charts**: chart_create, chart_configure_interaction
- **Layouts**: layout_create, layout_add_filter, layout_set_grid, layout_add_section, layout_get
- **Themes**: theme_create, theme_extend, theme_validate, theme_export_css, theme_list, theme_activate
- **Pages**: page_create, page_add_navbar, page_set_auth, page_list, page_get_app_config

### Component Validation
ALWAYS validate DMC components before use:
1. Check props with `get_component_props(component_name)`
2. Validate usage with `validate_component(component_name, props)`
3. Fix any errors before proceeding

### Project Theme
Theme: [YOUR_THEME_NAME or "default"]
Color scheme: [light/dark]
Primary color: [color name]
```

## Cross-Plugin Configuration

If using with data-platform, add this section:

```markdown
## Data + Visualization Workflow

### Data Loading (data-platform)
- `/data ingest {file}` - Load CSV, Parquet, or JSON
- `/data schema {table}` - View database schema
- `/data profile {data_ref}` - Statistical summary

### Visualization (viz-platform)
- `/viz chart {type}` - Create charts from loaded data
- `/viz dashboard {template}` - Build dashboard layouts

### Workflow Pattern
1. Load data: `read_csv("data.csv")` → returns `data_ref`
2. Create chart: `chart_create(data_ref="data_ref", ...)`
3. Add to layout: `layout_add_section(chart_ref="...")`
4. Apply theme: `theme_activate("my-theme")`
```

## Agent Configuration

### Using theme-setup agent

When user mentions theming or brand colors:
```markdown
Use the theme-setup agent for:
- Creating new themes with brand colors
- Configuring typography and spacing
- Exporting themes as CSS
```

### Using layout-builder agent

When user wants dashboard structure:
```markdown
Use the layout-builder agent for:
- Creating dashboard layouts
- Adding filter components
- Configuring responsive grids
```

### Using component-check agent

For code review and debugging:
```markdown
Use the component-check agent for:
- Validating DMC component usage
- Fixing prop errors
- Understanding component APIs
```

## Example Project CLAUDE.md

```markdown
# Project: Sales Dashboard

## Tech Stack
- Backend: FastAPI
- Frontend: Dash with Mantine Components
- Data: PostgreSQL + pandas

## Data (data-platform)
- Database: PostgreSQL with sales data
- Key tables: orders, customers, products

## Visualization (viz-platform)
- Theme: corporate (indigo primary, light mode)
- Layout: sidebar with date and category filters
- Charts: line (trends), bar (comparisons), pie (breakdown)

### Component Validation
ALWAYS use component-check before rendering:
- get_component_props first
- validate_component after

### Dashboard Structure
```
Sidebar: Navigation links
Header: Title + date range filter
Main:
  - Row 1: KPI cards
  - Row 2: Line chart (sales over time)
  - Row 3: Bar chart (by category) + Pie chart (by region)
```
```

## Troubleshooting

### MCP tools not available
1. Check venv exists: `ls mcp-servers/viz-platform/.venv/`
2. Rebuild if needed: `cd mcp-servers/viz-platform && python -m venv .venv && pip install -r requirements.txt`
3. Restart Claude Code session

### Component validation fails
1. Check DMC version matches registry
2. Use `list_components()` to see available components
3. Verify prop names are camelCase

### Charts not rendering
1. Verify data_ref exists with `list_data()`
2. Check column names match data
3. Validate theme is active
