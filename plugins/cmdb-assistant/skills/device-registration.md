# Device Registration Skill

How to register devices into NetBox.

## Prerequisites

Load these skills:
- `system-discovery` - Bash commands for gathering system info
- `netbox-patterns` - Best practices for data quality
- `mcp-tools-reference` - MCP tool reference

## Registration Workflow

### Phase 1: System Discovery

Use commands from `system-discovery` skill to gather:
- Hostname, OS, hardware model, serial number
- CPU, memory, disk
- Network interfaces with IPs
- Running Docker containers

### Phase 2: Pre-Registration Checks

1. **Check if device exists:**
   ```
   dcim_list_devices name=<hostname>
   ```
   If exists, suggest `/cmdb-sync` instead.

2. **Verify/Create site:**
   ```
   dcim_list_sites name=<site-name>
   ```
   If not found, list available sites or offer to create.

3. **Verify/Create platform:**
   ```
   dcim_list_platforms name=<platform-name>
   ```
   Create if not exists with `dcim_create_platform`.

4. **Verify/Create device role:**
   ```
   dcim_list_device_roles name=<role-name>
   ```

### Phase 3: Device Creation

1. **Get/Create manufacturer and device type:**
   ```
   dcim_list_manufacturers name="<manufacturer>"
   dcim_list_device_types manufacturer_id=X model="<model>"
   ```

2. **Create device:**
   ```
   dcim_create_device
     name=<hostname>
     device_type=<device_type_id>
     role=<role_id>
     site=<site_id>
     platform=<platform_id>
     tenant=<tenant_id>  # if provided
     serial=<serial>
     description="Registered via cmdb-assistant"
   ```

3. **Create interfaces:**
   For each network interface:
   ```
   dcim_create_interface
     device=<device_id>
     name=<interface_name>
     type=<type>
     mac_address=<mac>
     enabled=true
   ```

4. **Create IP addresses:**
   For each IP:
   ```
   ipam_create_ip_address
     address=<ip/prefix>
     assigned_object_type="dcim.interface"
     assigned_object_id=<interface_id>
     status="active"
   ```

5. **Set primary IP:**
   ```
   dcim_update_device
     id=<device_id>
     primary_ip4=<primary_ip_id>
   ```

### Phase 4: Container Registration (if Docker)

1. **Create/Get cluster type:**
   ```
   virt_list_cluster_types name="Docker Compose"
   virt_create_cluster_type name="Docker Compose" slug="docker-compose"
   ```

2. **Create cluster:**
   ```
   virt_create_cluster
     name=<project-name>
     type=<cluster_type_id>
     site=<site_id>
     description="Docker Compose stack on <hostname>"
   ```

3. **Create VMs for containers:**
   For each running container:
   ```
   virt_create_vm
     name=<container_name>
     cluster=<cluster_id>
     site=<site_id>
     role=<role_id>
     status="active"
     vcpus=<cpu_shares>
     memory=<memory_mb>
     disk=<disk_gb>
   ```

### Phase 5: Documentation

Add journal entry:
```
extras_create_journal_entry
  assigned_object_type="dcim.device"
  assigned_object_id=<device_id>
  comments="Device registered via /cmdb-register command\n\nDiscovered:\n- X network interfaces\n- Y IP addresses\n- Z Docker containers"
```

## Summary Report Template

```markdown
## Machine Registration Complete

### Device Created
- **Name:** <hostname>
- **Site:** <site>
- **Platform:** <platform>
- **Role:** <role>
- **ID:** <device_id>
- **URL:** https://netbox.example.com/dcim/devices/<id>/

### Network Interfaces
| Interface | Type | MAC | IP Address |
|-----------|------|-----|------------|
| eth0 | 1000base-t | aa:bb:cc:dd:ee:ff | 192.168.1.100/24 |

### Primary IP: 192.168.1.100

### Docker Containers Registered (if applicable)
**Cluster:** <cluster_name> (ID: <cluster_id>)

| Container | Role | vCPUs | Memory | Status |
|-----------|------|-------|--------|--------|
| media_jellyfin | Media Server | 2.0 | 2048MB | Active |

### Next Steps
- Run `/cmdb-sync` periodically to keep data current
- Run `/cmdb-audit` to check data quality
- Add tags for classification
```

## Error Handling

| Error | Action |
|-------|--------|
| Device already exists | Suggest `/cmdb-sync` or ask to proceed |
| Site not found | List available sites, offer to create new |
| Docker not available | Skip container registration, note in summary |
| Permission denied | Note which operations failed, suggest fixes |
