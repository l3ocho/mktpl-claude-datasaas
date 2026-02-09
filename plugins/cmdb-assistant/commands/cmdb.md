---
name: cmdb
description: NetBox CMDB infrastructure management — type /cmdb <action> for commands
---

# /cmdb

NetBox CMDB integration for infrastructure management.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `search` | `/cmdb-assistant:cmdb-search` | Search NetBox for devices, IPs, sites |
| `device` | `/cmdb-assistant:cmdb-device` | Manage network devices (create, view, update, delete) |
| `ip` | `/cmdb-assistant:cmdb-ip` | Manage IP addresses and prefixes |
| `site` | `/cmdb-assistant:cmdb-site` | Manage sites, locations, racks, and regions |
| `audit` | `/cmdb-assistant:cmdb-audit` | Data quality analysis (VMs, devices, naming, roles) |
| `register` | `/cmdb-assistant:cmdb-register` | Register current machine into NetBox |
| `sync` | `/cmdb-assistant:cmdb-sync` | Sync machine state with NetBox (detect drift) |
| `topology` | `/cmdb-assistant:cmdb-topology` | Infrastructure topology diagrams |
| `change-audit` | `/cmdb-assistant:cmdb-change-audit` | NetBox audit trail queries with filtering |
| `ip-conflicts` | `/cmdb-assistant:cmdb-ip-conflicts` | Detect IP conflicts and overlapping prefixes |
| `setup` | `/cmdb-assistant:cmdb-setup` | Setup wizard for NetBox MCP server |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/cmdb search`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/cmdb-assistant:cmdb-search`)
