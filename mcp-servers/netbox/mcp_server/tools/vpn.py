"""
VPN tools for NetBox MCP Server.

Covers: Tunnels, Tunnel Groups, Tunnel Terminations, IKE/IPSec Policies, and L2VPN.
"""
import logging
from typing import List, Dict, Optional, Any
from ..netbox_client import NetBoxClient

logger = logging.getLogger(__name__)


class VPNTools:
    """Tools for VPN operations in NetBox"""

    def __init__(self, client: NetBoxClient):
        self.client = client
        self.base_endpoint = 'vpn'

    # ==================== Tunnel Groups ====================

    async def list_tunnel_groups(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all tunnel groups."""
        params = {k: v for k, v in {'name': name, 'slug': slug, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/tunnel-groups', params=params)

    async def get_tunnel_group(self, id: int) -> Dict:
        """Get a specific tunnel group by ID."""
        return self.client.get(f'{self.base_endpoint}/tunnel-groups', id)

    async def create_tunnel_group(
        self,
        name: str,
        slug: str,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new tunnel group."""
        data = {'name': name, 'slug': slug, **kwargs}
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/tunnel-groups', data)

    async def update_tunnel_group(self, id: int, **kwargs) -> Dict:
        """Update a tunnel group."""
        return self.client.patch(f'{self.base_endpoint}/tunnel-groups', id, kwargs)

    async def delete_tunnel_group(self, id: int) -> None:
        """Delete a tunnel group."""
        self.client.delete(f'{self.base_endpoint}/tunnel-groups', id)

    # ==================== Tunnels ====================

    async def list_tunnels(
        self,
        name: Optional[str] = None,
        status: Optional[str] = None,
        group_id: Optional[int] = None,
        encapsulation: Optional[str] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all tunnels with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'status': status, 'group_id': group_id,
            'encapsulation': encapsulation, 'tenant_id': tenant_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/tunnels', params=params)

    async def get_tunnel(self, id: int) -> Dict:
        """Get a specific tunnel by ID."""
        return self.client.get(f'{self.base_endpoint}/tunnels', id)

    async def create_tunnel(
        self,
        name: str,
        status: str = 'active',
        encapsulation: str = 'ipsec-tunnel',
        group: Optional[int] = None,
        ipsec_profile: Optional[int] = None,
        tenant: Optional[int] = None,
        tunnel_id: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new tunnel."""
        data = {'name': name, 'status': status, 'encapsulation': encapsulation, **kwargs}
        for key, val in [
            ('group', group), ('ipsec_profile', ipsec_profile),
            ('tenant', tenant), ('tunnel_id', tunnel_id), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/tunnels', data)

    async def update_tunnel(self, id: int, **kwargs) -> Dict:
        """Update a tunnel."""
        return self.client.patch(f'{self.base_endpoint}/tunnels', id, kwargs)

    async def delete_tunnel(self, id: int) -> None:
        """Delete a tunnel."""
        self.client.delete(f'{self.base_endpoint}/tunnels', id)

    # ==================== Tunnel Terminations ====================

    async def list_tunnel_terminations(
        self,
        tunnel_id: Optional[int] = None,
        role: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all tunnel terminations."""
        params = {k: v for k, v in {
            'tunnel_id': tunnel_id, 'role': role, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/tunnel-terminations', params=params)

    async def get_tunnel_termination(self, id: int) -> Dict:
        """Get a specific tunnel termination by ID."""
        return self.client.get(f'{self.base_endpoint}/tunnel-terminations', id)

    async def create_tunnel_termination(
        self,
        tunnel: int,
        role: str,
        termination_type: str,
        termination_id: int,
        outside_ip: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Create a new tunnel termination."""
        data = {
            'tunnel': tunnel, 'role': role,
            'termination_type': termination_type, 'termination_id': termination_id, **kwargs
        }
        if outside_ip:
            data['outside_ip'] = outside_ip
        return self.client.create(f'{self.base_endpoint}/tunnel-terminations', data)

    async def update_tunnel_termination(self, id: int, **kwargs) -> Dict:
        """Update a tunnel termination."""
        return self.client.patch(f'{self.base_endpoint}/tunnel-terminations', id, kwargs)

    async def delete_tunnel_termination(self, id: int) -> None:
        """Delete a tunnel termination."""
        self.client.delete(f'{self.base_endpoint}/tunnel-terminations', id)

    # ==================== IKE Proposals ====================

    async def list_ike_proposals(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all IKE proposals."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/ike-proposals', params=params)

    async def get_ike_proposal(self, id: int) -> Dict:
        """Get a specific IKE proposal by ID."""
        return self.client.get(f'{self.base_endpoint}/ike-proposals', id)

    async def create_ike_proposal(
        self,
        name: str,
        authentication_method: str,
        encryption_algorithm: str,
        authentication_algorithm: str,
        group: int,
        sa_lifetime: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new IKE proposal."""
        data = {
            'name': name, 'authentication_method': authentication_method,
            'encryption_algorithm': encryption_algorithm,
            'authentication_algorithm': authentication_algorithm, 'group': group, **kwargs
        }
        if sa_lifetime:
            data['sa_lifetime'] = sa_lifetime
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/ike-proposals', data)

    async def update_ike_proposal(self, id: int, **kwargs) -> Dict:
        """Update an IKE proposal."""
        return self.client.patch(f'{self.base_endpoint}/ike-proposals', id, kwargs)

    async def delete_ike_proposal(self, id: int) -> None:
        """Delete an IKE proposal."""
        self.client.delete(f'{self.base_endpoint}/ike-proposals', id)

    # ==================== IKE Policies ====================

    async def list_ike_policies(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all IKE policies."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/ike-policies', params=params)

    async def get_ike_policy(self, id: int) -> Dict:
        """Get a specific IKE policy by ID."""
        return self.client.get(f'{self.base_endpoint}/ike-policies', id)

    async def create_ike_policy(
        self,
        name: str,
        version: int,
        mode: str,
        proposals: List[int],
        preshared_key: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new IKE policy."""
        data = {'name': name, 'version': version, 'mode': mode, 'proposals': proposals, **kwargs}
        if preshared_key:
            data['preshared_key'] = preshared_key
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/ike-policies', data)

    async def update_ike_policy(self, id: int, **kwargs) -> Dict:
        """Update an IKE policy."""
        return self.client.patch(f'{self.base_endpoint}/ike-policies', id, kwargs)

    async def delete_ike_policy(self, id: int) -> None:
        """Delete an IKE policy."""
        self.client.delete(f'{self.base_endpoint}/ike-policies', id)

    # ==================== IPSec Proposals ====================

    async def list_ipsec_proposals(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all IPSec proposals."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/ipsec-proposals', params=params)

    async def get_ipsec_proposal(self, id: int) -> Dict:
        """Get a specific IPSec proposal by ID."""
        return self.client.get(f'{self.base_endpoint}/ipsec-proposals', id)

    async def create_ipsec_proposal(
        self,
        name: str,
        encryption_algorithm: str,
        authentication_algorithm: str,
        sa_lifetime_seconds: Optional[int] = None,
        sa_lifetime_data: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new IPSec proposal."""
        data = {
            'name': name, 'encryption_algorithm': encryption_algorithm,
            'authentication_algorithm': authentication_algorithm, **kwargs
        }
        for key, val in [
            ('sa_lifetime_seconds', sa_lifetime_seconds),
            ('sa_lifetime_data', sa_lifetime_data), ('description', description)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/ipsec-proposals', data)

    async def update_ipsec_proposal(self, id: int, **kwargs) -> Dict:
        """Update an IPSec proposal."""
        return self.client.patch(f'{self.base_endpoint}/ipsec-proposals', id, kwargs)

    async def delete_ipsec_proposal(self, id: int) -> None:
        """Delete an IPSec proposal."""
        self.client.delete(f'{self.base_endpoint}/ipsec-proposals', id)

    # ==================== IPSec Policies ====================

    async def list_ipsec_policies(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all IPSec policies."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/ipsec-policies', params=params)

    async def get_ipsec_policy(self, id: int) -> Dict:
        """Get a specific IPSec policy by ID."""
        return self.client.get(f'{self.base_endpoint}/ipsec-policies', id)

    async def create_ipsec_policy(
        self,
        name: str,
        proposals: List[int],
        pfs_group: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new IPSec policy."""
        data = {'name': name, 'proposals': proposals, **kwargs}
        if pfs_group:
            data['pfs_group'] = pfs_group
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/ipsec-policies', data)

    async def update_ipsec_policy(self, id: int, **kwargs) -> Dict:
        """Update an IPSec policy."""
        return self.client.patch(f'{self.base_endpoint}/ipsec-policies', id, kwargs)

    async def delete_ipsec_policy(self, id: int) -> None:
        """Delete an IPSec policy."""
        self.client.delete(f'{self.base_endpoint}/ipsec-policies', id)

    # ==================== IPSec Profiles ====================

    async def list_ipsec_profiles(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all IPSec profiles."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/ipsec-profiles', params=params)

    async def get_ipsec_profile(self, id: int) -> Dict:
        """Get a specific IPSec profile by ID."""
        return self.client.get(f'{self.base_endpoint}/ipsec-profiles', id)

    async def create_ipsec_profile(
        self,
        name: str,
        mode: str,
        ike_policy: int,
        ipsec_policy: int,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new IPSec profile."""
        data = {'name': name, 'mode': mode, 'ike_policy': ike_policy, 'ipsec_policy': ipsec_policy, **kwargs}
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/ipsec-profiles', data)

    async def update_ipsec_profile(self, id: int, **kwargs) -> Dict:
        """Update an IPSec profile."""
        return self.client.patch(f'{self.base_endpoint}/ipsec-profiles', id, kwargs)

    async def delete_ipsec_profile(self, id: int) -> None:
        """Delete an IPSec profile."""
        self.client.delete(f'{self.base_endpoint}/ipsec-profiles', id)

    # ==================== L2VPN ====================

    async def list_l2vpns(
        self,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        type: Optional[str] = None,
        tenant_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all L2VPNs with optional filtering."""
        params = {k: v for k, v in {
            'name': name, 'slug': slug, 'type': type, 'tenant_id': tenant_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/l2vpns', params=params)

    async def get_l2vpn(self, id: int) -> Dict:
        """Get a specific L2VPN by ID."""
        return self.client.get(f'{self.base_endpoint}/l2vpns', id)

    async def create_l2vpn(
        self,
        name: str,
        slug: str,
        type: str,
        identifier: Optional[int] = None,
        tenant: Optional[int] = None,
        description: Optional[str] = None,
        import_targets: Optional[List[int]] = None,
        export_targets: Optional[List[int]] = None,
        **kwargs
    ) -> Dict:
        """Create a new L2VPN."""
        data = {'name': name, 'slug': slug, 'type': type, **kwargs}
        for key, val in [
            ('identifier', identifier), ('tenant', tenant), ('description', description),
            ('import_targets', import_targets), ('export_targets', export_targets)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/l2vpns', data)

    async def update_l2vpn(self, id: int, **kwargs) -> Dict:
        """Update an L2VPN."""
        return self.client.patch(f'{self.base_endpoint}/l2vpns', id, kwargs)

    async def delete_l2vpn(self, id: int) -> None:
        """Delete an L2VPN."""
        self.client.delete(f'{self.base_endpoint}/l2vpns', id)

    # ==================== L2VPN Terminations ====================

    async def list_l2vpn_terminations(
        self,
        l2vpn_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all L2VPN terminations."""
        params = {k: v for k, v in {'l2vpn_id': l2vpn_id, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/l2vpn-terminations', params=params)

    async def get_l2vpn_termination(self, id: int) -> Dict:
        """Get a specific L2VPN termination by ID."""
        return self.client.get(f'{self.base_endpoint}/l2vpn-terminations', id)

    async def create_l2vpn_termination(
        self,
        l2vpn: int,
        assigned_object_type: str,
        assigned_object_id: int,
        **kwargs
    ) -> Dict:
        """Create a new L2VPN termination."""
        data = {
            'l2vpn': l2vpn, 'assigned_object_type': assigned_object_type,
            'assigned_object_id': assigned_object_id, **kwargs
        }
        return self.client.create(f'{self.base_endpoint}/l2vpn-terminations', data)

    async def update_l2vpn_termination(self, id: int, **kwargs) -> Dict:
        """Update an L2VPN termination."""
        return self.client.patch(f'{self.base_endpoint}/l2vpn-terminations', id, kwargs)

    async def delete_l2vpn_termination(self, id: int) -> None:
        """Delete an L2VPN termination."""
        self.client.delete(f'{self.base_endpoint}/l2vpn-terminations', id)
