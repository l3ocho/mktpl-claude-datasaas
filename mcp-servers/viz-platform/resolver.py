"""Design contract resolver — enforces surface hierarchy and component locks."""

from pathlib import Path
import json
from typing import Optional, Literal

SurfaceLevel = Literal["base", "raised", "overlay", "nested_in_overlay"]

# Context inference defaults per RFC-09
COMPONENT_SURFACE_DEFAULTS: dict[str, str] = {
    "AppShellMain": "base",
    "Container": "base",
    "Stack": "base",
    "Group": "base",
    "Card": "raised",
    "Paper": "raised",
    "Modal": "overlay",
    "Drawer": "overlay",
    "Popover": "overlay",
}


class DesignContract:
    def __init__(self, contract_path: Path):
        self.path = contract_path
        self.data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text())

    def is_active(self) -> bool:
        return bool(self.data)

    def resolve_surface(self, scheme: str, level: str) -> dict:
        surfaces = self.data.get("schemes", {}).get(scheme, {}).get("surfaces", {})
        return surfaces.get(level, {})

    def infer_surface_level(
        self,
        component_name: str,
        parent_context: Optional[str] = None,
    ) -> str:
        if parent_context == "overlay":
            return "nested_in_overlay"
        return COMPONENT_SURFACE_DEFAULTS.get(component_name, "base")

    def get_lock(self, component_name: str) -> Optional[dict]:
        return self.data.get("component_locks", {}).get(component_name)

    def resolve_component(
        self,
        component_name: str,
        scheme: str = "light",
        surface_context: Optional[str] = None,
        requested_props: Optional[dict] = None,
    ) -> dict:
        """Merge contract-enforced props with requested props. Contract wins."""
        requested = requested_props or {}
        if not self.is_active():
            return requested

        level = surface_context or self.infer_surface_level(component_name)
        surface = self.resolve_surface(scheme, level)
        lock = self.get_lock(component_name)

        resolved = dict(requested)

        # Surface enforcement
        if surface.get("bg"):
            resolved["bg"] = surface["bg"]
        if surface.get("border"):
            resolved["withBorder"] = True
            resolved["borderColor"] = surface["border"]
        if surface.get("variant"):
            resolved["variant"] = surface["variant"]

        # Lock enforcement (overrides surface where specified)
        if lock and "spec" in lock:
            resolved.update(lock["spec"])

        return resolved

    def lock_component(
        self,
        component_name: str,
        spec: dict,
        reference_file: str,
        reference_line: int,
    ) -> None:
        """Write a component lock entry to the contract file."""
        from datetime import datetime, timezone

        if not self.data:
            raise ValueError("Cannot lock component: no active contract. Run /viz setup first.")

        if "component_locks" not in self.data:
            self.data["component_locks"] = {}

        self.data["component_locks"][component_name] = {
            "locked_at": datetime.now(timezone.utc).isoformat(),
            "reference_file": reference_file,
            "reference_line": reference_line,
            "spec": spec,
        }

        # Update meta timestamp
        self.data.setdefault("meta", {})["updated_at"] = datetime.now(timezone.utc).isoformat()

        self.path.write_text(json.dumps(self.data, indent=2))


def load_contract(project_root: Path) -> DesignContract:
    """Load design contract from consumer project root."""
    return DesignContract(project_root / ".claude" / "design-contract.json")
