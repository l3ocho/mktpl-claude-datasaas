"""
IPAM (IP Address Management) tools for NetBox MCP Server.

Covers: IP Addresses, Prefixes, VLANs, VRFs, ASNs, and related models.
"""
import logging
from typing import List, Dict, Optional, Any
from ..netbox_client import NetBoxClient

logger = logging.getLogger(__name__)


class IPAMTools:
    """Tools for IPAM operations in NetBox"""

    def __init__(self, client: NetBoxClient):
        self.client = client
        self.base_endpoint = 'ipam'

    # ==================== ASN Ranges ====================

    async def list_asn_ranges(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all ASN ranges."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/asn-ranges', params=params)

    async def get_asn_range(self, id: int) -> Dict:
        """Get a specific ASN range by ID."""
        return self.client.get(f'{self.base_endpoint}/asn-ranges', id)

    async def create_asn_range(self, name: str, slug: str, rir: int, start: int, end: int, **kwargs) -> Dict:
        """Create a new ASN range."""
        data = {'name': name, 'slug': slug, 'rir': rir, 'start': start, 'end': end, **kwargs}
        return self.client.create(f'{self.base_endpoint}/asn-ranges', data)

    async def update_asn_range(self, id: int, **kwargs) -> Dict:
        """Update an ASN range."""
        return self.client.patch(f'{self.base_endpoint}/asn-ranges', id, kwargs)

    async def delete_asn_range(self, id: int) -> None:
        """Delete an ASN range."""
        self.client.delete(f'{self.base_endpoint}/asn-ranges', id)

    # ==================== ASNs ====================

    async def list_asns(
        self,
        asn: Optional[int] = None,
        rir_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all ASNs."""
        params = {k: v for k, v in {
            'asn': asn, 'rir_id': rir_id, 'tenant_id': tenant_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/asns', params=params)

    async def get_asn(self, id: int) -> Dict:
        """Get a specific ASN by ID."""
        return self.client.get(f'{self.base_endpoint}/asns', id)

    async def create_asn(
        self,
        asn: int,
        rir: int,
        tenant: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new ASN."""
        data = {'asn': asn, 'rir': rir, **kwargs}
        if tenant:
            data['tenant'] = tenant
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/asns', data)

    async def update_asn(self, id: int, **kwargs) -> Dict:
        """Update an ASN."""
        return self.client.patch(f'{self.base_endpoint}/asns', id, kwargs)

    async def delete_asn(self, id: int) -> None:
        """Delete an ASN."""
        self.client.delete(f'{self.base_endpoint}/asns', id)

    # ==================== RIRs ====================

    async def list_rirs(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all RIRs (Regional Internet Registries)."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/rirs', params=params)

    async def get_rir(self, id: int) -> Dict:
        """Get a specific RIR by ID."""
        return self.client.get(f'{self.base_endpoint}/rirs', id)

    async def create_rir(self, name: str, slug: str, is_private: bool = False, **kwargs) -> Dict:
        """Create a new RIR."""
        data = {'name': name, 'slug': slug, 'is_private': is_private, **kwargs}
        return self.client.create(f'{self.base_endpoint}/rirs', data)

    async def update_rir(self, id: int, **kwargs) -> Dict:
        """Update a RIR."""
        return self.client.patch(f'{self.base_endpoint}/rirs', id, kwargs)

    async def delete_rir(self, id: int) -> None:
        """Delete a RIR."""
        self.client.delete(f'{self.base_endpoint}/rirs', id)

    # ==================== Aggregates ====================

    async def list_aggregates(
        self,
        prefix: Optional[str] = None,
        rir_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all aggregates."""
        params = {k: v for k, v in {
            'prefix': prefix, 'rir_id': rir_id, 'tenant_id': tenant_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/aggregates', params=params)

    async def get_aggregate(self, id: int) -> Dict:
        """Get a specific aggregate by ID."""
        return self.client.get(f'{self.base_endpoint}/aggregates', id)

    async def create_aggregate(
        self,
        prefix: str,
        rir: int,
        tenant: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new aggregate."""
        data = {'prefix': prefix, 'rir': rir, **kwargs}
        if tenant:
            data['tenant'] = tenant
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/aggregates', data)

    async def update_aggregate(self, id: int, **kwargs) -> Dict:
        """Update an aggregate."""
        return self.client.patch(f'{self.base_endpoint}/aggregates', id, kwargs)

    async def delete_aggregate(self, id: int) -> None:
        """Delete an aggregate."""
        self.client.delete(f'{self.base_endpoint}/aggregates', id)

    # ==================== Roles ====================

    async def list_roles(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all IPAM roles."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/roles', params=params)

    async def get_role(self, id: int) -> Dict:
        """Get a specific role by ID."""
        return self.client.get(f'{self.base_endpoint}/roles', id)

    async def create_role(self, name: str, slug: str, weight: int = 1000, **kwargs) -> Dict:
        """Create a new IPAM role."""
        data = {'name': name, 'slug': slug, 'weight': weight, **kwargs}
        return self.client.create(f'{self.base_endpoint}/roles', data)

    async def update_role(self, id: int, **kwargs) -> Dict:
        """Update a role."""
        return self.client.patch(f'{self.base_endpoint}/roles', id, kwargs)

    async def delete_role(self, id: int) -> None:
        """Delete a role."""
        self.client.delete(f'{self.base_endpoint}/roles', id)

    # ==================== Prefixes ====================

    async def list_prefixes(
        self,
        prefix: Optional[str] = None,
        site_id: Optional[int] = None,
        vrf_id: Optional[int] = None,
        vlan_id: Optional[int] = None,
        role_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        status: Optional[str] = None,
        family: Optional[int] = None,
        is_pool: Optional[bool] = None,
        within: Optional[str] = None,
        within_include: Optional[str] = None,
        contains: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all prefixes with optional filtering."""
        params = {k: v for k, v in {
            'prefix': prefix, 'site_id': site_id, 'vrf_id': vrf_id,
            'vlan_id': vlan_id, 'role_id': role_id, 'tenant_id': tenant_id,
            'status': status, 'family': family, 'is_pool': is_pool,
            'within': within, 'within_include': within_include, 'contains': contains, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/prefixes', params=params)

    async def get_prefix(self, id: int) -> Dict:
        """Get a specific prefix by ID."""
        return self.client.get(f'{self.base_endpoint}/prefixes', id)

    async def create_prefix(
        self,
        prefix: str,
        status: str = 'active',
        site: Optional[int] = None,
        vrf: Optional[int] = None,
        vlan: Optional[int] = None,
        role: Optional[int] = None,
        tenant: Optional[int] = None,
        is_pool: bool = False,
        mark_utilized: bool = False,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new prefix."""
        data = {'prefix': prefix, 'status': status, 'is_pool': is_pool, 'mark_utilized': mark_utilized, **kwargs}
        for key, val in [
            ('site', site), ('vrf', vrf), ('vlan', vlan),
            ('role', role), ('tenant', tenant), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/prefixes', data)

    async def update_prefix(self, id: int, **kwargs) -> Dict:
        """Update a prefix."""
        return self.client.patch(f'{self.base_endpoint}/prefixes', id, kwargs)

    async def delete_prefix(self, id: int) -> None:
        """Delete a prefix."""
        self.client.delete(f'{self.base_endpoint}/prefixes', id)

    async def list_available_prefixes(self, id: int) -> List[Dict]:
        """List available child prefixes within a prefix."""
        return self.client.list(f'{self.base_endpoint}/prefixes/{id}/available-prefixes', paginate=False)

    async def create_available_prefix(self, id: int, prefix_length: int, **kwargs) -> Dict:
        """Create a new prefix from available space."""
        data = {'prefix_length': prefix_length, **kwargs}
        return self.client.create(f'{self.base_endpoint}/prefixes/{id}/available-prefixes', data)

    async def list_available_ips(self, id: int) -> List[Dict]:
        """List available IP addresses within a prefix."""
        return self.client.list(f'{self.base_endpoint}/prefixes/{id}/available-ips', paginate=False)

    async def create_available_ip(self, id: int, **kwargs) -> Dict:
        """Create a new IP address from available space in prefix."""
        return self.client.create(f'{self.base_endpoint}/prefixes/{id}/available-ips', kwargs)

    # ==================== IP Ranges ====================

    async def list_ip_ranges(
        self,
        start_address: Optional[str] = None,
        end_address: Optional[str] = None,
        vrf_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all IP ranges."""
        params = {k: v for k, v in {
            'start_address': start_address, 'end_address': end_address,
            'vrf_id': vrf_id, 'tenant_id': tenant_id, 'status': status, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/ip-ranges', params=params)

    async def get_ip_range(self, id: int) -> Dict:
        """Get a specific IP range by ID."""
        return self.client.get(f'{self.base_endpoint}/ip-ranges', id)

    async def create_ip_range(
        self,
        start_address: str,
        end_address: str,
        status: str = 'active',
        vrf: Optional[int] = None,
        tenant: Optional[int] = None,
        role: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new IP range."""
        data = {'start_address': start_address, 'end_address': end_address, 'status': status, **kwargs}
        for key, val in [('vrf', vrf), ('tenant', tenant), ('role', role), ('description', description)]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/ip-ranges', data)

    async def update_ip_range(self, id: int, **kwargs) -> Dict:
        """Update an IP range."""
        return self.client.patch(f'{self.base_endpoint}/ip-ranges', id, kwargs)

    async def delete_ip_range(self, id: int) -> None:
        """Delete an IP range."""
        self.client.delete(f'{self.base_endpoint}/ip-ranges', id)

    async def list_available_ips_in_range(self, id: int) -> List[Dict]:
        """List available IP addresses within an IP range."""
        return self.client.list(f'{self.base_endpoint}/ip-ranges/{id}/available-ips', paginate=False)

    # ==================== IP Addresses ====================

    async def list_ip_addresses(
        self,
        address: Optional[str] = None,
        vrf_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        status: Optional[str] = None,
        role: Optional[str] = None,
        interface_id: Optional[int] = None,
        device_id: Optional[int] = None,
        virtual_machine_id: Optional[int] = None,
        family: Optional[int] = None,
        parent: Optional[str] = None,
        dns_name: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all IP addresses with optional filtering."""
        params = {k: v for k, v in {
            'address': address, 'vrf_id': vrf_id, 'tenant_id': tenant_id,
            'status': status, 'role': role, 'interface_id': interface_id,
            'device_id': device_id, 'virtual_machine_id': virtual_machine_id,
            'family': family, 'parent': parent, 'dns_name': dns_name, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/ip-addresses', params=params)

    async def get_ip_address(self, id: int) -> Dict:
        """Get a specific IP address by ID."""
        return self.client.get(f'{self.base_endpoint}/ip-addresses', id)

    async def create_ip_address(
        self,
        address: str,
        status: str = 'active',
        vrf: Optional[int] = None,
        tenant: Optional[int] = None,
        role: Optional[str] = None,
        assigned_object_type: Optional[str] = None,
        assigned_object_id: Optional[int] = None,
        nat_inside: Optional[int] = None,
        dns_name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new IP address."""
        data = {'address': address, 'status': status, **kwargs}
        for key, val in [
            ('vrf', vrf), ('tenant', tenant), ('role', role),
            ('assigned_object_type', assigned_object_type),
            ('assigned_object_id', assigned_object_id),
            ('nat_inside', nat_inside), ('dns_name', dns_name),
            ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/ip-addresses', data)

    async def update_ip_address(self, id: int, **kwargs) -> Dict:
        """Update an IP address."""
        return self.client.patch(f'{self.base_endpoint}/ip-addresses', id, kwargs)

    async def delete_ip_address(self, id: int) -> None:
        """Delete an IP address."""
        self.client.delete(f'{self.base_endpoint}/ip-addresses', id)

    # ==================== FHRP Groups ====================

    async def list_fhrp_groups(
        self,
        protocol: Optional[str] = None,
        group_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all FHRP groups."""
        params = {k: v for k, v in {'protocol': protocol, 'group_id': group_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/fhrp-groups', params=params)

    async def get_fhrp_group(self, id: int) -> Dict:
        """Get a specific FHRP group by ID."""
        return self.client.get(f'{self.base_endpoint}/fhrp-groups', id)

    async def create_fhrp_group(
        self,
        protocol: str,
        group_id: int,
        auth_type: Optional[str] = None,
        auth_key: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new FHRP group."""
        data = {'protocol': protocol, 'group_id': group_id, **kwargs}
        if auth_type:
            data['auth_type'] = auth_type
        if auth_key:
            data['auth_key'] = auth_key
        return self.client.create(f'{self.base_endpoint}/fhrp-groups', data)

    async def update_fhrp_group(self, id: int, **kwargs) -> Dict:
        """Update an FHRP group."""
        return self.client.patch(f'{self.base_endpoint}/fhrp-groups', id, kwargs)

    async def delete_fhrp_group(self, id: int) -> None:
        """Delete an FHRP group."""
        self.client.delete(f'{self.base_endpoint}/fhrp-groups', id)

    # ==================== FHRP Group Assignments ====================

    async def list_fhrp_group_assignments(self, group_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all FHRP group assignments."""
        params = {k: v for k, v in {'group_id': group_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/fhrp-group-assignments', params=params)

    async def get_fhrp_group_assignment(self, id: int) -> Dict:
        """Get a specific FHRP group assignment by ID."""
        return self.client.get(f'{self.base_endpoint}/fhrp-group-assignments', id)

    async def create_fhrp_group_assignment(
        self,
        group: int,
        interface_type: str,
        interface_id: int,
        priority: int = 100,
        **kwargs
    ) -> Dict:
        """Create a new FHRP group assignment."""
        data = {
            'group': group, 'interface_type': interface_type,
            'interface_id': interface_id, 'priority': priority, **kwargs
        }
        return self.client.create(f'{self.base_endpoint}/fhrp-group-assignments', data)

    async def update_fhrp_group_assignment(self, id: int, **kwargs) -> Dict:
        """Update an FHRP group assignment."""
        return self.client.patch(f'{self.base_endpoint}/fhrp-group-assignments', id, kwargs)

    async def delete_fhrp_group_assignment(self, id: int) -> None:
        """Delete an FHRP group assignment."""
        self.client.delete(f'{self.base_endpoint}/fhrp-group-assignments', id)

    # ==================== VLAN Groups ====================

    async def list_vlan_groups(
        self,
        name: Optional[str] = None,
        site_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all VLAN groups."""
        params = {k: v for k, v in {'name': name, 'site_id': site_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/vlan-groups', params=params)

    async def get_vlan_group(self, id: int) -> Dict:
        """Get a specific VLAN group by ID."""
        return self.client.get(f'{self.base_endpoint}/vlan-groups', id)

    async def create_vlan_group(
        self,
        name: str,
        slug: str,
        scope_type: Optional[str] = None,
        scope_id: Optional[int] = None,
        min_vid: int = 1,
        max_vid: int = 4094,
        **kwargs
    ) -> Dict:
        """Create a new VLAN group."""
        data = {'name': name, 'slug': slug, 'min_vid': min_vid, 'max_vid': max_vid, **kwargs}
        if scope_type:
            data['scope_type'] = scope_type
        if scope_id:
            data['scope_id'] = scope_id
        return self.client.create(f'{self.base_endpoint}/vlan-groups', data)

    async def update_vlan_group(self, id: int, **kwargs) -> Dict:
        """Update a VLAN group."""
        return self.client.patch(f'{self.base_endpoint}/vlan-groups', id, kwargs)

    async def delete_vlan_group(self, id: int) -> None:
        """Delete a VLAN group."""
        self.client.delete(f'{self.base_endpoint}/vlan-groups', id)

    async def list_available_vlans(self, id: int) -> List[Dict]:
        """List available VLANs in a VLAN group."""
        return self.client.list(f'{self.base_endpoint}/vlan-groups/{id}/available-vlans', paginate=False)

    # ==================== VLANs ====================

    async def list_vlans(
        self,
        vid: Optional[int] = None,
        name: Optional[str] = None,
        site_id: Optional[int] = None,
        group_id: Optional[int] = None,
        role_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all VLANs with optional filtering."""
        params = {k: v for k, v in {
            'vid': vid, 'name': name, 'site_id': site_id, 'group_id': group_id,
            'role_id': role_id, 'tenant_id': tenant_id, 'status': status, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/vlans', params=params)

    async def get_vlan(self, id: int) -> Dict:
        """Get a specific VLAN by ID."""
        return self.client.get(f'{self.base_endpoint}/vlans', id)

    async def create_vlan(
        self,
        vid: int,
        name: str,
        status: str = 'active',
        site: Optional[int] = None,
        group: Optional[int] = None,
        role: Optional[int] = None,
        tenant: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new VLAN."""
        data = {'vid': vid, 'name': name, 'status': status, **kwargs}
        for key, val in [
            ('site', site), ('group', group), ('role', role),
            ('tenant', tenant), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/vlans', data)

    async def update_vlan(self, id: int, **kwargs) -> Dict:
        """Update a VLAN."""
        return self.client.patch(f'{self.base_endpoint}/vlans', id, kwargs)

    async def delete_vlan(self, id: int) -> None:
        """Delete a VLAN."""
        self.client.delete(f'{self.base_endpoint}/vlans', id)

    # ==================== VRFs ====================

    async def list_vrfs(
        self,
        name: Optional[str] = None,
        rd: Optional[str] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all VRFs with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'rd': rd, 'tenant_id': tenant_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/vrfs', params=params)

    async def get_vrf(self, id: int) -> Dict:
        """Get a specific VRF by ID."""
        return self.client.get(f'{self.base_endpoint}/vrfs', id)

    async def create_vrf(
        self,
        name: str,
        rd: Optional[str] = None,
        tenant: Optional[int] = None,
        enforce_unique: bool = True,
        description: Optional[str] = None,
        import_targets: Optional[List[int]] = None,
        export_targets: Optional[List[int]] = None,
        **kwargs
    ) -> Dict:
        """Create a new VRF."""
        data = {'name': name, 'enforce_unique': enforce_unique, **kwargs}
        for key, val in [
            ('rd', rd), ('tenant', tenant), ('description', description),
            ('import_targets', import_targets), ('export_targets', export_targets)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/vrfs', data)

    async def update_vrf(self, id: int, **kwargs) -> Dict:
        """Update a VRF."""
        return self.client.patch(f'{self.base_endpoint}/vrfs', id, kwargs)

    async def delete_vrf(self, id: int) -> None:
        """Delete a VRF."""
        self.client.delete(f'{self.base_endpoint}/vrfs', id)

    # ==================== Route Targets ====================

    async def list_route_targets(
        self,
        name: Optional[str] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all route targets."""
        params = {k: v for k, v in {'name': name, 'tenant_id': tenant_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/route-targets', params=params)

    async def get_route_target(self, id: int) -> Dict:
        """Get a specific route target by ID."""
        return self.client.get(f'{self.base_endpoint}/route-targets', id)

    async def create_route_target(
        self,
        name: str,
        tenant: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new route target."""
        data = {'name': name, **kwargs}
        if tenant:
            data['tenant'] = tenant
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/route-targets', data)

    async def update_route_target(self, id: int, **kwargs) -> Dict:
        """Update a route target."""
        return self.client.patch(f'{self.base_endpoint}/route-targets', id, kwargs)

    async def delete_route_target(self, id: int) -> None:
        """Delete a route target."""
        self.client.delete(f'{self.base_endpoint}/route-targets', id)

    # ==================== Services ====================

    async def list_services(
        self,
        device_id: Optional[int] = None,
        virtual_machine_id: Optional[int] = None,
        name: Optional[str] = None,
        protocol: Optional[str] = None,
        port: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all services."""
        params = {k: v for k, v in {
            'device_id': device_id, 'virtual_machine_id': virtual_machine_id,
            'name': name, 'protocol': protocol, 'port': port, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/services', params=params)

    async def get_service(self, id: int) -> Dict:
        """Get a specific service by ID."""
        return self.client.get(f'{self.base_endpoint}/services', id)

    async def create_service(
        self,
        name: str,
        ports: List[int],
        protocol: str,
        device: Optional[int] = None,
        virtual_machine: Optional[int] = None,
        ipaddresses: Optional[List[int]] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new service."""
        data = {'name': name, 'ports': ports, 'protocol': protocol, **kwargs}
        for key, val in [
            ('device', device), ('virtual_machine', virtual_machine),
            ('ipaddresses', ipaddresses), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/services', data)

    async def update_service(self, id: int, **kwargs) -> Dict:
        """Update a service."""
        return self.client.patch(f'{self.base_endpoint}/services', id, kwargs)

    async def delete_service(self, id: int) -> None:
        """Delete a service."""
        self.client.delete(f'{self.base_endpoint}/services', id)

    # ==================== Service Templates ====================

    async def list_service_templates(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all service templates."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/service-templates', params=params)

    async def get_service_template(self, id: int) -> Dict:
        """Get a specific service template by ID."""
        return self.client.get(f'{self.base_endpoint}/service-templates', id)

    async def create_service_template(
        self,
        name: str,
        ports: List[int],
        protocol: str,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new service template."""
        data = {'name': name, 'ports': ports, 'protocol': protocol, **kwargs}
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/service-templates', data)

    async def update_service_template(self, id: int, **kwargs) -> Dict:
        """Update a service template."""
        return self.client.patch(f'{self.base_endpoint}/service-templates', id, kwargs)

    async def delete_service_template(self, id: int) -> None:
        """Delete a service template."""
        self.client.delete(f'{self.base_endpoint}/service-templates', id)
