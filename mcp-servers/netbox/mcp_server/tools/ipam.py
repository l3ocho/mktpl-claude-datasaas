"""
IPAM (IP Address Management) tools for NetBox MCP Server.

Covers: IP Addresses, Prefixes, and Services only.
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
