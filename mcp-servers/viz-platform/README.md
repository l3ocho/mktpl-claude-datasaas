# viz-platform MCP Server

Model Context Protocol (MCP) server for Dash Mantine Components validation and visualization tools.

## Overview

This MCP server provides 21 tools for:
- **DMC Validation**: Version-locked component registry prevents Claude from hallucinating invalid props
- **Chart Creation**: Plotly-based visualization with theme integration
- **Layout Composition**: Dashboard layouts with responsive grids
- **Theme Management**: Design token-based theming system
- **Page Structure**: Multi-page Dash app generation

## Tools

### DMC Tools (3)

| Tool | Description |
|------|-------------|
| `list_components` | List available DMC components by category |
| `get_component_props` | Get valid props, types, and defaults for a component |
| `validate_component` | Validate component definition before use |

### Chart Tools (2)

| Tool | Description |
|------|-------------|
| `chart_create` | Create Plotly chart (line, bar, scatter, pie, histogram, area, heatmap) |
| `chart_configure_interaction` | Configure chart interactions (zoom, pan, hover) |

### Layout Tools (5)

| Tool | Description |
|------|-------------|
| `layout_create` | Create dashboard layout structure |
| `layout_add_filter` | Add filter components to layout |
| `layout_set_grid` | Configure responsive grid settings |
| `layout_get` | Retrieve layout configuration |
| `layout_add_section` | Add sections to layout |

### Theme Tools (6)

| Tool | Description |
|------|-------------|
| `theme_create` | Create new theme with design tokens |
| `theme_extend` | Extend existing theme with overrides |
| `theme_validate` | Validate theme completeness |
| `theme_export_css` | Export theme as CSS custom properties |
| `theme_list` | List available themes |
| `theme_activate` | Set active theme for visualizations |

### Page Tools (5)

| Tool | Description |
|------|-------------|
| `page_create` | Create new page structure |
| `page_add_navbar` | Add navigation bar to page |
| `page_set_auth` | Configure page authentication |
| `page_list` | List available pages |
| `page_get_app_config` | Get full app configuration |

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DMC_VERSION` | No | Dash Mantine Components version (auto-detected if installed) |
| `VIZ_DEFAULT_THEME` | No | Default theme name |
| `CLAUDE_PROJECT_DIR` | No | Project directory for theme storage |

### Theme Storage

Themes can be stored at two levels:
- **User-level**: `~/.config/claude/themes/`
- **Project-level**: `{project}/.viz-platform/themes/`

Project-level themes take precedence.

## Component Registry

The server uses a static JSON registry for DMC component validation:
- Pre-generated from DMC source code
- Version-tagged (e.g., `dmc_2_5.json`)
- Prevents hallucination of non-existent props
- Fast, deterministic validation

Registry files are stored in `registry/` directory.

## Tests

94 tests with coverage:
- `test_config.py`: 82% coverage
- `test_component_registry.py`: 92% coverage
- `test_dmc_tools.py`: 88% coverage
- `test_chart_tools.py`: 68% coverage
- `test_theme_tools.py`: 99% coverage

Run tests:
```bash
cd mcp-servers/viz-platform
source .venv/bin/activate
pytest tests/ -v
```

## Dependencies

- Python 3.10+
- FastMCP
- plotly
- dash-mantine-components (optional, for version detection)

## Usage

This MCP server is used by the `viz-platform` plugin. See the plugin's commands in `plugins/viz-platform/commands/` for usage.
