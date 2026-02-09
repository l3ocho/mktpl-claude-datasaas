"""
DCIM (Data Center Infrastructure Management) tools for NetBox MCP Server.

Covers: Sites, Devices, and Interfaces only.
"""
import logging
from typing import List, Dict, Optional, Any
from ..netbox_client import NetBoxClient

logger = logging.getLogger(__name__)


class DCIMTools:
    """Tools for DCIM operations in NetBox"""

    def __init__(self, client: NetBoxClient):
        self.client = client
        self.base_endpoint = 'dcim'

    # ==================== Sites ====================

    async def list_sites(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        status: Optional[str] = None,
        region_id: Optional[int] = None,
        group_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all sites with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'status': status,
            'region_id': region_id, 'group_id': group_id, 'tenant_id': tenant_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/sites', params=params)

    async def get_site(self, id: int) -> Dict:
        """Get a specific site by ID."""
        return self.client.get(f'{self.base_endpoint}/sites', id)

    async def create_site(
        self,
        name: str,
        slug: str,
        status: str = 'active',
        region: Optional[int] = None,
        group: Optional[int] = None,
        tenant: Optional[int] = None,
        facility: Optional[str] = None,
        time_zone: Optional[str] = None,
        description: Optional[str] = None,
        physical_address: Optional[str] = None,
        shipping_address: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        **kwargs
    ) -> Dict:
        """Create a new site."""
        data = {'name': name, 'slug': slug, 'status': status, **kwargs}
        for key, val in [
            ('region', region), ('group', group), ('tenant', tenant),
            ('facility', facility), ('time_zone', time_zone),
            ('description', description), ('physical_address', physical_address),
            ('shipping_address', shipping_address), ('latitude', latitude),
            ('longitude', longitude)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/sites', data)

    async def update_site(self, id: int, **kwargs) -> Dict:
        """Update a site."""
        return self.client.patch(f'{self.base_endpoint}/sites', id, kwargs)

    # ==================== Devices ====================

    async def list_devices(
        self,
        name: Optional[str] = None,
        site_id: Optional[int] = None,
        location_id: Optional[int] = None,
        rack_id: Optional[int] = None,
        status: Optional[str] = None,
        role_id: Optional[int] = None,
        device_type_id: Optional[int] = None,
        manufacturer_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        serial: Optional[str] = None,
        asset_tag: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all devices with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'site_id': site_id, 'location_id': location_id,
            'rack_id': rack_id, 'status': status, 'role_id': role_id,
            'device_type_id': device_type_id, 'manufacturer_id': manufacturer_id,
            'platform_id': platform_id, 'tenant_id': tenant_id,
            'serial': serial, 'asset_tag': asset_tag, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/devices', params=params)

    async def get_device(self, id: int) -> Dict:
        """Get a specific device by ID."""
        return self.client.get(f'{self.base_endpoint}/devices', id)

    async def create_device(
        self,
        name: str,
        device_type: int,
        role: int,
        site: int,
        status: str = 'active',
        location: Optional[int] = None,
        rack: Optional[int] = None,
        position: Optional[float] = None,
        face: Optional[str] = None,
        platform: Optional[int] = None,
        tenant: Optional[int] = None,
        serial: Optional[str] = None,
        asset_tag: Optional[str] = None,
        primary_ip4: Optional[int] = None,
        primary_ip6: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Create a new device."""
        data = {
            'name': name, 'device_type': device_type, 'role': role,
            'site': site, 'status': status, **kwargs
        }
        for key, val in [
            ('location', location), ('rack', rack), ('position', position),
            ('face', face), ('platform', platform), ('tenant', tenant),
            ('serial', serial), ('asset_tag', asset_tag),
            ('primary_ip4', primary_ip4), ('primary_ip6', primary_ip6)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/devices', data)

    async def update_device(self, id: int, **kwargs) -> Dict:
        """Update a device."""
        return self.client.patch(f'{self.base_endpoint}/devices', id, kwargs)

    # ==================== Interfaces ====================

    async def list_interfaces(
        self,
        device_id: Optional[int] = None,
        name: Optional[str] = None,
        type: Optional[str] = None,
        enabled: Optional[bool] = None,
        **kwargs
    ) -> List[Dict]:
        """List all interfaces."""
        params = {k: v for k, v in {
            'device_id': device_id, 'name': name, 'type': type, 'enabled': enabled, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/interfaces', params=params)

    async def get_interface(self, id: int) -> Dict:
        """Get a specific interface by ID."""
        return self.client.get(f'{self.base_endpoint}/interfaces', id)

    async def create_interface(
        self,
        device: int,
        name: str,
        type: str,
        enabled: bool = True,
        mtu: Optional[int] = None,
        mac_address: Optional[str] = None,
        description: Optional[str] = None,
        mode: Optional[str] = None,
        untagged_vlan: Optional[int] = None,
        tagged_vlans: Optional[List[int]] = None,
        **kwargs
    ) -> Dict:
        """Create a new interface."""
        data = {'device': device, 'name': name, 'type': type, 'enabled': enabled, **kwargs}
        for key, val in [
            ('mtu', mtu), ('mac_address', mac_address), ('description', description),
            ('mode', mode), ('untagged_vlan', untagged_vlan), ('tagged_vlans', tagged_vlans)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/interfaces', data)
