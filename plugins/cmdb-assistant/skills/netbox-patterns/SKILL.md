---
description: NetBox best practices for data quality and consistency based on official NetBox Labs guidelines
---

# NetBox Best Practices Skill

Reference documentation for proper NetBox data modeling, following official NetBox Labs guidelines.

## CRITICAL: Dependency Order

Objects must be created in this order due to foreign key dependencies. Creating objects out of order results in validation errors.

```
1. ORGANIZATION (no dependencies)
   ├── Tenant Groups
   ├── Tenants (optional: Tenant Group)
   ├── Regions
   ├── Site Groups
   └── Tags

2. SITES AND LOCATIONS
   ├── Sites (optional: Region, Site Group, Tenant)
   └── Locations (requires: Site, optional: parent Location)

3. DCIM PREREQUISITES
   ├── Manufacturers
   ├── Device Types (requires: Manufacturer)
   ├── Platforms
   ├── Device Roles
   └── Rack Roles

4. RACKS
   └── Racks (requires: Site, optional: Location, Rack Role, Tenant)

5. DEVICES
   ├── Devices (requires: Device Type, Role, Site; optional: Rack, Location)
   └── Interfaces (requires: Device)

6. VIRTUALIZATION
   ├── Cluster Types
   ├── Cluster Groups
   ├── Clusters (requires: Cluster Type, optional: Site)
   ├── Virtual Machines (requires: Cluster OR Site)
   └── VM Interfaces (requires: Virtual Machine)

7. IPAM
   ├── VRFs (optional: Tenant)
   ├── Prefixes (optional: VRF, Site, Tenant)
   ├── IP Addresses (optional: VRF, Tenant, Interface)
   └── VLANs (optional: Site, Tenant)

8. CONNECTIONS (last)
   └── Cables (requires: endpoints)
```

**Key Rule:** NEVER create a VM before its cluster exists. NEVER create a device before its site exists.

## HIGH: Site Assignment

**All infrastructure objects should have a site:**

| Object Type | Site Requirement |
|-------------|------------------|
| Devices | **REQUIRED** |
| Racks | **REQUIRED** |
| VMs | RECOMMENDED (via cluster or direct) |
| Clusters | RECOMMENDED |
| Prefixes | RECOMMENDED |
| VLANs | RECOMMENDED |

**Why Sites Matter:**
- Location-based queries and filtering
- Power and capacity budgeting
- Physical inventory tracking
- Compliance and audit requirements

## HIGH: Tenant Usage

Use tenants for logical resource separation:

**When to Use Tenants:**
- Multi-team environments (assign resources to teams)
- Multi-customer scenarios (MSP, hosting)
- Cost allocation requirements
- Access control boundaries

**Apply Tenants To:**
- Sites (who owns the physical location)
- Devices (who operates the hardware)
- VMs (who owns the workload)
- Prefixes (who owns the IP space)
- VLANs (who owns the network segment)

## HIGH: Platform Tracking

Platforms track OS/runtime information for automation and lifecycle management.

**Platform Examples:**
| Device Type | Platform Examples |
|-------------|-------------------|
| Servers | Ubuntu 24.04, Windows Server 2022, RHEL 9 |
| Network | Cisco IOS 17.x, Junos 23.x, Arista EOS |
| Raspberry Pi | Raspberry Pi OS (Bookworm), Ubuntu Server ARM |
| Containers | Docker Container (as runtime indicator) |

**Benefits:**
- Vulnerability tracking (CVE correlation)
- Configuration management integration
- Lifecycle management (EOL tracking)
- Automation targeting

## MEDIUM: Tag Conventions

Use tags for cross-cutting classification that spans object types.

**Recommended Tag Patterns:**

| Pattern | Purpose | Examples |
|---------|---------|----------|
| `env:*` | Environment classification | `env:production`, `env:staging`, `env:development` |
| `app:*` | Application grouping | `app:web`, `app:database`, `app:monitoring` |
| `team:*` | Ownership | `team:platform`, `team:infra`, `team:devops` |
| `backup:*` | Backup policy | `backup:daily`, `backup:weekly`, `backup:none` |
| `monitoring:*` | Monitoring level | `monitoring:critical`, `monitoring:standard` |

**Tags vs Custom Fields:**
- Tags: Cross-object classification, multiple values, filtering
- Custom Fields: Object-specific structured data, single values, reporting

## MEDIUM: Naming Conventions

Consistent naming improves searchability and automation compatibility.

**Recommended Patterns:**

| Object Type | Pattern | Examples |
|-------------|---------|----------|
| Devices | `{role}-{location}-{number}` | `web-dc1-01`, `db-cloud-02`, `fw-home-01` |
| VMs | `{env}-{app}-{number}` | `prod-api-01`, `dev-worker-03` |
| Clusters | `{site}-{type}` | `dc1-vmware`, `home-docker` |
| Prefixes | Include purpose in description | "Production web tier /24" |
| VLANs | `{site}-{function}` | `dc1-mgmt`, `home-iot` |

**Avoid:**
- Inconsistent casing (mixing `HotServ` and `hotserv`)
- Mixed separators (mixing `hhl_cluster` and `media-cluster`)
- Generic names without context (`server1`, `vm2`)
- Special characters other than hyphen

## MEDIUM: Role Consolidation

Avoid role fragmentation - use general roles with platform/tags for specificity.

**Instead of:**
```
nginx-web-server
apache-web-server
web-server-frontend
web-server-api
```

**Use:**
```
web-server (role) + platform (nginx/apache) + tags (frontend, api)
```

**Recommended Role Categories:**

| Category | Roles |
|----------|-------|
| Infrastructure | `hypervisor`, `storage-server`, `network-device`, `firewall` |
| Compute | `application-server`, `database-server`, `web-server`, `api-server` |
| Services | `container-host`, `load-balancer`, `monitoring-server`, `backup-server` |
| Development | `development-workstation`, `ci-runner`, `build-server` |
| Containers | `reverse-proxy`, `database`, `cache`, `queue`, `worker` |

## Docker Containers as VMs

NetBox's Virtualization module can model Docker containers:

**Approach:**
1. Create device for physical Docker host
2. Create cluster (type: "Docker Compose" or "Docker Swarm")
3. Associate cluster with host device
4. Create VMs for each container in the cluster

**VM Fields for Containers:**
- `name`: Container name (e.g., `media_jellyfin`)
- `role`: Container function (e.g., `Media Server`)
- `vcpus`: CPU limit/shares
- `memory`: Memory limit (MB)
- `disk`: Volume size estimate
- `description`: Container purpose
- `comments`: Image, ports, volumes, dependencies

**This is a pragmatic modeling choice** - containers aren't VMs, but the Virtualization module is the closest fit for tracking container workloads.

## Primary IP Workflow

To set a device/VM's primary IP:

1. Create interface on device/VM
2. Create IP address assigned to interface
3. Set IP as `primary_ip4` or `primary_ip6` on device/VM

**Why Primary IP Matters:**
- Used for device connectivity checks
- Displayed in device list views
- Used by automation tools (NAPALM, Ansible)
- Required for many integrations

## Data Quality Checklist

Before closing a sprint or audit:

- [ ] All VMs have site assignment (direct or via cluster)
- [ ] All VMs have tenant assignment
- [ ] All active devices have platform
- [ ] All active devices have primary IP
- [ ] Naming follows conventions
- [ ] No orphaned prefixes (allocated but unused)
- [ ] Tags applied consistently
- [ ] Clusters scoped to sites
- [ ] Roles not overly fragmented

## MCP Tool Reference

**Dependency Order for Creation:**
```
1. dcim_create_site
2. dcim_create_manufacturer
3. dcim_create_device_type
4. dcim_create_device_role
5. dcim_create_platform
6. dcim_create_device
7. virt_create_cluster_type
8. virt_create_cluster
9. virt_create_vm
10. dcim_create_interface / virt_create_vm_interface
11. ipam_create_ip_address
12. dcim_update_device (set primary_ip4)
```

**Lookup Before Create:**
Always check if object exists before creating to avoid duplicates:
```
1. dcim_list_devices name=<hostname>
2. If exists, update; if not, create
```
