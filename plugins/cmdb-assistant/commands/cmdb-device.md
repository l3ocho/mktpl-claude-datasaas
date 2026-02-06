---
name: cmdb device
---

# /cmdb device

Manage network devices in NetBox.

## Skills to Load

- `skills/visual-header.md`
- `skills/mcp-tools-reference.md`

## Usage

```
/cmdb device <action> [options]
```

## Instructions

Execute `skills/visual-header.md` with context "Device Management".

### Actions

**List/View:**
- `list` or `show all` - List all devices: `dcim_list_devices`
- `show <name>` - Get device details: `dcim_get_device`
- `at <site>` - List devices at site

**Create:**
- `create <name>` - Create new device
- Required: name, device_type, role, site
- Use `dcim_list_device_types`, `dcim_list_device_roles`, `dcim_list_sites` to find IDs

**Update:**
- `update <name>` - Update device properties
- Get device ID first, then use `dcim_update_device`

**Delete:**
- `delete <name>` - Delete device (ask confirmation first)

### Related Operations

After creating a device, offer to:
- Add interfaces: `dcim_create_interface`
- Assign IP addresses: `ipam_create_ip_address`
- Add to rack: `dcim_update_device`

## Examples

- `/cmdb device list`
- `/cmdb device show core-router-01`
- `/cmdb device create web-server-03`
- `/cmdb device at headquarters`

## User Request

$ARGUMENTS
