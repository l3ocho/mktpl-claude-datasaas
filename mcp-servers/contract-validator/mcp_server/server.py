"""
MCP Server entry point for Contract Validator.

Provides cross-plugin compatibility validation and Claude.md agent verification
tools to Claude Code via JSON-RPC 2.0 over stdio.
"""
import asyncio
import logging
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .parse_tools import ParseTools
from .validation_tools import ValidationTools
from .report_tools import ReportTools

# Suppress noisy MCP validation warnings on stderr
logging.basicConfig(level=logging.INFO)
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class ContractValidatorMCPServer:
    """MCP Server for cross-plugin compatibility validation"""

    def __init__(self):
        self.server = Server("contract-validator-mcp")
        self.parse_tools = ParseTools()
        self.validation_tools = ValidationTools()
        self.report_tools = ReportTools()

    async def initialize(self):
        """Initialize server."""
        logger.info("Contract Validator MCP Server initialized")

    def setup_tools(self):
        """Register all available tools with the MCP server"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
            tools = [
                # Parse tools (to be implemented in #186)
                Tool(
                    name="parse_plugin_interface",
                    description="Parse plugin README.md to extract interface declarations (inputs, outputs, tools)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "plugin_path": {
                                "type": "string",
                                "description": "Path to plugin directory or README.md"
                            }
                        },
                        "required": ["plugin_path"]
                    }
                ),
                Tool(
                    name="parse_claude_md_agents",
                    description="Parse Claude.md to extract agent definitions and their tool sequences",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "claude_md_path": {
                                "type": "string",
                                "description": "Path to CLAUDE.md file"
                            }
                        },
                        "required": ["claude_md_path"]
                    }
                ),
                # Validation tools (to be implemented in #187)
                Tool(
                    name="validate_compatibility",
                    description="Validate compatibility between two plugin interfaces",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "plugin_a": {
                                "type": "string",
                                "description": "Path to first plugin"
                            },
                            "plugin_b": {
                                "type": "string",
                                "description": "Path to second plugin"
                            }
                        },
                        "required": ["plugin_a", "plugin_b"]
                    }
                ),
                Tool(
                    name="validate_agent_refs",
                    description="Validate that all tool references in an agent definition exist",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_name": {
                                "type": "string",
                                "description": "Name of agent to validate"
                            },
                            "claude_md_path": {
                                "type": "string",
                                "description": "Path to CLAUDE.md containing agent"
                            },
                            "plugin_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to available plugins"
                            }
                        },
                        "required": ["agent_name", "claude_md_path"]
                    }
                ),
                Tool(
                    name="validate_data_flow",
                    description="Validate data flow through an agent's tool sequence",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_name": {
                                "type": "string",
                                "description": "Name of agent to validate"
                            },
                            "claude_md_path": {
                                "type": "string",
                                "description": "Path to CLAUDE.md containing agent"
                            }
                        },
                        "required": ["agent_name", "claude_md_path"]
                    }
                ),
                Tool(
                    name="validate_workflow_integration",
                    description="Validate that a domain plugin exposes the required advisory interfaces (gate command, review command, advisory agent) expected by projman's domain-consultation skill. Also checks gate contract version compatibility.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "plugin_path": {
                                "type": "string",
                                "description": "Path to the domain plugin directory"
                            },
                            "domain_label": {
                                "type": "string",
                                "description": "The Domain/* label it claims to handle, e.g. Domain/Viz"
                            },
                            "expected_contract": {
                                "type": "string",
                                "description": "Expected contract version (e.g., 'v1'). If provided, validates the gate command's contract matches."
                            }
                        },
                        "required": ["plugin_path", "domain_label"]
                    }
                ),
                # Report tools (to be implemented in #188)
                Tool(
                    name="generate_compatibility_report",
                    description="Generate a comprehensive compatibility report for all plugins",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "marketplace_path": {
                                "type": "string",
                                "description": "Path to marketplace root directory"
                            },
                            "format": {
                                "type": "string",
                                "enum": ["markdown", "json"],
                                "default": "markdown",
                                "description": "Output format"
                            }
                        },
                        "required": ["marketplace_path"]
                    }
                ),
                Tool(
                    name="list_issues",
                    description="List validation issues with optional filtering",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "marketplace_path": {
                                "type": "string",
                                "description": "Path to marketplace root directory"
                            },
                            "severity": {
                                "type": "string",
                                "enum": ["error", "warning", "info", "all"],
                                "default": "all",
                                "description": "Filter by severity"
                            },
                            "issue_type": {
                                "type": "string",
                                "enum": ["missing_tool", "interface_mismatch", "optional_dependency", "undeclared_output", "all"],
                                "default": "all",
                                "description": "Filter by issue type"
                            }
                        },
                        "required": ["marketplace_path"]
                    }
                )
            ]
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool invocation."""
            try:
                # All tools return placeholder responses for now
                # Actual implementation will be added in issues #186, #187, #188

                if name == "parse_plugin_interface":
                    result = await self._parse_plugin_interface(**arguments)
                elif name == "parse_claude_md_agents":
                    result = await self._parse_claude_md_agents(**arguments)
                elif name == "validate_compatibility":
                    result = await self._validate_compatibility(**arguments)
                elif name == "validate_agent_refs":
                    result = await self._validate_agent_refs(**arguments)
                elif name == "validate_data_flow":
                    result = await self._validate_data_flow(**arguments)
                elif name == "validate_workflow_integration":
                    result = await self._validate_workflow_integration(**arguments)
                elif name == "generate_compatibility_report":
                    result = await self._generate_compatibility_report(**arguments)
                elif name == "list_issues":
                    result = await self._list_issues(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, default=str)
                )]

            except Exception as e:
                logger.error(f"Tool {name} failed: {e}")
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2)
                )]

    # Parse tool implementations (Issue #186)

    async def _parse_plugin_interface(self, plugin_path: str) -> dict:
        """Parse plugin interface from README.md"""
        return await self.parse_tools.parse_plugin_interface(plugin_path)

    async def _parse_claude_md_agents(self, claude_md_path: str) -> dict:
        """Parse agents from CLAUDE.md"""
        return await self.parse_tools.parse_claude_md_agents(claude_md_path)

    # Validation tool implementations (Issue #187)

    async def _validate_compatibility(self, plugin_a: str, plugin_b: str) -> dict:
        """Validate compatibility between plugins"""
        return await self.validation_tools.validate_compatibility(plugin_a, plugin_b)

    async def _validate_agent_refs(self, agent_name: str, claude_md_path: str, plugin_paths: list = None) -> dict:
        """Validate agent tool references"""
        return await self.validation_tools.validate_agent_refs(agent_name, claude_md_path, plugin_paths)

    async def _validate_data_flow(self, agent_name: str, claude_md_path: str) -> dict:
        """Validate agent data flow"""
        return await self.validation_tools.validate_data_flow(agent_name, claude_md_path)

    async def _validate_workflow_integration(
        self,
        plugin_path: str,
        domain_label: str,
        expected_contract: str = None
    ) -> dict:
        """Validate domain plugin exposes required advisory interfaces"""
        return await self.validation_tools.validate_workflow_integration(
            plugin_path, domain_label, expected_contract
        )

    # Report tool implementations (Issue #188)

    async def _generate_compatibility_report(self, marketplace_path: str, format: str = "markdown") -> dict:
        """Generate comprehensive compatibility report"""
        return await self.report_tools.generate_compatibility_report(marketplace_path, format)

    async def _list_issues(self, marketplace_path: str, severity: str = "all", issue_type: str = "all") -> dict:
        """List validation issues with filtering"""
        return await self.report_tools.list_issues(marketplace_path, severity, issue_type)

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
    server = ContractValidatorMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
