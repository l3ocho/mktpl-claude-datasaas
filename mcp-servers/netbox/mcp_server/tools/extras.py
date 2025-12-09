"""
Extras tools for NetBox MCP Server.

Covers: Tags, Custom Fields, Custom Links, Webhooks, Journal Entries, and more.
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

    async def update_tag(self, id: int, **kwargs) -> Dict:
        """Update a tag."""
        return self.client.patch(f'{self.base_endpoint}/tags', id, kwargs)

    async def delete_tag(self, id: int) -> None:
        """Delete a tag."""
        self.client.delete(f'{self.base_endpoint}/tags', id)

    # ==================== Custom Fields ====================

    async def list_custom_fields(
        self,
        name: Optional[str] = None,
        type: Optional[str] = None,
        content_types: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all custom fields."""
        params = {k: v for k, v in {
            'name': name, 'type': type, 'content_types': content_types, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/custom-fields', params=params)

    async def get_custom_field(self, id: int) -> Dict:
        """Get a specific custom field by ID."""
        return self.client.get(f'{self.base_endpoint}/custom-fields', id)

    async def create_custom_field(
        self,
        name: str,
        content_types: List[str],
        type: str = 'text',
        label: Optional[str] = None,
        description: Optional[str] = None,
        required: bool = False,
        filter_logic: str = 'loose',
        default: Optional[Any] = None,
        weight: int = 100,
        validation_minimum: Optional[int] = None,
        validation_maximum: Optional[int] = None,
        validation_regex: Optional[str] = None,
        choice_set: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Create a new custom field."""
        data = {
            'name': name, 'content_types': content_types, 'type': type,
            'required': required, 'filter_logic': filter_logic, 'weight': weight, **kwargs
        }
        for key, val in [
            ('label', label), ('description', description), ('default', default),
            ('validation_minimum', validation_minimum), ('validation_maximum', validation_maximum),
            ('validation_regex', validation_regex), ('choice_set', choice_set)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/custom-fields', data)

    async def update_custom_field(self, id: int, **kwargs) -> Dict:
        """Update a custom field."""
        return self.client.patch(f'{self.base_endpoint}/custom-fields', id, kwargs)

    async def delete_custom_field(self, id: int) -> None:
        """Delete a custom field."""
        self.client.delete(f'{self.base_endpoint}/custom-fields', id)

    # ==================== Custom Field Choice Sets ====================

    async def list_custom_field_choice_sets(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all custom field choice sets."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/custom-field-choice-sets', params=params)

    async def get_custom_field_choice_set(self, id: int) -> Dict:
        """Get a specific custom field choice set by ID."""
        return self.client.get(f'{self.base_endpoint}/custom-field-choice-sets', id)

    async def create_custom_field_choice_set(
        self,
        name: str,
        extra_choices: List[List[str]],
        description: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new custom field choice set."""
        data = {'name': name, 'extra_choices': extra_choices, **kwargs}
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/custom-field-choice-sets', data)

    async def update_custom_field_choice_set(self, id: int, **kwargs) -> Dict:
        """Update a custom field choice set."""
        return self.client.patch(f'{self.base_endpoint}/custom-field-choice-sets', id, kwargs)

    async def delete_custom_field_choice_set(self, id: int) -> None:
        """Delete a custom field choice set."""
        self.client.delete(f'{self.base_endpoint}/custom-field-choice-sets', id)

    # ==================== Custom Links ====================

    async def list_custom_links(
        self,
        name: Optional[str] = None,
        content_types: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all custom links."""
        params = {k: v for k, v in {
            'name': name, 'content_types': content_types, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/custom-links', params=params)

    async def get_custom_link(self, id: int) -> Dict:
        """Get a specific custom link by ID."""
        return self.client.get(f'{self.base_endpoint}/custom-links', id)

    async def create_custom_link(
        self,
        name: str,
        content_types: List[str],
        link_text: str,
        link_url: str,
        enabled: bool = True,
        new_window: bool = False,
        weight: int = 100,
        group_name: Optional[str] = None,
        button_class: str = 'outline-dark',
        **kwargs
    ) -> Dict:
        """Create a new custom link."""
        data = {
            'name': name, 'content_types': content_types,
            'link_text': link_text, 'link_url': link_url,
            'enabled': enabled, 'new_window': new_window,
            'weight': weight, 'button_class': button_class, **kwargs
        }
        if group_name:
            data['group_name'] = group_name
        return self.client.create(f'{self.base_endpoint}/custom-links', data)

    async def update_custom_link(self, id: int, **kwargs) -> Dict:
        """Update a custom link."""
        return self.client.patch(f'{self.base_endpoint}/custom-links', id, kwargs)

    async def delete_custom_link(self, id: int) -> None:
        """Delete a custom link."""
        self.client.delete(f'{self.base_endpoint}/custom-links', id)

    # ==================== Webhooks ====================

    async def list_webhooks(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all webhooks."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/webhooks', params=params)

    async def get_webhook(self, id: int) -> Dict:
        """Get a specific webhook by ID."""
        return self.client.get(f'{self.base_endpoint}/webhooks', id)

    async def create_webhook(
        self,
        name: str,
        payload_url: str,
        content_types: List[str],
        type_create: bool = True,
        type_update: bool = True,
        type_delete: bool = True,
        type_job_start: bool = False,
        type_job_end: bool = False,
        enabled: bool = True,
        http_method: str = 'POST',
        http_content_type: str = 'application/json',
        additional_headers: Optional[str] = None,
        body_template: Optional[str] = None,
        secret: Optional[str] = None,
        ssl_verification: bool = True,
        ca_file_path: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a new webhook."""
        data = {
            'name': name, 'payload_url': payload_url, 'content_types': content_types,
            'type_create': type_create, 'type_update': type_update, 'type_delete': type_delete,
            'type_job_start': type_job_start, 'type_job_end': type_job_end,
            'enabled': enabled, 'http_method': http_method,
            'http_content_type': http_content_type, 'ssl_verification': ssl_verification, **kwargs
        }
        for key, val in [
            ('additional_headers', additional_headers), ('body_template', body_template),
            ('secret', secret), ('ca_file_path', ca_file_path)
        ]:
            if val is not None:
                data[key] = val
        return self.client.create(f'{self.base_endpoint}/webhooks', data)

    async def update_webhook(self, id: int, **kwargs) -> Dict:
        """Update a webhook."""
        return self.client.patch(f'{self.base_endpoint}/webhooks', id, kwargs)

    async def delete_webhook(self, id: int) -> None:
        """Delete a webhook."""
        self.client.delete(f'{self.base_endpoint}/webhooks', id)

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

    async def update_journal_entry(self, id: int, **kwargs) -> Dict:
        """Update a journal entry."""
        return self.client.patch(f'{self.base_endpoint}/journal-entries', id, kwargs)

    async def delete_journal_entry(self, id: int) -> None:
        """Delete a journal entry."""
        self.client.delete(f'{self.base_endpoint}/journal-entries', id)

    # ==================== Config Contexts ====================

    async def list_config_contexts(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all config contexts."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/config-contexts', params=params)

    async def get_config_context(self, id: int) -> Dict:
        """Get a specific config context by ID."""
        return self.client.get(f'{self.base_endpoint}/config-contexts', id)

    async def create_config_context(
        self,
        name: str,
        data: Dict[str, Any],
        weight: int = 1000,
        description: Optional[str] = None,
        is_active: bool = True,
        regions: Optional[List[int]] = None,
        site_groups: Optional[List[int]] = None,
        sites: Optional[List[int]] = None,
        locations: Optional[List[int]] = None,
        device_types: Optional[List[int]] = None,
        roles: Optional[List[int]] = None,
        platforms: Optional[List[int]] = None,
        cluster_types: Optional[List[int]] = None,
        cluster_groups: Optional[List[int]] = None,
        clusters: Optional[List[int]] = None,
        tenant_groups: Optional[List[int]] = None,
        tenants: Optional[List[int]] = None,
        tags: Optional[List[str]] = None,
        **kwargs
    ) -> Dict:
        """Create a new config context."""
        context_data = {
            'name': name, 'data': data, 'weight': weight, 'is_active': is_active, **kwargs
        }
        for key, val in [
            ('description', description), ('regions', regions),
            ('site_groups', site_groups), ('sites', sites),
            ('locations', locations), ('device_types', device_types),
            ('roles', roles), ('platforms', platforms),
            ('cluster_types', cluster_types), ('cluster_groups', cluster_groups),
            ('clusters', clusters), ('tenant_groups', tenant_groups),
            ('tenants', tenants), ('tags', tags)
        ]:
            if val is not None:
                context_data[key] = val
        return self.client.create(f'{self.base_endpoint}/config-contexts', context_data)

    async def update_config_context(self, id: int, **kwargs) -> Dict:
        """Update a config context."""
        return self.client.patch(f'{self.base_endpoint}/config-contexts', id, kwargs)

    async def delete_config_context(self, id: int) -> None:
        """Delete a config context."""
        self.client.delete(f'{self.base_endpoint}/config-contexts', id)

    # ==================== Config Templates ====================

    async def list_config_templates(self, name: Optional[str] = None, **kwargs) -> List[Dict]:
        """List all config templates."""
        params = {k: v for k, v in {'name': name, **kwargs}.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/config-templates', params=params)

    async def get_config_template(self, id: int) -> Dict:
        """Get a specific config template by ID."""
        return self.client.get(f'{self.base_endpoint}/config-templates', id)

    async def create_config_template(
        self,
        name: str,
        template_code: str,
        description: Optional[str] = None,
        environment_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict:
        """Create a new config template."""
        data = {'name': name, 'template_code': template_code, **kwargs}
        if description:
            data['description'] = description
        if environment_params:
            data['environment_params'] = environment_params
        return self.client.create(f'{self.base_endpoint}/config-templates', data)

    async def update_config_template(self, id: int, **kwargs) -> Dict:
        """Update a config template."""
        return self.client.patch(f'{self.base_endpoint}/config-templates', id, kwargs)

    async def delete_config_template(self, id: int) -> None:
        """Delete a config template."""
        self.client.delete(f'{self.base_endpoint}/config-templates', id)

    # ==================== Export Templates ====================

    async def list_export_templates(
        self,
        name: Optional[str] = None,
        content_types: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all export templates."""
        params = {k: v for k, v in {
            'name': name, 'content_types': content_types, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/export-templates', params=params)

    async def get_export_template(self, id: int) -> Dict:
        """Get a specific export template by ID."""
        return self.client.get(f'{self.base_endpoint}/export-templates', id)

    async def create_export_template(
        self,
        name: str,
        content_types: List[str],
        template_code: str,
        description: Optional[str] = None,
        mime_type: str = 'text/plain',
        file_extension: Optional[str] = None,
        as_attachment: bool = True,
        **kwargs
    ) -> Dict:
        """Create a new export template."""
        data = {
            'name': name, 'content_types': content_types,
            'template_code': template_code, 'mime_type': mime_type,
            'as_attachment': as_attachment, **kwargs
        }
        if description:
            data['description'] = description
        if file_extension:
            data['file_extension'] = file_extension
        return self.client.create(f'{self.base_endpoint}/export-templates', data)

    async def update_export_template(self, id: int, **kwargs) -> Dict:
        """Update an export template."""
        return self.client.patch(f'{self.base_endpoint}/export-templates', id, kwargs)

    async def delete_export_template(self, id: int) -> None:
        """Delete an export template."""
        self.client.delete(f'{self.base_endpoint}/export-templates', id)

    # ==================== Saved Filters ====================

    async def list_saved_filters(
        self,
        name: Optional[str] = None,
        content_types: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all saved filters."""
        params = {k: v for k, v in {
            'name': name, 'content_types': content_types, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/saved-filters', params=params)

    async def get_saved_filter(self, id: int) -> Dict:
        """Get a specific saved filter by ID."""
        return self.client.get(f'{self.base_endpoint}/saved-filters', id)

    async def create_saved_filter(
        self,
        name: str,
        slug: str,
        content_types: List[str],
        parameters: Dict[str, Any],
        description: Optional[str] = None,
        weight: int = 100,
        enabled: bool = True,
        shared: bool = True,
        **kwargs
    ) -> Dict:
        """Create a new saved filter."""
        data = {
            'name': name, 'slug': slug, 'content_types': content_types,
            'parameters': parameters, 'weight': weight,
            'enabled': enabled, 'shared': shared, **kwargs
        }
        if description:
            data['description'] = description
        return self.client.create(f'{self.base_endpoint}/saved-filters', data)

    async def update_saved_filter(self, id: int, **kwargs) -> Dict:
        """Update a saved filter."""
        return self.client.patch(f'{self.base_endpoint}/saved-filters', id, kwargs)

    async def delete_saved_filter(self, id: int) -> None:
        """Delete a saved filter."""
        self.client.delete(f'{self.base_endpoint}/saved-filters', id)

    # ==================== Image Attachments ====================

    async def list_image_attachments(
        self,
        object_type: Optional[str] = None,
        object_id: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """List all image attachments."""
        params = {k: v for k, v in {
            'object_type': object_type, 'object_id': object_id, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/image-attachments', params=params)

    async def get_image_attachment(self, id: int) -> Dict:
        """Get a specific image attachment by ID."""
        return self.client.get(f'{self.base_endpoint}/image-attachments', id)

    async def delete_image_attachment(self, id: int) -> None:
        """Delete an image attachment."""
        self.client.delete(f'{self.base_endpoint}/image-attachments', id)

    # ==================== Object Changes (Audit Log) ====================

    async def list_object_changes(
        self,
        user_id: Optional[int] = None,
        changed_object_type: Optional[str] = None,
        changed_object_id: Optional[int] = None,
        action: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """List all object changes (audit log)."""
        params = {k: v for k, v in {
            'user_id': user_id, 'changed_object_type': changed_object_type,
            'changed_object_id': changed_object_id, 'action': action, **kwargs
        }.items() if v is not None}
        return self.client.list(f'{self.base_endpoint}/object-changes', params=params)

    async def get_object_change(self, id: int) -> Dict:
        """Get a specific object change by ID."""
        return self.client.get(f'{self.base_endpoint}/object-changes', id)

    # ==================== Scripts ====================

    async def list_scripts(self, **kwargs) -> List[Dict]:
        """List all available scripts."""
        return self.client.list(f'{self.base_endpoint}/scripts', params=kwargs)

    async def get_script(self, id: str) -> Dict:
        """Get a specific script by ID."""
        return self.client.get(f'{self.base_endpoint}/scripts', id)

    async def run_script(self, id: str, data: Dict[str, Any], commit: bool = True) -> Dict:
        """Run a script with the provided data."""
        payload = {'data': data, 'commit': commit}
        return self.client.create(f'{self.base_endpoint}/scripts/{id}', payload)

    # ==================== Reports ====================

    async def list_reports(self, **kwargs) -> List[Dict]:
        """List all available reports."""
        return self.client.list(f'{self.base_endpoint}/reports', params=kwargs)

    async def get_report(self, id: str) -> Dict:
        """Get a specific report by ID."""
        return self.client.get(f'{self.base_endpoint}/reports', id)

    async def run_report(self, id: str) -> Dict:
        """Run a report."""
        return self.client.create(f'{self.base_endpoint}/reports/{id}', {})
