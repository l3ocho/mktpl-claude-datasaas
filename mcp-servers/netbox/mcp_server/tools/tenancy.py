"""
Tenancy tools for NetBox MCP Server.

Covers: Tenants, Tenant Groups, Contacts, Contact Groups, and Contact Roles.
"""
import logging
from typing import List, Dict, Optional, Any
from ..netbox_client import NetBoxClient

logger = logging.getLogger(__name__)


class TenancyTools:
    """Tools for Tenancy operations in NetBox"""

    def __init__(self, client: NetBoxClient):
        self.client = client
        self.base_endpoint = 'tenancy'

    # ==================== Tenant Groups ====================

    async def list_tenant_groups(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        parent_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all tenant groups."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'parent_id': parent_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/tenant-groups', params=params)

    async def get_tenant_group(self, id: int) -> Dict:
        """Get a specific tenant group by ID."""
        return self.client.get(f'{self.base_endpoint}/tenant-groups', id)

    async def create_tenant_group(
        self,
        name: str,
        slug: str,
        parent: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new tenant group."""
        data = {'name': name, 'slug': slug, **kwargs}
        if parent:
            data['parent'] = parent
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/tenant-groups', data)

    async def update_tenant_group(self, id: int, **kwargs) -> Dict:
        """Update a tenant group."""
        return self.client.patch(f'{self.base_endpoint}/tenant-groups', id, kwargs)

    async def delete_tenant_group(self, id: int) -> None:
        """Delete a tenant group."""
        self.client.delete(f'{self.base_endpoint}/tenant-groups', id)

    # ==================== Tenants ====================

    async def list_tenants(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        group_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all tenants with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'group_id': group_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/tenants', params=params)

    async def get_tenant(self, id: int) -> Dict:
        """Get a specific tenant by ID."""
        return self.client.get(f'{self.base_endpoint}/tenants', id)

    async def create_tenant(
        self,
        name: str,
        slug: str,
        group: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new tenant."""
        data = {'name': name, 'slug': slug, **kwargs}
        if group:
            data['group'] = group
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/tenants', data)

    async def update_tenant(self, id: int, **kwargs) -> Dict:
        """Update a tenant."""
        return self.client.patch(f'{self.base_endpoint}/tenants', id, kwargs)

    async def delete_tenant(self, id: int) -> None:
        """Delete a tenant."""
        self.client.delete(f'{self.base_endpoint}/tenants', id)

    # ==================== Contact Groups ====================

    async def list_contact_groups(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        parent_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all contact groups."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'parent_id': parent_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/contact-groups', params=params)

    async def get_contact_group(self, id: int) -> Dict:
        """Get a specific contact group by ID."""
        return self.client.get(f'{self.base_endpoint}/contact-groups', id)

    async def create_contact_group(
        self,
        name: str,
        slug: str,
        parent: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new contact group."""
        data = {'name': name, 'slug': slug, **kwargs}
        if parent:
            data['parent'] = parent
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/contact-groups', data)

    async def update_contact_group(self, id: int, **kwargs) -> Dict:
        """Update a contact group."""
        return self.client.patch(f'{self.base_endpoint}/contact-groups', id, kwargs)

    async def delete_contact_group(self, id: int) -> None:
        """Delete a contact group."""
        self.client.delete(f'{self.base_endpoint}/contact-groups', id)

    # ==================== Contact Roles ====================

    async def list_contact_roles(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all contact roles."""
        params = {k: v for k, v in {'name': name, 'slug': slug, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/contact-roles', params=params)

    async def get_contact_role(self, id: int) -> Dict:
        """Get a specific contact role by ID."""
        return self.client.get(f'{self.base_endpoint}/contact-roles', id)

    async def create_contact_role(
        self,
        name: str,
        slug: str,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new contact role."""
        data = {'name': name, 'slug': slug, **kwargs}
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/contact-roles', data)

    async def update_contact_role(self, id: int, **kwargs) -> Dict:
        """Update a contact role."""
        return self.client.patch(f'{self.base_endpoint}/contact-roles', id, kwargs)

    async def delete_contact_role(self, id: int) -> None:
        """Delete a contact role."""
        self.client.delete(f'{self.base_endpoint}/contact-roles', id)

    # ==================== Contacts ====================

    async def list_contacts(
        self,
        name: Optional[str] = None,
        group_id: Optional[int] = None,
        email: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all contacts with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'group_id': group_id, 'email': email, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/contacts', params=params)

    async def get_contact(self, id: int) -> Dict:
        """Get a specific contact by ID."""
        return self.client.get(f'{self.base_endpoint}/contacts', id)

    async def create_contact(
        self,
        name: str,
        group: Optional[int] = None,
        title: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        link: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new contact."""
        data = {'name': name, **kwargs}
        for key, val in [
            ('group', group), ('title', title), ('phone', phone),
            ('email', email), ('address', address), ('link', link),
            ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/contacts', data)

    async def update_contact(self, id: int, **kwargs) -> Dict:
        """Update a contact."""
        return self.client.patch(f'{self.base_endpoint}/contacts', id, kwargs)

    async def delete_contact(self, id: int) -> None:
        """Delete a contact."""
        self.client.delete(f'{self.base_endpoint}/contacts', id)

    # ==================== Contact Assignments ====================

    async def list_contact_assignments(
        self,
        contact_id: Optional[int] = None,
        role_id: Optional[int] = None,
        object_type: Optional[str] = None,
        object_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all contact assignments."""
        params = {k: v for k, v in {
            'contact_id': contact_id, 'role_id': role_id,
            'object_type': object_type, 'object_id': object_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/contact-assignments', params=params)

    async def get_contact_assignment(self, id: int) -> Dict:
        """Get a specific contact assignment by ID."""
        return self.client.get(f'{self.base_endpoint}/contact-assignments', id)

    async def create_contact_assignment(
        self,
        contact: int,
        role: int,
        object_type: str,
        object_id: int,
        priority: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new contact assignment."""
        data = {
            'contact': contact, 'role': role,
            'object_type': object_type, 'object_id': object_id, **kwargs
        }
        if priority:
            data['priority'] = priority
        return self.client.create(f'{self.base_endpoint}/contact-assignments', data)

    async def update_contact_assignment(self, id: int, **kwargs) -> Dict:
        """Update a contact assignment."""
        return self.client.patch(f'{self.base_endpoint}/contact-assignments', id, kwargs)

    async def delete_contact_assignment(self, id: int) -> None:
        """Delete a contact assignment."""
        self.client.delete(f'{self.base_endpoint}/contact-assignments', id)
