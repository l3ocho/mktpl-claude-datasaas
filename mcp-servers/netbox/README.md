# NetBox MCP Server

MCP (Model Context Protocol) server for comprehensive NetBox API integration with Claude Code.

## Overview

This MCP server provides Claude Code with full access to the NetBox REST API, enabling infrastructure management, documentation, and automation workflows. It covers all major NetBox application areas:

- **DCIM** - Sites, Locations, Racks, Devices, Interfaces, Cables, Power
- **IPAM** - IP Addresses, Prefixes, VLANs, VRFs, ASNs, Services
- **Circuits** - Providers, Circuits, Terminations
- **Virtualization** - Clusters, Virtual Machines, VM Interfaces
- **Tenancy** - Tenants, Contacts, Contact Assignments
- **VPN** - Tunnels, IKE/IPSec Policies, L2VPN
- **Wireless** - Wireless LANs, Links, Groups
- **Extras** - Tags, Custom Fields, Webhooks, Config Contexts, Audit Log

## Installation

### 1. Clone and Setup

```bash
cd /path/to/mcp-servers/netbox
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Credentials

Create the system-level configuration file:

```bash
mkdir -p ~/.config/claude
cat > ~/.config/claude/netbox.env << 'EOF'
NETBOX_API_URL=https://your-netbox-instance/api
NETBOX_API_TOKEN=your-api-token-here
NETBOX_VERIFY_SSL=true
NETBOX_TIMEOUT=30
EOF
```

**Getting a NetBox API Token:**
1. Log into your NetBox instance
2. Navigate to your profile (top-right menu)
3. Go to "API Tokens"
4. Click "Add a token"
5. Copy the generated token

### 3. Register with Claude Code

Add to your Claude Code MCP configuration (`~/.config/claude/mcp.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "netbox": {
      "command": "/path/to/mcp-servers/netbox/.venv/bin/python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/mcp-servers/netbox"
    }
  }
}
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NETBOX_API_URL` | Yes | - | Full URL to NetBox API (e.g., `https://netbox.example.com/api`) |
| `NETBOX_API_TOKEN` | Yes | - | API authentication token |
| `NETBOX_VERIFY_SSL` | No | `true` | Verify SSL certificates |
| `NETBOX_TIMEOUT` | No | `30` | Request timeout in seconds |

### Configuration Hierarchy

1. **System-level** (`~/.config/claude/netbox.env`): Credentials and defaults
2. **Project-level** (`.env` in current directory): Optional overrides

## Module Filtering (Token Optimization)

By default, the NetBox MCP server registers all 182 tools across 8 modules, consuming ~19,810 tokens of context. For most workflows, you only need a subset of modules.

### Configuration

Add `NETBOX_ENABLED_MODULES` to your `~/.config/claude/netbox.env`:

```bash
# Enable only specific modules (comma-separated)
NETBOX_ENABLED_MODULES=dcim,ipam,virtualization,extras
```

If unset, all modules are enabled (backward compatible).

### Available Modules

| Module | Tool Count | Description | cmdb-assistant Commands |
|--------|------------|-------------|------------------------|
| `dcim` | ~60 | Sites, devices, racks, interfaces, cables | `/cmdb device`, `/cmdb site`, `/cmdb search`, `/cmdb topology` |
| `ipam` | ~40 | IP addresses, prefixes, VLANs, VRFs | `/cmdb ip`, `/cmdb ip-conflicts`, `/cmdb search` |
| `virtualization` | ~20 | Clusters, VMs, VM interfaces | `/cmdb search`, `/cmdb audit`, `/cmdb register` |
| `extras` | ~12 | Tags, journal entries, audit log | `/cmdb change-audit`, `/cmdb register` |
| `circuits` | ~15 | Providers, circuits, terminations | — |
| `tenancy` | ~12 | Tenants, contacts | — |
| `vpn` | ~15 | Tunnels, IKE/IPSec policies, L2VPN | — |
| `wireless` | ~8 | Wireless LANs, links, groups | — |

### Recommended Configurations

**For cmdb-assistant users** (~43 tools, ~4,500 tokens):
```bash
NETBOX_ENABLED_MODULES=dcim,ipam,virtualization,extras
```

**Basic infrastructure** (~100 tools):
```bash
NETBOX_ENABLED_MODULES=dcim,ipam
```

**Full CMDB** (all modules, ~182 tools):
```bash
# Omit NETBOX_ENABLED_MODULES or set to all modules
NETBOX_ENABLED_MODULES=dcim,ipam,circuits,virtualization,tenancy,vpn,wireless,extras
```

### Startup Logging

On startup, the server logs enabled modules and tool count:

```
NetBox MCP Server initialized: 43 tools registered (modules: dcim, extras, ipam, virtualization)
```

### Disabled Tool Behavior

Calling a tool from a disabled module returns a clear error:

```
Tool 'circuits_list_circuits' is not available (module 'circuits' not enabled).
Enabled modules: dcim, extras, ipam, virtualization
```

## Available Tools

### DCIM (Data Center Infrastructure Management)

| Tool | Description |
|------|-------------|
| `dcim_list_sites` | List all sites |
| `dcim_get_site` | Get site details |
| `dcim_create_site` | Create a new site |
| `dcim_update_site` | Update a site |
| `dcim_delete_site` | Delete a site |
| `dcim_list_devices` | List all devices |
| `dcim_get_device` | Get device details |
| `dcim_create_device` | Create a new device |
| `dcim_update_device` | Update a device |
| `dcim_delete_device` | Delete a device |
| `dcim_list_interfaces` | List device interfaces |
| `dcim_create_interface` | Create an interface |
| `dcim_list_racks` | List all racks |
| `dcim_create_rack` | Create a new rack |
| `dcim_list_cables` | List all cables |
| `dcim_create_cable` | Create a cable connection |
| ... and many more |

### IPAM (IP Address Management)

| Tool | Description |
|------|-------------|
| `ipam_list_prefixes` | List IP prefixes |
| `ipam_create_prefix` | Create a prefix |
| `ipam_list_available_prefixes` | List available child prefixes |
| `ipam_create_available_prefix` | Auto-allocate a prefix |
| `ipam_list_ip_addresses` | List IP addresses |
| `ipam_create_ip_address` | Create an IP address |
| `ipam_list_available_ips` | List available IPs in prefix |
| `ipam_create_available_ip` | Auto-allocate an IP |
| `ipam_list_vlans` | List VLANs |
| `ipam_create_vlan` | Create a VLAN |
| `ipam_list_vrfs` | List VRFs |
| ... and many more |

### Circuits

| Tool | Description |
|------|-------------|
| `circuits_list_providers` | List circuit providers |
| `circuits_create_provider` | Create a provider |
| `circuits_list_circuits` | List circuits |
| `circuits_create_circuit` | Create a circuit |
| `circ_list_terminations` | List terminations |
| ... and more |

### Virtualization

| Tool | Description |
|------|-------------|
| `virt_list_clusters` | List clusters |
| `virt_create_cluster` | Create a cluster |
| `virt_list_vms` | List VMs |
| `virt_create_vm` | Create a VM |
| `virt_list_vm_ifaces` | List VM interfaces |
| ... and more |

### Tenancy

| Tool | Description |
|------|-------------|
| `tenancy_list_tenants` | List tenants |
| `tenancy_create_tenant` | Create a tenant |
| `tenancy_list_contacts` | List contacts |
| `tenancy_create_contact` | Create a contact |
| ... and more |

### VPN

| Tool | Description |
|------|-------------|
| `vpn_list_tunnels` | List VPN tunnels |
| `vpn_create_tunnel` | Create a tunnel |
| `vpn_list_l2vpns` | List L2VPNs |
| `vpn_list_ike_policies` | List IKE policies |
| `vpn_list_ipsec_policies` | List IPSec policies |
| ... and more |

### Wireless

| Tool | Description |
|------|-------------|
| `wlan_list_lans` | List wireless LANs |
| `wlan_create_lan` | Create a WLAN |
| `wlan_list_links` | List wireless links |
| ... and more |

### Extras

| Tool | Description |
|------|-------------|
| `extras_list_tags` | List all tags |
| `extras_create_tag` | Create a tag |
| `extras_list_custom_fields` | List custom fields |
| `extras_list_webhooks` | List webhooks |
| `extras_list_journal_entries` | List journal entries |
| `extras_create_journal_entry` | Create journal entry |
| `extras_list_object_changes` | View audit log |
| `extras_list_config_contexts` | List config contexts |
| ... and more |

## Usage Examples

### List all devices at a site

```
Use the dcim_list_devices tool with site_id filter to see all devices at site 5
```

### Create a new prefix and allocate IPs

```
1. Use ipam_create_prefix to create 10.0.1.0/24
2. Use ipam_list_available_ips with the prefix ID to see available addresses
3. Use ipam_create_available_ip to auto-allocate the next IP
```

### Document a new server

```
1. Use dcim_create_device to create the device
2. Use dcim_create_interface to add network interfaces
3. Use ipam_create_ip_address to assign IPs to interfaces
4. Use extras_create_journal_entry to add notes
```

### Audit recent changes

```
Use extras_list_object_changes to see recent modifications in NetBox
```

## Architecture

```
mcp-servers/netbox/
├── mcp_server/
│   ├── __init__.py
│   ├── config.py          # Configuration loader
│   ├── netbox_client.py   # Generic HTTP client
│   ├── server.py          # MCP server entry point
│   └── tools/
│       ├── __init__.py
│       ├── dcim.py        # DCIM operations
│       ├── ipam.py        # IPAM operations
│       ├── circuits.py    # Circuits operations
│       ├── virtualization.py
│       ├── tenancy.py
│       ├── vpn.py
│       ├── wireless.py
│       └── extras.py
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
```

## API Coverage

This MCP server provides comprehensive coverage of the NetBox REST API v4.x:

- Full CRUD operations for all major models
- Filtering and search capabilities
- Special endpoints (available prefixes, available IPs)
- Pagination handling (automatic)
- Error handling with detailed messages

## Error Handling

The server returns detailed error messages from the NetBox API, including:
- Validation errors
- Authentication failures
- Not found errors
- Permission errors

## Security Notes

- API tokens should be kept secure and not committed to version control
- Use environment variables or the system config file for credentials
- SSL verification is enabled by default
- Consider using read-only tokens for query-only workflows

## Troubleshooting

### Common Issues

1. **Connection refused**: Check `NETBOX_API_URL` is correct and accessible
2. **401 Unauthorized**: Verify your API token is valid
3. **SSL errors**: Set `NETBOX_VERIFY_SSL=false` for self-signed certs (not recommended for production)
4. **Timeout errors**: Increase `NETBOX_TIMEOUT` for slow connections

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Follow the existing code patterns
2. Add tests for new functionality
3. Update documentation for new tools
4. Ensure compatibility with NetBox 4.x API

## License

MIT License - Part of the Leo Claude Marketplace.
