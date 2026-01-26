"""
Theme management tools for viz-platform.

Provides design token-based theming system for consistent visual styling.
"""
import copy
import logging
from typing import Dict, List, Optional, Any

from .theme_store import ThemeStore, DEFAULT_THEME, REQUIRED_TOKEN_CATEGORIES

logger = logging.getLogger(__name__)


class ThemeTools:
    """
    Design token-based theming tools.

    Creates and manages themes that integrate with DMC and Plotly.
    """

    def __init__(self, store: Optional[ThemeStore] = None):
        """
        Initialize theme tools.

        Args:
            store: Optional ThemeStore for persistence
        """
        self.store = store or ThemeStore()

    async def theme_create(
        self,
        name: str,
        tokens: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new theme with design tokens.

        Args:
            name: Unique theme name
            tokens: Design tokens dict with colors, spacing, typography, radii

        Returns:
            Dict with:
                - name: Theme name
                - tokens: Full token set (merged with defaults)
                - validation: Validation results
        """
        # Check for name collision
        if self.store.get_theme(name) and name != "default":
            return {
                "error": f"Theme '{name}' already exists. Use theme_extend to modify it.",
                "name": name
            }

        # Start with default tokens and merge provided ones
        theme_tokens = copy.deepcopy(DEFAULT_THEME["tokens"])
        theme_tokens = self._deep_merge(theme_tokens, tokens)

        # Create theme object
        theme = {
            "name": name,
            "version": "1.0.0",
            "tokens": theme_tokens
        }

        # Validate the theme
        validation = self._validate_tokens(theme_tokens)

        # Save to store
        self.store._themes[name] = theme

        return {
            "name": name,
            "tokens": theme_tokens,
            "validation": validation,
            "complete": validation["complete"]
        }

    async def theme_extend(
        self,
        base_theme: str,
        overrides: Dict[str, Any],
        new_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new theme by extending an existing one.

        Args:
            base_theme: Name of theme to extend
            overrides: Token overrides to apply
            new_name: Optional name for the new theme (defaults to base_theme_extended)

        Returns:
            Dict with the new theme or error
        """
        # Get base theme
        base = self.store.get_theme(base_theme)
        if not base:
            available = self.store.list_themes()
            return {
                "error": f"Base theme '{base_theme}' not found. Available: {available}",
                "name": None
            }

        # Determine new name
        name = new_name or f"{base_theme}_extended"

        # Check for collision
        if self.store.get_theme(name) and name != base_theme:
            return {
                "error": f"Theme '{name}' already exists. Choose a different name.",
                "name": name
            }

        # Merge tokens
        theme_tokens = copy.deepcopy(base.get("tokens", {}))
        theme_tokens = self._deep_merge(theme_tokens, overrides)

        # Create theme
        theme = {
            "name": name,
            "version": "1.0.0",
            "extends": base_theme,
            "tokens": theme_tokens
        }

        # Validate
        validation = self._validate_tokens(theme_tokens)

        # Save to store
        self.store._themes[name] = theme

        return {
            "name": name,
            "extends": base_theme,
            "tokens": theme_tokens,
            "validation": validation,
            "complete": validation["complete"]
        }

    async def theme_validate(self, theme_name: str) -> Dict[str, Any]:
        """
        Validate a theme for completeness.

        Args:
            theme_name: Theme name to validate

        Returns:
            Dict with:
                - valid: bool
                - complete: bool (all optional tokens present)
                - missing: List of missing required tokens
                - warnings: List of warnings
        """
        theme = self.store.get_theme(theme_name)
        if not theme:
            available = self.store.list_themes()
            return {
                "error": f"Theme '{theme_name}' not found. Available: {available}",
                "valid": False
            }

        tokens = theme.get("tokens", {})
        validation = self._validate_tokens(tokens)

        return {
            "theme_name": theme_name,
            "valid": validation["valid"],
            "complete": validation["complete"],
            "missing_required": validation["missing_required"],
            "missing_optional": validation["missing_optional"],
            "warnings": validation["warnings"]
        }

    async def theme_export_css(self, theme_name: str) -> Dict[str, Any]:
        """
        Export a theme as CSS custom properties.

        Args:
            theme_name: Theme name to export

        Returns:
            Dict with:
                - css: CSS custom properties string
                - variables: List of variable names
        """
        theme = self.store.get_theme(theme_name)
        if not theme:
            available = self.store.list_themes()
            return {
                "error": f"Theme '{theme_name}' not found. Available: {available}",
                "css": None
            }

        tokens = theme.get("tokens", {})
        css_vars = []
        var_names = []

        # Convert tokens to CSS custom properties
        css_vars.append(f"/* Theme: {theme_name} */")
        css_vars.append(":root {")

        # Colors
        colors = tokens.get("colors", {})
        css_vars.append("  /* Colors */")
        for key, value in self._flatten_tokens(colors, "color").items():
            var_name = f"--{key}"
            css_vars.append(f"  {var_name}: {value};")
            var_names.append(var_name)

        # Spacing
        spacing = tokens.get("spacing", {})
        css_vars.append("\n  /* Spacing */")
        for key, value in spacing.items():
            var_name = f"--spacing-{key}"
            css_vars.append(f"  {var_name}: {value};")
            var_names.append(var_name)

        # Typography
        typography = tokens.get("typography", {})
        css_vars.append("\n  /* Typography */")
        for key, value in self._flatten_tokens(typography, "font").items():
            var_name = f"--{key}"
            css_vars.append(f"  {var_name}: {value};")
            var_names.append(var_name)

        # Radii
        radii = tokens.get("radii", {})
        css_vars.append("\n  /* Border Radius */")
        for key, value in radii.items():
            var_name = f"--radius-{key}"
            css_vars.append(f"  {var_name}: {value};")
            var_names.append(var_name)

        # Shadows
        shadows = tokens.get("shadows", {})
        if shadows:
            css_vars.append("\n  /* Shadows */")
            for key, value in shadows.items():
                var_name = f"--shadow-{key}"
                css_vars.append(f"  {var_name}: {value};")
                var_names.append(var_name)

        # Transitions
        transitions = tokens.get("transitions", {})
        if transitions:
            css_vars.append("\n  /* Transitions */")
            for key, value in transitions.items():
                var_name = f"--transition-{key}"
                css_vars.append(f"  {var_name}: {value};")
                var_names.append(var_name)

        css_vars.append("}")

        css_content = "\n".join(css_vars)

        return {
            "theme_name": theme_name,
            "css": css_content,
            "variable_count": len(var_names),
            "variables": var_names
        }

    async def theme_list(self) -> Dict[str, Any]:
        """
        List all available themes.

        Returns:
            Dict with theme names and active theme
        """
        themes = self.store.list_themes()
        active = self.store._active_theme

        theme_info = {}
        for name in themes:
            theme = self.store.get_theme(name)
            theme_info[name] = {
                "extends": theme.get("extends"),
                "version": theme.get("version", "1.0.0")
            }

        return {
            "themes": theme_info,
            "active_theme": active,
            "count": len(themes)
        }

    async def theme_activate(self, theme_name: str) -> Dict[str, Any]:
        """
        Set the active theme.

        Args:
            theme_name: Theme to activate

        Returns:
            Dict with activation status
        """
        if self.store.set_active_theme(theme_name):
            return {
                "active_theme": theme_name,
                "success": True
            }
        return {
            "error": f"Theme '{theme_name}' not found.",
            "success": False
        }

    def _validate_tokens(self, tokens: Dict[str, Any]) -> Dict[str, Any]:
        """Validate token structure and completeness."""
        missing_required = []
        missing_optional = []
        warnings = []

        # Check required categories
        for category in REQUIRED_TOKEN_CATEGORIES:
            if category not in tokens:
                missing_required.append(category)

        # Check colors structure
        colors = tokens.get("colors", {})
        required_colors = ["primary", "background", "text"]
        for color in required_colors:
            if color not in colors:
                missing_required.append(f"colors.{color}")

        # Check spacing
        spacing = tokens.get("spacing", {})
        required_spacing = ["xs", "sm", "md", "lg"]
        for size in required_spacing:
            if size not in spacing:
                missing_optional.append(f"spacing.{size}")

        # Check typography
        typography = tokens.get("typography", {})
        if "fontFamily" not in typography:
            missing_optional.append("typography.fontFamily")
        if "fontSize" not in typography:
            missing_optional.append("typography.fontSize")

        # Check radii
        radii = tokens.get("radii", {})
        if "sm" not in radii and "md" not in radii:
            missing_optional.append("radii.sm or radii.md")

        # Warnings for common issues
        if "shadows" not in tokens:
            warnings.append("No shadows defined - components may have no elevation")
        if "transitions" not in tokens:
            warnings.append("No transitions defined - animations will use defaults")

        return {
            "valid": len(missing_required) == 0,
            "complete": len(missing_required) == 0 and len(missing_optional) == 0,
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "warnings": warnings
        }

    def _deep_merge(
        self,
        base: Dict[str, Any],
        override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = copy.deepcopy(base)

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def _flatten_tokens(
        self,
        tokens: Dict[str, Any],
        prefix: str
    ) -> Dict[str, str]:
        """Flatten nested token dict for CSS export."""
        result = {}

        for key, value in tokens.items():
            if isinstance(value, dict):
                nested = self._flatten_tokens(value, f"{prefix}-{key}")
                result.update(nested)
            else:
                result[f"{prefix}-{key}"] = str(value)

        return result
