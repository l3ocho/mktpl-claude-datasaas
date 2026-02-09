"""
Virtualization tools for NetBox MCP Server.

Covers: Clusters, Virtual Machines, and VM Interfaces only.
"""
import logging
from typing import List, Dict, Optional, Any
from ..netbox_client import NetBoxClient

logger = logging.getLogger(__name__)


class VirtualizationTools:
    """Tools for Virtualization operations in NetBox"""

    def __init__(self, client: NetBoxClient):
        self.client = client
        self.base_endpoint = 'virtualization'

    # ==================== Clusters ====================

    async def list_clusters(
        self,
        name: Optional[str] = None,
        type_id: Optional[int] = None,
        group_id: Optional[int] = None,
        site_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all clusters with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'type_id': type_id, 'group_id': group_id,
            'site_id': site_id, 'tenant_id': tenant_id, 'status': status, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/clusters', params=params)

    async def get_cluster(self, id: int) -> Dict:
        """Get a specific cluster by ID."""
        return self.client.get(f'{self.base_endpoint}/clusters', id)

    async def create_cluster(
        self,
        name: str,
        type: int,
        status: str = 'active',
        group: Optional[int] = None,
        site: Optional[int] = None,
        tenant: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new cluster."""
        data = {'name': name, 'type': type, 'status': status, **kwargs}
        for key, val in [
            ('group', group), ('site', site), ('tenant', tenant), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/clusters', data)

    # ==================== Virtual Machines ====================

    async def list_virtual_machines(
        self,
        name: Optional[str] = None,
        cluster_id: Optional[int] = None,
        site_id: Optional[int] = None,
        role_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all virtual machines with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'cluster_id': cluster_id, 'site_id': site_id,
            'role_id': role_id, 'tenant_id': tenant_id, 'platform_id': platform_id,
            'status': status, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/virtual-machines', params=params)

    async def get_virtual_machine(self, id: int) -> Dict:
        """Get a specific virtual machine by ID."""
        return self.client.get(f'{self.base_endpoint}/virtual-machines', id)

    async def create_virtual_machine(
        self,
        name: str,
        status: str = 'active',
        cluster: Optional[int] = None,
        site: Optional[int] = None,
        role: Optional[int] = None,
        tenant: Optional[int] = None,
        platform: Optional[int] = None,
        primary_ip4: Optional[int] = None,
        primary_ip6: Optional[int] = None,
        vcpus: Optional[float] = None,
        memory: Optional[int] = None,
        disk: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new virtual machine."""
        data = {'name': name, 'status': status, **kwargs}
        for key, val in [
            ('cluster', cluster), ('site', site), ('role', role),
            ('tenant', tenant), ('platform', platform),
            ('primary_ip4', primary_ip4), ('primary_ip6', primary_ip6),
            ('vcpus', vcpus), ('memory', memory), ('disk', disk),
            ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/virtual-machines', data)

    async def update_virtual_machine(self, id: int, **kwargs) -> Dict:
        """Update a virtual machine."""
        return self.client.patch(f'{self.base_endpoint}/virtual-machines', id, kwargs)

    # ==================== VM Interfaces ====================

    async def list_vm_interfaces(
        self,
        virtual_machine_id: Optional[int] = None,
        name: Optional[str] = None,
        enabled: Optional[bool] = None,
        **kwargs
    ) -> List[Dict]:
        """List all VM interfaces."""
        params = {k: v for k, v in {
            'virtual_machine_id': virtual_machine_id, 'name': name, 'enabled': enabled, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/interfaces', params=params)

    async def get_vm_interface(self, id: int) -> Dict:
        """Get a specific VM interface by ID."""
        return self.client.get(f'{self.base_endpoint}/interfaces', id)

    async def create_vm_interface(
        self,
        virtual_machine: int,
        name: str,
        enabled: bool = True,
        mtu: Optional[int] = None,
        mac_address: Optional[str] = None,
        description: Optional[str] = None,
        mode: Optional[str] = None,
        untagged_vlan: Optional[int] = None,
        tagged_vlans: Optional[List[int]] = None,
        **kwargs
    ) -> Dict:
        """Create a new VM interface."""
        data = {'virtual_machine': virtual_machine, 'name': name, 'enabled': enabled, **kwargs}
        for key, val in [
            ('mtu', mtu), ('mac_address', mac_address), ('description', description),
            ('mode', mode), ('untagged_vlan', untagged_vlan), ('tagged_vlans', tagged_vlans)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/interfaces', data)
