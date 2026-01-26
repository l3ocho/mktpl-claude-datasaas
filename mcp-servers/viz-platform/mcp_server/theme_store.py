"""
Theme storage and persistence for viz-platform.

Handles saving/loading themes from user and project locations.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


# Default theme based on Mantine defaults
DEFAULT_THEME = {
    "name": "default",
    "version": "1.0.0",
    "tokens": {
        "colors": {
            "primary": "#228be6",
            "secondary": "#868e96",
            "success": "#40c057",
            "warning": "#fab005",
            "error": "#fa5252",
            "info": "#15aabf",
            "background": {
                "base": "#ffffff",
                "subtle": "#f8f9fa",
                "dark": "#212529"
            },
            "text": {
                "primary": "#212529",
                "secondary": "#495057",
                "muted": "#868e96",
                "inverse": "#ffffff"
            },
            "border": "#dee2e6"
        },
        "spacing": {
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px"
        },
        "typography": {
            "fontFamily": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
            "fontFamilyMono": "ui-monospace, SFMono-Regular, Menlo, Monaco, monospace",
            "fontSize": {
                "xs": "12px",
                "sm": "14px",
                "md": "16px",
                "lg": "18px",
                "xl": "20px"
            },
            "fontWeight": {
                "normal": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700
            },
            "lineHeight": {
                "tight": 1.25,
                "normal": 1.5,
                "relaxed": 1.75
            }
        },
        "radii": {
            "none": "0px",
            "sm": "4px",
            "md": "8px",
            "lg": "16px",
            "xl": "24px",
            "full": "9999px"
        },
        "shadows": {
            "none": "none",
            "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
            "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
            "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)",
            "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1)"
        },
        "transitions": {
            "fast": "150ms",
            "normal": "300ms",
            "slow": "500ms"
        }
    }
}


# Required token categories for validation
REQUIRED_TOKEN_CATEGORIES = ["colors", "spacing", "typography", "radii"]


class ThemeStore:
    """
    Store and manage design themes.

    Handles persistence to user-level and project-level locations.
    """

    def __init__(self, project_dir: Optional[Path] = None):
        """
        Initialize theme store.

        Args:
            project_dir: Project directory for project-level themes
        """
        self.project_dir = project_dir
        self._themes: Dict[str, Dict[str, Any]] = {}
        self._active_theme: Optional[str] = None

        # Load default theme
        self._themes["default"] = DEFAULT_THEME.copy()

    @property
    def user_themes_dir(self) -> Path:
        """User-level themes directory."""
        return Path.home() / ".config" / "claude" / "themes"

    @property
    def project_themes_dir(self) -> Optional[Path]:
        """Project-level themes directory."""
        if self.project_dir:
            return self.project_dir / ".viz-platform" / "themes"
        return None

    def load_themes(self) -> int:
        """
        Load themes from user and project directories.

        Project themes take precedence over user themes.

        Returns:
            Number of themes loaded
        """
        count = 0

        # Load user themes
        if self.user_themes_dir.exists():
            for theme_file in self.user_themes_dir.glob("*.json"):
                try:
                    with open(theme_file, 'r') as f:
                        theme = json.load(f)
                    name = theme.get('name', theme_file.stem)
                    self._themes[name] = theme
                    count += 1
                    logger.debug(f"Loaded user theme: {name}")
                except Exception as e:
                    logger.warning(f"Failed to load theme {theme_file}: {e}")

        # Load project themes (override user themes)
        if self.project_themes_dir and self.project_themes_dir.exists():
            for theme_file in self.project_themes_dir.glob("*.json"):
                try:
                    with open(theme_file, 'r') as f:
                        theme = json.load(f)
                    name = theme.get('name', theme_file.stem)
                    self._themes[name] = theme
                    count += 1
                    logger.debug(f"Loaded project theme: {name}")
                except Exception as e:
                    logger.warning(f"Failed to load theme {theme_file}: {e}")

        return count

    def save_theme(
        self,
        theme: Dict[str, Any],
        location: str = "project"
    ) -> Path:
        """
        Save a theme to disk.

        Args:
            theme: Theme dict to save
            location: "user" or "project"

        Returns:
            Path where theme was saved
        """
        name = theme.get('name', 'unnamed')

        if location == "user":
            target_dir = self.user_themes_dir
        else:
            target_dir = self.project_themes_dir
            if not target_dir:
                target_dir = self.user_themes_dir

        target_dir.mkdir(parents=True, exist_ok=True)
        theme_path = target_dir / f"{name}.json"

        with open(theme_path, 'w') as f:
            json.dump(theme, f, indent=2)

        # Update in-memory store
        self._themes[name] = theme

        return theme_path

    def get_theme(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a theme by name."""
        return self._themes.get(name)

    def list_themes(self) -> List[str]:
        """List all available theme names."""
        return list(self._themes.keys())

    def set_active_theme(self, name: str) -> bool:
        """
        Set the active theme.

        Args:
            name: Theme name to activate

        Returns:
            True if theme was activated
        """
        if name in self._themes:
            self._active_theme = name
            return True
        return False

    def get_active_theme(self) -> Optional[Dict[str, Any]]:
        """Get the currently active theme."""
        if self._active_theme:
            return self._themes.get(self._active_theme)
        return None

    def delete_theme(self, name: str) -> bool:
        """
        Delete a theme.

        Args:
            name: Theme name to delete

        Returns:
            True if theme was deleted
        """
        if name == "default":
            return False  # Cannot delete default theme

        if name in self._themes:
            del self._themes[name]

            # Remove file if exists
            for themes_dir in [self.user_themes_dir, self.project_themes_dir]:
                if themes_dir and themes_dir.exists():
                    theme_path = themes_dir / f"{name}.json"
                    if theme_path.exists():
                        theme_path.unlink()

            if self._active_theme == name:
                self._active_theme = None

            return True
        return False
