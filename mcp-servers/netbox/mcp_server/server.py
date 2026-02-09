"""
MCP Server entry point for NetBox integration.

Provides essential NetBox tools to Claude Code via JSON-RPC 2.0 over stdio.
Covers DCIM, IPAM, Virtualization, and Extras modules.
"""
import asyncio
import logging
import json
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import NetBoxConfig
from .netbox_client import NetBoxClient
from .tools.dcim import DCIMTools
from .tools.ipam import IPAMTools
from .tools.virtualization import VirtualizationTools
from .tools.extras import ExtrasTools

# Suppress noisy MCP validation warnings on stderr
logging.basicConfig(level=logging.INFO)
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


# Tool definitions - 37 essential tools for tracking servers, services, IPs, and databases
TOOL_DEFINITIONS = {
    # ==================== DCIM: Servers, Sites, Interfaces ====================
    'dcim_list_sites': {
        'description': 'List all sites in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'status': {'type': 'string', 'description': 'Filter by status'},
        }
    },
    'dcim_get_site': {
        'description': 'Get a specific site by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Site ID'}},
        'required': ['id']
    },
    'dcim_create_site': {
        'description': 'Create a new site',
        'properties': {
            'name': {'type': 'string', 'description': 'Site name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'status': {'type': 'string', 'description': 'Status'},
        },
        'required': ['name', 'slug']
    },
    'dcim_update_site': {
        'description': 'Update an existing site',
        'properties': {
            'id': {'type': 'integer', 'description': 'Site ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'status': {'type': 'string', 'description': 'New status'},
        },
        'required': ['id']
    },
    'dcim_list_devices': {
        'description': 'List all devices (servers/VPS) in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'site_id': {'type': 'integer', 'description': 'Filter by site'},
            'status': {'type': 'string', 'description': 'Filter by status'},
            'role_id': {'type': 'integer', 'description': 'Filter by role'},
        }
    },
    'dcim_get_device': {
        'description': 'Get a specific device by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Device ID'}},
        'required': ['id']
    },
    'dcim_create_device': {
        'description': 'Create a new device',
        'properties': {
            'name': {'type': 'string', 'description': 'Device name'},
            'device_type': {'type': 'integer', 'description': 'Device type ID'},
            'role': {'type': 'integer', 'description': 'Device role ID'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'status': {'type': 'string', 'description': 'Status'},
        },
        'required': ['name', 'device_type', 'role', 'site']
    },
    'dcim_update_device': {
        'description': 'Update an existing device',
        'properties': {
            'id': {'type': 'integer', 'description': 'Device ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'status': {'type': 'string', 'description': 'New status'},
        },
        'required': ['id']
    },
    'dcim_list_interfaces': {
        'description': 'List device interfaces',
        'properties': {
            'device_id': {'type': 'integer', 'description': 'Filter by device'},
            'name': {'type': 'string', 'description': 'Filter by name'},
            'type': {'type': 'string', 'description': 'Filter by type'},
        }
    },
    'dcim_get_interface': {
        'description': 'Get a specific interface by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Interface ID'}},
        'required': ['id']
    },
    'dcim_create_interface': {
        'description': 'Create a new interface on a device',
        'properties': {
            'device': {'type': 'integer', 'description': 'Device ID'},
            'name': {'type': 'string', 'description': 'Interface name'},
            'type': {'type': 'string', 'description': 'Interface type'},
        },
        'required': ['device', 'name', 'type']
    },

    # ==================== IPAM: IPs, Prefixes, Services ====================
    'ipam_list_ip_addresses': {
        'description': 'List IP addresses',
        'properties': {
            'address': {'type': 'string', 'description': 'Filter by address'},
            'device_id': {'type': 'integer', 'description': 'Filter by device'},
            'status': {'type': 'string', 'description': 'Filter by status'},
        }
    },
    'ipam_get_ip_address': {
        'description': 'Get a specific IP address by ID',
        'properties': {'id': {'type': 'integer', 'description': 'IP address ID'}},
        'required': ['id']
    },
    'ipam_create_ip_address': {
        'description': 'Create an IP address',
        'properties': {
            'address': {'type': 'string', 'description': 'IP address with prefix (e.g., 192.168.1.1/24)'},
            'status': {'type': 'string', 'description': 'Status'},
            'assigned_object_type': {'type': 'string', 'description': 'Object type (dcim.interface or virtualization.vminterface)'},
            'assigned_object_id': {'type': 'integer', 'description': 'Object ID'},
        },
        'required': ['address']
    },
    'ipam_update_ip_address': {
        'description': 'Update an IP address',
        'properties': {
            'id': {'type': 'integer', 'description': 'IP address ID'},
            'status': {'type': 'string', 'description': 'New status'},
        },
        'required': ['id']
    },
    'ipam_list_prefixes': {
        'description': 'List IP prefixes',
        'properties': {
            'prefix': {'type': 'string', 'description': 'Filter by prefix'},
            'site_id': {'type': 'integer', 'description': 'Filter by site'},
            'status': {'type': 'string', 'description': 'Filter by status'},
        }
    },
    'ipam_get_prefix': {
        'description': 'Get a specific prefix by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Prefix ID'}},
        'required': ['id']
    },
    'ipam_create_prefix': {
        'description': 'Create an IP prefix',
        'properties': {
            'prefix': {'type': 'string', 'description': 'IP prefix (e.g., 192.168.1.0/24)'},
            'status': {'type': 'string', 'description': 'Status'},
            'site': {'type': 'integer', 'description': 'Site ID'},
        },
        'required': ['prefix']
    },
    'ipam_list_services': {
        'description': 'List services (applications, databases, etc.)',
        'properties': {
            'device_id': {'type': 'integer', 'description': 'Filter by device'},
            'virtual_machine_id': {'type': 'integer', 'description': 'Filter by VM'},
            'name': {'type': 'string', 'description': 'Filter by name'},
        }
    },
    'ipam_get_service': {
        'description': 'Get a specific service by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Service ID'}},
        'required': ['id']
    },
    'ipam_create_service': {
        'description': 'Create a service (app, database, etc.)',
        'properties': {
            'name': {'type': 'string', 'description': 'Service name'},
            'ports': {'type': 'array', 'description': 'Port numbers', 'items': {'type': 'integer'}},
            'protocol': {'type': 'string', 'description': 'Protocol (tcp/udp)'},
            'device': {'type': 'integer', 'description': 'Device ID (if on physical server)'},
            'virtual_machine': {'type': 'integer', 'description': 'VM ID (if on VM)'},
        },
        'required': ['name', 'ports', 'protocol']
    },

    # ==================== Virtualization: VMs, Clusters ====================
    'virt_list_clusters': {
        'description': 'List virtualization clusters',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'site_id': {'type': 'integer', 'description': 'Filter by site'},
        }
    },
    'virt_get_cluster': {
        'description': 'Get a specific cluster by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Cluster ID'}},
        'required': ['id']
    },
    'virt_create_cluster': {
        'description': 'Create a virtualization cluster',
        'properties': {
            'name': {'type': 'string', 'description': 'Cluster name'},
            'type': {'type': 'integer', 'description': 'Cluster type ID'},
            'site': {'type': 'integer', 'description': 'Site ID'},
        },
        'required': ['name', 'type']
    },
    'virt_list_vms': {
        'description': 'List virtual machines',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'cluster_id': {'type': 'integer', 'description': 'Filter by cluster'},
            'site_id': {'type': 'integer', 'description': 'Filter by site'},
            'status': {'type': 'string', 'description': 'Filter by status'},
        }
    },
    'virt_get_vm': {
        'description': 'Get a specific VM by ID',
        'properties': {'id': {'type': 'integer', 'description': 'VM ID'}},
        'required': ['id']
    },
    'virt_create_vm': {
        'description': 'Create a virtual machine',
        'properties': {
            'name': {'type': 'string', 'description': 'VM name'},
            'cluster': {'type': 'integer', 'description': 'Cluster ID'},
            'status': {'type': 'string', 'description': 'Status'},
            'vcpus': {'type': 'number', 'description': 'vCPU count'},
            'memory': {'type': 'integer', 'description': 'Memory in MB'},
            'disk': {'type': 'integer', 'description': 'Disk in GB'},
        },
        'required': ['name', 'cluster']
    },
    'virt_update_vm': {
        'description': 'Update a virtual machine',
        'properties': {
            'id': {'type': 'integer', 'description': 'VM ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'status': {'type': 'string', 'description': 'New status'},
        },
        'required': ['id']
    },
    'virt_list_vm_ifaces': {
        'description': 'List VM interfaces',
        'properties': {
            'virtual_machine_id': {'type': 'integer', 'description': 'Filter by VM'},
        }
    },
    'virt_get_vm_iface': {
        'description': 'Get a specific VM interface by ID',
        'properties': {'id': {'type': 'integer', 'description': 'VM interface ID'}},
        'required': ['id']
    },
    'virt_create_vm_iface': {
        'description': 'Create a VM interface',
        'properties': {
            'virtual_machine': {'type': 'integer', 'description': 'VM ID'},
            'name': {'type': 'string', 'description': 'Interface name'},
        },
        'required': ['virtual_machine', 'name']
    },

    # ==================== Extras: Tags, Journal Entries ====================
    'extras_list_tags': {
        'description': 'List all tags in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
        }
    },
    'extras_get_tag': {
        'description': 'Get a specific tag by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Tag ID'}},
        'required': ['id']
    },
    'extras_create_tag': {
        'description': 'Create a new tag',
        'properties': {
            'name': {'type': 'string', 'description': 'Tag name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'color': {'type': 'string', 'description': 'Hex color code'},
        },
        'required': ['name', 'slug']
    },
    'extras_list_journal_entries': {
        'description': 'List journal entries (audit/notes)',
        'properties': {
            'assigned_object_type': {'type': 'string', 'description': 'Object type'},
            'assigned_object_id': {'type': 'integer', 'description': 'Object ID'},
        }
    },
    'extras_get_journal_entry': {
        'description': 'Get a specific journal entry by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Entry ID'}},
        'required': ['id']
    },
    'extras_create_journal_entry': {
        'description': 'Create a journal entry',
        'properties': {
            'assigned_object_type': {'type': 'string', 'description': 'Object type (e.g., dcim.device)'},
            'assigned_object_id': {'type': 'integer', 'description': 'Object ID'},
            'comments': {'type': 'string', 'description': 'Journal entry text'},
            'kind': {'type': 'string', 'description': 'Kind (info, success, warning, danger)'},
        },
        'required': ['assigned_object_type', 'assigned_object_id', 'comments']
    },
}


# Tool name mappings for shortened virtualization tools (virt_ prefix)
TOOL_NAME_MAP = {
    # Virtualization tools (virt_ prefix -> virtualization category)
    'virt_list_clusters': ('virtualization', 'list_clusters'),
    'virt_get_cluster': ('virtualization', 'get_cluster'),
    'virt_create_cluster': ('virtualization', 'create_cluster'),
    'virt_list_vms': ('virtualization', 'list_virtual_machines'),
    'virt_get_vm': ('virtualization', 'get_virtual_machine'),
    'virt_create_vm': ('virtualization', 'create_virtual_machine'),
    'virt_update_vm': ('virtualization', 'update_virtual_machine'),
    'virt_list_vm_ifaces': ('virtualization', 'list_vm_interfaces'),
    'virt_get_vm_iface': ('virtualization', 'get_vm_interface'),
    'virt_create_vm_iface': ('virtualization', 'create_vm_interface'),
}


class NetBoxMCPServer:
    """MCP Server for NetBox integration"""

    def __init__(self):
        self.server = Server("netbox-mcp")
        self.config = None
        self.client = None
        # Tool instances - always instantiate all 4 modules
        self.dcim_tools = None
        self.ipam_tools = None
        self.virtualization_tools = None
        self.extras_tools = None

    async def initialize(self):
        """Initialize server and load configuration."""
        try:
            config_loader = NetBoxConfig()
            self.config = config_loader.load()

            self.client = NetBoxClient()

            # Always instantiate all 4 modules
            self.dcim_tools = DCIMTools(self.client)
            self.ipam_tools = IPAMTools(self.client)
            self.virtualization_tools = VirtualizationTools(self.client)
            self.extras_tools = ExtrasTools(self.client)

            tool_count = len(TOOL_DEFINITIONS)
            logger.info(
                f"NetBox MCP Server initialized: {tool_count} tools registered "
                f"(modules: dcim, ipam, virtualization, extras)"
            )
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise

    def setup_tools(self):
        """Register all available tools with the MCP server"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
            tools = []
            for name, definition in TOOL_DEFINITIONS.items():
                tools.append(Tool(
                    name=name,
                    description=definition['description'],
                    inputSchema={
                        'type': 'object',
                        'properties': definition.get('properties', {}),
                        'required': definition.get('required', [])
                    }
                ))
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool invocation."""
            try:
                result = await self._route_tool(name, arguments)
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, default=str)
                )]
            except Exception as e:
                logger.error(f"Tool {name} failed: {e}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

    async def _route_tool(self, name: str, arguments: dict):
        """Route tool call to appropriate handler.

        Tool names may be shortened (e.g., 'virt_list_vms' instead of
        'virtualization_list_virtual_machines') to meet the 28-character
        limit. TOOL_NAME_MAP handles the translation to actual method names.
        """
        # Check if this is a mapped short name
        if name in TOOL_NAME_MAP:
            category, method_name = TOOL_NAME_MAP[name]
        else:
            # Fall back to original logic for unchanged tools
            parts = name.split('_', 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid tool name format: {name}")
            category, method_name = parts[0], parts[1]

        # Map category to tool class
        tool_map = {
            'dcim': self.dcim_tools,
            'ipam': self.ipam_tools,
            'virtualization': self.virtualization_tools,
            'extras': self.extras_tools
        }

        tool_class = tool_map.get(category)
        if not tool_class:
            raise ValueError(f"Unknown tool category: {category}")

        # Get the method
        method = getattr(tool_class, method_name, None)
        if not method:
            raise ValueError(f"Unknown method: {method_name} in {category}")

        # Call the method
        return await method(**arguments)

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
    server = NetBoxMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
