# viz-platform Plugin

Visualization tools with Dash Mantine Components validation, Plotly charts, and theming for Claude Code.

## Features

- **DMC Validation**: Prevent prop hallucination with version-locked component registry
- **Chart Creation**: Plotly charts with automatic theme token application
- **Layout Builder**: Dashboard layouts with filters, grids, and responsive design
- **Theme System**: Create, extend, and export design tokens

## Installation

This plugin is part of the leo-claude-mktplace. Install via:

```bash
# From marketplace
claude plugins install leo-claude-mktplace/viz-platform

# Setup MCP server venv
cd ~/.claude/plugins/marketplaces/leo-claude-mktplace/mcp-servers/viz-platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

### System-Level (Optional)

Create `~/.config/claude/viz-platform.env` for default theme preferences:

```env
VIZ_PLATFORM_COLOR_SCHEME=light
VIZ_PLATFORM_PRIMARY_COLOR=blue
```

### Project-Level (Optional)

Add to project `.env` for project-specific settings:

```env
VIZ_PLATFORM_THEME=my-custom-theme
DMC_VERSION=0.14.7
```

## Commands

| Command | Description |
|---------|-------------|
| `/initial-setup` | Interactive setup wizard for DMC and theme preferences |
| `/component {name}` | Inspect component props and validation |
| `/chart {type}` | Create a Plotly chart |
| `/chart-export {format}` | Export chart to PNG, SVG, or PDF |
| `/dashboard {template}` | Create a dashboard layout |
| `/breakpoints {layout}` | Configure responsive breakpoints |
| `/accessibility-check` | Validate colors for color blind users |
| `/theme {name}` | Apply an existing theme |
| `/theme-new {name}` | Create a new custom theme |
| `/theme-css {name}` | Export theme as CSS |

## Agents

| Agent | Description |
|-------|-------------|
| `theme-setup` | Design-focused theme creation specialist |
| `layout-builder` | Dashboard layout and filter specialist |
| `component-check` | Strict component validation specialist |

## Tool Categories

### DMC Validation (3 tools)
Prevent invalid component props before runtime.

| Tool | Description |
|------|-------------|
| `list_components` | List available components by category |
| `get_component_props` | Get detailed prop specifications |
| `validate_component` | Validate a component configuration |

### Charts (3 tools)
Create Plotly charts with theme integration.

| Tool | Description |
|------|-------------|
| `chart_create` | Create a chart (line, bar, scatter, pie, etc.) |
| `chart_configure_interaction` | Configure chart interactivity |
| `chart_export` | Export chart to PNG, SVG, or PDF |

### Layouts (6 tools)
Build dashboard structures with filters and grids.

| Tool | Description |
|------|-------------|
| `layout_create` | Create a layout structure |
| `layout_add_filter` | Add filter components |
| `layout_set_grid` | Configure responsive grid |
| `layout_set_breakpoints` | Configure responsive breakpoints (xs-xl) |
| `layout_add_section` | Add content sections |
| `layout_get` | Retrieve layout details |

### Accessibility (3 tools)
Validate colors for accessibility and color blindness.

| Tool | Description |
|------|-------------|
| `accessibility_validate_colors` | Check colors for color blind accessibility |
| `accessibility_validate_theme` | Validate a theme's color accessibility |
| `accessibility_suggest_alternative` | Suggest accessible color alternatives |

### Themes (6 tools)
Manage design tokens and styling.

| Tool | Description |
|------|-------------|
| `theme_create` | Create a new theme |
| `theme_extend` | Extend an existing theme |
| `theme_validate` | Validate theme configuration |
| `theme_export_css` | Export as CSS custom properties |
| `theme_list` | List available themes |
| `theme_activate` | Set the active theme |

### Pages (5 tools)
Create full Dash app configurations.

| Tool | Description |
|------|-------------|
| `page_create` | Create a page structure |
| `page_add_navbar` | Add navigation bar |
| `page_set_auth` | Configure authentication |
| `page_list` | List pages |
| `page_get_app_config` | Get full app configuration |

## Component Validation

The key differentiator of viz-platform is the component registry system:

```python
# Before writing component code
get_component_props("Button")
# Returns: all valid props with types, enums, defaults

# After writing code
validate_component("Button", {"variant": "filled", "color": "blue"})
# Returns: {valid: true} or {valid: false, errors: [...]}
```

This prevents common DMC mistakes:
- Prop typos (`colour` vs `color`)
- Invalid enum values (`size="large"` vs `size="lg"`)
- Wrong case (`fullwidth` vs `fullWidth`)

## Example Workflow

```
/component Button
# → Shows all Button props with types and defaults

/theme-new corporate
# → Creates theme with brand colors

/chart bar
# → Creates bar chart with theme colors

/dashboard sidebar
# → Creates sidebar layout with filters

/theme-css corporate
# → Exports theme as CSS for external use
```

## Cross-Plugin Integration

viz-platform works seamlessly with data-platform:

1. **Load data** with data-platform: `/ingest sales.csv`
2. **Create chart** with viz-platform: `/chart line` using the data_ref
3. **Build layout** with viz-platform: `/dashboard` with filters
4. **Export** complete dashboard structure

## Chart Types

| Type | Best For |
|------|----------|
| `line` | Time series, trends |
| `bar` | Comparisons, categories |
| `scatter` | Correlations, distributions |
| `pie` | Part-to-whole |
| `area` | Cumulative trends |
| `histogram` | Frequency distributions |
| `box` | Statistical distributions |
| `heatmap` | Matrix correlations |
| `sunburst` | Hierarchical data |
| `treemap` | Hierarchical proportions |

## Layout Templates

| Template | Best For |
|----------|----------|
| `basic` | Simple dashboards, reports |
| `sidebar` | Navigation-heavy apps |
| `tabs` | Multi-page dashboards |
| `split` | Comparisons, master-detail |

## Responsive Breakpoints

The plugin supports mobile-first responsive design with standard breakpoints:

| Breakpoint | Min Width | Description |
|------------|-----------|-------------|
| `xs` | 0px | Extra small (mobile portrait) |
| `sm` | 576px | Small (mobile landscape) |
| `md` | 768px | Medium (tablet) |
| `lg` | 992px | Large (desktop) |
| `xl` | 1200px | Extra large (large desktop) |

Example:
```
/breakpoints my-dashboard
# Configure cols, spacing per breakpoint
```

## Color Accessibility

The plugin validates colors for color blindness:
- **Deuteranopia** (green-blind) - 6% of males
- **Protanopia** (red-blind) - 2.5% of males
- **Tritanopia** (blue-blind) - 0.01% of population

Includes WCAG contrast ratio checking and accessible palette suggestions.

## Requirements

- Python 3.10+
- dash-mantine-components >= 0.14.0
- plotly >= 5.18.0
- dash >= 2.14.0
- kaleido >= 0.2.1 (for chart export)
