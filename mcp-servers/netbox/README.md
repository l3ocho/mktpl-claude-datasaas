# NetBox MCP Server

MCP (Model Context Protocol) server for essential NetBox API integration with Claude Code.

## Overview

This MCP server provides Claude Code with focused access to the NetBox REST API for tracking **servers, services, IP addresses, and databases**. It has been optimized to include only essential tools:

- **DCIM** - Sites, Devices (servers/VPS), Interfaces
- **IPAM** - IP Addresses, Prefixes, Services (applications/databases)
- **Virtualization** - Clusters, Virtual Machines, VM Interfaces
- **Extras** - Tags, Journal Entries (audit/notes)

**Total:** 37 tools (~3,700 tokens) — down from 182 tools (~19,810 tokens).

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

Add to your Claude Code MCP configuration (`.claude/mcp.json` or project-level `.mcp.json`):

```json
{
  "mcpServers": {
    "netbox": {
      "command": "/path/to/mcp-servers/netbox/.venv/bin/python",
      "args": ["-m", "mcp_server"],
      "cwd": "/path/to/mcp-servers/netbox"
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "netbox": {
      "command": "C:\\path\\to\\mcp-servers\\netbox\\.venv\\Scripts\\python.exe",
      "args": ["-m", "mcp_server"],
      "cwd": "C:\\path\\to\\mcp-servers\\netbox"
    }
  }
}
```

## Available Tools (37 Total)

### DCIM: Sites, Devices, Interfaces (11 tools)

**Sites (4):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `dcim_list_sites` | List sites | `name`, `status` |
| `dcim_get_site` | Get site by ID | `id` (required) |
| `dcim_create_site` | Create site | `name`, `slug` (required), `status` |
| `dcim_update_site` | Update site | `id` (required), fields to update |

**Devices (4):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `dcim_list_devices` | List devices (servers/VPS) | `name`, `site_id`, `status`, `role_id` |
| `dcim_get_device` | Get device by ID | `id` (required) |
| `dcim_create_device` | Create device | `name`, `device_type`, `role`, `site` (required) |
| `dcim_update_device` | Update device | `id` (required), fields to update |

**Interfaces (3):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `dcim_list_interfaces` | List device interfaces | `device_id`, `name`, `type` |
| `dcim_get_interface` | Get interface by ID | `id` (required) |
| `dcim_create_interface` | Create interface | `device`, `name`, `type` (required) |

### IPAM: IPs, Prefixes, Services (10 tools)

**IP Addresses (4):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `ipam_list_ip_addresses` | List IP addresses | `address`, `device_id`, `status` |
| `ipam_get_ip_address` | Get IP by ID | `id` (required) |
| `ipam_create_ip_address` | Create IP address | `address` (required), `status`, `assigned_object_type` |
| `ipam_update_ip_address` | Update IP address | `id` (required), fields to update |

**Prefixes (3):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `ipam_list_prefixes` | List prefixes | `prefix`, `site_id`, `status` |
| `ipam_get_prefix` | Get prefix by ID | `id` (required) |
| `ipam_create_prefix` | Create prefix | `prefix` (required), `status`, `site` |

**Services (3):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `ipam_list_services` | List services (apps/databases) | `device_id`, `virtual_machine_id`, `name` |
| `ipam_get_service` | Get service by ID | `id` (required) |
| `ipam_create_service` | Create service | `name`, `ports`, `protocol` (required), `device`, `virtual_machine` |

### Virtualization: Clusters, VMs, VM Interfaces (10 tools)

**Clusters (3):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `virt_list_clusters` | List virtualization clusters | `name`, `site_id` |
| `virt_get_cluster` | Get cluster by ID | `id` (required) |
| `virt_create_cluster` | Create cluster | `name`, `type` (required), `site` |

**Virtual Machines (4):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `virt_list_vms` | List VMs | `name`, `cluster_id`, `site_id`, `status` |
| `virt_get_vm` | Get VM by ID | `id` (required) |
| `virt_create_vm` | Create VM | `name`, `cluster` (required), `vcpus`, `memory`, `disk` |
| `virt_update_vm` | Update VM | `id` (required), fields to update |

**VM Interfaces (3):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `virt_list_vm_ifaces` | List VM interfaces | `virtual_machine_id` |
| `virt_get_vm_iface` | Get VM interface by ID | `id` (required) |
| `virt_create_vm_iface` | Create VM interface | `virtual_machine`, `name` (required) |

### Extras: Tags, Journal Entries (6 tools)

**Tags (3):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `extras_list_tags` | List tags | `name` |
| `extras_get_tag` | Get tag by ID | `id` (required) |
| `extras_create_tag` | Create tag | `name`, `slug` (required), `color` |

**Journal Entries (3):**
| Tool | Description | Parameters |
|------|-------------|-----------|
| `extras_list_journal_entries` | List journal entries | `assigned_object_type`, `assigned_object_id` |
| `extras_get_journal_entry` | Get journal entry by ID | `id` (required) |
| `extras_create_journal_entry` | Create journal entry | `assigned_object_type`, `assigned_object_id`, `comments` (required), `kind` |

## Configuration

All configuration is done via environment variables in `~/.config/claude/netbox.env`:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NETBOX_API_URL` | Yes | — | NetBox API URL (e.g., https://netbox.example.com/api) |
| `NETBOX_API_TOKEN` | Yes | — | NetBox API token |
| `NETBOX_VERIFY_SSL` | No | true | Verify SSL certificates |
| `NETBOX_TIMEOUT` | No | 30 | Request timeout in seconds |

## Architecture

### Hybrid Configuration

- **System-level:** `~/.config/claude/netbox.env` (credentials)
- **Project-level:** `.env` (optional overrides)

### Tool Routing

Tool names follow the pattern `{module}_{action}_{resource}`:
- `dcim_list_sites` → DCIMTools.list_sites()
- `ipam_create_service` → IPAMTools.create_service()
- `virt_list_vms` → VirtualizationTools.list_virtual_machines()

Shortened names (virt_*) are mapped via TOOL_NAME_MAP to meet the 28-character MCP limit.

### Error Handling

All tools return JSON responses. Errors are caught and returned as:
```json
{
  "error": "Error message",
  "status_code": 404
}
```

## Development

### Testing

```bash
# Test import
python -c "from mcp_server.server import NetBoxMCPServer; print('OK')"

# Test tool count
python -c "from mcp_server.server import TOOL_DEFINITIONS; print(f'{len(TOOL_DEFINITIONS)} tools')"
```

### File Structure

```
netbox/
├── mcp_server/
│   ├── __init__.py
│   ├── server.py          # Main MCP server (37 TOOL_DEFINITIONS)
│   ├── config.py          # Configuration loader
│   ├── netbox_client.py   # HTTP client wrapper
│   └── tools/
│       ├── __init__.py
│       ├── dcim.py        # Sites, Devices, Interfaces
│       ├── ipam.py        # IPs, Prefixes, Services
│       ├── virtualization.py  # Clusters, VMs, VM Interfaces
│       └── extras.py      # Tags, Journal Entries
├── .venv/                 # Python virtual environment
├── requirements.txt
└── README.md
```

## Troubleshooting

### MCP Server Won't Start

**Check configuration:**
```bash
cat ~/.config/claude/netbox.env
```

**Test credentials:**
```bash
curl -H "Authorization: Token YOUR_TOKEN" https://netbox.example.com/api/
```

### Tools Not Appearing in Claude

**Verify MCP registration:**
```bash
cat ~/.claude/mcp.json  # or project-level .mcp.json
```

**Check MCP server logs:**
Claude Code will show MCP server stderr in the UI.

### Connection Errors

- Verify `NETBOX_API_URL` ends with `/api`
- Check firewall/network connectivity to NetBox instance
- Ensure API token has required permissions

## License

MIT License - See LICENSE file for details.

## Contributing

This MCP server is part of the leo-claude-mktplace project. For issues or contributions, refer to the main repository.
