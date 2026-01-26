"""
MCP Server entry point for viz-platform integration.

Provides Dash Mantine Components validation, charting, layout, theming, and page tools
to Claude Code via JSON-RPC 2.0 over stdio.
"""
import asyncio
import logging
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import VizPlatformConfig
from .dmc_tools import DMCTools
from .chart_tools import ChartTools
from .layout_tools import LayoutTools
from .theme_tools import ThemeTools
from .page_tools import PageTools

# Suppress noisy MCP validation warnings on stderr
logging.basicConfig(level=logging.INFO)
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class VizPlatformMCPServer:
    """MCP Server for visualization platform integration"""

    def __init__(self):
        self.server = Server("viz-platform-mcp")
        self.config = None
        self.dmc_tools = DMCTools()
        self.chart_tools = ChartTools()
        self.layout_tools = LayoutTools()
        self.theme_tools = ThemeTools()
        self.page_tools = PageTools()

    async def initialize(self):
        """Initialize server and load configuration."""
        try:
            config_loader = VizPlatformConfig()
            self.config = config_loader.load()

            # Initialize DMC tools with detected version
            dmc_version = self.config.get('dmc_version')
            self.dmc_tools.initialize(dmc_version)

            # Log available capabilities
            caps = []
            if self.config.get('dmc_available'):
                caps.append(f"DMC {dmc_version}")
                if self.dmc_tools._initialized:
                    caps.append(f"Registry loaded ({self.dmc_tools.registry.loaded_version})")
            else:
                caps.append("DMC (not installed)")

            logger.info(f"viz-platform MCP Server initialized with: {', '.join(caps)}")

        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise

    def setup_tools(self):
        """Register all available tools with the MCP server"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
            tools = []

            # DMC validation tools (Issue #172)
            tools.append(Tool(
                name="list_components",
                description=(
                    "List available Dash Mantine Components. "
                    "Returns components grouped by category with version info. "
                    "Use this to discover what components are available before building UI."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": (
                                "Optional category filter. Available categories: "
                                "buttons, inputs, navigation, feedback, overlays, "
                                "typography, layout, data_display, charts, dates"
                            )
                        }
                    },
                    "required": []
                }
            ))

            tools.append(Tool(
                name="get_component_props",
                description=(
                    "Get the props schema for a specific DMC component. "
                    "Returns all available props with types, defaults, and allowed values. "
                    "ALWAYS use this before creating a component to ensure valid props."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "component": {
                            "type": "string",
                            "description": "Component name (e.g., 'Button', 'TextInput', 'Select')"
                        }
                    },
                    "required": ["component"]
                }
            ))

            tools.append(Tool(
                name="validate_component",
                description=(
                    "Validate component props before use. "
                    "Checks for invalid props, type mismatches, and common mistakes. "
                    "Returns errors and warnings with suggestions for fixes."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "component": {
                            "type": "string",
                            "description": "Component name to validate"
                        },
                        "props": {
                            "type": "object",
                            "description": "Props object to validate"
                        }
                    },
                    "required": ["component", "props"]
                }
            ))

            # Chart tools (Issue #173)
            tools.append(Tool(
                name="chart_create",
                description=(
                    "Create a Plotly chart for data visualization. "
                    "Supports line, bar, scatter, pie, heatmap, histogram, and area charts. "
                    "Automatically applies theme colors when a theme is active."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "chart_type": {
                            "type": "string",
                            "enum": ["line", "bar", "scatter", "pie", "heatmap", "histogram", "area"],
                            "description": "Type of chart to create"
                        },
                        "data": {
                            "type": "object",
                            "description": (
                                "Data for the chart. For most charts: {x: [], y: []}. "
                                "For pie: {labels: [], values: []}. "
                                "For heatmap: {x: [], y: [], z: [[]]}"
                            )
                        },
                        "options": {
                            "type": "object",
                            "description": (
                                "Optional settings: title, x_label, y_label, color, "
                                "showlegend, height, width, horizontal (for bar)"
                            )
                        }
                    },
                    "required": ["chart_type", "data"]
                }
            ))

            tools.append(Tool(
                name="chart_configure_interaction",
                description=(
                    "Configure interactions on an existing chart. "
                    "Add hover templates, enable click data capture, selection modes, "
                    "and zoom behavior for Dash callback integration."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "figure": {
                            "type": "object",
                            "description": "Plotly figure JSON to modify"
                        },
                        "interactions": {
                            "type": "object",
                            "description": (
                                "Interaction config: hover_template (string), "
                                "click_data (bool), selection ('box'|'lasso'), zoom (bool)"
                            )
                        }
                    },
                    "required": ["figure", "interactions"]
                }
            ))

            # Layout tools (Issue #174)
            tools.append(Tool(
                name="layout_create",
                description=(
                    "Create a new dashboard layout container. "
                    "Templates available: dashboard, report, form, blank. "
                    "Returns layout reference for use with other layout tools."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Unique name for the layout"
                        },
                        "template": {
                            "type": "string",
                            "enum": ["dashboard", "report", "form", "blank"],
                            "description": "Layout template to use (default: blank)"
                        }
                    },
                    "required": ["name"]
                }
            ))

            tools.append(Tool(
                name="layout_add_filter",
                description=(
                    "Add a filter control to a layout. "
                    "Filter types: dropdown, multi_select, date_range, date, search, "
                    "checkbox_group, radio_group, slider, range_slider."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "layout_ref": {
                            "type": "string",
                            "description": "Layout name to add filter to"
                        },
                        "filter_type": {
                            "type": "string",
                            "enum": ["dropdown", "multi_select", "date_range", "date",
                                    "search", "checkbox_group", "radio_group", "slider", "range_slider"],
                            "description": "Type of filter control"
                        },
                        "options": {
                            "type": "object",
                            "description": (
                                "Filter options: label, data (for dropdown), placeholder, "
                                "position (section name), value, etc."
                            )
                        }
                    },
                    "required": ["layout_ref", "filter_type", "options"]
                }
            ))

            tools.append(Tool(
                name="layout_set_grid",
                description=(
                    "Configure the grid system for a layout. "
                    "Uses DMC Grid component patterns with 12 or 24 column system."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "layout_ref": {
                            "type": "string",
                            "description": "Layout name to configure"
                        },
                        "grid": {
                            "type": "object",
                            "description": (
                                "Grid config: cols (1-24), spacing (xs|sm|md|lg|xl), "
                                "breakpoints ({xs: cols, sm: cols, ...}), gutter"
                            )
                        }
                    },
                    "required": ["layout_ref", "grid"]
                }
            ))

            # Theme tools (Issue #175)
            tools.append(Tool(
                name="theme_create",
                description=(
                    "Create a new design theme with tokens. "
                    "Tokens include colors, spacing, typography, radii. "
                    "Missing tokens are filled from defaults."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Unique theme name"
                        },
                        "tokens": {
                            "type": "object",
                            "description": (
                                "Design tokens: colors (primary, background, text), "
                                "spacing (xs-xl), typography (fontFamily, fontSize), radii (sm-xl)"
                            )
                        }
                    },
                    "required": ["name", "tokens"]
                }
            ))

            tools.append(Tool(
                name="theme_extend",
                description=(
                    "Create a new theme by extending an existing one. "
                    "Only specify the tokens you want to override."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "base_theme": {
                            "type": "string",
                            "description": "Theme to extend (e.g., 'default')"
                        },
                        "overrides": {
                            "type": "object",
                            "description": "Token overrides to apply"
                        },
                        "new_name": {
                            "type": "string",
                            "description": "Name for the new theme (optional)"
                        }
                    },
                    "required": ["base_theme", "overrides"]
                }
            ))

            tools.append(Tool(
                name="theme_validate",
                description=(
                    "Validate a theme for completeness. "
                    "Checks for required tokens and common issues."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "theme_name": {
                            "type": "string",
                            "description": "Theme to validate"
                        }
                    },
                    "required": ["theme_name"]
                }
            ))

            tools.append(Tool(
                name="theme_export_css",
                description=(
                    "Export a theme as CSS custom properties. "
                    "Generates :root CSS variables for all tokens."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "theme_name": {
                            "type": "string",
                            "description": "Theme to export"
                        }
                    },
                    "required": ["theme_name"]
                }
            ))

            # Page tools (Issue #176)
            tools.append(Tool(
                name="page_create",
                description=(
                    "Create a new page for a multi-page Dash application. "
                    "Defines page routing and can link to a layout."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Unique page name (identifier)"
                        },
                        "path": {
                            "type": "string",
                            "description": "URL path (e.g., '/', '/settings')"
                        },
                        "layout_ref": {
                            "type": "string",
                            "description": "Optional layout reference to use"
                        },
                        "title": {
                            "type": "string",
                            "description": "Page title (defaults to name)"
                        }
                    },
                    "required": ["name", "path"]
                }
            ))

            tools.append(Tool(
                name="page_add_navbar",
                description=(
                    "Generate navigation component linking pages. "
                    "Creates top or side navigation with DMC components."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "pages": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of page names to include"
                        },
                        "options": {
                            "type": "object",
                            "description": (
                                "Navigation options: position (top|left|right), "
                                "brand (app name), collapsible (bool)"
                            )
                        }
                    },
                    "required": ["pages"]
                }
            ))

            tools.append(Tool(
                name="page_set_auth",
                description=(
                    "Configure authentication for a page. "
                    "Sets auth requirements, roles, and redirect behavior."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "page_ref": {
                            "type": "string",
                            "description": "Page name to configure"
                        },
                        "auth_config": {
                            "type": "object",
                            "description": (
                                "Auth config: type (none|basic|oauth|custom), "
                                "required (bool), roles (array), redirect (path)"
                            )
                        }
                    },
                    "required": ["page_ref", "auth_config"]
                }
            ))

            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool invocation."""
            try:
                # DMC validation tools
                if name == "list_components":
                    result = await self.dmc_tools.list_components(
                        category=arguments.get('category')
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "get_component_props":
                    component = arguments.get('component')
                    if not component:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "component is required"}, indent=2)
                        )]
                    result = await self.dmc_tools.get_component_props(component)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "validate_component":
                    component = arguments.get('component')
                    props = arguments.get('props', {})
                    if not component:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "component is required"}, indent=2)
                        )]
                    result = await self.dmc_tools.validate_component(component, props)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                # Chart tools
                elif name == "chart_create":
                    chart_type = arguments.get('chart_type')
                    data = arguments.get('data', {})
                    options = arguments.get('options', {})
                    if not chart_type:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "chart_type is required"}, indent=2)
                        )]
                    result = await self.chart_tools.chart_create(chart_type, data, options)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "chart_configure_interaction":
                    figure = arguments.get('figure')
                    interactions = arguments.get('interactions', {})
                    if not figure:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "figure is required"}, indent=2)
                        )]
                    result = await self.chart_tools.chart_configure_interaction(figure, interactions)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                # Layout tools
                elif name == "layout_create":
                    layout_name = arguments.get('name')
                    template = arguments.get('template')
                    if not layout_name:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "name is required"}, indent=2)
                        )]
                    result = await self.layout_tools.layout_create(layout_name, template)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "layout_add_filter":
                    layout_ref = arguments.get('layout_ref')
                    filter_type = arguments.get('filter_type')
                    options = arguments.get('options', {})
                    if not layout_ref or not filter_type:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "layout_ref and filter_type are required"}, indent=2)
                        )]
                    result = await self.layout_tools.layout_add_filter(layout_ref, filter_type, options)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "layout_set_grid":
                    layout_ref = arguments.get('layout_ref')
                    grid = arguments.get('grid', {})
                    if not layout_ref:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "layout_ref is required"}, indent=2)
                        )]
                    result = await self.layout_tools.layout_set_grid(layout_ref, grid)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                # Theme tools
                elif name == "theme_create":
                    theme_name = arguments.get('name')
                    tokens = arguments.get('tokens', {})
                    if not theme_name:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "name is required"}, indent=2)
                        )]
                    result = await self.theme_tools.theme_create(theme_name, tokens)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "theme_extend":
                    base_theme = arguments.get('base_theme')
                    overrides = arguments.get('overrides', {})
                    new_name = arguments.get('new_name')
                    if not base_theme:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "base_theme is required"}, indent=2)
                        )]
                    result = await self.theme_tools.theme_extend(base_theme, overrides, new_name)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "theme_validate":
                    theme_name = arguments.get('theme_name')
                    if not theme_name:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "theme_name is required"}, indent=2)
                        )]
                    result = await self.theme_tools.theme_validate(theme_name)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "theme_export_css":
                    theme_name = arguments.get('theme_name')
                    if not theme_name:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "theme_name is required"}, indent=2)
                        )]
                    result = await self.theme_tools.theme_export_css(theme_name)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                # Page tools
                elif name == "page_create":
                    page_name = arguments.get('name')
                    path = arguments.get('path')
                    layout_ref = arguments.get('layout_ref')
                    title = arguments.get('title')
                    if not page_name or not path:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "name and path are required"}, indent=2)
                        )]
                    result = await self.page_tools.page_create(page_name, path, layout_ref, title)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "page_add_navbar":
                    pages = arguments.get('pages', [])
                    options = arguments.get('options', {})
                    if not pages:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "pages list is required"}, indent=2)
                        )]
                    result = await self.page_tools.page_add_navbar(pages, options)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "page_set_auth":
                    page_ref = arguments.get('page_ref')
                    auth_config = arguments.get('auth_config', {})
                    if not page_ref:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "page_ref is required"}, indent=2)
                        )]
                    result = await self.page_tools.page_set_auth(page_ref, auth_config)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                logger.error(f"Tool {name} failed: {e}")
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2)
                )]

    async def run(self):
        """Run the MCP server"""
        await self.initialize()
        self.setup_tools()

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = VizPlatformMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
