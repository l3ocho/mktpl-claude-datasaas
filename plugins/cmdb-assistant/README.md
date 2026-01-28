# CMDB Assistant

A Claude Code plugin for NetBox CMDB integration - query, create, update, and manage your network infrastructure directly from Claude Code.

## What's New in v1.2.0

- **`/cmdb-topology`**: Generate Mermaid diagrams showing infrastructure topology (rack view, network view, site overview)
- **`/change-audit`**: Query and analyze NetBox audit log for change tracking and compliance
- **`/ip-conflicts`**: Detect IP address conflicts and overlapping prefixes

## What's New in v1.1.0

- **Data Quality Validation**: Hooks for SessionStart and PreToolUse that check data quality and warn about missing fields
- **Best Practices Skill**: Reference documentation for NetBox patterns (naming conventions, dependency order, role management)
- **`/cmdb-audit`**: Analyze data quality across VMs, devices, naming conventions, and roles
- **`/cmdb-register`**: Register the current machine into NetBox with all running applications (Docker containers, systemd services)
- **`/cmdb-sync`**: Synchronize existing machine state with NetBox (detect drift, update with confirmation)

## Features

- **Full CRUD Operations**: Create, read, update, and delete across all NetBox modules
- **Smart Search**: Find devices, IPs, sites, and more with natural language queries
- **IP Management**: Allocate IPs, manage prefixes, track VLANs
- **Infrastructure Documentation**: Document servers, network devices, and connections
- **Audit Trail**: Review changes and maintain infrastructure history
- **Data Quality Validation**: Proactive checks for missing site, tenant, platform assignments
- **Machine Registration**: Auto-discover and register servers with running applications
- **Drift Detection**: Sync machine state and detect changes over time

## Installation

### Prerequisites

1. A running NetBox instance (v4.x recommended)
2. NetBox API token with appropriate permissions
3. The NetBox MCP server configured (see below)

### Configure NetBox Credentials

Create the configuration file:

```bash
mkdir -p ~/.config/claude
cat > ~/.config/claude/netbox.env << 'EOF'
NETBOX_API_URL=https://your-netbox-instance/api
NETBOX_API_TOKEN=your-api-token-here
NETBOX_VERIFY_SSL=true
NETBOX_TIMEOUT=30
EOF
```

### Install the Plugin

Add to your Claude Code plugins or marketplace configuration.

## Commands

| Command | Description |
|---------|-------------|
| `/initial-setup` | Interactive setup wizard for NetBox MCP server |
| `/cmdb-search <query>` | Search for devices, IPs, sites, or any CMDB object |
| `/cmdb-device <action>` | Manage network devices (list, create, update, delete) |
| `/cmdb-ip <action>` | Manage IP addresses and prefixes |
| `/cmdb-site <action>` | Manage sites and locations |
| `/cmdb-audit [scope]` | Data quality analysis (all, vms, devices, naming, roles) |
| `/cmdb-register` | Register current machine into NetBox with running apps |
| `/cmdb-sync` | Sync machine state with NetBox (detect drift, update) |
| `/cmdb-topology <view>` | Generate Mermaid diagrams (rack, network, site, full) |
| `/change-audit [filters]` | Query NetBox audit log for change tracking |
| `/ip-conflicts [scope]` | Detect IP conflicts and overlapping prefixes |

## Agent

The **cmdb-assistant** agent provides conversational infrastructure management:

```
@cmdb-assistant Show me all devices at the headquarters site
@cmdb-assistant Allocate the next available IP from 10.0.1.0/24 for the new web server
@cmdb-assistant What changes were made to the network today?
```

## Usage Examples

### Search for Infrastructure

```
/cmdb-search router
/cmdb-search 10.0.1.0/24
/cmdb-search datacenter
```

### Device Management

```
/cmdb-device list
/cmdb-device show core-router-01
/cmdb-device create web-server-03
/cmdb-device at headquarters
```

### IP Address Management

```
/cmdb-ip prefixes
/cmdb-ip available in 10.0.1.0/24
/cmdb-ip allocate from 10.0.1.0/24
```

### Site Management

```
/cmdb-site list
/cmdb-site show headquarters
/cmdb-site racks at datacenter-east
```

## NetBox Coverage

This plugin provides access to the full NetBox API:

- **DCIM**: Sites, Locations, Racks, Devices, Interfaces, Cables, Power
- **IPAM**: IP Addresses, Prefixes, VLANs, VRFs, ASNs, Services
- **Circuits**: Providers, Circuits, Terminations
- **Virtualization**: Clusters, Virtual Machines, VM Interfaces
- **Tenancy**: Tenants, Contacts
- **VPN**: Tunnels, L2VPNs, IKE/IPSec Policies
- **Wireless**: WLANs, Wireless Links
- **Extras**: Tags, Custom Fields, Journal Entries, Audit Log

## Hooks

| Event | Purpose |
|-------|---------|
| `SessionStart` | Test NetBox connectivity, report data quality issues |
| `PreToolUse` | Validate VM/device parameters before create/update |

Hooks are **non-blocking** - they emit warnings but never prevent operations.

## Architecture

```
cmdb-assistant/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── .mcp.json                 # MCP server configuration
├── commands/
│   ├── initial-setup.md     # Setup wizard
│   ├── cmdb-search.md       # Search command
│   ├── cmdb-device.md       # Device management
│   ├── cmdb-ip.md           # IP management
│   ├── cmdb-site.md         # Site management
│   ├── cmdb-audit.md        # Data quality audit
│   ├── cmdb-register.md     # Machine registration
│   ├── cmdb-sync.md         # Machine sync
│   ├── cmdb-topology.md     # Topology visualization (NEW)
│   ├── change-audit.md      # Change audit log (NEW)
│   └── ip-conflicts.md      # IP conflict detection (NEW)
├── hooks/
│   ├── hooks.json           # Hook configuration
│   ├── startup-check.sh     # SessionStart validation
│   └── validate-input.sh    # PreToolUse validation
├── skills/
│   └── netbox-patterns/
│       └── SKILL.md         # NetBox best practices reference
├── agents/
│   └── cmdb-assistant.md    # Main assistant agent
└── README.md
```

The plugin uses the shared NetBox MCP server at `mcp-servers/netbox/`.

## Configuration

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `NETBOX_API_URL` | Full URL to NetBox API (e.g., `https://netbox.example.com/api`) |
| `NETBOX_API_TOKEN` | API authentication token |

### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NETBOX_VERIFY_SSL` | `true` | Verify SSL certificates |
| `NETBOX_TIMEOUT` | `30` | Request timeout in seconds |

## Getting a NetBox API Token

1. Log into your NetBox instance
2. Navigate to your profile (top-right menu)
3. Go to "API Tokens"
4. Click "Add a token"
5. Set appropriate permissions (read-only or read-write)
6. Copy the generated token

## Troubleshooting

### Connection Issues

- Verify `NETBOX_API_URL` is correct and accessible
- Check firewall rules allow access to NetBox
- For self-signed certificates, set `NETBOX_VERIFY_SSL=false`

### Authentication Errors

- Ensure API token is valid and not expired
- Check token has required permissions for the operation

### Timeout Errors

- Increase `NETBOX_TIMEOUT` for slow connections
- Check network latency to NetBox instance

## License

MIT License - Part of the Leo Claude Marketplace.
