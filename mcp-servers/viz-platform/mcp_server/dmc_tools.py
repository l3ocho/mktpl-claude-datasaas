"""
DMC (Dash Mantine Components) validation tools.

Provides component constraint layer to prevent Claude from hallucinating invalid props.
"""
import logging
from typing import Dict, List, Optional, Any

from .component_registry import ComponentRegistry

logger = logging.getLogger(__name__)


class DMCTools:
    """
    DMC component validation tools.

    These tools provide the "constraint layer" that validates component usage
    against a version-locked registry of DMC components.
    """

    def __init__(self, registry: Optional[ComponentRegistry] = None):
        """
        Initialize DMC tools with component registry.

        Args:
            registry: ComponentRegistry instance. If None, creates one.
        """
        self.registry = registry
        self._initialized = False

    def initialize(self, dmc_version: Optional[str] = None) -> bool:
        """
        Initialize the registry if not already provided.

        Args:
            dmc_version: DMC version to load registry for

        Returns:
            True if initialized successfully
        """
        if self.registry is None:
            self.registry = ComponentRegistry(dmc_version)

        if not self.registry.is_loaded():
            self.registry.load()

        self._initialized = self.registry.is_loaded()
        return self._initialized

    async def list_components(
        self,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List available DMC components, optionally filtered by category.

        Args:
            category: Optional category filter (e.g., "inputs", "buttons", "navigation")

        Returns:
            Dict with:
                - components: Dict[category -> [component names]]
                - categories: List of available categories
                - version: Loaded DMC registry version
                - total_count: Total number of components
        """
        if not self._initialized:
            return {
                "error": "Registry not initialized",
                "components": {},
                "categories": [],
                "version": None,
                "total_count": 0
            }

        components = self.registry.list_components(category)
        all_categories = self.registry.get_categories()

        # Count total components
        total = sum(len(comps) for comps in components.values())

        return {
            "components": components,
            "categories": all_categories if not category else [category],
            "version": self.registry.loaded_version,
            "total_count": total
        }

    async def get_component_props(self, component: str) -> Dict[str, Any]:
        """
        Get props schema for a specific component.

        Args:
            component: Component name (e.g., "Button", "TextInput")

        Returns:
            Dict with:
                - component: Component name
                - description: Component description
                - props: Dict of prop name -> {type, default, enum, description}
                - prop_count: Number of props
                - required: List of required prop names
            Or error dict if component not found
        """
        if not self._initialized:
            return {
                "error": "Registry not initialized",
                "component": component,
                "props": {},
                "prop_count": 0
            }

        comp_def = self.registry.get_component(component)
        if not comp_def:
            # Try to suggest similar component name
            similar = self._find_similar_component(component)
            error_msg = f"Component '{component}' not found in registry"
            if similar:
                error_msg += f". Did you mean '{similar}'?"

            return {
                "error": error_msg,
                "component": component,
                "props": {},
                "prop_count": 0
            }

        props = comp_def.get('props', {})

        # Extract required props
        required = [
            name for name, schema in props.items()
            if schema.get('required', False)
        ]

        return {
            "component": component,
            "description": comp_def.get('description', ''),
            "props": props,
            "prop_count": len(props),
            "required": required,
            "version": self.registry.loaded_version
        }

    async def validate_component(
        self,
        component: str,
        props: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate component props against registry.

        Args:
            component: Component name
            props: Props dict to validate

        Returns:
            Dict with:
                - valid: bool - True if all props are valid
                - errors: List of error messages
                - warnings: List of warning messages
                - validated_props: Number of props validated
                - component: Component name for reference
        """
        if not self._initialized:
            return {
                "valid": False,
                "errors": ["Registry not initialized"],
                "warnings": [],
                "validated_props": 0,
                "component": component
            }

        errors: List[str] = []
        warnings: List[str] = []

        # Check if component exists
        comp_def = self.registry.get_component(component)
        if not comp_def:
            similar = self._find_similar_component(component)
            error_msg = f"Unknown component: {component}"
            if similar:
                error_msg += f". Did you mean '{similar}'?"
            errors.append(error_msg)

            return {
                "valid": False,
                "errors": errors,
                "warnings": warnings,
                "validated_props": 0,
                "component": component
            }

        comp_props = comp_def.get('props', {})

        # Check for required props
        for prop_name, prop_schema in comp_props.items():
            if prop_schema.get('required', False) and prop_name not in props:
                errors.append(f"Missing required prop: '{prop_name}'")

        # Validate each provided prop
        for prop_name, prop_value in props.items():
            # Skip special props that are always allowed
            if prop_name in ('id', 'children', 'className', 'style', 'key'):
                continue

            result = self.registry.validate_prop(component, prop_name, prop_value)

            if not result.get('valid', True):
                error = result.get('error', f"Invalid prop: {prop_name}")
                # Distinguish between typos/unknown props and type errors
                if "Unknown prop" in error:
                    errors.append(f"❌ {error}")
                elif "expects one of" in error:
                    errors.append(f"❌ {error}")
                elif "expects type" in error:
                    warnings.append(f"⚠️ {error}")
                else:
                    errors.append(f"❌ {error}")

        # Check for props that exist but might have common mistakes
        self._check_common_mistakes(component, props, warnings)

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "validated_props": len(props),
            "component": component,
            "version": self.registry.loaded_version
        }

    def _find_similar_component(self, component: str) -> Optional[str]:
        """
        Find a similar component name for suggestions.

        Args:
            component: The (possibly misspelled) component name

        Returns:
            Similar component name, or None if no close match
        """
        if not self.registry:
            return None

        comp_lower = component.lower()
        all_components = []
        for comps in self.registry.categories.values():
            all_components.extend(comps)

        for comp in all_components:
            # Exact match after lowercase
            if comp.lower() == comp_lower:
                return comp
            # Check if it's a prefix match
            if comp.lower().startswith(comp_lower) or comp_lower.startswith(comp.lower()):
                return comp
            # Check for common typos
            if abs(len(comp) - len(component)) <= 2:
                if comp_lower[:4] == comp.lower()[:4]:
                    return comp

        return None

    def _check_common_mistakes(
        self,
        component: str,
        props: Dict[str, Any],
        warnings: List[str]
    ) -> None:
        """
        Check for common prop usage mistakes and add warnings.

        Args:
            component: Component name
            props: Props being used
            warnings: List to append warnings to
        """
        # Common mistake: using 'onclick' instead of callback pattern
        if 'onclick' in [p.lower() for p in props.keys()]:
            warnings.append(
                "⚠️ Dash uses callback patterns, not inline event handlers. "
                "Use 'n_clicks' prop with a callback instead."
            )

        # Common mistake: using 'class' instead of 'className'
        if 'class' in props:
            warnings.append(
                "⚠️ Use 'className' instead of 'class' for CSS classes."
            )

        # Button-specific checks
        if component == 'Button':
            if 'href' in props and 'component' not in props:
                warnings.append(
                    "⚠️ Button with 'href' should also set 'component=\"a\"' for proper anchor behavior."
                )

        # Input-specific checks
        if 'Input' in component:
            if 'value' in props and 'onChange' in [p for p in props.keys()]:
                warnings.append(
                    "⚠️ Dash uses 'value' prop with callbacks, not 'onChange'. "
                    "The value updates automatically through Dash callbacks."
                )
