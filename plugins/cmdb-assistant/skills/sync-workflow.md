# Sync Workflow Skill

How to synchronize machine state with NetBox.

## Prerequisites

Load these skills:
- `system-discovery` - Bash commands for system info
- `mcp-tools-reference` - MCP tool reference

## Sync Workflow

### Phase 1: Device Lookup

```
dcim_list_devices name=<hostname>
```

If not found, suggest `/cmdb register` first.

If found:
- Store device ID and current field values
- Fetch interfaces: `dcim_list_interfaces device_id=<device_id>`
- Fetch IPs: `ipam_list_ip_addresses device_id=<device_id>`
- Check clusters/VMs: `virt_list_clusters`, `virt_list_vms cluster=<cluster_id>`

### Phase 2: Current State Discovery

Use commands from `system-discovery` skill.

### Phase 3: Comparison

#### Device Attributes
| Field | Compare |
|-------|---------|
| Platform | OS version changed? |
| Status | Still active? |
| Serial | Match? |
| Description | Keep existing |

#### Network Interfaces
| Change Type | Detection |
|-------------|-----------|
| New interface | Exists locally but not in NetBox |
| Removed interface | In NetBox but not locally |
| Changed MAC | MAC address different |
| Interface type | Type mismatch |

#### IP Addresses
| Change Type | Detection |
|-------------|-----------|
| New IP | Exists locally but not in NetBox |
| Removed IP | In NetBox but not locally |
| Primary IP changed | Default route interface changed |

#### Docker Containers
| Change Type | Detection |
|-------------|-----------|
| New container | Running locally but no VM in cluster |
| Stopped container | VM exists but container not running |
| Resource change | vCPUs/memory different |

### Phase 4: Diff Report

```markdown
## Sync Diff Report

**Device:** <hostname> (ID: <device_id>)
**NetBox URL:** https://netbox.example.com/dcim/devices/<id>/

### Device Attributes
| Field | NetBox Value | Current Value | Action |
|-------|--------------|---------------|--------|
| Platform | Ubuntu 22.04 | Ubuntu 24.04 | UPDATE |

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

### Summary
- **Updates:** X
- **Creates:** Y
- **Removals/Offline:** Z
```

### Phase 5: Apply Updates

#### Device Updates
```
dcim_update_device id=<device_id> platform=<new_platform_id>
```

#### Interface Updates
New:
```
dcim_create_interface device=<device_id> name=<name> type=<type>
```

Removed (mark offline):
```
dcim_update_interface id=<id> enabled=false description="Marked offline by cmdb-sync"
```

Changed:
```
dcim_update_interface id=<id> mac_address=<new_mac>
```

#### IP Address Updates
New:
```
ipam_create_ip_address address=<ip/prefix> assigned_object_type="dcim.interface" assigned_object_id=<id>
```

Removed (unassign):
```
ipam_update_ip_address id=<id> assigned_object_type=null assigned_object_id=null
```

#### Primary IP Update
```
dcim_update_device id=<device_id> primary_ip4=<new_primary_ip_id>
```

#### Container/VM Updates
New:
```
virt_create_vm name=<name> cluster=<cluster_id> status="active"
```

Stopped:
```
virt_update_vm id=<id> status="offline"
```

### Phase 6: Journal Entry

```
extras_create_journal_entry
  assigned_object_type="dcim.device"
  assigned_object_id=<device_id>
  comments="Device synced via /cmdb sync command\n\nChanges applied:\n- <list>"
```

## Sync Modes

### Dry Run Mode
- Complete phases 1-4 (lookup, discovery, compare, diff report)
- Skip phases 5-6 (no updates, no journal)
- End with: "Dry run complete. No changes applied."

### Full Sync Mode
- Skip user confirmation
- Update all fields even if unchanged (force refresh)

## Error Handling

| Error | Action |
|-------|--------|
| Device not found | Suggest `/cmdb register` |
| Permission denied | Note which failed, continue others |
| Cluster not found | Offer to create or skip container sync |
| API errors | Log error, continue with remaining |
