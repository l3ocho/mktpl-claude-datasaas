---
name: cmdb ip
---

# /cmdb ip

Manage IP addresses and prefixes in NetBox.

## Skills to Load

- `skills/visual-header.md`
- `skills/ip-management.md`
- `skills/mcp-tools-reference.md`

## Usage

```
/cmdb ip <action> [options]
```

## Instructions

Execute `skills/visual-header.md` with context "IP Management".

Execute operations from `skills/ip-management.md`.

### Actions

**Prefixes:**
- `prefixes` - List all prefixes
- `prefix <cidr>` - Get prefix details
- `available in <prefix>` - Show available IPs
- `create prefix <cidr>` - Create new prefix

**IP Addresses:**
- `list` - List all IP addresses
- `show <address>` - Get IP details
- `allocate from <prefix>` - Auto-allocate next available
- `create <address>` - Create specific IP
- `assign <ip> to <device> <interface>` - Assign IP to interface

**VLANs and VRFs:**
- `vlans` - List VLANs
- `vlan <id>` - Get VLAN details
- `vrfs` - List VRFs

## Examples

- `/cmdb ip prefixes`
- `/cmdb ip available in 10.0.1.0/24`
- `/cmdb ip allocate from 10.0.1.0/24`
- `/cmdb ip assign 10.0.1.50/24 to web-server-01 eth0`

## User Request

$ARGUMENTS
