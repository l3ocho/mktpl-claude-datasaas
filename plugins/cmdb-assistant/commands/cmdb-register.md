---
description: Register the current machine into NetBox with all running applications
---

# CMDB Machine Registration

Register the current machine into NetBox, including hardware info, network interfaces, and running applications (Docker containers, services).

## Usage

```
/cmdb-register [--site <site-name>] [--tenant <tenant-name>] [--role <role-name>]
```

**Options:**
- `--site <name>`: Site to assign (will prompt if not provided)
- `--tenant <name>`: Tenant for resource isolation (optional)
- `--role <name>`: Device role (default: auto-detect based on services)

## Instructions

You are registering the current machine into NetBox. This is a multi-phase process that discovers local system information and creates corresponding NetBox objects.

**IMPORTANT:** Load the `netbox-patterns` skill for best practice reference.

### Phase 1: System Discovery (via Bash)

Gather system information using these commands:

#### 1.1 Basic Device Info

```bash
# Hostname
hostname

# OS/Platform info
cat /etc/os-release 2>/dev/null || uname -a

# Hardware model (varies by system)
# Raspberry Pi:
cat /proc/device-tree/model 2>/dev/null || echo "Unknown"

# x86 systems:
cat /sys/class/dmi/id/product_name 2>/dev/null || echo "Unknown"

# Serial number
# Raspberry Pi:
cat /proc/device-tree/serial-number 2>/dev/null || cat /proc/cpuinfo | grep Serial | cut -d: -f2 | tr -d ' ' 2>/dev/null

# x86 systems:
cat /sys/class/dmi/id/product_serial 2>/dev/null || echo "Unknown"

# CPU info
nproc

# Memory (MB)
free -m | awk '/Mem:/ {print $2}'

# Disk (GB, root filesystem)
df -BG / | awk 'NR==2 {print $2}' | tr -d 'G'
```

#### 1.2 Network Interfaces

```bash
# Get interfaces with IPs (JSON format)
ip -j addr show 2>/dev/null || ip addr show

# Get default gateway interface
ip route | grep default | awk '{print $5}' | head -1

# Get MAC addresses
ip -j link show 2>/dev/null || ip link show
```

#### 1.3 Running Applications

```bash
# Docker containers (if docker available)
docker ps --format '{"name":"{{.Names}}","image":"{{.Image}}","status":"{{.Status}}","ports":"{{.Ports}}"}' 2>/dev/null || echo "Docker not available"

# Docker Compose projects (check common locations)
find ~/apps /home/*/apps -name "docker-compose.yml" -o -name "docker-compose.yaml" 2>/dev/null | head -20

# Systemd services (running)
systemctl list-units --type=service --state=running --no-pager --plain 2>/dev/null | grep -v "^UNIT" | head -30
```

### Phase 2: Pre-Registration Checks (via MCP)

Before creating objects, verify prerequisites:

#### 2.1 Check if Device Already Exists

```
dcim_list_devices name=<hostname>
```

**If device exists:**
- Inform user and suggest `/cmdb-sync` instead
- Ask if they want to proceed with re-registration (will update existing)

#### 2.2 Verify/Create Site

If `--site` provided:
```
dcim_list_sites name=<site-name>
```

If site doesn't exist, ask user if they want to create it.

If no site provided, list available sites and ask user to choose:
```
dcim_list_sites
```

#### 2.3 Verify/Create Platform

Based on OS detected, check if platform exists:
```
dcim_list_platforms name=<platform-name>
```

**Platform naming:**
- `Raspberry Pi OS (Bookworm)` for Raspberry Pi
- `Ubuntu 24.04 LTS` for Ubuntu
- `Debian 12` for Debian
- Use format: `{OS Name} {Version}`

If platform doesn't exist, create it:
```
dcim_create_platform name=<platform-name> slug=<slug>
```

#### 2.4 Verify/Create Device Role

Based on detected services:
- If Docker containers found → `Docker Host`
- If only basic services → `Server`
- If specific role specified → Use that

```
dcim_list_device_roles name=<role-name>
```

### Phase 3: Device Registration (via MCP)

#### 3.1 Get/Create Manufacturer and Device Type

For Raspberry Pi:
```
dcim_list_manufacturers name="Raspberry Pi Foundation"
dcim_list_device_types manufacturer_id=X model="Raspberry Pi 4 Model B"
```

Create if not exists.

For generic x86:
```
dcim_list_manufacturers name=<detected-manufacturer>
```

#### 3.2 Create Device

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

#### 3.3 Create Interfaces

For each network interface discovered:
```
dcim_create_interface
  device=<device_id>
  name=<interface_name>  # eth0, wlan0, tailscale0, etc.
  type=<type>            # 1000base-t, virtual, other
  mac_address=<mac>
  enabled=true
```

**Interface type mapping:**
- `eth*`, `enp*` → `1000base-t`
- `wlan*` → `ieee802.11ax` (or appropriate wifi type)
- `tailscale*`, `docker*`, `br-*` → `virtual`
- `lo` → skip (loopback)

#### 3.4 Create IP Addresses

For each IP on each interface:
```
ipam_create_ip_address
  address=<ip/prefix>    # e.g., "192.168.1.100/24"
  assigned_object_type="dcim.interface"
  assigned_object_id=<interface_id>
  status="active"
  description="Discovered via cmdb-register"
```

#### 3.5 Set Primary IP

Identify primary IP (interface with default route):
```
dcim_update_device
  id=<device_id>
  primary_ip4=<primary_ip_id>
```

### Phase 4: Container Registration (via MCP)

If Docker containers were discovered:

#### 4.1 Create/Get Cluster Type

```
virt_list_cluster_types name="Docker Compose"
```

Create if not exists:
```
virt_create_cluster_type name="Docker Compose" slug="docker-compose"
```

#### 4.2 Create Cluster

For each Docker Compose project directory found:
```
virt_create_cluster
  name=<project-name>  # e.g., "apps-hotport"
  type=<cluster_type_id>
  site=<site_id>
  description="Docker Compose stack on <hostname>"
```

#### 4.3 Create VMs for Containers

For each running container:
```
virt_create_vm
  name=<container_name>
  cluster=<cluster_id>
  site=<site_id>
  role=<role_id>        # Map container function to role
  status="active"
  vcpus=<cpu_shares>    # Default 1.0 if unknown
  memory=<memory_mb>    # Default 256 if unknown
  disk=<disk_gb>        # Default 5 if unknown
  description=<container purpose>
  comments=<image, ports, volumes info>
```

**Container role mapping:**
- `*caddy*`, `*nginx*`, `*traefik*` → "Reverse Proxy"
- `*db*`, `*postgres*`, `*mysql*`, `*redis*` → "Database"
- `*webui*`, `*frontend*` → "Web Application"
- Others → Infer from image name or use generic "Container"

### Phase 5: Documentation

#### 5.1 Add Journal Entry

```
extras_create_journal_entry
  assigned_object_type="dcim.device"
  assigned_object_id=<device_id>
  comments="Device registered via /cmdb-register command\n\nDiscovered:\n- X network interfaces\n- Y IP addresses\n- Z Docker containers"
```

### Phase 6: Summary Report

Present registration summary:

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
| tailscale0 | virtual | - | 100.x.x.x/32 |

### Primary IP: 192.168.1.100

### Docker Containers Registered (if applicable)
**Cluster:** <cluster_name> (ID: <cluster_id>)

| Container | Role | vCPUs | Memory | Status |
|-----------|------|-------|--------|--------|
| media_jellyfin | Media Server | 2.0 | 2048MB | Active |
| media_sonarr | Media Management | 1.0 | 512MB | Active |

### Next Steps
- Run `/cmdb-sync` periodically to keep data current
- Run `/cmdb-audit` to check data quality
- Add tags for classification (env:*, team:*, etc.)
```

## Error Handling

- **Device already exists:** Suggest `/cmdb-sync` or ask to proceed
- **Site not found:** List available sites, offer to create new
- **Docker not available:** Skip container registration, note in summary
- **Permission denied:** Note which operations failed, suggest fixes

## User Request

$ARGUMENTS
