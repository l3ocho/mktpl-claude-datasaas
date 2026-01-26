"""
Multi-page app tools for viz-platform.

Provides tools for building complete Dash applications with routing and navigation.
"""
import logging
from typing import Dict, List, Optional, Any
from uuid import uuid4

logger = logging.getLogger(__name__)


# Navigation position options
NAV_POSITIONS = ["top", "left", "right"]

# Auth types supported
AUTH_TYPES = ["none", "basic", "oauth", "custom"]


class PageTools:
    """
    Multi-page Dash application tools.

    Creates page definitions, navigation, and auth configuration.
    """

    def __init__(self):
        """Initialize page tools."""
        self._pages: Dict[str, Dict[str, Any]] = {}
        self._navbars: Dict[str, Dict[str, Any]] = {}
        self._app_config: Dict[str, Any] = {
            "title": "Dash App",
            "suppress_callback_exceptions": True
        }

    async def page_create(
        self,
        name: str,
        path: str,
        layout_ref: Optional[str] = None,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new page definition.

        Args:
            name: Unique page name (used as identifier)
            path: URL path for the page (e.g., "/", "/settings")
            layout_ref: Optional layout reference to use for the page
            title: Optional page title (defaults to name)

        Returns:
            Dict with:
                - page_ref: Reference to use in other tools
                - path: URL path
                - registered: Whether page was registered
        """
        # Validate path format
        if not path.startswith('/'):
            return {
                "error": f"Path must start with '/'. Got: {path}",
                "page_ref": None
            }

        # Check for name collision
        if name in self._pages:
            return {
                "error": f"Page '{name}' already exists. Use a different name.",
                "page_ref": name
            }

        # Check for path collision
        for page_name, page_data in self._pages.items():
            if page_data['path'] == path:
                return {
                    "error": f"Path '{path}' already used by page '{page_name}'.",
                    "page_ref": None
                }

        # Create page definition
        page = {
            "id": str(uuid4()),
            "name": name,
            "path": path,
            "title": title or name,
            "layout_ref": layout_ref,
            "auth": None,
            "metadata": {}
        }

        self._pages[name] = page

        return {
            "page_ref": name,
            "path": path,
            "title": page["title"],
            "layout_ref": layout_ref,
            "registered": True
        }

    async def page_add_navbar(
        self,
        pages: List[str],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a navigation component linking pages.

        Args:
            pages: List of page names to include in navigation
            options: Navigation options:
                - position: "top", "left", or "right"
                - style: Style variant
                - brand: Brand/logo text or config
                - collapsible: Whether to collapse on mobile

        Returns:
            Dict with:
                - navbar_id: Navigation ID
                - pages: List of page links generated
                - component: DMC component structure
        """
        options = options or {}

        # Validate pages exist
        missing_pages = [p for p in pages if p not in self._pages]
        if missing_pages:
            return {
                "error": f"Pages not found: {missing_pages}. Create them first.",
                "navbar_id": None
            }

        # Validate position
        position = options.get("position", "top")
        if position not in NAV_POSITIONS:
            return {
                "error": f"Invalid position '{position}'. Must be one of: {NAV_POSITIONS}",
                "navbar_id": None
            }

        # Generate navbar ID
        navbar_id = f"navbar_{len(self._navbars)}"

        # Build page links
        page_links = []
        for page_name in pages:
            page = self._pages[page_name]
            page_links.append({
                "label": page["title"],
                "href": page["path"],
                "page_ref": page_name
            })

        # Build DMC component structure
        if position == "top":
            component = self._build_top_navbar(page_links, options)
        else:
            component = self._build_side_navbar(page_links, options, position)

        # Store navbar config
        self._navbars[navbar_id] = {
            "id": navbar_id,
            "position": position,
            "pages": pages,
            "options": options,
            "component": component
        }

        return {
            "navbar_id": navbar_id,
            "position": position,
            "pages": page_links,
            "component": component
        }

    async def page_set_auth(
        self,
        page_ref: str,
        auth_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Configure authentication for a page.

        Args:
            page_ref: Page name to configure
            auth_config: Authentication configuration:
                - type: "none", "basic", "oauth", "custom"
                - required: Whether auth is required (default True)
                - roles: List of required roles (optional)
                - redirect: Redirect path for unauthenticated users

        Returns:
            Dict with:
                - page_ref: Page reference
                - auth_type: Type of auth configured
                - protected: Whether page is protected
        """
        # Validate page exists
        if page_ref not in self._pages:
            available = list(self._pages.keys())
            return {
                "error": f"Page '{page_ref}' not found. Available: {available}",
                "page_ref": page_ref
            }

        # Validate auth type
        auth_type = auth_config.get("type", "basic")
        if auth_type not in AUTH_TYPES:
            return {
                "error": f"Invalid auth type '{auth_type}'. Must be one of: {AUTH_TYPES}",
                "page_ref": page_ref
            }

        # Build auth config
        auth = {
            "type": auth_type,
            "required": auth_config.get("required", True),
            "roles": auth_config.get("roles", []),
            "redirect": auth_config.get("redirect", "/login")
        }

        # Handle OAuth-specific config
        if auth_type == "oauth":
            auth["provider"] = auth_config.get("provider", "generic")
            auth["scopes"] = auth_config.get("scopes", [])

        # Update page
        self._pages[page_ref]["auth"] = auth

        return {
            "page_ref": page_ref,
            "auth_type": auth_type,
            "protected": auth["required"],
            "roles": auth["roles"],
            "redirect": auth["redirect"]
        }

    async def page_list(self) -> Dict[str, Any]:
        """
        List all registered pages.

        Returns:
            Dict with pages and their configurations
        """
        pages_info = {}
        for name, page in self._pages.items():
            pages_info[name] = {
                "path": page["path"],
                "title": page["title"],
                "layout_ref": page["layout_ref"],
                "protected": page["auth"] is not None and page["auth"].get("required", False)
            }

        return {
            "pages": pages_info,
            "count": len(pages_info),
            "navbars": list(self._navbars.keys())
        }

    async def page_get_app_config(self) -> Dict[str, Any]:
        """
        Get the complete app configuration for Dash.

        Returns:
            Dict with app config including pages, navbars, and settings
        """
        # Build pages config
        pages_config = []
        for name, page in self._pages.items():
            pages_config.append({
                "name": name,
                "path": page["path"],
                "title": page["title"],
                "layout_ref": page["layout_ref"]
            })

        # Build routing config
        routes = {page["path"]: name for name, page in self._pages.items()}

        return {
            "app": self._app_config,
            "pages": pages_config,
            "routes": routes,
            "navbars": list(self._navbars.values()),
            "page_count": len(self._pages)
        }

    def _build_top_navbar(
        self,
        page_links: List[Dict[str, str]],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build a top navigation bar component."""
        brand = options.get("brand", "App")

        # Build nav links
        nav_items = []
        for link in page_links:
            nav_items.append({
                "component": "NavLink",
                "props": {
                    "label": link["label"],
                    "href": link["href"]
                }
            })

        return {
            "component": "AppShell.Header",
            "children": [
                {
                    "component": "Group",
                    "props": {"justify": "space-between", "h": "100%", "px": "md"},
                    "children": [
                        {
                            "component": "Text",
                            "props": {"size": "lg", "fw": 700},
                            "children": brand
                        },
                        {
                            "component": "Group",
                            "props": {"gap": "sm"},
                            "children": nav_items
                        }
                    ]
                }
            ]
        }

    def _build_side_navbar(
        self,
        page_links: List[Dict[str, str]],
        options: Dict[str, Any],
        position: str
    ) -> Dict[str, Any]:
        """Build a side navigation bar component."""
        brand = options.get("brand", "App")

        # Build nav links
        nav_items = []
        for link in page_links:
            nav_items.append({
                "component": "NavLink",
                "props": {
                    "label": link["label"],
                    "href": link["href"]
                }
            })

        navbar_component = "AppShell.Navbar" if position == "left" else "AppShell.Aside"

        return {
            "component": navbar_component,
            "props": {"p": "md"},
            "children": [
                {
                    "component": "Text",
                    "props": {"size": "lg", "fw": 700, "mb": "md"},
                    "children": brand
                },
                {
                    "component": "Stack",
                    "props": {"gap": "xs"},
                    "children": nav_items
                }
            ]
        }
