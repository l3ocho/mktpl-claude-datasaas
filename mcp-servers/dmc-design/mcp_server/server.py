"""
MCP Server entry point for dmc-design integration.

Provides Dash Mantine Components validation, theming, accessibility tools,
and design contract resolution to Claude Code via JSON-RPC 2.0 over stdio.
"""
import asyncio
import logging
import json
from datetime import datetime, timezone
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import VizPlatformConfig
from .dmc_tools import DMCTools
from .theme_tools import ThemeTools
from .accessibility_tools import AccessibilityTools

# Import resolver from parent package directory
import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent.parent))
from resolver import load_contract, DesignContract

# Suppress noisy MCP validation warnings on stderr
logging.basicConfig(level=logging.INFO)
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class DmcDesignMCPServer:
    """MCP Server for DMC design system integration"""

    def __init__(self):
        self.server = Server("dmc-design-mcp")
        self.config = None
        self.dmc_tools = DMCTools()
        self.theme_tools = ThemeTools()
        self.accessibility_tools = AccessibilityTools(theme_store=self.theme_tools.store)

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

            logger.info(f"dmc-design MCP Server initialized with: {', '.join(caps)}")

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
                    "Returns errors and warnings with suggestions for fixes. "
                    "If a design contract is active, contract-enforced props are merged before validation."
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
                        },
                        "surface_context": {
                            "type": "string",
                            "enum": ["base", "raised", "overlay", "nested_in_overlay"],
                            "description": "Optional surface context for contract resolution"
                        },
                        "scheme": {
                            "type": "string",
                            "enum": ["light", "dark"],
                            "description": "Active color scheme for contract resolution (default: light)"
                        }
                    },
                    "required": ["component", "props"]
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

            # Accessibility tools (Issue #248)
            tools.append(Tool(
                name="accessibility_validate_colors",
                description=(
                    "Validate colors for color blind accessibility. "
                    "Checks contrast ratios for deuteranopia, protanopia, tritanopia. "
                    "Returns issues, simulations, and accessible palette suggestions."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "colors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of hex colors to validate (e.g., ['#228be6', '#40c057'])"
                        },
                        "check_types": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Color blindness types to check: deuteranopia, protanopia, tritanopia (default: all)"
                        },
                        "min_contrast_ratio": {
                            "type": "number",
                            "description": "Minimum WCAG contrast ratio (default: 4.5 for AA)"
                        }
                    },
                    "required": ["colors"]
                }
            ))

            tools.append(Tool(
                name="accessibility_validate_theme",
                description=(
                    "Validate a theme's colors for accessibility. "
                    "Extracts all colors from theme tokens and checks for color blind safety."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "theme_name": {
                            "type": "string",
                            "description": "Theme name to validate"
                        }
                    },
                    "required": ["theme_name"]
                }
            ))

            tools.append(Tool(
                name="accessibility_suggest_alternative",
                description=(
                    "Suggest accessible alternative colors for a given color. "
                    "Provides alternatives optimized for specific color blindness types."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "color": {
                            "type": "string",
                            "description": "Hex color to find alternatives for"
                        },
                        "deficiency_type": {
                            "type": "string",
                            "enum": ["deuteranopia", "protanopia", "tritanopia"],
                            "description": "Color blindness type to optimize for"
                        }
                    },
                    "required": ["color", "deficiency_type"]
                }
            ))

            # Design contract tools (RFC-09)
            tools.append(Tool(
                name="contract_load",
                description=(
                    "Load the design contract from the consumer project. "
                    "Reads `.claude/design-contract.json` from the given project root. "
                    "Returns the contract data or an empty object if no contract exists."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_root": {
                            "type": "string",
                            "description": "Absolute path to the consumer project root (defaults to CWD)"
                        }
                    },
                    "required": []
                }
            ))

            tools.append(Tool(
                name="contract_validate",
                description=(
                    "Validate a design contract against the JSON schema. "
                    "Returns a list of validation errors (empty list means valid)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_root": {
                            "type": "string",
                            "description": "Absolute path to the consumer project root (defaults to CWD)"
                        }
                    },
                    "required": []
                }
            ))

            tools.append(Tool(
                name="contract_resolve_component",
                description=(
                    "Resolve component props against the active design contract. "
                    "Contract-enforced props override requested props. "
                    "Returns the merged props object."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "component": {
                            "type": "string",
                            "description": "DMC component name (e.g., 'Card', 'Modal')"
                        },
                        "scheme": {
                            "type": "string",
                            "enum": ["light", "dark"],
                            "description": "Active color scheme (default: light)"
                        },
                        "surface_context": {
                            "type": "string",
                            "enum": ["base", "raised", "overlay", "nested_in_overlay"],
                            "description": "Override inferred surface level"
                        },
                        "requested_props": {
                            "type": "object",
                            "description": "Props the caller wants to set (may be overridden by contract)"
                        },
                        "project_root": {
                            "type": "string",
                            "description": "Absolute path to the consumer project root (defaults to CWD)"
                        }
                    },
                    "required": ["component"]
                }
            ))

            tools.append(Tool(
                name="contract_lock_component",
                description=(
                    "Lock a component's props in the design contract. "
                    "Lock entries override surface-derived props for the named component. "
                    "Use to preserve intentional design decisions across code changes."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "component": {
                            "type": "string",
                            "description": "DMC component name to lock"
                        },
                        "spec": {
                            "type": "object",
                            "description": "Props to lock (these always win in resolution)"
                        },
                        "reference_file": {
                            "type": "string",
                            "description": "Source file where the canonical usage lives"
                        },
                        "reference_line": {
                            "type": "integer",
                            "description": "Line number of the canonical usage"
                        },
                        "project_root": {
                            "type": "string",
                            "description": "Absolute path to the consumer project root (defaults to CWD)"
                        }
                    },
                    "required": ["component", "spec", "reference_file", "reference_line"]
                }
            ))

            tools.append(Tool(
                name="contract_get_surface",
                description=(
                    "Get the surface specification for a scheme and level. "
                    "Returns bg, border, and variant tokens for the requested surface."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "scheme": {
                            "type": "string",
                            "enum": ["light", "dark"],
                            "description": "Color scheme"
                        },
                        "level": {
                            "type": "string",
                            "enum": ["base", "raised", "overlay", "nested_in_overlay"],
                            "description": "Surface level"
                        },
                        "project_root": {
                            "type": "string",
                            "description": "Absolute path to the consumer project root (defaults to CWD)"
                        }
                    },
                    "required": ["scheme", "level"]
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
                    # Apply contract resolution if contract is active
                    surface_context = arguments.get('surface_context')
                    scheme = arguments.get('scheme', 'light')
                    try:
                        contract = load_contract(Path.cwd())
                        if contract.is_active():
                            props = contract.resolve_component(
                                component_name=component,
                                scheme=scheme,
                                surface_context=surface_context,
                                requested_props=props
                            )
                    except Exception:
                        pass  # Contract resolution failure is non-fatal
                    result = await self.dmc_tools.validate_component(component, props)
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

                # Accessibility tools
                elif name == "accessibility_validate_colors":
                    colors = arguments.get('colors')
                    if not colors:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "colors list is required"}, indent=2)
                        )]
                    result = await self.accessibility_tools.accessibility_validate_colors(
                        colors=colors,
                        check_types=arguments.get('check_types'),
                        min_contrast_ratio=arguments.get('min_contrast_ratio', 4.5)
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "accessibility_validate_theme":
                    theme_name = arguments.get('theme_name')
                    if not theme_name:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "theme_name is required"}, indent=2)
                        )]
                    result = await self.accessibility_tools.accessibility_validate_theme(theme_name)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "accessibility_suggest_alternative":
                    color = arguments.get('color')
                    deficiency_type = arguments.get('deficiency_type')
                    if not color or not deficiency_type:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "color and deficiency_type are required"}, indent=2)
                        )]
                    result = await self.accessibility_tools.accessibility_suggest_alternative(
                        color, deficiency_type
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                # Design contract tools (RFC-09)
                elif name == "contract_load":
                    project_root = Path(arguments.get('project_root') or Path.cwd())
                    contract = load_contract(Path(project_root))
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "active": contract.is_active(),
                            "contract": contract.data,
                            "path": str(contract.path)
                        }, indent=2)
                    )]

                elif name == "contract_validate":
                    try:
                        import jsonschema
                    except ImportError:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "jsonschema package not installed. Run: pip install jsonschema"}, indent=2)
                        )]
                    project_root = Path(arguments.get('project_root') or Path.cwd())
                    contract = load_contract(project_root)
                    if not contract.is_active():
                        return [TextContent(
                            type="text",
                            text=json.dumps({"valid": False, "errors": ["No contract found at " + str(contract.path)]}, indent=2)
                        )]
                    schema_path = Path(__file__).parent.parent / "schemas" / "design-contract.schema.json"
                    schema = json.loads(schema_path.read_text())
                    errors = []
                    try:
                        jsonschema.validate(instance=contract.data, schema=schema)
                    except jsonschema.ValidationError as e:
                        errors.append(e.message)
                    except jsonschema.SchemaError as e:
                        errors.append(f"Schema error: {e.message}")
                    return [TextContent(
                        type="text",
                        text=json.dumps({"valid": len(errors) == 0, "errors": errors}, indent=2)
                    )]

                elif name == "contract_resolve_component":
                    component = arguments.get('component')
                    if not component:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "component is required"}, indent=2)
                        )]
                    project_root = Path(arguments.get('project_root') or Path.cwd())
                    contract = load_contract(project_root)
                    resolved = contract.resolve_component(
                        component_name=component,
                        scheme=arguments.get('scheme', 'light'),
                        surface_context=arguments.get('surface_context'),
                        requested_props=arguments.get('requested_props', {})
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "component": component,
                            "resolved_props": resolved,
                            "contract_active": contract.is_active()
                        }, indent=2)
                    )]

                elif name == "contract_lock_component":
                    component = arguments.get('component')
                    spec = arguments.get('spec', {})
                    reference_file = arguments.get('reference_file')
                    reference_line = arguments.get('reference_line')
                    if not component or not reference_file or reference_line is None:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "component, reference_file, and reference_line are required"}, indent=2)
                        )]
                    project_root = Path(arguments.get('project_root') or Path.cwd())
                    contract = load_contract(project_root)
                    contract.lock_component(
                        component_name=component,
                        spec=spec,
                        reference_file=reference_file,
                        reference_line=reference_line
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "locked": True,
                            "component": component,
                            "spec": spec
                        }, indent=2)
                    )]

                elif name == "contract_get_surface":
                    scheme = arguments.get('scheme')
                    level = arguments.get('level')
                    if not scheme or not level:
                        return [TextContent(
                            type="text",
                            text=json.dumps({"error": "scheme and level are required"}, indent=2)
                        )]
                    project_root = Path(arguments.get('project_root') or Path.cwd())
                    contract = load_contract(project_root)
                    surface = contract.resolve_surface(scheme, level)
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "scheme": scheme,
                            "level": level,
                            "surface": surface,
                            "contract_active": contract.is_active()
                        }, indent=2)
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
    server = DmcDesignMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
