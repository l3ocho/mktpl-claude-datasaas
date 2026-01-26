"""
Layout composition tools for dashboard building.

Provides tools for creating structured layouts with grids, filters, and sections.
"""
import logging
from typing import Dict, List, Optional, Any
from uuid import uuid4

logger = logging.getLogger(__name__)


# Layout templates
TEMPLATES = {
    "dashboard": {
        "sections": ["header", "filters", "main", "footer"],
        "default_grid": {"cols": 12, "spacing": "md"},
        "description": "Standard dashboard with header, filters, main content, and footer"
    },
    "report": {
        "sections": ["title", "summary", "content", "appendix"],
        "default_grid": {"cols": 1, "spacing": "lg"},
        "description": "Report layout with title, summary, and content sections"
    },
    "form": {
        "sections": ["header", "fields", "actions"],
        "default_grid": {"cols": 2, "spacing": "md"},
        "description": "Form layout with header, fields, and action buttons"
    },
    "blank": {
        "sections": ["main"],
        "default_grid": {"cols": 12, "spacing": "md"},
        "description": "Blank canvas for custom layouts"
    }
}


# Filter type definitions
FILTER_TYPES = {
    "dropdown": {
        "component": "Select",
        "props": ["label", "data", "placeholder", "clearable", "searchable", "value"]
    },
    "multi_select": {
        "component": "MultiSelect",
        "props": ["label", "data", "placeholder", "clearable", "searchable", "value"]
    },
    "date_range": {
        "component": "DateRangePicker",
        "props": ["label", "placeholder", "value", "minDate", "maxDate"]
    },
    "date": {
        "component": "DatePicker",
        "props": ["label", "placeholder", "value", "minDate", "maxDate"]
    },
    "search": {
        "component": "TextInput",
        "props": ["label", "placeholder", "value", "icon"]
    },
    "checkbox_group": {
        "component": "CheckboxGroup",
        "props": ["label", "children", "value"]
    },
    "radio_group": {
        "component": "RadioGroup",
        "props": ["label", "children", "value"]
    },
    "slider": {
        "component": "Slider",
        "props": ["label", "min", "max", "step", "value", "marks"]
    },
    "range_slider": {
        "component": "RangeSlider",
        "props": ["label", "min", "max", "step", "value", "marks"]
    }
}


class LayoutTools:
    """
    Dashboard layout composition tools.

    Creates layouts that map to DMC Grid and AppShell components.
    """

    def __init__(self):
        """Initialize layout tools."""
        self._layouts: Dict[str, Dict[str, Any]] = {}

    async def layout_create(
        self,
        name: str,
        template: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new layout container.

        Args:
            name: Unique name for the layout
            template: Optional template (dashboard, report, form, blank)

        Returns:
            Dict with:
                - layout_ref: Reference to use in other tools
                - template: Template used
                - sections: Available sections
                - grid: Default grid configuration
        """
        # Validate template
        template = template or "blank"
        if template not in TEMPLATES:
            return {
                "error": f"Invalid template '{template}'. Must be one of: {list(TEMPLATES.keys())}",
                "layout_ref": None
            }

        # Check for name collision
        if name in self._layouts:
            return {
                "error": f"Layout '{name}' already exists. Use a different name or modify existing.",
                "layout_ref": name
            }

        template_config = TEMPLATES[template]

        # Create layout structure
        layout = {
            "id": str(uuid4()),
            "name": name,
            "template": template,
            "sections": {section: {"items": []} for section in template_config["sections"]},
            "grid": template_config["default_grid"].copy(),
            "filters": [],
            "metadata": {
                "description": template_config["description"]
            }
        }

        self._layouts[name] = layout

        return {
            "layout_ref": name,
            "template": template,
            "sections": template_config["sections"],
            "grid": layout["grid"],
            "description": template_config["description"]
        }

    async def layout_add_filter(
        self,
        layout_ref: str,
        filter_type: str,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add a filter control to a layout.

        Args:
            layout_ref: Layout name to add filter to
            filter_type: Type of filter (dropdown, date_range, search, checkbox_group, etc.)
            options: Filter options (label, data for dropdown, placeholder, position)

        Returns:
            Dict with:
                - filter_id: Unique ID for the filter
                - component: DMC component that will be used
                - props: Props that were set
                - position: Where filter was placed
        """
        # Validate layout exists
        if layout_ref not in self._layouts:
            return {
                "error": f"Layout '{layout_ref}' not found. Create it first with layout_create.",
                "filter_id": None
            }

        # Validate filter type
        if filter_type not in FILTER_TYPES:
            return {
                "error": f"Invalid filter_type '{filter_type}'. Must be one of: {list(FILTER_TYPES.keys())}",
                "filter_id": None
            }

        filter_config = FILTER_TYPES[filter_type]
        layout = self._layouts[layout_ref]

        # Generate filter ID
        filter_id = f"filter_{filter_type}_{len(layout['filters'])}"

        # Extract relevant props
        props = {"id": filter_id}
        for prop in filter_config["props"]:
            if prop in options:
                props[prop] = options[prop]

        # Determine position
        position = options.get("position", "filters")
        if position not in layout["sections"]:
            # Default to first available section
            position = list(layout["sections"].keys())[0]

        # Create filter definition
        filter_def = {
            "id": filter_id,
            "type": filter_type,
            "component": filter_config["component"],
            "props": props,
            "position": position
        }

        layout["filters"].append(filter_def)
        layout["sections"][position]["items"].append({
            "type": "filter",
            "ref": filter_id
        })

        return {
            "filter_id": filter_id,
            "component": filter_config["component"],
            "props": props,
            "position": position,
            "layout_ref": layout_ref
        }

    async def layout_set_grid(
        self,
        layout_ref: str,
        grid: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Configure the grid system for a layout.

        Args:
            layout_ref: Layout name to configure
            grid: Grid configuration:
                - cols: Number of columns (default 12)
                - spacing: Gap between items (xs, sm, md, lg, xl)
                - breakpoints: Responsive breakpoints {xs: cols, sm: cols, ...}
                - gutter: Gutter size

        Returns:
            Dict with:
                - grid: Updated grid configuration
                - layout_ref: Layout reference
        """
        # Validate layout exists
        if layout_ref not in self._layouts:
            return {
                "error": f"Layout '{layout_ref}' not found. Create it first with layout_create.",
                "grid": None
            }

        layout = self._layouts[layout_ref]

        # Validate spacing if provided
        valid_spacing = ["xs", "sm", "md", "lg", "xl"]
        if "spacing" in grid and grid["spacing"] not in valid_spacing:
            return {
                "error": f"Invalid spacing '{grid['spacing']}'. Must be one of: {valid_spacing}",
                "grid": layout["grid"]
            }

        # Validate cols
        if "cols" in grid:
            cols = grid["cols"]
            if not isinstance(cols, int) or cols < 1 or cols > 24:
                return {
                    "error": f"Invalid cols '{cols}'. Must be integer between 1 and 24.",
                    "grid": layout["grid"]
                }

        # Update grid configuration
        layout["grid"].update(grid)

        # Process breakpoints if provided
        if "breakpoints" in grid:
            bp = grid["breakpoints"]
            layout["grid"]["breakpoints"] = bp

        return {
            "grid": layout["grid"],
            "layout_ref": layout_ref
        }

    async def layout_get(self, layout_ref: str) -> Dict[str, Any]:
        """
        Get a layout's full configuration.

        Args:
            layout_ref: Layout name to retrieve

        Returns:
            Full layout configuration or error
        """
        if layout_ref not in self._layouts:
            return {
                "error": f"Layout '{layout_ref}' not found.",
                "layout": None
            }

        layout = self._layouts[layout_ref]

        return {
            "layout": layout,
            "filter_count": len(layout["filters"]),
            "sections": list(layout["sections"].keys())
        }

    async def layout_add_section(
        self,
        layout_ref: str,
        section_name: str,
        position: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Add a custom section to a layout.

        Args:
            layout_ref: Layout name
            section_name: Name for the new section
            position: Optional position index (appends if not specified)

        Returns:
            Dict with sections list and the new section name
        """
        if layout_ref not in self._layouts:
            return {
                "error": f"Layout '{layout_ref}' not found.",
                "sections": []
            }

        layout = self._layouts[layout_ref]

        if section_name in layout["sections"]:
            return {
                "error": f"Section '{section_name}' already exists.",
                "sections": list(layout["sections"].keys())
            }

        # Add new section
        layout["sections"][section_name] = {"items": []}

        return {
            "section_name": section_name,
            "sections": list(layout["sections"].keys()),
            "layout_ref": layout_ref
        }

    def get_available_templates(self) -> Dict[str, Any]:
        """Get list of available layout templates."""
        return {
            name: {
                "sections": config["sections"],
                "description": config["description"]
            }
            for name, config in TEMPLATES.items()
        }

    def get_available_filter_types(self) -> Dict[str, Any]:
        """Get list of available filter types."""
        return {
            name: {
                "component": config["component"],
                "props": config["props"]
            }
            for name, config in FILTER_TYPES.items()
        }
