## Infrastructure Management (cmdb-assistant)

This project uses the **cmdb-assistant** plugin for NetBox CMDB integration to manage network infrastructure.

### Available Commands

| Command | Description |
|---------|-------------|
| `/cmdb-search` | Search across all NetBox objects |
| `/cmdb-device` | Manage devices (create, update, list) |
| `/cmdb-ip` | Manage IP addresses and prefixes |
| `/cmdb-site` | Manage sites and locations |

### MCP Tools Available

The following NetBox MCP tools are available for infrastructure management:

**DCIM (Data Center Infrastructure Management):**
- `dcim_list_devices`, `dcim_get_device`, `dcim_create_device`, `dcim_update_device` - Device management
- `dcim_list_sites`, `dcim_get_site`, `dcim_create_site` - Site management
- `dcim_list_racks`, `dcim_get_rack`, `dcim_create_rack` - Rack management
- `dcim_list_interfaces`, `dcim_create_interface` - Interface management
- `dcim_list_cables`, `dcim_create_cable` - Cable management
- `dcim_list_device_types`, `dcim_list_device_roles`, `dcim_list_manufacturers` - Reference data
- `dcim_list_regions`, `dcim_list_locations` - Location hierarchy

**IPAM (IP Address Management):**
- `ipam_list_ip_addresses`, `ipam_create_ip_address`, `ipam_get_ip_address` - IP address management
- `ipam_list_prefixes`, `ipam_create_prefix`, `ipam_list_available_prefixes` - Prefix management
- `ipam_list_vlans`, `ipam_create_vlan` - VLAN management
- `ipam_list_vrfs`, `ipam_create_vrf` - VRF management
- `ipam_list_available_ips`, `ipam_create_available_ip` - IP allocation

**Virtualization:**
- `virtualization_list_virtual_machines`, `virtualization_create_virtual_machine` - VM management
- `virtualization_list_clusters`, `virtualization_create_cluster` - Cluster management
- `virtualization_list_vm_interfaces` - VM interface management

**Circuits:**
- `circuits_list_circuits`, `circuits_create_circuit` - Circuit management
- `circuits_list_providers`, `circuits_create_provider` - Provider management

**Tenancy:**
- `tenancy_list_tenants`, `tenancy_create_tenant` - Tenant management
- `tenancy_list_contacts`, `tenancy_create_contact` - Contact management

**Extras:**
- `extras_list_tags`, `extras_create_tag` - Tag management
- `extras_list_journal_entries`, `extras_create_journal_entry` - Audit journal
- `extras_list_object_changes` - Change tracking

### Usage Guidelines

- Use NetBox MCP tools for all infrastructure queries and modifications
- Always verify device/IP existence before creating duplicates
- Use tags for categorization and filtering
- Create journal entries for significant changes to maintain audit trail
- Check available IPs in a prefix before manual allocation
