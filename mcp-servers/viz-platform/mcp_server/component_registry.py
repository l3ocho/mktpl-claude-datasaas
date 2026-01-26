"""
DMC Component Registry for viz-platform.

Provides version-locked component definitions to prevent Claude from
hallucinating invalid props. Uses static JSON registries pre-generated
from DMC source.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class ComponentRegistry:
    """
    Version-locked registry of Dash Mantine Components.

    Loads component definitions from static JSON files and provides
    lookup methods for validation tools.
    """

    def __init__(self, dmc_version: Optional[str] = None):
        """
        Initialize the component registry.

        Args:
            dmc_version: Installed DMC version (e.g., "0.14.7").
                        If None, will try to detect or use fallback.
        """
        self.dmc_version = dmc_version
        self.registry_dir = Path(__file__).parent.parent / 'registry'
        self.components: Dict[str, Dict[str, Any]] = {}
        self.categories: Dict[str, List[str]] = {}
        self.loaded_version: Optional[str] = None

    def load(self) -> bool:
        """
        Load the component registry for the configured DMC version.

        Returns:
            True if registry loaded successfully, False otherwise
        """
        registry_file = self._find_registry_file()

        if not registry_file:
            logger.warning(
                f"No registry found for DMC {self.dmc_version}. "
                "Component validation will be limited."
            )
            return False

        try:
            with open(registry_file, 'r') as f:
                data = json.load(f)

            self.loaded_version = data.get('version')
            self.components = data.get('components', {})
            self.categories = data.get('categories', {})

            logger.info(
                f"Loaded component registry v{self.loaded_version} "
                f"with {len(self.components)} components"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to load registry: {e}")
            return False

    def _find_registry_file(self) -> Optional[Path]:
        """
        Find the best matching registry file for the DMC version.

        Strategy:
        1. Exact major.minor match (e.g., dmc_0_14.json for 0.14.7)
        2. Fallback to latest available registry

        Returns:
            Path to registry file, or None if not found
        """
        if not self.registry_dir.exists():
            logger.warning(f"Registry directory not found: {self.registry_dir}")
            return None

        # Try exact major.minor match
        if self.dmc_version:
            parts = self.dmc_version.split('.')
            if len(parts) >= 2:
                major_minor = f"{parts[0]}_{parts[1]}"
                exact_match = self.registry_dir / f"dmc_{major_minor}.json"
                if exact_match.exists():
                    return exact_match

        # Fallback: find latest registry
        registry_files = list(self.registry_dir.glob("dmc_*.json"))
        if registry_files:
            # Sort by version and return latest
            registry_files.sort(reverse=True)
            fallback = registry_files[0]
            if self.dmc_version:
                logger.warning(
                    f"No exact match for DMC {self.dmc_version}, "
                    f"using fallback: {fallback.name}"
                )
            return fallback

        return None

    def get_component(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get component definition by name.

        Args:
            name: Component name (e.g., "Button", "TextInput")

        Returns:
            Component definition dict, or None if not found
        """
        return self.components.get(name)

    def get_component_props(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get props schema for a component.

        Args:
            name: Component name

        Returns:
            Props dict with type info, or None if component not found
        """
        component = self.get_component(name)
        if component:
            return component.get('props', {})
        return None

    def list_components(self, category: Optional[str] = None) -> Dict[str, List[str]]:
        """
        List available components, optionally filtered by category.

        Args:
            category: Optional category filter (e.g., "inputs", "buttons")

        Returns:
            Dict of category -> component names
        """
        if category:
            if category in self.categories:
                return {category: self.categories[category]}
            return {}
        return self.categories

    def get_categories(self) -> List[str]:
        """
        Get list of available component categories.

        Returns:
            List of category names
        """
        return list(self.categories.keys())

    def validate_prop(
        self,
        component: str,
        prop_name: str,
        prop_value: Any
    ) -> Dict[str, Any]:
        """
        Validate a single prop value against the registry.

        Args:
            component: Component name
            prop_name: Prop name
            prop_value: Value to validate

        Returns:
            Dict with valid: bool, error: Optional[str]
        """
        props = self.get_component_props(component)
        if props is None:
            return {
                'valid': False,
                'error': f"Unknown component: {component}"
            }

        if prop_name not in props:
            # Check for similar prop names (typo detection)
            similar = self._find_similar_props(prop_name, props.keys())
            if similar:
                return {
                    'valid': False,
                    'error': f"Unknown prop '{prop_name}' for {component}. Did you mean '{similar}'?"
                }
            return {
                'valid': False,
                'error': f"Unknown prop '{prop_name}' for {component}"
            }

        prop_schema = props[prop_name]
        return self._validate_value(prop_value, prop_schema, prop_name)

    def _validate_value(
        self,
        value: Any,
        schema: Dict[str, Any],
        prop_name: str
    ) -> Dict[str, Any]:
        """
        Validate a value against a prop schema.

        Args:
            value: Value to validate
            schema: Prop schema from registry
            prop_name: Prop name (for error messages)

        Returns:
            Dict with valid: bool, error: Optional[str]
        """
        prop_type = schema.get('type', 'any')

        # Any type always valid
        if prop_type == 'any':
            return {'valid': True}

        # Check enum values
        if 'enum' in schema:
            if value not in schema['enum']:
                return {
                    'valid': False,
                    'error': f"Prop '{prop_name}' expects one of {schema['enum']}, got '{value}'"
                }
            return {'valid': True}

        # Type checking
        type_checks = {
            'string': lambda v: isinstance(v, str),
            'number': lambda v: isinstance(v, (int, float)),
            'integer': lambda v: isinstance(v, int),
            'boolean': lambda v: isinstance(v, bool),
            'array': lambda v: isinstance(v, list),
            'object': lambda v: isinstance(v, dict),
        }

        checker = type_checks.get(prop_type)
        if checker and not checker(value):
            return {
                'valid': False,
                'error': f"Prop '{prop_name}' expects type '{prop_type}', got '{type(value).__name__}'"
            }

        return {'valid': True}

    def _find_similar_props(
        self,
        prop_name: str,
        available_props: List[str]
    ) -> Optional[str]:
        """
        Find a similar prop name for typo suggestions.

        Uses simple edit distance heuristic.

        Args:
            prop_name: The (possibly misspelled) prop name
            available_props: List of valid prop names

        Returns:
            Most similar prop name, or None if no close match
        """
        prop_lower = prop_name.lower()

        for prop in available_props:
            # Exact match after lowercase
            if prop.lower() == prop_lower:
                return prop
            # Common typos: extra/missing letter
            if abs(len(prop) - len(prop_name)) == 1:
                if prop_lower.startswith(prop.lower()[:3]):
                    return prop

        return None

    def is_loaded(self) -> bool:
        """Check if registry is loaded."""
        return len(self.components) > 0


def load_registry(dmc_version: Optional[str] = None) -> ComponentRegistry:
    """
    Convenience function to load and return a component registry.

    Args:
        dmc_version: Optional DMC version string

    Returns:
        Loaded ComponentRegistry instance
    """
    registry = ComponentRegistry(dmc_version)
    registry.load()
    return registry
