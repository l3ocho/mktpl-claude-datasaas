#!/usr/bin/env python3
"""
Generate DMC Component Registry from installed dash-mantine-components package.

This script introspects the installed DMC package and generates a JSON registry
file containing component definitions, props, types, and defaults.

Usage:
    python generate-dmc-registry.py [--output registry/dmc_X_Y.json]

Requirements:
    - dash-mantine-components must be installed
    - Run from the mcp-servers/viz-platform directory
"""
import argparse
import inspect
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, get_type_hints


def get_dmc_version() -> Optional[str]:
    """Get installed DMC version."""
    try:
        from importlib.metadata import version
        return version('dash-mantine-components')
    except Exception:
        return None


def get_component_categories() -> Dict[str, List[str]]:
    """Define component categories."""
    return {
        "buttons": ["Button", "ActionIcon", "CopyButton", "FileButton", "UnstyledButton"],
        "inputs": [
            "TextInput", "PasswordInput", "NumberInput", "Textarea",
            "Select", "MultiSelect", "Checkbox", "Switch", "Radio",
            "Slider", "RangeSlider", "ColorInput", "ColorPicker",
            "DateInput", "DatePicker", "TimeInput"
        ],
        "navigation": ["Anchor", "Breadcrumbs", "Burger", "NavLink", "Pagination", "Stepper", "Tabs"],
        "feedback": ["Alert", "Loader", "Notification", "Progress", "RingProgress", "Skeleton"],
        "overlays": ["Dialog", "Drawer", "HoverCard", "Menu", "Modal", "Popover", "Tooltip"],
        "typography": ["Blockquote", "Code", "Highlight", "Mark", "Text", "Title"],
        "layout": [
            "AppShell", "AspectRatio", "Center", "Container", "Flex",
            "Grid", "Group", "Paper", "SimpleGrid", "Space", "Stack"
        ],
        "data": [
            "Accordion", "Avatar", "Badge", "Card", "Image",
            "Indicator", "Kbd", "Spoiler", "Table", "ThemeIcon", "Timeline"
        ]
    }


def extract_prop_type(prop_info: Dict[str, Any]) -> Dict[str, Any]:
    """Extract prop type information from Dash component prop."""
    result = {"type": "any"}

    if 'type' not in prop_info:
        return result

    prop_type = prop_info['type']

    if isinstance(prop_type, dict):
        type_name = prop_type.get('name', 'any')

        # Map Dash types to JSON schema types
        type_mapping = {
            'string': 'string',
            'number': 'number',
            'bool': 'boolean',
            'boolean': 'boolean',
            'array': 'array',
            'object': 'object',
            'node': 'any',
            'element': 'any',
            'any': 'any',
            'func': 'any',
        }

        result['type'] = type_mapping.get(type_name, 'any')

        # Handle enums
        if type_name == 'enum' and 'value' in prop_type:
            values = prop_type['value']
            if isinstance(values, list):
                enum_values = []
                for v in values:
                    if isinstance(v, dict) and 'value' in v:
                        # Remove quotes from string values
                        val = v['value'].strip("'\"")
                        enum_values.append(val)
                    elif isinstance(v, str):
                        enum_values.append(v.strip("'\""))
                if enum_values:
                    result['enum'] = enum_values
                    result['type'] = 'string'

        # Handle union types
        elif type_name == 'union' and 'value' in prop_type:
            # For unions, just mark as any for simplicity
            result['type'] = 'any'

    elif isinstance(prop_type, str):
        result['type'] = prop_type

    return result


def extract_component_props(component_class) -> Dict[str, Any]:
    """Extract props from a Dash component class."""
    props = {}

    # Try to get _prop_names or similar
    if hasattr(component_class, '_prop_names'):
        prop_names = component_class._prop_names
    else:
        prop_names = []

    # Try to get _type attribute for prop definitions
    if hasattr(component_class, '_type'):
        prop_types = getattr(component_class, '_type', {})
    else:
        prop_types = {}

    # Get default values
    if hasattr(component_class, '_default_props'):
        defaults = component_class._default_props
    else:
        defaults = {}

    # Try to extract from _prop_descriptions
    if hasattr(component_class, '_prop_descriptions'):
        descriptions = component_class._prop_descriptions
    else:
        descriptions = {}

    for prop_name in prop_names:
        if prop_name.startswith('_'):
            continue

        prop_info = {}

        # Get type info if available
        if prop_name in prop_types:
            prop_info = extract_prop_type({'type': prop_types[prop_name]})
        else:
            prop_info = {'type': 'any'}

        # Add default if exists
        if prop_name in defaults:
            prop_info['default'] = defaults[prop_name]

        # Add description if exists
        if prop_name in descriptions:
            prop_info['description'] = descriptions[prop_name]

        props[prop_name] = prop_info

    return props


def generate_registry() -> Dict[str, Any]:
    """Generate the component registry from installed DMC."""
    try:
        import dash_mantine_components as dmc
    except ImportError:
        print("ERROR: dash-mantine-components not installed")
        print("Install with: pip install dash-mantine-components")
        sys.exit(1)

    version = get_dmc_version()
    categories = get_component_categories()

    registry = {
        "version": version,
        "generated": date.today().isoformat(),
        "categories": categories,
        "components": {}
    }

    # Get all components from categories
    all_components = set()
    for comp_list in categories.values():
        all_components.update(comp_list)

    # Extract props for each component
    for comp_name in sorted(all_components):
        if hasattr(dmc, comp_name):
            comp_class = getattr(dmc, comp_name)
            try:
                props = extract_component_props(comp_class)
                if props:
                    registry["components"][comp_name] = {
                        "description": comp_class.__doc__ or f"{comp_name} component",
                        "props": props
                    }
                    print(f"  Extracted: {comp_name} ({len(props)} props)")
            except Exception as e:
                print(f"  Warning: Failed to extract {comp_name}: {e}")
        else:
            print(f"  Warning: Component not found: {comp_name}")

    return registry


def main():
    parser = argparse.ArgumentParser(
        description="Generate DMC component registry from installed package"
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (default: auto-generated based on version)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print to stdout instead of writing file'
    )

    args = parser.parse_args()

    print("Generating DMC Component Registry...")
    print("=" * 50)

    registry = generate_registry()

    print("=" * 50)
    print(f"Generated registry for DMC {registry['version']}")
    print(f"Total components: {len(registry['components'])}")

    if args.dry_run:
        print(json.dumps(registry, indent=2))
        return

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        version = registry['version']
        if version:
            major_minor = '_'.join(version.split('.')[:2])
            output_path = Path(__file__).parent.parent / 'registry' / f'dmc_{major_minor}.json'
        else:
            output_path = Path(__file__).parent.parent / 'registry' / 'dmc_unknown.json'

    # Create directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write registry
    with open(output_path, 'w') as f:
        json.dump(registry, indent=2, fp=f)

    print(f"Registry written to: {output_path}")


if __name__ == "__main__":
    main()
