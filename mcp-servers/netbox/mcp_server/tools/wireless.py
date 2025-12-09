"""
Wireless tools for NetBox MCP Server.

Covers: Wireless LANs, Wireless LAN Groups, and Wireless Links.
"""
import logging
from typing import List, Dict, Optional, Any
from ..netbox_client import NetBoxClient

logger = logging.getLogger(__name__)


class WirelessTools:
    """Tools for Wireless operations in NetBox"""

    def __init__(self, client: NetBoxClient):
        self.client = client
        self.base_endpoint = 'wireless'

    # ==================== Wireless LAN Groups ====================

    async def list_wireless_lan_groups(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        parent_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all wireless LAN groups."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'parent_id': parent_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/wireless-lan-groups', params=params)

    async def get_wireless_lan_group(self, id: int) -> Dict:
        """Get a specific wireless LAN group by ID."""
        return self.client.get(f'{self.base_endpoint}/wireless-lan-groups', id)

    async def create_wireless_lan_group(
        self,
        name: str,
        slug: str,
        parent: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new wireless LAN group."""
        data = {'name': name, 'slug': slug, **kwargs}
        if parent:
            data['parent'] = parent
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/wireless-lan-groups', data)

    async def update_wireless_lan_group(self, id: int, **kwargs) -> Dict:
        """Update a wireless LAN group."""
        return self.client.patch(f'{self.base_endpoint}/wireless-lan-groups', id, kwargs)

    async def delete_wireless_lan_group(self, id: int) -> None:
        """Delete a wireless LAN group."""
        self.client.delete(f'{self.base_endpoint}/wireless-lan-groups', id)

    # ==================== Wireless LANs ====================

    async def list_wireless_lans(
        self,
        ssid: Optional[str] = None,
        group_id: Optional[int] = None,
        vlan_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        status: Optional[str] = None,
        auth_type: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all wireless LANs with optional filtering."""
        params = {k: v for k, v in {
            'ssid': ssid, 'group_id': group_id, 'vlan_id': vlan_id,
            'tenant_id': tenant_id, 'status': status, 'auth_type': auth_type, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/wireless-lans', params=params)

    async def get_wireless_lan(self, id: int) -> Dict:
        """Get a specific wireless LAN by ID."""
        return self.client.get(f'{self.base_endpoint}/wireless-lans', id)

    async def create_wireless_lan(
        self,
        ssid: str,
        status: str = 'active',
        group: Optional[int] = None,
        vlan: Optional[int] = None,
        tenant: Optional[int] = None,
        auth_type: Optional[str] = None,
        auth_cipher: Optional[str] = None,
        auth_psk: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new wireless LAN."""
        data = {'ssid': ssid, 'status': status, **kwargs}
        for key, val in [
            ('group', group), ('vlan', vlan), ('tenant', tenant),
            ('auth_type', auth_type), ('auth_cipher', auth_cipher),
            ('auth_psk', auth_psk), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/wireless-lans', data)

    async def update_wireless_lan(self, id: int, **kwargs) -> Dict:
        """Update a wireless LAN."""
        return self.client.patch(f'{self.base_endpoint}/wireless-lans', id, kwargs)

    async def delete_wireless_lan(self, id: int) -> None:
        """Delete a wireless LAN."""
        self.client.delete(f'{self.base_endpoint}/wireless-lans', id)

    # ==================== Wireless Links ====================

    async def list_wireless_links(
        self,
        ssid: Optional[str] = None,
        status: Optional[str] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all wireless links with optional filtering."""
        params = {k: v for k, v in {
            'ssid': ssid, 'status': status, 'tenant_id': tenant_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/wireless-links', params=params)

    async def get_wireless_link(self, id: int) -> Dict:
        """Get a specific wireless link by ID."""
        return self.client.get(f'{self.base_endpoint}/wireless-links', id)

    async def create_wireless_link(
        self,
        interface_a: int,
        interface_b: int,
        ssid: Optional[str] = None,
        status: str = 'connected',
        tenant: Optional[int] = None,
        auth_type: Optional[str] = None,
        auth_cipher: Optional[str] = None,
        auth_psk: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new wireless link."""
        data = {'interface_a': interface_a, 'interface_b': interface_b, 'status': status, **kwargs}
        for key, val in [
            ('ssid', ssid), ('tenant', tenant), ('auth_type', auth_type),
            ('auth_cipher', auth_cipher), ('auth_psk', auth_psk), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/wireless-links', data)

    async def update_wireless_link(self, id: int, **kwargs) -> Dict:
        """Update a wireless link."""
        return self.client.patch(f'{self.base_endpoint}/wireless-links', id, kwargs)

    async def delete_wireless_link(self, id: int) -> None:
        """Delete a wireless link."""
        self.client.delete(f'{self.base_endpoint}/wireless-links', id)
