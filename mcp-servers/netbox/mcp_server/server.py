"""
MCP Server entry point for NetBox integration.

Provides comprehensive NetBox tools to Claude Code via JSON-RPC 2.0 over stdio.
Covers the entire NetBox REST API: DCIM, IPAM, Circuits, Virtualization,
Tenancy, VPN, Wireless, and Extras.
"""
import asyncio
import logging
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import NetBoxConfig
from .netbox_client import NetBoxClient
from .tools.dcim import DCIMTools
from .tools.ipam import IPAMTools
from .tools.circuits import CircuitsTools
from .tools.virtualization import VirtualizationTools
from .tools.tenancy import TenancyTools
from .tools.vpn import VPNTools
from .tools.wireless import WirelessTools
from .tools.extras import ExtrasTools

# Suppress noisy MCP validation warnings on stderr
logging.basicConfig(level=logging.INFO)
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


# Tool definitions organized by category
TOOL_DEFINITIONS = {
    # ==================== DCIM Tools ====================
    'dcim_list_regions': {
        'description': 'List all regions in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'slug': {'type': 'string', 'description': 'Filter by slug'}
        }
    },
    'dcim_get_region': {
        'description': 'Get a specific region by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Region ID'}},
        'required': ['id']
    },
    'dcim_create_region': {
        'description': 'Create a new region',
        'properties': {
            'name': {'type': 'string', 'description': 'Region name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'parent': {'type': 'integer', 'description': 'Parent region ID'}
        },
        'required': ['name', 'slug']
    },
    'dcim_update_region': {
        'description': 'Update an existing region',
        'properties': {
            'id': {'type': 'integer', 'description': 'Region ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'slug': {'type': 'string', 'description': 'New slug'}
        },
        'required': ['id']
    },
    'dcim_delete_region': {
        'description': 'Delete a region',
        'properties': {'id': {'type': 'integer', 'description': 'Region ID'}},
        'required': ['id']
    },
    'dcim_list_sites': {
        'description': 'List all sites in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'status': {'type': 'string', 'description': 'Filter by status (active, planned, staging, decommissioning, retired)'},
            'region_id': {'type': 'integer', 'description': 'Filter by region ID'},
            'tenant_id': {'type': 'integer', 'description': 'Filter by tenant ID'}
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
            'status': {'type': 'string', 'description': 'Site status'},
            'region': {'type': 'integer', 'description': 'Region ID'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'},
            'facility': {'type': 'string', 'description': 'Facility name'},
            'time_zone': {'type': 'string', 'description': 'Time zone'},
            'description': {'type': 'string', 'description': 'Description'},
            'physical_address': {'type': 'string', 'description': 'Physical address'},
            'shipping_address': {'type': 'string', 'description': 'Shipping address'}
        },
        'required': ['name', 'slug']
    },
    'dcim_update_site': {
        'description': 'Update an existing site',
        'properties': {
            'id': {'type': 'integer', 'description': 'Site ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'slug': {'type': 'string', 'description': 'New slug'},
            'status': {'type': 'string', 'description': 'Status'},
            'region': {'type': 'integer', 'description': 'Region ID'},
            'group': {'type': 'integer', 'description': 'Site group ID'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'},
            'facility': {'type': 'string', 'description': 'Facility name'},
            'time_zone': {'type': 'string', 'description': 'Time zone'},
            'description': {'type': 'string', 'description': 'Description'},
            'physical_address': {'type': 'string', 'description': 'Physical address'},
            'shipping_address': {'type': 'string', 'description': 'Shipping address'},
            'latitude': {'type': 'number', 'description': 'Latitude'},
            'longitude': {'type': 'number', 'description': 'Longitude'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['id']
    },
    'dcim_delete_site': {
        'description': 'Delete a site',
        'properties': {'id': {'type': 'integer', 'description': 'Site ID'}},
        'required': ['id']
    },
    'dcim_list_locations': {
        'description': 'List all locations in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'site_id': {'type': 'integer', 'description': 'Filter by site ID'}
        }
    },
    'dcim_get_location': {
        'description': 'Get a specific location by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Location ID'}},
        'required': ['id']
    },
    'dcim_create_location': {
        'description': 'Create a new location',
        'properties': {
            'name': {'type': 'string', 'description': 'Location name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'parent': {'type': 'integer', 'description': 'Parent location ID'}
        },
        'required': ['name', 'slug', 'site']
    },
    'dcim_update_location': {
        'description': 'Update an existing location',
        'properties': {
            'id': {'type': 'integer', 'description': 'Location ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'slug': {'type': 'string', 'description': 'New slug'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'parent': {'type': 'integer', 'description': 'Parent location ID'},
            'description': {'type': 'string', 'description': 'Description'}
        },
        'required': ['id']
    },
    'dcim_delete_location': {
        'description': 'Delete a location',
        'properties': {'id': {'type': 'integer', 'description': 'Location ID'}},
        'required': ['id']
    },
    'dcim_list_racks': {
        'description': 'List all racks in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'site_id': {'type': 'integer', 'description': 'Filter by site ID'},
            'location_id': {'type': 'integer', 'description': 'Filter by location ID'},
            'status': {'type': 'string', 'description': 'Filter by status'}
        }
    },
    'dcim_get_rack': {
        'description': 'Get a specific rack by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Rack ID'}},
        'required': ['id']
    },
    'dcim_create_rack': {
        'description': 'Create a new rack',
        'properties': {
            'name': {'type': 'string', 'description': 'Rack name'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'location': {'type': 'integer', 'description': 'Location ID'},
            'status': {'type': 'string', 'description': 'Rack status'},
            'u_height': {'type': 'integer', 'description': 'Rack height in U'}
        },
        'required': ['name', 'site']
    },
    'dcim_update_rack': {
        'description': 'Update an existing rack',
        'properties': {
            'id': {'type': 'integer', 'description': 'Rack ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'location': {'type': 'integer', 'description': 'Location ID'},
            'status': {'type': 'string', 'description': 'Status'},
            'role': {'type': 'integer', 'description': 'Role ID'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'},
            'u_height': {'type': 'integer', 'description': 'Rack height in U'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['id']
    },
    'dcim_delete_rack': {
        'description': 'Delete a rack',
        'properties': {'id': {'type': 'integer', 'description': 'Rack ID'}},
        'required': ['id']
    },
    'dcim_list_manufacturers': {
        'description': 'List all manufacturers in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'dcim_get_manufacturer': {
        'description': 'Get a specific manufacturer by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Manufacturer ID'}},
        'required': ['id']
    },
    'dcim_create_manufacturer': {
        'description': 'Create a new manufacturer',
        'properties': {
            'name': {'type': 'string', 'description': 'Manufacturer name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'}
        },
        'required': ['name', 'slug']
    },
    'dcim_update_manufacturer': {
        'description': 'Update an existing manufacturer',
        'properties': {
            'id': {'type': 'integer', 'description': 'Manufacturer ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'slug': {'type': 'string', 'description': 'New slug'},
            'description': {'type': 'string', 'description': 'Description'}
        },
        'required': ['id']
    },
    'dcim_delete_manufacturer': {
        'description': 'Delete a manufacturer',
        'properties': {'id': {'type': 'integer', 'description': 'Manufacturer ID'}},
        'required': ['id']
    },
    'dcim_list_device_types': {
        'description': 'List all device types in NetBox',
        'properties': {
            'manufacturer_id': {'type': 'integer', 'description': 'Filter by manufacturer ID'},
            'model': {'type': 'string', 'description': 'Filter by model name'}
        }
    },
    'dcim_get_device_type': {
        'description': 'Get a specific device type by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Device type ID'}},
        'required': ['id']
    },
    'dcim_create_device_type': {
        'description': 'Create a new device type',
        'properties': {
            'manufacturer': {'type': 'integer', 'description': 'Manufacturer ID'},
            'model': {'type': 'string', 'description': 'Model name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'u_height': {'type': 'number', 'description': 'Height in rack units'}
        },
        'required': ['manufacturer', 'model', 'slug']
    },
    'dcim_update_device_type': {
        'description': 'Update an existing device type',
        'properties': {
            'id': {'type': 'integer', 'description': 'Device type ID'},
            'manufacturer': {'type': 'integer', 'description': 'Manufacturer ID'},
            'model': {'type': 'string', 'description': 'Model name'},
            'slug': {'type': 'string', 'description': 'New slug'},
            'u_height': {'type': 'number', 'description': 'Height in rack units'},
            'is_full_depth': {'type': 'boolean', 'description': 'Is full depth'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['id']
    },
    'dcim_delete_device_type': {
        'description': 'Delete a device type',
        'properties': {'id': {'type': 'integer', 'description': 'Device type ID'}},
        'required': ['id']
    },
    'dcim_list_device_roles': {
        'description': 'List all device roles in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'dcim_get_device_role': {
        'description': 'Get a specific device role by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Device role ID'}},
        'required': ['id']
    },
    'dcim_create_device_role': {
        'description': 'Create a new device role',
        'properties': {
            'name': {'type': 'string', 'description': 'Role name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'color': {'type': 'string', 'description': 'Hex color code'},
            'vm_role': {'type': 'boolean', 'description': 'Can be assigned to VMs'}
        },
        'required': ['name', 'slug']
    },
    'dcim_update_device_role': {
        'description': 'Update an existing device role',
        'properties': {
            'id': {'type': 'integer', 'description': 'Device role ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'slug': {'type': 'string', 'description': 'New slug'},
            'color': {'type': 'string', 'description': 'Hex color code'},
            'vm_role': {'type': 'boolean', 'description': 'Can be assigned to VMs'},
            'description': {'type': 'string', 'description': 'Description'}
        },
        'required': ['id']
    },
    'dcim_delete_device_role': {
        'description': 'Delete a device role',
        'properties': {'id': {'type': 'integer', 'description': 'Device role ID'}},
        'required': ['id']
    },
    'dcim_list_platforms': {
        'description': 'List all platforms in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'manufacturer_id': {'type': 'integer', 'description': 'Filter by manufacturer ID'}
        }
    },
    'dcim_get_platform': {
        'description': 'Get a specific platform by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Platform ID'}},
        'required': ['id']
    },
    'dcim_create_platform': {
        'description': 'Create a new platform',
        'properties': {
            'name': {'type': 'string', 'description': 'Platform name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'manufacturer': {'type': 'integer', 'description': 'Manufacturer ID'}
        },
        'required': ['name', 'slug']
    },
    'dcim_update_platform': {
        'description': 'Update an existing platform',
        'properties': {
            'id': {'type': 'integer', 'description': 'Platform ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'slug': {'type': 'string', 'description': 'New slug'},
            'manufacturer': {'type': 'integer', 'description': 'Manufacturer ID'},
            'description': {'type': 'string', 'description': 'Description'}
        },
        'required': ['id']
    },
    'dcim_delete_platform': {
        'description': 'Delete a platform',
        'properties': {'id': {'type': 'integer', 'description': 'Platform ID'}},
        'required': ['id']
    },
    'dcim_list_devices': {
        'description': 'List all devices in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'site_id': {'type': 'integer', 'description': 'Filter by site ID'},
            'rack_id': {'type': 'integer', 'description': 'Filter by rack ID'},
            'status': {'type': 'string', 'description': 'Filter by status'},
            'role_id': {'type': 'integer', 'description': 'Filter by role ID'},
            'device_type_id': {'type': 'integer', 'description': 'Filter by device type ID'},
            'manufacturer_id': {'type': 'integer', 'description': 'Filter by manufacturer ID'},
            'serial': {'type': 'string', 'description': 'Filter by serial number'}
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
            'status': {'type': 'string', 'description': 'Device status'},
            'rack': {'type': 'integer', 'description': 'Rack ID'},
            'position': {'type': 'number', 'description': 'Position in rack'},
            'serial': {'type': 'string', 'description': 'Serial number'},
            'platform': {'type': 'integer', 'description': 'Platform ID'},
            'primary_ip4': {'type': 'integer', 'description': 'Primary IPv4 address ID'},
            'primary_ip6': {'type': 'integer', 'description': 'Primary IPv6 address ID'},
            'asset_tag': {'type': 'string', 'description': 'Asset tag'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['name', 'device_type', 'role', 'site']
    },
    'dcim_update_device': {
        'description': 'Update an existing device',
        'properties': {
            'id': {'type': 'integer', 'description': 'Device ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'status': {'type': 'string', 'description': 'New status'},
            'platform': {'type': 'integer', 'description': 'Platform ID'},
            'primary_ip4': {'type': 'integer', 'description': 'Primary IPv4 address ID'},
            'primary_ip6': {'type': 'integer', 'description': 'Primary IPv6 address ID'},
            'serial': {'type': 'string', 'description': 'Serial number'},
            'asset_tag': {'type': 'string', 'description': 'Asset tag'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'rack': {'type': 'integer', 'description': 'Rack ID'},
            'position': {'type': 'number', 'description': 'Position in rack'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['id']
    },
    'dcim_delete_device': {
        'description': 'Delete a device',
        'properties': {'id': {'type': 'integer', 'description': 'Device ID'}},
        'required': ['id']
    },
    'dcim_list_interfaces': {
        'description': 'List all device interfaces in NetBox',
        'properties': {
            'device_id': {'type': 'integer', 'description': 'Filter by device ID'},
            'name': {'type': 'string', 'description': 'Filter by name'},
            'type': {'type': 'string', 'description': 'Filter by interface type'}
        }
    },
    'dcim_get_interface': {
        'description': 'Get a specific interface by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Interface ID'}},
        'required': ['id']
    },
    'dcim_create_interface': {
        'description': 'Create a new device interface',
        'properties': {
            'device': {'type': 'integer', 'description': 'Device ID'},
            'name': {'type': 'string', 'description': 'Interface name'},
            'type': {'type': 'string', 'description': 'Interface type (e.g., 1000base-t, 10gbase-x-sfpp)'},
            'enabled': {'type': 'boolean', 'description': 'Interface enabled'},
            'mac_address': {'type': 'string', 'description': 'MAC address'}
        },
        'required': ['device', 'name', 'type']
    },
    'dcim_update_interface': {
        'description': 'Update an existing interface',
        'properties': {
            'id': {'type': 'integer', 'description': 'Interface ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'type': {'type': 'string', 'description': 'Interface type'},
            'enabled': {'type': 'boolean', 'description': 'Interface enabled'},
            'mtu': {'type': 'integer', 'description': 'MTU'},
            'mac_address': {'type': 'string', 'description': 'MAC address'},
            'description': {'type': 'string', 'description': 'Description'},
            'mode': {'type': 'string', 'description': 'VLAN mode'},
            'untagged_vlan': {'type': 'integer', 'description': 'Untagged VLAN ID'},
            'tagged_vlans': {'type': 'array', 'description': 'Tagged VLAN IDs'}
        },
        'required': ['id']
    },
    'dcim_delete_interface': {
        'description': 'Delete an interface',
        'properties': {'id': {'type': 'integer', 'description': 'Interface ID'}},
        'required': ['id']
    },
    'dcim_list_cables': {
        'description': 'List all cables in NetBox',
        'properties': {
            'site_id': {'type': 'integer', 'description': 'Filter by site ID'},
            'device_id': {'type': 'integer', 'description': 'Filter by device ID'},
            'status': {'type': 'string', 'description': 'Filter by status'}
        }
    },
    'dcim_get_cable': {
        'description': 'Get a specific cable by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Cable ID'}},
        'required': ['id']
    },
    'dcim_create_cable': {
        'description': 'Create a new cable connection',
        'properties': {
            'a_terminations': {'type': 'array', 'description': 'A-side terminations [{object_type, object_id}]'},
            'b_terminations': {'type': 'array', 'description': 'B-side terminations [{object_type, object_id}]'},
            'type': {'type': 'string', 'description': 'Cable type'},
            'status': {'type': 'string', 'description': 'Cable status'},
            'label': {'type': 'string', 'description': 'Cable label'}
        },
        'required': ['a_terminations', 'b_terminations']
    },
    'dcim_update_cable': {
        'description': 'Update an existing cable',
        'properties': {
            'id': {'type': 'integer', 'description': 'Cable ID'},
            'type': {'type': 'string', 'description': 'Cable type'},
            'status': {'type': 'string', 'description': 'Cable status'},
            'label': {'type': 'string', 'description': 'Cable label'},
            'color': {'type': 'string', 'description': 'Cable color'},
            'length': {'type': 'number', 'description': 'Cable length'},
            'length_unit': {'type': 'string', 'description': 'Length unit'}
        },
        'required': ['id']
    },
    'dcim_delete_cable': {
        'description': 'Delete a cable',
        'properties': {'id': {'type': 'integer', 'description': 'Cable ID'}},
        'required': ['id']
    },
    'dcim_list_power_panels': {
        'description': 'List all power panels in NetBox',
        'properties': {'site_id': {'type': 'integer', 'description': 'Filter by site ID'}}
    },
    'dcim_get_power_panel': {
        'description': 'Get a specific power panel by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Power panel ID'}},
        'required': ['id']
    },
    'dcim_create_power_panel': {
        'description': 'Create a new power panel',
        'properties': {
            'site': {'type': 'integer', 'description': 'Site ID'},
            'name': {'type': 'string', 'description': 'Panel name'},
            'location': {'type': 'integer', 'description': 'Location ID'}
        },
        'required': ['site', 'name']
    },
    'dcim_list_power_feeds': {
        'description': 'List all power feeds in NetBox',
        'properties': {'power_panel_id': {'type': 'integer', 'description': 'Filter by power panel ID'}}
    },
    'dcim_get_power_feed': {
        'description': 'Get a specific power feed by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Power feed ID'}},
        'required': ['id']
    },
    'dcim_create_power_feed': {
        'description': 'Create a new power feed',
        'properties': {
            'power_panel': {'type': 'integer', 'description': 'Power panel ID'},
            'name': {'type': 'string', 'description': 'Feed name'},
            'voltage': {'type': 'integer', 'description': 'Voltage'},
            'amperage': {'type': 'integer', 'description': 'Amperage'}
        },
        'required': ['power_panel', 'name']
    },
    'dcim_list_virtual_chassis': {
        'description': 'List all virtual chassis in NetBox',
        'properties': {}
    },
    'dcim_get_virtual_chassis': {
        'description': 'Get a specific virtual chassis by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Virtual chassis ID'}},
        'required': ['id']
    },
    'dcim_list_inventory_items': {
        'description': 'List all inventory items in NetBox',
        'properties': {'device_id': {'type': 'integer', 'description': 'Filter by device ID'}}
    },
    'dcim_get_inventory_item': {
        'description': 'Get a specific inventory item by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Inventory item ID'}},
        'required': ['id']
    },

    # ==================== IPAM Tools ====================
    'ipam_list_vrfs': {
        'description': 'List all VRFs in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'rd': {'type': 'string', 'description': 'Filter by route distinguisher'}
        }
    },
    'ipam_get_vrf': {
        'description': 'Get a specific VRF by ID',
        'properties': {'id': {'type': 'integer', 'description': 'VRF ID'}},
        'required': ['id']
    },
    'ipam_create_vrf': {
        'description': 'Create a new VRF',
        'properties': {
            'name': {'type': 'string', 'description': 'VRF name'},
            'rd': {'type': 'string', 'description': 'Route distinguisher'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'}
        },
        'required': ['name']
    },
    'ipam_update_vrf': {
        'description': 'Update an existing VRF',
        'properties': {
            'id': {'type': 'integer', 'description': 'VRF ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'rd': {'type': 'string', 'description': 'Route distinguisher'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'},
            'enforce_unique': {'type': 'boolean', 'description': 'Enforce unique IPs'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['id']
    },
    'ipam_delete_vrf': {
        'description': 'Delete a VRF',
        'properties': {'id': {'type': 'integer', 'description': 'VRF ID'}},
        'required': ['id']
    },
    'ipam_list_prefixes': {
        'description': 'List all IP prefixes in NetBox',
        'properties': {
            'prefix': {'type': 'string', 'description': 'Filter by prefix (CIDR)'},
            'site_id': {'type': 'integer', 'description': 'Filter by site ID'},
            'vrf_id': {'type': 'integer', 'description': 'Filter by VRF ID'},
            'vlan_id': {'type': 'integer', 'description': 'Filter by VLAN ID'},
            'status': {'type': 'string', 'description': 'Filter by status'},
            'within': {'type': 'string', 'description': 'Find prefixes within this prefix'}
        }
    },
    'ipam_get_prefix': {
        'description': 'Get a specific prefix by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Prefix ID'}},
        'required': ['id']
    },
    'ipam_create_prefix': {
        'description': 'Create a new IP prefix',
        'properties': {
            'prefix': {'type': 'string', 'description': 'Prefix in CIDR notation'},
            'status': {'type': 'string', 'description': 'Status (active, container, reserved, deprecated)'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'vrf': {'type': 'integer', 'description': 'VRF ID'},
            'vlan': {'type': 'integer', 'description': 'VLAN ID'},
            'role': {'type': 'integer', 'description': 'Role ID'},
            'is_pool': {'type': 'boolean', 'description': 'Is a pool'}
        },
        'required': ['prefix']
    },
    'ipam_update_prefix': {
        'description': 'Update an existing prefix',
        'properties': {
            'id': {'type': 'integer', 'description': 'Prefix ID'},
            'prefix': {'type': 'string', 'description': 'Prefix in CIDR notation'},
            'status': {'type': 'string', 'description': 'Status'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'vrf': {'type': 'integer', 'description': 'VRF ID'},
            'vlan': {'type': 'integer', 'description': 'VLAN ID'},
            'role': {'type': 'integer', 'description': 'Role ID'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'},
            'is_pool': {'type': 'boolean', 'description': 'Is a pool'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['id']
    },
    'ipam_delete_prefix': {
        'description': 'Delete a prefix',
        'properties': {'id': {'type': 'integer', 'description': 'Prefix ID'}},
        'required': ['id']
    },
    'ipam_list_available_prefixes': {
        'description': 'List available child prefixes within a prefix',
        'properties': {'id': {'type': 'integer', 'description': 'Parent prefix ID'}},
        'required': ['id']
    },
    'ipam_create_available_prefix': {
        'description': 'Create a new prefix from available space',
        'properties': {
            'id': {'type': 'integer', 'description': 'Parent prefix ID'},
            'prefix_length': {'type': 'integer', 'description': 'Desired prefix length'}
        },
        'required': ['id', 'prefix_length']
    },
    'ipam_list_ip_addresses': {
        'description': 'List all IP addresses in NetBox',
        'properties': {
            'address': {'type': 'string', 'description': 'Filter by address'},
            'vrf_id': {'type': 'integer', 'description': 'Filter by VRF ID'},
            'device_id': {'type': 'integer', 'description': 'Filter by device ID'},
            'virtual_machine_id': {'type': 'integer', 'description': 'Filter by VM ID'},
            'status': {'type': 'string', 'description': 'Filter by status'},
            'dns_name': {'type': 'string', 'description': 'Filter by DNS name'}
        }
    },
    'ipam_get_ip_address': {
        'description': 'Get a specific IP address by ID',
        'properties': {'id': {'type': 'integer', 'description': 'IP address ID'}},
        'required': ['id']
    },
    'ipam_create_ip_address': {
        'description': 'Create a new IP address',
        'properties': {
            'address': {'type': 'string', 'description': 'IP address with prefix length'},
            'status': {'type': 'string', 'description': 'Status'},
            'vrf': {'type': 'integer', 'description': 'VRF ID'},
            'dns_name': {'type': 'string', 'description': 'DNS name'},
            'assigned_object_type': {'type': 'string', 'description': 'Object type to assign to'},
            'assigned_object_id': {'type': 'integer', 'description': 'Object ID to assign to'}
        },
        'required': ['address']
    },
    'ipam_update_ip_address': {
        'description': 'Update an existing IP address',
        'properties': {
            'id': {'type': 'integer', 'description': 'IP address ID'},
            'address': {'type': 'string', 'description': 'IP address with prefix length'},
            'status': {'type': 'string', 'description': 'Status'},
            'vrf': {'type': 'integer', 'description': 'VRF ID'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'},
            'dns_name': {'type': 'string', 'description': 'DNS name'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'},
            'assigned_object_type': {'type': 'string', 'description': 'Object type to assign to'},
            'assigned_object_id': {'type': 'integer', 'description': 'Object ID to assign to'}
        },
        'required': ['id']
    },
    'ipam_delete_ip_address': {
        'description': 'Delete an IP address',
        'properties': {'id': {'type': 'integer', 'description': 'IP address ID'}},
        'required': ['id']
    },
    'ipam_list_available_ips': {
        'description': 'List available IP addresses within a prefix',
        'properties': {'id': {'type': 'integer', 'description': 'Prefix ID'}},
        'required': ['id']
    },
    'ipam_create_available_ip': {
        'description': 'Create a new IP address from available space in prefix',
        'properties': {'id': {'type': 'integer', 'description': 'Prefix ID'}},
        'required': ['id']
    },
    'ipam_list_vlan_groups': {
        'description': 'List all VLAN groups in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'ipam_get_vlan_group': {
        'description': 'Get a specific VLAN group by ID',
        'properties': {'id': {'type': 'integer', 'description': 'VLAN group ID'}},
        'required': ['id']
    },
    'ipam_create_vlan_group': {
        'description': 'Create a new VLAN group',
        'properties': {
            'name': {'type': 'string', 'description': 'Group name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'min_vid': {'type': 'integer', 'description': 'Minimum VLAN ID'},
            'max_vid': {'type': 'integer', 'description': 'Maximum VLAN ID'}
        },
        'required': ['name', 'slug']
    },
    'ipam_list_vlans': {
        'description': 'List all VLANs in NetBox',
        'properties': {
            'vid': {'type': 'integer', 'description': 'Filter by VLAN ID'},
            'name': {'type': 'string', 'description': 'Filter by name'},
            'site_id': {'type': 'integer', 'description': 'Filter by site ID'},
            'group_id': {'type': 'integer', 'description': 'Filter by VLAN group ID'},
            'status': {'type': 'string', 'description': 'Filter by status'}
        }
    },
    'ipam_get_vlan': {
        'description': 'Get a specific VLAN by ID',
        'properties': {'id': {'type': 'integer', 'description': 'VLAN ID'}},
        'required': ['id']
    },
    'ipam_create_vlan': {
        'description': 'Create a new VLAN',
        'properties': {
            'vid': {'type': 'integer', 'description': 'VLAN ID number'},
            'name': {'type': 'string', 'description': 'VLAN name'},
            'status': {'type': 'string', 'description': 'Status'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'group': {'type': 'integer', 'description': 'VLAN group ID'}
        },
        'required': ['vid', 'name']
    },
    'ipam_update_vlan': {
        'description': 'Update an existing VLAN',
        'properties': {
            'id': {'type': 'integer', 'description': 'VLAN ID'},
            'vid': {'type': 'integer', 'description': 'VLAN ID number'},
            'name': {'type': 'string', 'description': 'VLAN name'},
            'status': {'type': 'string', 'description': 'Status'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'group': {'type': 'integer', 'description': 'VLAN group ID'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'},
            'role': {'type': 'integer', 'description': 'Role ID'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['id']
    },
    'ipam_delete_vlan': {
        'description': 'Delete a VLAN',
        'properties': {'id': {'type': 'integer', 'description': 'VLAN ID'}},
        'required': ['id']
    },
    'ipam_list_asns': {
        'description': 'List all ASNs in NetBox',
        'properties': {
            'asn': {'type': 'integer', 'description': 'Filter by ASN number'},
            'rir_id': {'type': 'integer', 'description': 'Filter by RIR ID'}
        }
    },
    'ipam_get_asn': {
        'description': 'Get a specific ASN by ID',
        'properties': {'id': {'type': 'integer', 'description': 'ASN ID'}},
        'required': ['id']
    },
    'ipam_create_asn': {
        'description': 'Create a new ASN',
        'properties': {
            'asn': {'type': 'integer', 'description': 'ASN number'},
            'rir': {'type': 'integer', 'description': 'RIR ID'}
        },
        'required': ['asn', 'rir']
    },
    'ipam_list_rirs': {
        'description': 'List all RIRs in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'ipam_get_rir': {
        'description': 'Get a specific RIR by ID',
        'properties': {'id': {'type': 'integer', 'description': 'RIR ID'}},
        'required': ['id']
    },
    'ipam_list_aggregates': {
        'description': 'List all aggregates in NetBox',
        'properties': {
            'prefix': {'type': 'string', 'description': 'Filter by prefix'},
            'rir_id': {'type': 'integer', 'description': 'Filter by RIR ID'}
        }
    },
    'ipam_get_aggregate': {
        'description': 'Get a specific aggregate by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Aggregate ID'}},
        'required': ['id']
    },
    'ipam_create_aggregate': {
        'description': 'Create a new aggregate',
        'properties': {
            'prefix': {'type': 'string', 'description': 'Prefix in CIDR notation'},
            'rir': {'type': 'integer', 'description': 'RIR ID'}
        },
        'required': ['prefix', 'rir']
    },
    'ipam_list_services': {
        'description': 'List all services in NetBox',
        'properties': {
            'device_id': {'type': 'integer', 'description': 'Filter by device ID'},
            'virtual_machine_id': {'type': 'integer', 'description': 'Filter by VM ID'},
            'name': {'type': 'string', 'description': 'Filter by name'}
        }
    },
    'ipam_get_service': {
        'description': 'Get a specific service by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Service ID'}},
        'required': ['id']
    },
    'ipam_create_service': {
        'description': 'Create a new service',
        'properties': {
            'name': {'type': 'string', 'description': 'Service name'},
            'ports': {'type': 'array', 'description': 'List of ports'},
            'protocol': {'type': 'string', 'description': 'Protocol (tcp/udp)'},
            'device': {'type': 'integer', 'description': 'Device ID'},
            'virtual_machine': {'type': 'integer', 'description': 'VM ID'}
        },
        'required': ['name', 'ports', 'protocol']
    },

    # ==================== Circuits Tools ====================
    'circuits_list_providers': {
        'description': 'List all circuit providers in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'circuits_get_provider': {
        'description': 'Get a specific provider by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Provider ID'}},
        'required': ['id']
    },
    'circuits_create_provider': {
        'description': 'Create a new circuit provider',
        'properties': {
            'name': {'type': 'string', 'description': 'Provider name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'}
        },
        'required': ['name', 'slug']
    },
    'circuits_update_provider': {
        'description': 'Update an existing provider',
        'properties': {'id': {'type': 'integer', 'description': 'Provider ID'}},
        'required': ['id']
    },
    'circuits_delete_provider': {
        'description': 'Delete a provider',
        'properties': {'id': {'type': 'integer', 'description': 'Provider ID'}},
        'required': ['id']
    },
    'circuits_list_circuit_types': {
        'description': 'List all circuit types in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'circuits_get_circuit_type': {
        'description': 'Get a specific circuit type by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Circuit type ID'}},
        'required': ['id']
    },
    'circuits_create_circuit_type': {
        'description': 'Create a new circuit type',
        'properties': {
            'name': {'type': 'string', 'description': 'Type name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'}
        },
        'required': ['name', 'slug']
    },
    'circuits_list_circuits': {
        'description': 'List all circuits in NetBox',
        'properties': {
            'cid': {'type': 'string', 'description': 'Filter by circuit ID'},
            'provider_id': {'type': 'integer', 'description': 'Filter by provider ID'},
            'type_id': {'type': 'integer', 'description': 'Filter by type ID'},
            'status': {'type': 'string', 'description': 'Filter by status'}
        }
    },
    'circuits_get_circuit': {
        'description': 'Get a specific circuit by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Circuit ID'}},
        'required': ['id']
    },
    'circuits_create_circuit': {
        'description': 'Create a new circuit',
        'properties': {
            'cid': {'type': 'string', 'description': 'Circuit ID'},
            'provider': {'type': 'integer', 'description': 'Provider ID'},
            'type': {'type': 'integer', 'description': 'Circuit type ID'},
            'status': {'type': 'string', 'description': 'Status'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'}
        },
        'required': ['cid', 'provider', 'type']
    },
    'circuits_update_circuit': {
        'description': 'Update an existing circuit',
        'properties': {'id': {'type': 'integer', 'description': 'Circuit ID'}},
        'required': ['id']
    },
    'circuits_delete_circuit': {
        'description': 'Delete a circuit',
        'properties': {'id': {'type': 'integer', 'description': 'Circuit ID'}},
        'required': ['id']
    },
    'circuits_list_circuit_terminations': {
        'description': 'List all circuit terminations in NetBox',
        'properties': {
            'circuit_id': {'type': 'integer', 'description': 'Filter by circuit ID'},
            'site_id': {'type': 'integer', 'description': 'Filter by site ID'}
        }
    },
    'circuits_get_circuit_termination': {
        'description': 'Get a specific circuit termination by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Termination ID'}},
        'required': ['id']
    },
    'circuits_create_circuit_termination': {
        'description': 'Create a new circuit termination',
        'properties': {
            'circuit': {'type': 'integer', 'description': 'Circuit ID'},
            'term_side': {'type': 'string', 'description': 'Termination side (A/Z)'},
            'site': {'type': 'integer', 'description': 'Site ID'}
        },
        'required': ['circuit', 'term_side']
    },

    # ==================== Virtualization Tools ====================
    'virtualization_list_cluster_types': {
        'description': 'List all cluster types in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'virtualization_get_cluster_type': {
        'description': 'Get a specific cluster type by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Cluster type ID'}},
        'required': ['id']
    },
    'virtualization_create_cluster_type': {
        'description': 'Create a new cluster type',
        'properties': {
            'name': {'type': 'string', 'description': 'Type name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'}
        },
        'required': ['name', 'slug']
    },
    'virtualization_list_cluster_groups': {
        'description': 'List all cluster groups in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'virtualization_get_cluster_group': {
        'description': 'Get a specific cluster group by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Cluster group ID'}},
        'required': ['id']
    },
    'virtualization_create_cluster_group': {
        'description': 'Create a new cluster group',
        'properties': {
            'name': {'type': 'string', 'description': 'Group name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'}
        },
        'required': ['name', 'slug']
    },
    'virtualization_list_clusters': {
        'description': 'List all clusters in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'type_id': {'type': 'integer', 'description': 'Filter by type ID'},
            'group_id': {'type': 'integer', 'description': 'Filter by group ID'},
            'site_id': {'type': 'integer', 'description': 'Filter by site ID'}
        }
    },
    'virtualization_get_cluster': {
        'description': 'Get a specific cluster by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Cluster ID'}},
        'required': ['id']
    },
    'virtualization_create_cluster': {
        'description': 'Create a new cluster',
        'properties': {
            'name': {'type': 'string', 'description': 'Cluster name'},
            'type': {'type': 'integer', 'description': 'Cluster type ID'},
            'group': {'type': 'integer', 'description': 'Cluster group ID'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'status': {'type': 'string', 'description': 'Status'}
        },
        'required': ['name', 'type']
    },
    'virtualization_update_cluster': {
        'description': 'Update an existing cluster',
        'properties': {
            'id': {'type': 'integer', 'description': 'Cluster ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'type': {'type': 'integer', 'description': 'Cluster type ID'},
            'group': {'type': 'integer', 'description': 'Cluster group ID'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'status': {'type': 'string', 'description': 'Status'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['id']
    },
    'virtualization_delete_cluster': {
        'description': 'Delete a cluster',
        'properties': {'id': {'type': 'integer', 'description': 'Cluster ID'}},
        'required': ['id']
    },
    'virtualization_list_virtual_machines': {
        'description': 'List all virtual machines in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'cluster_id': {'type': 'integer', 'description': 'Filter by cluster ID'},
            'site_id': {'type': 'integer', 'description': 'Filter by site ID'},
            'status': {'type': 'string', 'description': 'Filter by status'}
        }
    },
    'virtualization_get_virtual_machine': {
        'description': 'Get a specific virtual machine by ID',
        'properties': {'id': {'type': 'integer', 'description': 'VM ID'}},
        'required': ['id']
    },
    'virtualization_create_virtual_machine': {
        'description': 'Create a new virtual machine',
        'properties': {
            'name': {'type': 'string', 'description': 'VM name'},
            'cluster': {'type': 'integer', 'description': 'Cluster ID'},
            'status': {'type': 'string', 'description': 'Status'},
            'role': {'type': 'integer', 'description': 'Role ID'},
            'vcpus': {'type': 'number', 'description': 'Number of vCPUs'},
            'memory': {'type': 'integer', 'description': 'Memory in MB'},
            'disk': {'type': 'integer', 'description': 'Disk in GB'}
        },
        'required': ['name']
    },
    'virtualization_update_virtual_machine': {
        'description': 'Update an existing virtual machine',
        'properties': {
            'id': {'type': 'integer', 'description': 'VM ID'},
            'name': {'type': 'string', 'description': 'New name'},
            'status': {'type': 'string', 'description': 'Status'},
            'cluster': {'type': 'integer', 'description': 'Cluster ID'},
            'site': {'type': 'integer', 'description': 'Site ID'},
            'role': {'type': 'integer', 'description': 'Role ID'},
            'tenant': {'type': 'integer', 'description': 'Tenant ID'},
            'platform': {'type': 'integer', 'description': 'Platform ID'},
            'vcpus': {'type': 'number', 'description': 'Number of vCPUs'},
            'memory': {'type': 'integer', 'description': 'Memory in MB'},
            'disk': {'type': 'integer', 'description': 'Disk in GB'},
            'primary_ip4': {'type': 'integer', 'description': 'Primary IPv4 address ID'},
            'primary_ip6': {'type': 'integer', 'description': 'Primary IPv6 address ID'},
            'description': {'type': 'string', 'description': 'Description'},
            'comments': {'type': 'string', 'description': 'Comments'}
        },
        'required': ['id']
    },
    'virtualization_delete_virtual_machine': {
        'description': 'Delete a virtual machine',
        'properties': {'id': {'type': 'integer', 'description': 'VM ID'}},
        'required': ['id']
    },
    'virtualization_list_vm_interfaces': {
        'description': 'List all VM interfaces in NetBox',
        'properties': {
            'virtual_machine_id': {'type': 'integer', 'description': 'Filter by VM ID'},
            'name': {'type': 'string', 'description': 'Filter by name'}
        }
    },
    'virtualization_get_vm_interface': {
        'description': 'Get a specific VM interface by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Interface ID'}},
        'required': ['id']
    },
    'virtualization_create_vm_interface': {
        'description': 'Create a new VM interface',
        'properties': {
            'virtual_machine': {'type': 'integer', 'description': 'VM ID'},
            'name': {'type': 'string', 'description': 'Interface name'},
            'enabled': {'type': 'boolean', 'description': 'Enabled'}
        },
        'required': ['virtual_machine', 'name']
    },

    # ==================== Tenancy Tools ====================
    'tenancy_list_tenant_groups': {
        'description': 'List all tenant groups in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'tenancy_get_tenant_group': {
        'description': 'Get a specific tenant group by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Tenant group ID'}},
        'required': ['id']
    },
    'tenancy_create_tenant_group': {
        'description': 'Create a new tenant group',
        'properties': {
            'name': {'type': 'string', 'description': 'Group name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'}
        },
        'required': ['name', 'slug']
    },
    'tenancy_list_tenants': {
        'description': 'List all tenants in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'group_id': {'type': 'integer', 'description': 'Filter by group ID'}
        }
    },
    'tenancy_get_tenant': {
        'description': 'Get a specific tenant by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Tenant ID'}},
        'required': ['id']
    },
    'tenancy_create_tenant': {
        'description': 'Create a new tenant',
        'properties': {
            'name': {'type': 'string', 'description': 'Tenant name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'group': {'type': 'integer', 'description': 'Tenant group ID'}
        },
        'required': ['name', 'slug']
    },
    'tenancy_update_tenant': {
        'description': 'Update an existing tenant',
        'properties': {'id': {'type': 'integer', 'description': 'Tenant ID'}},
        'required': ['id']
    },
    'tenancy_delete_tenant': {
        'description': 'Delete a tenant',
        'properties': {'id': {'type': 'integer', 'description': 'Tenant ID'}},
        'required': ['id']
    },
    'tenancy_list_contacts': {
        'description': 'List all contacts in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'email': {'type': 'string', 'description': 'Filter by email'}
        }
    },
    'tenancy_get_contact': {
        'description': 'Get a specific contact by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Contact ID'}},
        'required': ['id']
    },
    'tenancy_create_contact': {
        'description': 'Create a new contact',
        'properties': {
            'name': {'type': 'string', 'description': 'Contact name'},
            'email': {'type': 'string', 'description': 'Email address'},
            'phone': {'type': 'string', 'description': 'Phone number'}
        },
        'required': ['name']
    },

    # ==================== VPN Tools ====================
    'vpn_list_tunnels': {
        'description': 'List all VPN tunnels in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'status': {'type': 'string', 'description': 'Filter by status'}
        }
    },
    'vpn_get_tunnel': {
        'description': 'Get a specific tunnel by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Tunnel ID'}},
        'required': ['id']
    },
    'vpn_create_tunnel': {
        'description': 'Create a new VPN tunnel',
        'properties': {
            'name': {'type': 'string', 'description': 'Tunnel name'},
            'status': {'type': 'string', 'description': 'Status'},
            'encapsulation': {'type': 'string', 'description': 'Encapsulation type'}
        },
        'required': ['name']
    },
    'vpn_list_l2vpns': {
        'description': 'List all L2VPNs in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'type': {'type': 'string', 'description': 'Filter by type'}
        }
    },
    'vpn_get_l2vpn': {
        'description': 'Get a specific L2VPN by ID',
        'properties': {'id': {'type': 'integer', 'description': 'L2VPN ID'}},
        'required': ['id']
    },
    'vpn_create_l2vpn': {
        'description': 'Create a new L2VPN',
        'properties': {
            'name': {'type': 'string', 'description': 'L2VPN name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'},
            'type': {'type': 'string', 'description': 'Type'}
        },
        'required': ['name', 'slug', 'type']
    },
    'vpn_list_ike_policies': {
        'description': 'List all IKE policies in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'vpn_list_ipsec_policies': {
        'description': 'List all IPSec policies in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'vpn_list_ipsec_profiles': {
        'description': 'List all IPSec profiles in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },

    # ==================== Wireless Tools ====================
    'wireless_list_wireless_lan_groups': {
        'description': 'List all wireless LAN groups in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'wireless_get_wireless_lan_group': {
        'description': 'Get a specific wireless LAN group by ID',
        'properties': {'id': {'type': 'integer', 'description': 'WLAN group ID'}},
        'required': ['id']
    },
    'wireless_create_wireless_lan_group': {
        'description': 'Create a new wireless LAN group',
        'properties': {
            'name': {'type': 'string', 'description': 'Group name'},
            'slug': {'type': 'string', 'description': 'URL-friendly slug'}
        },
        'required': ['name', 'slug']
    },
    'wireless_list_wireless_lans': {
        'description': 'List all wireless LANs in NetBox',
        'properties': {
            'ssid': {'type': 'string', 'description': 'Filter by SSID'},
            'group_id': {'type': 'integer', 'description': 'Filter by group ID'},
            'status': {'type': 'string', 'description': 'Filter by status'}
        }
    },
    'wireless_get_wireless_lan': {
        'description': 'Get a specific wireless LAN by ID',
        'properties': {'id': {'type': 'integer', 'description': 'WLAN ID'}},
        'required': ['id']
    },
    'wireless_create_wireless_lan': {
        'description': 'Create a new wireless LAN',
        'properties': {
            'ssid': {'type': 'string', 'description': 'SSID'},
            'status': {'type': 'string', 'description': 'Status'},
            'group': {'type': 'integer', 'description': 'Group ID'},
            'vlan': {'type': 'integer', 'description': 'VLAN ID'}
        },
        'required': ['ssid']
    },
    'wireless_list_wireless_links': {
        'description': 'List all wireless links in NetBox',
        'properties': {
            'ssid': {'type': 'string', 'description': 'Filter by SSID'},
            'status': {'type': 'string', 'description': 'Filter by status'}
        }
    },
    'wireless_get_wireless_link': {
        'description': 'Get a specific wireless link by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Link ID'}},
        'required': ['id']
    },

    # ==================== Extras Tools ====================
    'extras_list_tags': {
        'description': 'List all tags in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'slug': {'type': 'string', 'description': 'Filter by slug'}
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
            'color': {'type': 'string', 'description': 'Hex color code'}
        },
        'required': ['name', 'slug']
    },
    'extras_update_tag': {
        'description': 'Update an existing tag',
        'properties': {'id': {'type': 'integer', 'description': 'Tag ID'}},
        'required': ['id']
    },
    'extras_delete_tag': {
        'description': 'Delete a tag',
        'properties': {'id': {'type': 'integer', 'description': 'Tag ID'}},
        'required': ['id']
    },
    'extras_list_custom_fields': {
        'description': 'List all custom fields in NetBox',
        'properties': {
            'name': {'type': 'string', 'description': 'Filter by name'},
            'type': {'type': 'string', 'description': 'Filter by type'}
        }
    },
    'extras_get_custom_field': {
        'description': 'Get a specific custom field by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Custom field ID'}},
        'required': ['id']
    },
    'extras_list_webhooks': {
        'description': 'List all webhooks in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'extras_get_webhook': {
        'description': 'Get a specific webhook by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Webhook ID'}},
        'required': ['id']
    },
    'extras_list_journal_entries': {
        'description': 'List all journal entries in NetBox',
        'properties': {
            'assigned_object_type': {'type': 'string', 'description': 'Filter by object type'},
            'assigned_object_id': {'type': 'integer', 'description': 'Filter by object ID'}
        }
    },
    'extras_get_journal_entry': {
        'description': 'Get a specific journal entry by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Journal entry ID'}},
        'required': ['id']
    },
    'extras_create_journal_entry': {
        'description': 'Create a new journal entry',
        'properties': {
            'assigned_object_type': {'type': 'string', 'description': 'Object type'},
            'assigned_object_id': {'type': 'integer', 'description': 'Object ID'},
            'comments': {'type': 'string', 'description': 'Comments'},
            'kind': {'type': 'string', 'description': 'Kind (info, success, warning, danger)'}
        },
        'required': ['assigned_object_type', 'assigned_object_id', 'comments']
    },
    'extras_list_config_contexts': {
        'description': 'List all config contexts in NetBox',
        'properties': {'name': {'type': 'string', 'description': 'Filter by name'}}
    },
    'extras_get_config_context': {
        'description': 'Get a specific config context by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Config context ID'}},
        'required': ['id']
    },
    'extras_list_object_changes': {
        'description': 'List all object changes (audit log) in NetBox',
        'properties': {
            'user_id': {'type': 'integer', 'description': 'Filter by user ID'},
            'changed_object_type': {'type': 'string', 'description': 'Filter by object type'},
            'action': {'type': 'string', 'description': 'Filter by action (create, update, delete)'}
        }
    },
    'extras_get_object_change': {
        'description': 'Get a specific object change by ID',
        'properties': {'id': {'type': 'integer', 'description': 'Object change ID'}},
        'required': ['id']
    },
}


class NetBoxMCPServer:
    """MCP Server for NetBox integration"""

    def __init__(self):
        self.server = Server("netbox-mcp")
        self.config = None
        self.client = None
        self.dcim_tools = None
        self.ipam_tools = None
        self.circuits_tools = None
        self.virtualization_tools = None
        self.tenancy_tools = None
        self.vpn_tools = None
        self.wireless_tools = None
        self.extras_tools = None

    async def initialize(self):
        """Initialize server and load configuration."""
        try:
            config_loader = NetBoxConfig()
            self.config = config_loader.load()

            self.client = NetBoxClient()
            self.dcim_tools = DCIMTools(self.client)
            self.ipam_tools = IPAMTools(self.client)
            self.circuits_tools = CircuitsTools(self.client)
            self.virtualization_tools = VirtualizationTools(self.client)
            self.tenancy_tools = TenancyTools(self.client)
            self.vpn_tools = VPNTools(self.client)
            self.wireless_tools = WirelessTools(self.client)
            self.extras_tools = ExtrasTools(self.client)

            logger.info(f"NetBox MCP Server initialized for {self.config['api_url']}")
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
        """Route tool call to appropriate handler."""
        parts = name.split('_', 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid tool name format: {name}")

        category, method_name = parts[0], parts[1]

        # Map category to tool class
        tool_map = {
            'dcim': self.dcim_tools,
            'ipam': self.ipam_tools,
            'circuits': self.circuits_tools,
            'virtualization': self.virtualization_tools,
            'tenancy': self.tenancy_tools,
            'vpn': self.vpn_tools,
            'wireless': self.wireless_tools,
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
