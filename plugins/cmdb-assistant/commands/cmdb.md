---
description: NetBox CMDB infrastructure management
---

# /cmdb

NetBox CMDB integration for infrastructure management.

## Sub-commands

| Sub-command | Description |
|-------------|-------------|
| `/cmdb search` | Search NetBox for devices, IPs, sites |
| `/cmdb device` | Manage network devices (create, view, update, delete) |
| `/cmdb ip` | Manage IP addresses and prefixes |
| `/cmdb site` | Manage sites, locations, racks, and regions |
| `/cmdb audit` | Data quality analysis (VMs, devices, naming, roles) |
| `/cmdb register` | Register current machine into NetBox |
| `/cmdb sync` | Sync machine state with NetBox (detect drift) |
| `/cmdb topology` | Infrastructure topology diagrams |
| `/cmdb change-audit` | NetBox audit trail queries with filtering |
| `/cmdb ip-conflicts` | Detect IP conflicts and overlapping prefixes |
| `/cmdb setup` | Setup wizard for NetBox MCP server |
