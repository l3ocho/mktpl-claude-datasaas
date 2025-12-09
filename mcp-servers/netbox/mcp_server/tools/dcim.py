"""
DCIM (Data Center Infrastructure Management) tools for NetBox MCP Server.

Covers: Sites, Locations, Racks, Devices, Cables, Interfaces, and related models.
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

    # ==================== Regions ====================

    async def list_regions(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        parent_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all regions with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'parent_id': parent_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/regions', params=params)

    async def get_region(self, id: int) -> Dict:
        """Get a specific region by ID."""
        return self.client.get(f'{self.base_endpoint}/regions', id)

    async def create_region(self, name: str, slug: str, parent: Optional[int] = None, **kwargs) -> Dict:
        """Create a new region."""
        data = {'name': name, 'slug': slug, **kwargs}
        if parent:
            data['parent'] = parent
        return self.client.create(f'{self.base_endpoint}/regions', data)

    async def update_region(self, id: int, **kwargs) -> Dict:
        """Update a region."""
        return self.client.patch(f'{self.base_endpoint}/regions', id, kwargs)

    async def delete_region(self, id: int) -> None:
        """Delete a region."""
        self.client.delete(f'{self.base_endpoint}/regions', id)

    # ==================== Site Groups ====================

    async def list_site_groups(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        parent_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all site groups with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'parent_id': parent_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/site-groups', params=params)

    async def get_site_group(self, id: int) -> Dict:
        """Get a specific site group by ID."""
        return self.client.get(f'{self.base_endpoint}/site-groups', id)

    async def create_site_group(self, name: str, slug: str, parent: Optional[int] = None, **kwargs) -> Dict:
        """Create a new site group."""
        data = {'name': name, 'slug': slug, **kwargs}
        if parent:
            data['parent'] = parent
        return self.client.create(f'{self.base_endpoint}/site-groups', data)

    async def update_site_group(self, id: int, **kwargs) -> Dict:
        """Update a site group."""
        return self.client.patch(f'{self.base_endpoint}/site-groups', id, kwargs)

    async def delete_site_group(self, id: int) -> None:
        """Delete a site group."""
        self.client.delete(f'{self.base_endpoint}/site-groups', id)

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

    async def delete_site(self, id: int) -> None:
        """Delete a site."""
        self.client.delete(f'{self.base_endpoint}/sites', id)

    # ==================== Locations ====================

    async def list_locations(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        site_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all locations with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'site_id': site_id, 'parent_id': parent_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/locations', params=params)

    async def get_location(self, id: int) -> Dict:
        """Get a specific location by ID."""
        return self.client.get(f'{self.base_endpoint}/locations', id)

    async def create_location(
        self,
        name: str,
        slug: str,
        site: int,
        parent: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Create a new location."""
        data = {'name': name, 'slug': slug, 'site': site, **kwargs}
        if parent:
            data['parent'] = parent
        return self.client.create(f'{self.base_endpoint}/locations', data)

    async def update_location(self, id: int, **kwargs) -> Dict:
        """Update a location."""
        return self.client.patch(f'{self.base_endpoint}/locations', id, kwargs)

    async def delete_location(self, id: int) -> None:
        """Delete a location."""
        self.client.delete(f'{self.base_endpoint}/locations', id)

    # ==================== Rack Roles ====================

    async def list_rack_roles(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all rack roles."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/rack-roles', params=params)

    async def get_rack_role(self, id: int) -> Dict:
        """Get a specific rack role by ID."""
        return self.client.get(f'{self.base_endpoint}/rack-roles', id)

    async def create_rack_role(self, name: str, slug: str, color: str = '9e9e9e', **kwargs) -> Dict:
        """Create a new rack role."""
        data = {'name': name, 'slug': slug, 'color': color, **kwargs}
        return self.client.create(f'{self.base_endpoint}/rack-roles', data)

    async def update_rack_role(self, id: int, **kwargs) -> Dict:
        """Update a rack role."""
        return self.client.patch(f'{self.base_endpoint}/rack-roles', id, kwargs)

    async def delete_rack_role(self, id: int) -> None:
        """Delete a rack role."""
        self.client.delete(f'{self.base_endpoint}/rack-roles', id)

    # ==================== Rack Types ====================

    async def list_rack_types(self, manufacturer_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all rack types."""
        params = {k: v for k, v in {'manufacturer_id': manufacturer_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/rack-types', params=params)

    async def get_rack_type(self, id: int) -> Dict:
        """Get a specific rack type by ID."""
        return self.client.get(f'{self.base_endpoint}/rack-types', id)

    async def create_rack_type(
        self,
        manufacturer: int,
        model: str,
        slug: str,
        form_factor: str = '4-post-frame',
        width: int = 19,
        u_height: int = 42,
        **kwargs
    ) -> Dict:
        """Create a new rack type."""
        data = {
            'manufacturer': manufacturer, 'model': model, 'slug': slug,
            'form_factor': form_factor, 'width': width, 'u_height': u_height, **kwargs
        }
        return self.client.create(f'{self.base_endpoint}/rack-types', data)

    async def update_rack_type(self, id: int, **kwargs) -> Dict:
        """Update a rack type."""
        return self.client.patch(f'{self.base_endpoint}/rack-types', id, kwargs)

    async def delete_rack_type(self, id: int) -> None:
        """Delete a rack type."""
        self.client.delete(f'{self.base_endpoint}/rack-types', id)

    # ==================== Racks ====================

    async def list_racks(
        self,
        name: Optional[str] = None,
        site_id: Optional[int] = None,
        location_id: Optional[int] = None,
        status: Optional[str] = None,
        role_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all racks with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'site_id': site_id, 'location_id': location_id,
            'status': status, 'role_id': role_id, 'tenant_id': tenant_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/racks', params=params)

    async def get_rack(self, id: int) -> Dict:
        """Get a specific rack by ID."""
        return self.client.get(f'{self.base_endpoint}/racks', id)

    async def create_rack(
        self,
        name: str,
        site: int,
        status: str = 'active',
        location: Optional[int] = None,
        role: Optional[int] = None,
        tenant: Optional[int] = None,
        rack_type: Optional[int] = None,
        width: int = 19,
        u_height: int = 42,
        **kwargs
    ) -> Dict:
        """Create a new rack."""
        data = {'name': name, 'site': site, 'status': status, 'width': width, 'u_height': u_height, **kwargs}
        for key, val in [('location', location), ('role', role), ('tenant', tenant), ('rack_type', rack_type)]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/racks', data)

    async def update_rack(self, id: int, **kwargs) -> Dict:
        """Update a rack."""
        return self.client.patch(f'{self.base_endpoint}/racks', id, kwargs)

    async def delete_rack(self, id: int) -> None:
        """Delete a rack."""
        self.client.delete(f'{self.base_endpoint}/racks', id)

    # ==================== Rack Reservations ====================

    async def list_rack_reservations(
        self,
        rack_id: Optional[int] = None,
        site_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all rack reservations."""
        params = {k: v for k, v in {
            'rack_id': rack_id, 'site_id': site_id, 'tenant_id': tenant_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/rack-reservations', params=params)

    async def get_rack_reservation(self, id: int) -> Dict:
        """Get a specific rack reservation by ID."""
        return self.client.get(f'{self.base_endpoint}/rack-reservations', id)

    async def create_rack_reservation(
        self,
        rack: int,
        units: List[int],
        user: int,
        description: str,
        tenant: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Create a new rack reservation."""
        data = {'rack': rack, 'units': units, 'user': user, 'description': description, **kwargs}
        if tenant:
            data['tenant'] = tenant
        return self.client.create(f'{self.base_endpoint}/rack-reservations', data)

    async def update_rack_reservation(self, id: int, **kwargs) -> Dict:
        """Update a rack reservation."""
        return self.client.patch(f'{self.base_endpoint}/rack-reservations', id, kwargs)

    async def delete_rack_reservation(self, id: int) -> None:
        """Delete a rack reservation."""
        self.client.delete(f'{self.base_endpoint}/rack-reservations', id)

    # ==================== Manufacturers ====================

    async def list_manufacturers(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all manufacturers."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/manufacturers', params=params)

    async def get_manufacturer(self, id: int) -> Dict:
        """Get a specific manufacturer by ID."""
        return self.client.get(f'{self.base_endpoint}/manufacturers', id)

    async def create_manufacturer(self, name: str, slug: str, **kwargs) -> Dict:
        """Create a new manufacturer."""
        data = {'name': name, 'slug': slug, **kwargs}
        return self.client.create(f'{self.base_endpoint}/manufacturers', data)

    async def update_manufacturer(self, id: int, **kwargs) -> Dict:
        """Update a manufacturer."""
        return self.client.patch(f'{self.base_endpoint}/manufacturers', id, kwargs)

    async def delete_manufacturer(self, id: int) -> None:
        """Delete a manufacturer."""
        self.client.delete(f'{self.base_endpoint}/manufacturers', id)

    # ==================== Device Types ====================

    async def list_device_types(
        self,
        manufacturer_id: Optional[int] = None,
        model: Optional[str] = None,
        slug: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all device types."""
        params = {k: v for k, v in {
            'manufacturer_id': manufacturer_id, 'model': model, 'slug': slug, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/device-types', params=params)

    async def get_device_type(self, id: int) -> Dict:
        """Get a specific device type by ID."""
        return self.client.get(f'{self.base_endpoint}/device-types', id)

    async def create_device_type(
        self,
        manufacturer: int,
        model: str,
        slug: str,
        u_height: float = 1.0,
        is_full_depth: bool = True,
        **kwargs
    ) -> Dict:
        """Create a new device type."""
        data = {
            'manufacturer': manufacturer, 'model': model, 'slug': slug,
            'u_height': u_height, 'is_full_depth': is_full_depth, **kwargs
        }
        return self.client.create(f'{self.base_endpoint}/device-types', data)

    async def update_device_type(self, id: int, **kwargs) -> Dict:
        """Update a device type."""
        return self.client.patch(f'{self.base_endpoint}/device-types', id, kwargs)

    async def delete_device_type(self, id: int) -> None:
        """Delete a device type."""
        self.client.delete(f'{self.base_endpoint}/device-types', id)

    # ==================== Module Types ====================

    async def list_module_types(self, manufacturer_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all module types."""
        params = {k: v for k, v in {'manufacturer_id': manufacturer_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/module-types', params=params)

    async def get_module_type(self, id: int) -> Dict:
        """Get a specific module type by ID."""
        return self.client.get(f'{self.base_endpoint}/module-types', id)

    async def create_module_type(self, manufacturer: int, model: str, **kwargs) -> Dict:
        """Create a new module type."""
        data = {'manufacturer': manufacturer, 'model': model, **kwargs}
        return self.client.create(f'{self.base_endpoint}/module-types', data)

    async def update_module_type(self, id: int, **kwargs) -> Dict:
        """Update a module type."""
        return self.client.patch(f'{self.base_endpoint}/module-types', id, kwargs)

    async def delete_module_type(self, id: int) -> None:
        """Delete a module type."""
        self.client.delete(f'{self.base_endpoint}/module-types', id)

    # ==================== Device Roles ====================

    async def list_device_roles(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all device roles."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/device-roles', params=params)

    async def get_device_role(self, id: int) -> Dict:
        """Get a specific device role by ID."""
        return self.client.get(f'{self.base_endpoint}/device-roles', id)

    async def create_device_role(
        self,
        name: str,
        slug: str,
        color: str = '9e9e9e',
        vm_role: bool = False,
        **kwargs
    ) -> Dict:
        """Create a new device role."""
        data = {'name': name, 'slug': slug, 'color': color, 'vm_role': vm_role, **kwargs}
        return self.client.create(f'{self.base_endpoint}/device-roles', data)

    async def update_device_role(self, id: int, **kwargs) -> Dict:
        """Update a device role."""
        return self.client.patch(f'{self.base_endpoint}/device-roles', id, kwargs)

    async def delete_device_role(self, id: int) -> None:
        """Delete a device role."""
        self.client.delete(f'{self.base_endpoint}/device-roles', id)

    # ==================== Platforms ====================

    async def list_platforms(self, name: Optional[str] = None, manufacturer_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all platforms."""
        params = {k: v for k, v in {'name': name, 'manufacturer_id': manufacturer_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/platforms', params=params)

    async def get_platform(self, id: int) -> Dict:
        """Get a specific platform by ID."""
        return self.client.get(f'{self.base_endpoint}/platforms', id)

    async def create_platform(
        self,
        name: str,
        slug: str,
        manufacturer: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Create a new platform."""
        data = {'name': name, 'slug': slug, **kwargs}
        if manufacturer:
            data['manufacturer'] = manufacturer
        return self.client.create(f'{self.base_endpoint}/platforms', data)

    async def update_platform(self, id: int, **kwargs) -> Dict:
        """Update a platform."""
        return self.client.patch(f'{self.base_endpoint}/platforms', id, kwargs)

    async def delete_platform(self, id: int) -> None:
        """Delete a platform."""
        self.client.delete(f'{self.base_endpoint}/platforms', id)

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

    async def delete_device(self, id: int) -> None:
        """Delete a device."""
        self.client.delete(f'{self.base_endpoint}/devices', id)

    # ==================== Modules ====================

    async def list_modules(self, device_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all modules."""
        params = {k: v for k, v in {'device_id': device_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/modules', params=params)

    async def get_module(self, id: int) -> Dict:
        """Get a specific module by ID."""
        return self.client.get(f'{self.base_endpoint}/modules', id)

    async def create_module(self, device: int, module_bay: int, module_type: int, **kwargs) -> Dict:
        """Create a new module."""
        data = {'device': device, 'module_bay': module_bay, 'module_type': module_type, **kwargs}
        return self.client.create(f'{self.base_endpoint}/modules', data)

    async def update_module(self, id: int, **kwargs) -> Dict:
        """Update a module."""
        return self.client.patch(f'{self.base_endpoint}/modules', id, kwargs)

    async def delete_module(self, id: int) -> None:
        """Delete a module."""
        self.client.delete(f'{self.base_endpoint}/modules', id)

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

    async def update_interface(self, id: int, **kwargs) -> Dict:
        """Update an interface."""
        return self.client.patch(f'{self.base_endpoint}/interfaces', id, kwargs)

    async def delete_interface(self, id: int) -> None:
        """Delete an interface."""
        self.client.delete(f'{self.base_endpoint}/interfaces', id)

    # ==================== Console Ports ====================

    async def list_console_ports(self, device_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all console ports."""
        params = {k: v for k, v in {'device_id': device_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/console-ports', params=params)

    async def get_console_port(self, id: int) -> Dict:
        """Get a specific console port by ID."""
        return self.client.get(f'{self.base_endpoint}/console-ports', id)

    async def create_console_port(self, device: int, name: str, **kwargs) -> Dict:
        """Create a new console port."""
        data = {'device': device, 'name': name, **kwargs}
        return self.client.create(f'{self.base_endpoint}/console-ports', data)

    async def update_console_port(self, id: int, **kwargs) -> Dict:
        """Update a console port."""
        return self.client.patch(f'{self.base_endpoint}/console-ports', id, kwargs)

    async def delete_console_port(self, id: int) -> None:
        """Delete a console port."""
        self.client.delete(f'{self.base_endpoint}/console-ports', id)

    # ==================== Console Server Ports ====================

    async def list_console_server_ports(self, device_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all console server ports."""
        params = {k: v for k, v in {'device_id': device_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/console-server-ports', params=params)

    async def get_console_server_port(self, id: int) -> Dict:
        """Get a specific console server port by ID."""
        return self.client.get(f'{self.base_endpoint}/console-server-ports', id)

    async def create_console_server_port(self, device: int, name: str, **kwargs) -> Dict:
        """Create a new console server port."""
        data = {'device': device, 'name': name, **kwargs}
        return self.client.create(f'{self.base_endpoint}/console-server-ports', data)

    async def update_console_server_port(self, id: int, **kwargs) -> Dict:
        """Update a console server port."""
        return self.client.patch(f'{self.base_endpoint}/console-server-ports', id, kwargs)

    async def delete_console_server_port(self, id: int) -> None:
        """Delete a console server port."""
        self.client.delete(f'{self.base_endpoint}/console-server-ports', id)

    # ==================== Power Ports ====================

    async def list_power_ports(self, device_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all power ports."""
        params = {k: v for k, v in {'device_id': device_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/power-ports', params=params)

    async def get_power_port(self, id: int) -> Dict:
        """Get a specific power port by ID."""
        return self.client.get(f'{self.base_endpoint}/power-ports', id)

    async def create_power_port(self, device: int, name: str, **kwargs) -> Dict:
        """Create a new power port."""
        data = {'device': device, 'name': name, **kwargs}
        return self.client.create(f'{self.base_endpoint}/power-ports', data)

    async def update_power_port(self, id: int, **kwargs) -> Dict:
        """Update a power port."""
        return self.client.patch(f'{self.base_endpoint}/power-ports', id, kwargs)

    async def delete_power_port(self, id: int) -> None:
        """Delete a power port."""
        self.client.delete(f'{self.base_endpoint}/power-ports', id)

    # ==================== Power Outlets ====================

    async def list_power_outlets(self, device_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all power outlets."""
        params = {k: v for k, v in {'device_id': device_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/power-outlets', params=params)

    async def get_power_outlet(self, id: int) -> Dict:
        """Get a specific power outlet by ID."""
        return self.client.get(f'{self.base_endpoint}/power-outlets', id)

    async def create_power_outlet(self, device: int, name: str, **kwargs) -> Dict:
        """Create a new power outlet."""
        data = {'device': device, 'name': name, **kwargs}
        return self.client.create(f'{self.base_endpoint}/power-outlets', data)

    async def update_power_outlet(self, id: int, **kwargs) -> Dict:
        """Update a power outlet."""
        return self.client.patch(f'{self.base_endpoint}/power-outlets', id, kwargs)

    async def delete_power_outlet(self, id: int) -> None:
        """Delete a power outlet."""
        self.client.delete(f'{self.base_endpoint}/power-outlets', id)

    # ==================== Power Panels ====================

    async def list_power_panels(self, site_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all power panels."""
        params = {k: v for k, v in {'site_id': site_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/power-panels', params=params)

    async def get_power_panel(self, id: int) -> Dict:
        """Get a specific power panel by ID."""
        return self.client.get(f'{self.base_endpoint}/power-panels', id)

    async def create_power_panel(self, site: int, name: str, location: Optional[int] = None, **kwargs) -> Dict:
        """Create a new power panel."""
        data = {'site': site, 'name': name, **kwargs}
        if location:
            data['location'] = location
        return self.client.create(f'{self.base_endpoint}/power-panels', data)

    async def update_power_panel(self, id: int, **kwargs) -> Dict:
        """Update a power panel."""
        return self.client.patch(f'{self.base_endpoint}/power-panels', id, kwargs)

    async def delete_power_panel(self, id: int) -> None:
        """Delete a power panel."""
        self.client.delete(f'{self.base_endpoint}/power-panels', id)

    # ==================== Power Feeds ====================

    async def list_power_feeds(self, power_panel_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all power feeds."""
        params = {k: v for k, v in {'power_panel_id': power_panel_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/power-feeds', params=params)

    async def get_power_feed(self, id: int) -> Dict:
        """Get a specific power feed by ID."""
        return self.client.get(f'{self.base_endpoint}/power-feeds', id)

    async def create_power_feed(
        self,
        power_panel: int,
        name: str,
        status: str = 'active',
        type: str = 'primary',
        supply: str = 'ac',
        phase: str = 'single-phase',
        voltage: int = 120,
        amperage: int = 20,
        **kwargs
    ) -> Dict:
        """Create a new power feed."""
        data = {
            'power_panel': power_panel, 'name': name, 'status': status,
            'type': type, 'supply': supply, 'phase': phase,
            'voltage': voltage, 'amperage': amperage, **kwargs
        }
        return self.client.create(f'{self.base_endpoint}/power-feeds', data)

    async def update_power_feed(self, id: int, **kwargs) -> Dict:
        """Update a power feed."""
        return self.client.patch(f'{self.base_endpoint}/power-feeds', id, kwargs)

    async def delete_power_feed(self, id: int) -> None:
        """Delete a power feed."""
        self.client.delete(f'{self.base_endpoint}/power-feeds', id)

    # ==================== Cables ====================

    async def list_cables(
        self,
        site_id: Optional[int] = None,
        device_id: Optional[int] = None,
        rack_id: Optional[int] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all cables."""
        params = {k: v for k, v in {
            'site_id': site_id, 'device_id': device_id, 'rack_id': rack_id,
            'type': type, 'status': status, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/cables', params=params)

    async def get_cable(self, id: int) -> Dict:
        """Get a specific cable by ID."""
        return self.client.get(f'{self.base_endpoint}/cables', id)

    async def create_cable(
        self,
        a_terminations: List[Dict],
        b_terminations: List[Dict],
        type: Optional[str] = None,
        status: str = 'connected',
        label: Optional[str] = None,
        color: Optional[str] = None,
        length: Optional[float] = None,
        length_unit: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Create a new cable.

        a_terminations and b_terminations are lists of dicts with:
        - object_type: e.g., 'dcim.interface'
        - object_id: ID of the object
        """
        data = {
            'a_terminations': a_terminations,
            'b_terminations': b_terminations,
            'status': status,
            **kwargs
        }
        for key, val in [
            ('type', type), ('label', label), ('color', color),
            ('length', length), ('length_unit', length_unit)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/cables', data)

    async def update_cable(self, id: int, **kwargs) -> Dict:
        """Update a cable."""
        return self.client.patch(f'{self.base_endpoint}/cables', id, kwargs)

    async def delete_cable(self, id: int) -> None:
        """Delete a cable."""
        self.client.delete(f'{self.base_endpoint}/cables', id)

    # ==================== Virtual Chassis ====================

    async def list_virtual_chassis(self, **kwargs) -> List[Dict]:
        """List all virtual chassis."""
        return self.client.list(f'{self.base_endpoint}/virtual-chassis', params=kwargs)

    async def get_virtual_chassis(self, id: int) -> Dict:
        """Get a specific virtual chassis by ID."""
        return self.client.get(f'{self.base_endpoint}/virtual-chassis', id)

    async def create_virtual_chassis(self, name: str, domain: Optional[str] = None, **kwargs) -> Dict:
        """Create a new virtual chassis."""
        data = {'name': name, **kwargs}
        if domain:
            data['domain'] = domain
        return self.client.create(f'{self.base_endpoint}/virtual-chassis', data)

    async def update_virtual_chassis(self, id: int, **kwargs) -> Dict:
        """Update a virtual chassis."""
        return self.client.patch(f'{self.base_endpoint}/virtual-chassis', id, kwargs)

    async def delete_virtual_chassis(self, id: int) -> None:
        """Delete a virtual chassis."""
        self.client.delete(f'{self.base_endpoint}/virtual-chassis', id)

    # ==================== Inventory Items ====================

    async def list_inventory_items(self, device_id: Optional[int] = None, **kwargs) -> List[Dict]:
        """List all inventory items."""
        params = {k: v for k, v in {'device_id': device_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/inventory-items', params=params)

    async def get_inventory_item(self, id: int) -> Dict:
        """Get a specific inventory item by ID."""
        return self.client.get(f'{self.base_endpoint}/inventory-items', id)

    async def create_inventory_item(
        self,
        device: int,
        name: str,
        parent: Optional[int] = None,
        manufacturer: Optional[int] = None,
        part_id: Optional[str] = None,
        serial: Optional[str] = None,
        asset_tag: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new inventory item."""
        data = {'device': device, 'name': name, **kwargs}
        for key, val in [
            ('parent', parent), ('manufacturer', manufacturer),
            ('part_id', part_id), ('serial', serial), ('asset_tag', asset_tag)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/inventory-items', data)

    async def update_inventory_item(self, id: int, **kwargs) -> Dict:
        """Update an inventory item."""
        return self.client.patch(f'{self.base_endpoint}/inventory-items', id, kwargs)

    async def delete_inventory_item(self, id: int) -> None:
        """Delete an inventory item."""
        self.client.delete(f'{self.base_endpoint}/inventory-items', id)
