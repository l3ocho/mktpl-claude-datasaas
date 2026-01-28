---
description: Synchronize current machine state with existing NetBox record
---

# CMDB Machine Sync

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🖥️ CMDB-ASSISTANT · Machine Sync                                │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the synchronization.

Update an existing NetBox device record with the current machine state. Compares local system information with NetBox and applies changes.

## Usage

```
/cmdb-sync [--full] [--dry-run]
```

**Options:**
- `--full`: Force refresh all fields, even unchanged ones
- `--dry-run`: Show what would change without applying updates

## Instructions

You are synchronizing the current machine's state with its NetBox record. This involves comparing current system state with stored data and updating differences.

**IMPORTANT:** Load the `netbox-patterns` skill for best practice reference.

### Phase 1: Device Lookup (via MCP)

First, find the existing device record:

```bash
# Get current hostname
hostname
```

```
dcim_list_devices name=<hostname>
```

**If device not found:**
- Inform user: "Device '<hostname>' not found in NetBox"
- Suggest: "Run `/cmdb-register` to register this machine first"
- Exit sync

**If device found:**
- Store device ID and all current field values
- Fetch interfaces: `dcim_list_interfaces device_id=<device_id>`
- Fetch IPs: `ipam_list_ip_addresses device_id=<device_id>`

Also check for associated clusters/VMs:
```
virt_list_clusters  # Look for cluster associated with this device
virt_list_vms cluster=<cluster_id>  # If cluster found
```

### Phase 2: Current State Discovery (via Bash)

Gather current system information (same as `/cmdb-register`):

```bash
# Device info
hostname
cat /etc/os-release 2>/dev/null || uname -a
nproc
free -m | awk '/Mem:/ {print $2}'
df -BG / | awk 'NR==2 {print $2}' | tr -d 'G'

# Network interfaces with IPs
ip -j addr show 2>/dev/null || ip addr show

# Docker containers
docker ps --format '{"name":"{{.Names}}","image":"{{.Image}}","status":"{{.Status}}"}' 2>/dev/null || echo "[]"
```

### Phase 3: Comparison

Compare discovered state with NetBox record:

#### 3.1 Device Attributes

| Field | Compare |
|-------|---------|
| Platform | OS version changed? |
| Status | Still active? |
| Serial | Match? |
| Description | Keep existing |

#### 3.2 Network Interfaces

| Change Type | Detection |
|-------------|-----------|
| New interface | Interface exists locally but not in NetBox |
| Removed interface | Interface in NetBox but not locally |
| Changed MAC | MAC address different |
| Interface type | Type mismatch |

#### 3.3 IP Addresses

| Change Type | Detection |
|-------------|-----------|
| New IP | IP exists locally but not in NetBox |
| Removed IP | IP in NetBox but not locally (on this device) |
| Primary IP changed | Default route interface changed |

#### 3.4 Docker Containers

| Change Type | Detection |
|-------------|-----------|
| New container | Container running locally but no VM in cluster |
| Stopped container | VM exists but container not running |
| Resource change | vCPUs/memory different (if trackable) |

### Phase 4: Diff Report

Present changes to user:

```markdown
## Sync Diff Report

**Device:** <hostname> (ID: <device_id>)
**NetBox URL:** https://netbox.example.com/dcim/devices/<id>/

### Device Attributes
| Field | NetBox Value | Current Value | Action |
|-------|--------------|---------------|--------|
| Platform | Ubuntu 22.04 | Ubuntu 24.04 | UPDATE |
| Status | active | active | - |

### Network Interfaces

#### New Interfaces (will create)
| Interface | Type | MAC | IPs |
|-----------|------|-----|-----|
| tailscale0 | virtual | - | 100.x.x.x/32 |

#### Removed Interfaces (will mark offline)
| Interface | Type | Reason |
|-----------|------|--------|
| eth1 | 1000base-t | Not found locally |

#### Changed Interfaces
| Interface | Field | Old | New |
|-----------|-------|-----|-----|
| eth0 | mac_address | aa:bb:cc:00:00:00 | aa:bb:cc:11:11:11 |

### IP Addresses

#### New IPs (will create)
- 192.168.1.150/24 on eth0

#### Removed IPs (will unassign)
- 192.168.1.100/24 from eth0

### Docker Containers

#### New Containers (will create VMs)
| Container | Image | Role |
|-----------|-------|------|
| media_lidarr | linuxserver/lidarr | Media Management |

#### Stopped Containers (will mark offline)
| Container | Last Status |
|-----------|-------------|
| media_bazarr | Exited |

### Summary
- **Updates:** X
- **Creates:** Y
- **Removals/Offline:** Z
```

### Phase 5: User Confirmation

If not `--dry-run`:

```
The following changes will be applied:
- Update device platform to "Ubuntu 24.04"
- Create interface "tailscale0"
- Create IP "100.x.x.x/32" on tailscale0
- Create VM "media_lidarr" in cluster
- Mark VM "media_bazarr" as offline

Proceed with sync? [Y/n]
```

**Use AskUserQuestion** to get confirmation.

### Phase 6: Apply Updates (via MCP)

Only if user confirms (or `--full` specified):

#### 6.1 Device Updates

```
dcim_update_device
  id=<device_id>
  platform=<new_platform_id>
  # ... other changed fields
```

#### 6.2 Interface Updates

**For new interfaces:**
```
dcim_create_interface
  device=<device_id>
  name=<interface_name>
  type=<type>
  mac_address=<mac>
  enabled=true
```

**For removed interfaces:**
```
dcim_update_interface
  id=<interface_id>
  enabled=false
  description="Marked offline by cmdb-sync - interface no longer present"
```

**For changed interfaces:**
```
dcim_update_interface
  id=<interface_id>
  mac_address=<new_mac>
```

#### 6.3 IP Address Updates

**For new IPs:**
```
ipam_create_ip_address
  address=<ip/prefix>
  assigned_object_type="dcim.interface"
  assigned_object_id=<interface_id>
  status="active"
```

**For removed IPs:**
```
ipam_update_ip_address
  id=<ip_id>
  assigned_object_type=null
  assigned_object_id=null
  description="Unassigned by cmdb-sync"
```

#### 6.4 Primary IP Update

If primary IP changed:
```
dcim_update_device
  id=<device_id>
  primary_ip4=<new_primary_ip_id>
```

#### 6.5 Container/VM Updates

**For new containers:**
```
virt_create_vm
  name=<container_name>
  cluster=<cluster_id>
  status="active"
  # ... other fields
```

**For stopped containers:**
```
virt_update_vm
  id=<vm_id>
  status="offline"
  description="Container stopped - detected by cmdb-sync"
```

### Phase 7: Journal Entry

Document the sync:

```
extras_create_journal_entry
  assigned_object_type="dcim.device"
  assigned_object_id=<device_id>
  comments="Device synced via /cmdb-sync command\n\nChanges applied:\n- <list of changes>"
```

### Phase 8: Summary Report

```markdown
## Sync Complete

**Device:** <hostname>
**Sync Time:** <timestamp>

### Changes Applied
- Updated platform: Ubuntu 22.04 → Ubuntu 24.04
- Created interface: tailscale0 (ID: X)
- Created IP: 100.x.x.x/32 (ID: Y)
- Created VM: media_lidarr (ID: Z)
- Marked VM offline: media_bazarr (ID: W)

### Current State
- **Interfaces:** 4 (3 active, 1 offline)
- **IP Addresses:** 5
- **Containers/VMs:** 8 (7 active, 1 offline)

### Next Sync
Run `/cmdb-sync` again after:
- Adding/removing Docker containers
- Changing network configuration
- OS upgrades
```

## Dry Run Mode

If `--dry-run` specified:
- Complete Phase 1-4 (lookup, discovery, compare, diff report)
- Skip Phase 5-8 (no confirmation, no updates, no journal)
- End with: "Dry run complete. No changes applied. Run without --dry-run to apply."

## Full Sync Mode

If `--full` specified:
- Skip user confirmation
- Update all fields even if unchanged (force refresh)
- Useful for ensuring NetBox matches current state exactly

## Error Handling

- **Device not found:** Suggest `/cmdb-register`
- **Permission denied on updates:** Note which failed, continue with others
- **Cluster not found:** Offer to create or skip container sync
- **API errors:** Log error, continue with remaining updates

## User Request

$ARGUMENTS
