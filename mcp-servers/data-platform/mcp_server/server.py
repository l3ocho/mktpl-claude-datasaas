"""
MCP Server entry point for Data Platform integration.

Provides pandas, PostgreSQL/PostGIS, and dbt tools to Claude Code via JSON-RPC 2.0 over stdio.
"""
import asyncio
import logging
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import DataPlatformConfig
from .data_store import DataStore
from .pandas_tools import PandasTools
from .postgres_tools import PostgresTools
from .dbt_tools import DbtTools

# Suppress noisy MCP validation warnings on stderr
logging.basicConfig(level=logging.INFO)
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class DataPlatformMCPServer:
    """MCP Server for data platform integration"""

    def __init__(self):
        self.server = Server("data-platform-mcp")
        self.config = None
        self.pandas_tools = None
        self.postgres_tools = None
        self.dbt_tools = None

    async def initialize(self):
        """Initialize server and load configuration."""
        try:
            config_loader = DataPlatformConfig()
            self.config = config_loader.load()

            self.pandas_tools = PandasTools()
            self.postgres_tools = PostgresTools()
            self.dbt_tools = DbtTools()

            # Log available capabilities
            caps = []
            caps.append("pandas")
            if self.config.get('postgres_available'):
                caps.append("PostgreSQL")
            if self.config.get('dbt_available'):
                caps.append("dbt")

            logger.info(f"Data Platform MCP Server initialized with: {', '.join(caps)}")

        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise

    def setup_tools(self):
        """Register all available tools with the MCP server"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
            tools = [
                # pandas tools - always available
                Tool(
                    name="read_csv",
                    description="Load CSV file into DataFrame",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to CSV file"
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name for data_ref"
                            },
                            "chunk_size": {
                                "type": "integer",
                                "description": "Process in chunks of this size"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="read_parquet",
                    description="Load Parquet file into DataFrame",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to Parquet file"
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name for data_ref"
                            },
                            "columns": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional list of columns to load"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="read_json",
                    description="Load JSON/JSONL file into DataFrame",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to JSON file"
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name for data_ref"
                            },
                            "lines": {
                                "type": "boolean",
                                "default": False,
                                "description": "Read as JSON Lines format"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="to_csv",
                    description="Export DataFrame to CSV file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_ref": {
                                "type": "string",
                                "description": "Reference to stored DataFrame"
                            },
                            "file_path": {
                                "type": "string",
                                "description": "Output file path"
                            },
                            "index": {
                                "type": "boolean",
                                "default": False,
                                "description": "Include index column"
                            }
                        },
                        "required": ["data_ref", "file_path"]
                    }
                ),
                Tool(
                    name="to_parquet",
                    description="Export DataFrame to Parquet file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_ref": {
                                "type": "string",
                                "description": "Reference to stored DataFrame"
                            },
                            "file_path": {
                                "type": "string",
                                "description": "Output file path"
                            },
                            "compression": {
                                "type": "string",
                                "default": "snappy",
                                "description": "Compression codec"
                            }
                        },
                        "required": ["data_ref", "file_path"]
                    }
                ),
                Tool(
                    name="describe",
                    description="Get statistical summary of DataFrame",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_ref": {
                                "type": "string",
                                "description": "Reference to stored DataFrame"
                            }
                        },
                        "required": ["data_ref"]
                    }
                ),
                Tool(
                    name="head",
                    description="Get first N rows of DataFrame",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_ref": {
                                "type": "string",
                                "description": "Reference to stored DataFrame"
                            },
                            "n": {
                                "type": "integer",
                                "default": 10,
                                "description": "Number of rows"
                            }
                        },
                        "required": ["data_ref"]
                    }
                ),
                Tool(
                    name="tail",
                    description="Get last N rows of DataFrame",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_ref": {
                                "type": "string",
                                "description": "Reference to stored DataFrame"
                            },
                            "n": {
                                "type": "integer",
                                "default": 10,
                                "description": "Number of rows"
                            }
                        },
                        "required": ["data_ref"]
                    }
                ),
                Tool(
                    name="filter",
                    description="Filter DataFrame rows by condition",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_ref": {
                                "type": "string",
                                "description": "Reference to stored DataFrame"
                            },
                            "condition": {
                                "type": "string",
                                "description": "pandas query string (e.g., 'age > 30 and city == \"NYC\"')"
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name for result data_ref"
                            }
                        },
                        "required": ["data_ref", "condition"]
                    }
                ),
                Tool(
                    name="select",
                    description="Select specific columns from DataFrame",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_ref": {
                                "type": "string",
                                "description": "Reference to stored DataFrame"
                            },
                            "columns": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of column names to select"
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name for result data_ref"
                            }
                        },
                        "required": ["data_ref", "columns"]
                    }
                ),
                Tool(
                    name="groupby",
                    description="Group DataFrame and aggregate",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_ref": {
                                "type": "string",
                                "description": "Reference to stored DataFrame"
                            },
                            "by": {
                                "oneOf": [
                                    {"type": "string"},
                                    {"type": "array", "items": {"type": "string"}}
                                ],
                                "description": "Column(s) to group by"
                            },
                            "agg": {
                                "type": "object",
                                "description": "Aggregation dict (e.g., {\"sales\": \"sum\", \"count\": \"mean\"})"
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name for result data_ref"
                            }
                        },
                        "required": ["data_ref", "by", "agg"]
                    }
                ),
                Tool(
                    name="join",
                    description="Join two DataFrames",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "left_ref": {
                                "type": "string",
                                "description": "Reference to left DataFrame"
                            },
                            "right_ref": {
                                "type": "string",
                                "description": "Reference to right DataFrame"
                            },
                            "on": {
                                "oneOf": [
                                    {"type": "string"},
                                    {"type": "array", "items": {"type": "string"}}
                                ],
                                "description": "Column(s) to join on (if same name in both)"
                            },
                            "left_on": {
                                "oneOf": [
                                    {"type": "string"},
                                    {"type": "array", "items": {"type": "string"}}
                                ],
                                "description": "Left join column(s)"
                            },
                            "right_on": {
                                "oneOf": [
                                    {"type": "string"},
                                    {"type": "array", "items": {"type": "string"}}
                                ],
                                "description": "Right join column(s)"
                            },
                            "how": {
                                "type": "string",
                                "enum": ["inner", "left", "right", "outer"],
                                "default": "inner",
                                "description": "Join type"
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name for result data_ref"
                            }
                        },
                        "required": ["left_ref", "right_ref"]
                    }
                ),
                Tool(
                    name="list_data",
                    description="List all stored DataFrames",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="drop_data",
                    description="Remove a DataFrame from storage",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_ref": {
                                "type": "string",
                                "description": "Reference to drop"
                            }
                        },
                        "required": ["data_ref"]
                    }
                ),
                # PostgreSQL tools
                Tool(
                    name="pg_connect",
                    description="Test PostgreSQL connection and return status",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="pg_query",
                    description="Execute SELECT query and return results as data_ref",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "SQL SELECT query"
                            },
                            "params": {
                                "type": "array",
                                "items": {},
                                "description": "Query parameters (use $1, $2, etc.)"
                            },
                            "name": {
                                "type": "string",
                                "description": "Optional name for result data_ref"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="pg_execute",
                    description="Execute INSERT/UPDATE/DELETE query",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "SQL DML query"
                            },
                            "params": {
                                "type": "array",
                                "items": {},
                                "description": "Query parameters"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="pg_tables",
                    description="List all tables in schema",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "schema": {
                                "type": "string",
                                "default": "public",
                                "description": "Schema name"
                            }
                        }
                    }
                ),
                Tool(
                    name="pg_columns",
                    description="Get column information for a table",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table": {
                                "type": "string",
                                "description": "Table name"
                            },
                            "schema": {
                                "type": "string",
                                "default": "public",
                                "description": "Schema name"
                            }
                        },
                        "required": ["table"]
                    }
                ),
                Tool(
                    name="pg_schemas",
                    description="List all schemas in database",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                # PostGIS tools
                Tool(
                    name="st_tables",
                    description="List PostGIS-enabled tables",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "schema": {
                                "type": "string",
                                "default": "public",
                                "description": "Schema name"
                            }
                        }
                    }
                ),
                Tool(
                    name="st_geometry_type",
                    description="Get geometry type of a column",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table": {
                                "type": "string",
                                "description": "Table name"
                            },
                            "column": {
                                "type": "string",
                                "description": "Geometry column name"
                            },
                            "schema": {
                                "type": "string",
                                "default": "public",
                                "description": "Schema name"
                            }
                        },
                        "required": ["table", "column"]
                    }
                ),
                Tool(
                    name="st_srid",
                    description="Get SRID of geometry column",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table": {
                                "type": "string",
                                "description": "Table name"
                            },
                            "column": {
                                "type": "string",
                                "description": "Geometry column name"
                            },
                            "schema": {
                                "type": "string",
                                "default": "public",
                                "description": "Schema name"
                            }
                        },
                        "required": ["table", "column"]
                    }
                ),
                Tool(
                    name="st_extent",
                    description="Get bounding box of all geometries",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table": {
                                "type": "string",
                                "description": "Table name"
                            },
                            "column": {
                                "type": "string",
                                "description": "Geometry column name"
                            },
                            "schema": {
                                "type": "string",
                                "default": "public",
                                "description": "Schema name"
                            }
                        },
                        "required": ["table", "column"]
                    }
                ),
                # dbt tools
                Tool(
                    name="dbt_parse",
                    description="Validate dbt project (pre-flight check)",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="dbt_run",
                    description="Run dbt models with pre-validation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "select": {
                                "type": "string",
                                "description": "Model selection (e.g., 'model_name', '+model_name', 'tag:daily')"
                            },
                            "exclude": {
                                "type": "string",
                                "description": "Models to exclude"
                            },
                            "full_refresh": {
                                "type": "boolean",
                                "default": False,
                                "description": "Rebuild incremental models"
                            }
                        }
                    }
                ),
                Tool(
                    name="dbt_test",
                    description="Run dbt tests",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "select": {
                                "type": "string",
                                "description": "Test selection"
                            },
                            "exclude": {
                                "type": "string",
                                "description": "Tests to exclude"
                            }
                        }
                    }
                ),
                Tool(
                    name="dbt_build",
                    description="Run dbt build (run + test) with pre-validation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "select": {
                                "type": "string",
                                "description": "Model/test selection"
                            },
                            "exclude": {
                                "type": "string",
                                "description": "Resources to exclude"
                            },
                            "full_refresh": {
                                "type": "boolean",
                                "default": False,
                                "description": "Rebuild incremental models"
                            }
                        }
                    }
                ),
                Tool(
                    name="dbt_compile",
                    description="Compile dbt models to SQL without executing",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "select": {
                                "type": "string",
                                "description": "Model selection"
                            }
                        }
                    }
                ),
                Tool(
                    name="dbt_ls",
                    description="List dbt resources",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "select": {
                                "type": "string",
                                "description": "Resource selection"
                            },
                            "resource_type": {
                                "type": "string",
                                "enum": ["model", "test", "seed", "snapshot", "source"],
                                "description": "Filter by type"
                            },
                            "output": {
                                "type": "string",
                                "enum": ["name", "path", "json"],
                                "default": "name",
                                "description": "Output format"
                            }
                        }
                    }
                ),
                Tool(
                    name="dbt_docs_generate",
                    description="Generate dbt documentation",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="dbt_lineage",
                    description="Get model dependencies and lineage",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "model": {
                                "type": "string",
                                "description": "Model name to analyze"
                            }
                        },
                        "required": ["model"]
                    }
                )
            ]
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool invocation."""
            try:
                # Route to appropriate tool handler
                # pandas tools
                if name == "read_csv":
                    result = await self.pandas_tools.read_csv(**arguments)
                elif name == "read_parquet":
                    result = await self.pandas_tools.read_parquet(**arguments)
                elif name == "read_json":
                    result = await self.pandas_tools.read_json(**arguments)
                elif name == "to_csv":
                    result = await self.pandas_tools.to_csv(**arguments)
                elif name == "to_parquet":
                    result = await self.pandas_tools.to_parquet(**arguments)
                elif name == "describe":
                    result = await self.pandas_tools.describe(**arguments)
                elif name == "head":
                    result = await self.pandas_tools.head(**arguments)
                elif name == "tail":
                    result = await self.pandas_tools.tail(**arguments)
                elif name == "filter":
                    result = await self.pandas_tools.filter(**arguments)
                elif name == "select":
                    result = await self.pandas_tools.select(**arguments)
                elif name == "groupby":
                    result = await self.pandas_tools.groupby(**arguments)
                elif name == "join":
                    result = await self.pandas_tools.join(**arguments)
                elif name == "list_data":
                    result = await self.pandas_tools.list_data()
                elif name == "drop_data":
                    result = await self.pandas_tools.drop_data(**arguments)
                # PostgreSQL tools
                elif name == "pg_connect":
                    result = await self.postgres_tools.pg_connect()
                elif name == "pg_query":
                    result = await self.postgres_tools.pg_query(**arguments)
                elif name == "pg_execute":
                    result = await self.postgres_tools.pg_execute(**arguments)
                elif name == "pg_tables":
                    result = await self.postgres_tools.pg_tables(**arguments)
                elif name == "pg_columns":
                    result = await self.postgres_tools.pg_columns(**arguments)
                elif name == "pg_schemas":
                    result = await self.postgres_tools.pg_schemas()
                # PostGIS tools
                elif name == "st_tables":
                    result = await self.postgres_tools.st_tables(**arguments)
                elif name == "st_geometry_type":
                    result = await self.postgres_tools.st_geometry_type(**arguments)
                elif name == "st_srid":
                    result = await self.postgres_tools.st_srid(**arguments)
                elif name == "st_extent":
                    result = await self.postgres_tools.st_extent(**arguments)
                # dbt tools
                elif name == "dbt_parse":
                    result = await self.dbt_tools.dbt_parse()
                elif name == "dbt_run":
                    result = await self.dbt_tools.dbt_run(**arguments)
                elif name == "dbt_test":
                    result = await self.dbt_tools.dbt_test(**arguments)
                elif name == "dbt_build":
                    result = await self.dbt_tools.dbt_build(**arguments)
                elif name == "dbt_compile":
                    result = await self.dbt_tools.dbt_compile(**arguments)
                elif name == "dbt_ls":
                    result = await self.dbt_tools.dbt_ls(**arguments)
                elif name == "dbt_docs_generate":
                    result = await self.dbt_tools.dbt_docs_generate()
                elif name == "dbt_lineage":
                    result = await self.dbt_tools.dbt_lineage(**arguments)
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
    server = DataPlatformMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
