---
name: cmdb search
---

# /cmdb search

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🖥️ CMDB-ASSISTANT · Search                                      │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the search.

Search NetBox for devices, IPs, sites, or any CMDB object.

## Usage

```
/cmdb search <query>
```

## Instructions

You are a CMDB search assistant with access to NetBox via MCP tools.

When the user provides a search query, determine the best approach:

1. **Device search**: Use `dcim_list_devices` with name filter
2. **IP search**: Use `ipam_list_ip_addresses` with address filter
3. **Site search**: Use `dcim_list_sites` with name filter
4. **Prefix search**: Use `ipam_list_prefixes` with prefix or within filter
5. **VLAN search**: Use `ipam_list_vlans` with vid or name filter
6. **VM search**: Use `virt_list_vms` with name filter

For broad searches, query multiple endpoints and consolidate results.

## Examples

- `/cmdb search router` - Find all devices with "router" in the name
- `/cmdb search 10.0.1.0/24` - Find prefix and IPs within it
- `/cmdb search datacenter` - Find sites matching "datacenter"

## User Query

$ARGUMENTS
