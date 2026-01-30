# NetBox MCP Tools Reference

Complete reference for NetBox MCP tools organized by category.

## DCIM (Data Center Infrastructure Management)

### Sites and Locations
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dcim_list_sites` | List all sites | `name`, `status`, `region_id` |
| `dcim_get_site` | Get site details | `id` |
| `dcim_create_site` | Create new site | `name`, `slug`, `status` |
| `dcim_update_site` | Update site | `id`, fields to update |
| `dcim_delete_site` | Delete site | `id` |
| `dcim_list_locations` | List locations within sites | `site_id`, `parent_id` |
| `dcim_get_location` | Get location details | `id` |
| `dcim_create_location` | Create location | `name`, `slug`, `site` |
| `dcim_update_location` | Update location | `id`, fields to update |
| `dcim_delete_location` | Delete location | `id` |
| `dcim_list_regions` | List regions | `name` |
| `dcim_get_region` | Get region details | `id` |
| `dcim_create_region` | Create region | `name`, `slug` |
| `dcim_update_region` | Update region | `id`, fields to update |
| `dcim_delete_region` | Delete region | `id` |

### Racks
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dcim_list_racks` | List racks | `site_id`, `location_id`, `name` |
| `dcim_get_rack` | Get rack details | `id` |
| `dcim_create_rack` | Create rack | `name`, `site`, `u_height` |
| `dcim_update_rack` | Update rack | `id`, fields to update |
| `dcim_delete_rack` | Delete rack | `id` |

### Devices
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dcim_list_devices` | List devices | `name`, `site_id`, `role_id`, `status` |
| `dcim_get_device` | Get device details | `id` |
| `dcim_create_device` | Create device | `name`, `device_type`, `role`, `site` |
| `dcim_update_device` | Update device | `id`, `primary_ip4`, etc. |
| `dcim_delete_device` | Delete device | `id` |

### Device Types and Roles
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dcim_list_device_types` | List device types | `manufacturer_id`, `model` |
| `dcim_get_device_type` | Get type details | `id` |
| `dcim_create_device_type` | Create device type | `manufacturer`, `model`, `slug` |
| `dcim_update_device_type` | Update device type | `id`, fields |
| `dcim_delete_device_type` | Delete device type | `id` |
| `dcim_list_device_roles` | List device roles | `name` |
| `dcim_get_device_role` | Get role details | `id` |
| `dcim_create_device_role` | Create device role | `name`, `slug` |
| `dcim_update_device_role` | Update device role | `id`, fields |
| `dcim_delete_device_role` | Delete device role | `id` |

### Manufacturers and Platforms
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dcim_list_manufacturers` | List manufacturers | `name` |
| `dcim_get_manufacturer` | Get manufacturer details | `id` |
| `dcim_create_manufacturer` | Create manufacturer | `name`, `slug` |
| `dcim_update_manufacturer` | Update manufacturer | `id`, fields |
| `dcim_delete_manufacturer` | Delete manufacturer | `id` |
| `dcim_list_platforms` | List platforms | `name` |
| `dcim_get_platform` | Get platform details | `id` |
| `dcim_create_platform` | Create platform | `name`, `slug` |
| `dcim_update_platform` | Update platform | `id`, fields |
| `dcim_delete_platform` | Delete platform | `id` |

### Interfaces and Cables
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dcim_list_interfaces` | List interfaces | `device_id`, `name`, `type` |
| `dcim_get_interface` | Get interface details | `id` |
| `dcim_create_interface` | Create interface | `device`, `name`, `type` |
| `dcim_update_interface` | Update interface | `id`, `enabled`, `mac_address` |
| `dcim_delete_interface` | Delete interface | `id` |
| `dcim_list_cables` | List cables | `device_id`, `site_id` |
| `dcim_get_cable` | Get cable details | `id` |
| `dcim_create_cable` | Create cable | `a_terminations`, `b_terminations` |
| `dcim_update_cable` | Update cable | `id`, fields |
| `dcim_delete_cable` | Delete cable | `id` |

### Power
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dcim_list_power_panels` | List power panels | `site_id` |
| `dcim_get_power_panel` | Get panel details | `id` |
| `dcim_create_power_panel` | Create power panel | `name`, `site` |
| `dcim_list_power_feeds` | List power feeds | `power_panel_id` |
| `dcim_get_power_feed` | Get feed details | `id` |
| `dcim_create_power_feed` | Create power feed | `name`, `power_panel`, `supply` |

### Other DCIM
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dcim_list_virtual_chassis` | List virtual chassis | (varies) |
| `dcim_get_virtual_chassis` | Get virtual chassis | `id` |
| `dcim_list_inventory_items` | List inventory items | `device_id` |
| `dcim_get_inventory_item` | Get inventory item | `id` |

## IPAM (IP Address Management)

### Prefixes
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `ipam_list_prefixes` | List prefixes | `prefix`, `vrf_id`, `within`, `contains` |
| `ipam_get_prefix` | Get prefix details | `id` |
| `ipam_create_prefix` | Create prefix | `prefix`, `status`, `site`, `vrf` |
| `ipam_update_prefix` | Update prefix | `id`, `status`, etc. |
| `ipam_delete_prefix` | Delete prefix | `id` |
| `ipam_list_available_prefixes` | List available child prefixes | `prefix_id` |
| `ipam_create_available_prefix` | Allocate from parent | `prefix_id`, `prefix_length` |

### IP Addresses
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `ipam_list_ip_addresses` | List IP addresses | `address`, `vrf_id`, `device_id`, `status` |
| `ipam_get_ip_address` | Get IP details | `id` |
| `ipam_create_ip_address` | Create IP address | `address`, `assigned_object_type`, `assigned_object_id` |
| `ipam_update_ip_address` | Update IP address | `id`, `status`, etc. |
| `ipam_delete_ip_address` | Delete IP address | `id` |
| `ipam_list_available_ips` | List available IPs in prefix | `prefix_id` |
| `ipam_create_available_ip` | Allocate next available | `prefix_id` |

### VLANs and VRFs
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `ipam_list_vlans` | List VLANs | `vid`, `name`, `site_id` |
| `ipam_get_vlan` | Get VLAN details | `id` |
| `ipam_create_vlan` | Create VLAN | `vid`, `name`, `site` |
| `ipam_update_vlan` | Update VLAN | `id`, fields |
| `ipam_delete_vlan` | Delete VLAN | `id` |
| `ipam_list_vlan_groups` | List VLAN groups | `site_id` |
| `ipam_get_vlan_group` | Get VLAN group | `id` |
| `ipam_create_vlan_group` | Create VLAN group | `name`, `slug`, `scope_type` |
| `ipam_list_vrfs` | List VRFs | `name` |
| `ipam_get_vrf` | Get VRF details | `id` |
| `ipam_create_vrf` | Create VRF | `name`, `rd` |
| `ipam_update_vrf` | Update VRF | `id`, fields |
| `ipam_delete_vrf` | Delete VRF | `id` |

### Other IPAM
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `ipam_list_asns` | List ASNs | (varies) |
| `ipam_get_asn` | Get ASN details | `id` |
| `ipam_create_asn` | Create ASN | `asn`, `rir` |
| `ipam_list_rirs` | List RIRs | `name` |
| `ipam_get_rir` | Get RIR details | `id` |
| `ipam_list_aggregates` | List aggregates | `prefix`, `rir_id` |
| `ipam_get_aggregate` | Get aggregate | `id` |
| `ipam_create_aggregate` | Create aggregate | `prefix`, `rir` |
| `ipam_list_services` | List services | `device_id`, `name` |
| `ipam_get_service` | Get service details | `id` |
| `ipam_create_service` | Create service | `name`, `ports`, `protocol` |

## Virtualization

### Clusters
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `virt_list_cluster_types` | List cluster types | `name` |
| `virt_get_cluster_type` | Get cluster type | `id` |
| `virt_create_cluster_type` | Create cluster type | `name`, `slug` |
| `virt_list_cluster_groups` | List cluster groups | `name` |
| `virt_get_cluster_group` | Get cluster group | `id` |
| `virt_create_cluster_group` | Create cluster group | `name`, `slug` |
| `virt_list_clusters` | List clusters | `name`, `site_id`, `type_id` |
| `virt_get_cluster` | Get cluster details | `id` |
| `virt_create_cluster` | Create cluster | `name`, `type`, `site` |
| `virt_update_cluster` | Update cluster | `id`, fields |
| `virt_delete_cluster` | Delete cluster | `id` |

### Virtual Machines
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `virt_list_vms` | List VMs | `name`, `cluster_id`, `site_id`, `status` |
| `virt_get_vm` | Get VM details | `id` |
| `virt_create_vm` | Create VM | `name`, `cluster`, `site`, `status` |
| `virt_update_vm` | Update VM | `id`, `status`, etc. |
| `virt_delete_vm` | Delete VM | `id` |
| `virt_list_vm_ifaces` | List VM interfaces | `virtual_machine_id` |
| `virt_get_vm_iface` | Get VM interface | `id` |
| `virt_create_vm_iface` | Create VM interface | `virtual_machine`, `name` |

## Circuits

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `circuits_list_providers` | List providers | `name` |
| `circuits_get_provider` | Get provider | `id` |
| `circuits_create_provider` | Create provider | `name`, `slug` |
| `circuits_update_provider` | Update provider | `id`, fields |
| `circuits_delete_provider` | Delete provider | `id` |
| `circ_list_types` | List circuit types | `name` |
| `circ_get_type` | Get circuit type | `id` |
| `circ_create_type` | Create circuit type | `name`, `slug` |
| `circuits_list_circuits` | List circuits | `provider_id`, `type_id` |
| `circuits_get_circuit` | Get circuit | `id` |
| `circuits_create_circuit` | Create circuit | `cid`, `provider`, `type` |
| `circuits_update_circuit` | Update circuit | `id`, fields |
| `circuits_delete_circuit` | Delete circuit | `id` |
| `circ_list_terminations` | List terminations | `circuit_id` |
| `circ_get_termination` | Get termination | `id` |
| `circ_create_termination` | Create termination | `circuit`, `site`, `term_side` |

## Tenancy

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `tenancy_list_tenant_groups` | List tenant groups | `name` |
| `tenancy_get_tenant_group` | Get tenant group | `id` |
| `tenancy_create_tenant_group` | Create tenant group | `name`, `slug` |
| `tenancy_list_tenants` | List tenants | `name`, `group_id` |
| `tenancy_get_tenant` | Get tenant | `id` |
| `tenancy_create_tenant` | Create tenant | `name`, `slug` |
| `tenancy_update_tenant` | Update tenant | `id`, fields |
| `tenancy_delete_tenant` | Delete tenant | `id` |
| `tenancy_list_contacts` | List contacts | `name` |
| `tenancy_get_contact` | Get contact | `id` |
| `tenancy_create_contact` | Create contact | `name` |

## VPN

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `vpn_list_tunnels` | List VPN tunnels | `name` |
| `vpn_get_tunnel` | Get tunnel | `id` |
| `vpn_create_tunnel` | Create tunnel | `name`, `status` |
| `vpn_list_l2vpns` | List L2VPNs | `name` |
| `vpn_get_l2vpn` | Get L2VPN | `id` |
| `vpn_create_l2vpn` | Create L2VPN | `name`, `type` |
| `vpn_list_ike_policies` | List IKE policies | (varies) |
| `vpn_list_ipsec_policies` | List IPSec policies | (varies) |
| `vpn_list_ipsec_profiles` | List IPSec profiles | (varies) |

## Wireless

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `wlan_list_groups` | List WLAN groups | `name` |
| `wlan_get_group` | Get WLAN group | `id` |
| `wlan_create_group` | Create WLAN group | `name`, `slug` |
| `wlan_list_lans` | List WLANs | `ssid` |
| `wlan_get_lan` | Get WLAN | `id` |
| `wlan_create_lan` | Create WLAN | `ssid`, `group` |
| `wlan_list_links` | List wireless links | (varies) |
| `wlan_get_link` | Get wireless link | `id` |

## Extras

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `extras_list_tags` | List tags | `name` |
| `extras_get_tag` | Get tag | `id` |
| `extras_create_tag` | Create tag | `name`, `slug`, `color` |
| `extras_update_tag` | Update tag | `id`, fields |
| `extras_delete_tag` | Delete tag | `id` |
| `extras_list_custom_fields` | List custom fields | `name` |
| `extras_get_custom_field` | Get custom field | `id` |
| `extras_list_webhooks` | List webhooks | `name` |
| `extras_get_webhook` | Get webhook | `id` |
| `extras_list_journal_entries` | List journal entries | `assigned_object_type`, `assigned_object_id` |
| `extras_get_journal_entry` | Get journal entry | `id` |
| `extras_create_journal_entry` | Create journal entry | `assigned_object_type`, `assigned_object_id`, `comments` |
| `extras_list_object_changes` | List audit log | `user_id`, `changed_object_type`, `action` |
| `extras_get_object_change` | Get change details | `id` |
| `extras_list_config_contexts` | List config contexts | `name` |
| `extras_get_config_context` | Get config context | `id` |

## Common Object Types for Filtering

| Category | Object Types |
|----------|--------------|
| DCIM | `dcim.device`, `dcim.interface`, `dcim.site`, `dcim.rack`, `dcim.cable` |
| IPAM | `ipam.ipaddress`, `ipam.prefix`, `ipam.vlan`, `ipam.vrf` |
| Virtualization | `virtualization.virtualmachine`, `virtualization.cluster` |
| Tenancy | `tenancy.tenant`, `tenancy.contact` |
