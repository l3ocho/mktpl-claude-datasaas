"""
Extras tools for NetBox MCP Server.

Covers: Tags and Journal Entries only.
"""
import logging
from typing import List, Dict, Optional, Any
from ..netbox_client import NetBoxClient

logger = logging.getLogger(__name__)


class ExtrasTools:
    """Tools for Extras operations in NetBox"""

    def __init__(self, client: NetBoxClient):
        self.client = client
        self.base_endpoint = 'extras'

    # ==================== Tags ====================

    async def list_tags(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        color: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all tags with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'color': color, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/tags', params=params)

    async def get_tag(self, id: int) -> Dict:
        """Get a specific tag by ID."""
        return self.client.get(f'{self.base_endpoint}/tags', id)

    async def create_tag(
        self,
        name: str,
        slug: str,
        color: str = '9e9e9e',
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new tag."""
        data = {'name': name, 'slug': slug, 'color': color, **kwargs}
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/tags', data)

    # ==================== Journal Entries ====================

    async def list_journal_entries(
        self,
        assigned_object_type: Optional[str] = None,
        assigned_object_id: Optional[int] = None,
        kind: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all journal entries."""
        params = {k: v for k, v in {
            'assigned_object_type': assigned_object_type,
            'assigned_object_id': assigned_object_id, 'kind': kind, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/journal-entries', params=params)

    async def get_journal_entry(self, id: int) -> Dict:
        """Get a specific journal entry by ID."""
        return self.client.get(f'{self.base_endpoint}/journal-entries', id)

    async def create_journal_entry(
        self,
        assigned_object_type: str,
        assigned_object_id: int,
        comments: str,
        kind: str = 'info',
        **kwargs
    ) -> Dict:
        """Create a new journal entry."""
        data = {
            'assigned_object_type': assigned_object_type,
            'assigned_object_id': assigned_object_id,
            'comments': comments, 'kind': kind, **kwargs
        }
        return self.client.create(f'{self.base_endpoint}/journal-entries', data)
