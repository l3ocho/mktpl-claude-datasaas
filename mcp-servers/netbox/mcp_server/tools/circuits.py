"""
Circuits tools for NetBox MCP Server.

Covers: Providers, Circuits, Circuit Types, Circuit Terminations, and related models.
"""
import logging
from typing import List, Dict, Optional, Any
from ..netbox_client import NetBoxClient

logger = logging.getLogger(__name__)


class CircuitsTools:
    """Tools for Circuits operations in NetBox"""

    def __init__(self, client: NetBoxClient):
        self.client = client
        self.base_endpoint = 'circuits'

    # ==================== Providers ====================

    async def list_providers(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all circuit providers."""
        params = {k: v for k, v in {'name': name, 'slug': slug, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/providers', params=params)

    async def get_provider(self, id: int) -> Dict:
        """Get a specific provider by ID."""
        return self.client.get(f'{self.base_endpoint}/providers', id)

    async def create_provider(
        self,
        name: str,
        slug: str,
        asns: Optional[List[int]] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new provider."""
        data = {'name': name, 'slug': slug, **kwargs}
        if asns:
            data['asns'] = asns
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/providers', data)

    async def update_provider(self, id: int, **kwargs) -> Dict:
        """Update a provider."""
        return self.client.patch(f'{self.base_endpoint}/providers', id, kwargs)

    async def delete_provider(self, id: int) -> None:
        """Delete a provider."""
        self.client.delete(f'{self.base_endpoint}/providers', id)

    # ==================== Provider Accounts ====================

    async def list_provider_accounts(
        self,
        provider_id: Optional[int] = None,
        name: Optional[str] = None,
        account: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all provider accounts."""
        params = {k: v for k, v in {
            'provider_id': provider_id, 'name': name, 'account': account, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/provider-accounts', params=params)

    async def get_provider_account(self, id: int) -> Dict:
        """Get a specific provider account by ID."""
        return self.client.get(f'{self.base_endpoint}/provider-accounts', id)

    async def create_provider_account(
        self,
        provider: int,
        account: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new provider account."""
        data = {'provider': provider, 'account': account, **kwargs}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/provider-accounts', data)

    async def update_provider_account(self, id: int, **kwargs) -> Dict:
        """Update a provider account."""
        return self.client.patch(f'{self.base_endpoint}/provider-accounts', id, kwargs)

    async def delete_provider_account(self, id: int) -> None:
        """Delete a provider account."""
        self.client.delete(f'{self.base_endpoint}/provider-accounts', id)

    # ==================== Provider Networks ====================

    async def list_provider_networks(
        self,
        provider_id: Optional[int] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all provider networks."""
        params = {k: v for k, v in {
            'provider_id': provider_id, 'name': name, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/provider-networks', params=params)

    async def get_provider_network(self, id: int) -> Dict:
        """Get a specific provider network by ID."""
        return self.client.get(f'{self.base_endpoint}/provider-networks', id)

    async def create_provider_network(
        self,
        provider: int,
        name: str,
        service_id: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new provider network."""
        data = {'provider': provider, 'name': name, **kwargs}
        if service_id:
            data['service_id'] = service_id
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/provider-networks', data)

    async def update_provider_network(self, id: int, **kwargs) -> Dict:
        """Update a provider network."""
        return self.client.patch(f'{self.base_endpoint}/provider-networks', id, kwargs)

    async def delete_provider_network(self, id: int) -> None:
        """Delete a provider network."""
        self.client.delete(f'{self.base_endpoint}/provider-networks', id)

    # ==================== Circuit Types ====================

    async def list_circuit_types(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all circuit types."""
        params = {k: v for k, v in {'name': name, 'slug': slug, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/circuit-types', params=params)

    async def get_circuit_type(self, id: int) -> Dict:
        """Get a specific circuit type by ID."""
        return self.client.get(f'{self.base_endpoint}/circuit-types', id)

    async def create_circuit_type(
        self,
        name: str,
        slug: str,
        color: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new circuit type."""
        data = {'name': name, 'slug': slug, **kwargs}
        if color:
            data['color'] = color
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/circuit-types', data)

    async def update_circuit_type(self, id: int, **kwargs) -> Dict:
        """Update a circuit type."""
        return self.client.patch(f'{self.base_endpoint}/circuit-types', id, kwargs)

    async def delete_circuit_type(self, id: int) -> None:
        """Delete a circuit type."""
        self.client.delete(f'{self.base_endpoint}/circuit-types', id)

    # ==================== Circuit Groups ====================

    async def list_circuit_groups(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all circuit groups."""
        params = {k: v for k, v in {'name': name, 'slug': slug, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/circuit-groups', params=params)

    async def get_circuit_group(self, id: int) -> Dict:
        """Get a specific circuit group by ID."""
        return self.client.get(f'{self.base_endpoint}/circuit-groups', id)

    async def create_circuit_group(
        self,
        name: str,
        slug: str,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new circuit group."""
        data = {'name': name, 'slug': slug, **kwargs}
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/circuit-groups', data)

    async def update_circuit_group(self, id: int, **kwargs) -> Dict:
        """Update a circuit group."""
        return self.client.patch(f'{self.base_endpoint}/circuit-groups', id, kwargs)

    async def delete_circuit_group(self, id: int) -> None:
        """Delete a circuit group."""
        self.client.delete(f'{self.base_endpoint}/circuit-groups', id)

    # ==================== Circuit Group Assignments ====================

    async def list_circuit_group_assignments(
        self,
        group_id: Optional[int] = None,
        circuit_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all circuit group assignments."""
        params = {k: v for k, v in {
            'group_id': group_id, 'circuit_id': circuit_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/circuit-group-assignments', params=params)

    async def get_circuit_group_assignment(self, id: int) -> Dict:
        """Get a specific circuit group assignment by ID."""
        return self.client.get(f'{self.base_endpoint}/circuit-group-assignments', id)

    async def create_circuit_group_assignment(
        self,
        group: int,
        circuit: int,
        priority: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new circuit group assignment."""
        data = {'group': group, 'circuit': circuit, **kwargs}
        if priority:
            data['priority'] = priority
        return self.client.create(f'{self.base_endpoint}/circuit-group-assignments', data)

    async def update_circuit_group_assignment(self, id: int, **kwargs) -> Dict:
        """Update a circuit group assignment."""
        return self.client.patch(f'{self.base_endpoint}/circuit-group-assignments', id, kwargs)

    async def delete_circuit_group_assignment(self, id: int) -> None:
        """Delete a circuit group assignment."""
        self.client.delete(f'{self.base_endpoint}/circuit-group-assignments', id)

    # ==================== Circuits ====================

    async def list_circuits(
        self,
        cid: Optional[str] = None,
        provider_id: Optional[int] = None,
        provider_account_id: Optional[int] = None,
        type_id: Optional[int] = None,
        status: Optional[str] = None,
        tenant_id: Optional[int] = None,
        site_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all circuits with optional filtering."""
        params = {k: v for k, v in {
            'cid': cid, 'provider_id': provider_id, 'provider_account_id': provider_account_id,
            'type_id': type_id, 'status': status, 'tenant_id': tenant_id, 'site_id': site_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/circuits', params=params)

    async def get_circuit(self, id: int) -> Dict:
        """Get a specific circuit by ID."""
        return self.client.get(f'{self.base_endpoint}/circuits', id)

    async def create_circuit(
        self,
        cid: str,
        provider: int,
        type: int,
        status: str = 'active',
        provider_account: Optional[int] = None,
        tenant: Optional[int] = None,
        install_date: Optional[str] = None,
        termination_date: Optional[str] = None,
        commit_rate: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new circuit."""
        data = {'cid': cid, 'provider': provider, 'type': type, 'status': status, **kwargs}
        for key, val in [
            ('provider_account', provider_account), ('tenant', tenant),
            ('install_date', install_date), ('termination_date', termination_date),
            ('commit_rate', commit_rate), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/circuits', data)

    async def update_circuit(self, id: int, **kwargs) -> Dict:
        """Update a circuit."""
        return self.client.patch(f'{self.base_endpoint}/circuits', id, kwargs)

    async def delete_circuit(self, id: int) -> None:
        """Delete a circuit."""
        self.client.delete(f'{self.base_endpoint}/circuits', id)

    # ==================== Circuit Terminations ====================

    async def list_circuit_terminations(
        self,
        circuit_id: Optional[int] = None,
        site_id: Optional[int] = None,
        provider_network_id: Optional[int] = None,
        term_side: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all circuit terminations."""
        params = {k: v for k, v in {
            'circuit_id': circuit_id, 'site_id': site_id,
            'provider_network_id': provider_network_id, 'term_side': term_side, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/circuit-terminations', params=params)

    async def get_circuit_termination(self, id: int) -> Dict:
        """Get a specific circuit termination by ID."""
        return self.client.get(f'{self.base_endpoint}/circuit-terminations', id)

    async def create_circuit_termination(
        self,
        circuit: int,
        term_side: str,
        site: Optional[int] = None,
        provider_network: Optional[int] = None,
        port_speed: Optional[int] = None,
        upstream_speed: Optional[int] = None,
        xconnect_id: Optional[str] = None,
        pp_info: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new circuit termination."""
        data = {'circuit': circuit, 'term_side': term_side, **kwargs}
        for key, val in [
            ('site', site), ('provider_network', provider_network),
            ('port_speed', port_speed), ('upstream_speed', upstream_speed),
            ('xconnect_id', xconnect_id), ('pp_info', pp_info), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/circuit-terminations', data)

    async def update_circuit_termination(self, id: int, **kwargs) -> Dict:
        """Update a circuit termination."""
        return self.client.patch(f'{self.base_endpoint}/circuit-terminations', id, kwargs)

    async def delete_circuit_termination(self, id: int) -> None:
        """Delete a circuit termination."""
        self.client.delete(f'{self.base_endpoint}/circuit-terminations', id)

    async def get_circuit_termination_paths(self, id: int) -> Dict:
        """Get cable paths for a circuit termination."""
        return self.client.get(f'{self.base_endpoint}/circuit-terminations', f'{id}/paths')
