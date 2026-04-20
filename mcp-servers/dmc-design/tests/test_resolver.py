"""Unit tests for design contract resolver."""
import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from resolver import DesignContract, load_contract


SAMPLE_CONTRACT = {
    "schemes": {
        "light": {
            "surfaces": {
                "base": {"bg": "white", "border": None, "variant": None},
                "raised": {"bg": "white", "border": "gray.2", "variant": "outline"},
                "overlay": {"bg": "gray.0", "border": None, "variant": None},
                "nested_in_overlay": {"bg": "white", "border": None, "variant": None},
            }
        },
        "dark": {
            "surfaces": {
                "base": {"bg": "dark.8", "border": None, "variant": None},
                "raised": {"bg": "dark.7", "border": "dark.5", "variant": "outline"},
                "overlay": {"bg": "dark.6", "border": None, "variant": None},
                "nested_in_overlay": {"bg": "dark.7", "border": None, "variant": None},
            }
        },
    },
    "component_locks": {
        "Modal": {
            "locked_at": "2026-04-18T14:30:00Z",
            "reference_file": "app/pages/example.py",
            "reference_line": 42,
            "spec": {"padding": "md", "radius": "md", "withCloseButton": True},
        }
    },
    "interaction": {
        "hover_delta": -1,
        "focus_ring": {"size": 2, "color_token": "primary.5"},
        "disabled_opacity": 0.55,
        "error_token": "red.6",
    },
    "density": "compact",
    "meta": {
        "version": "1.0.0",
        "created_at": "2026-04-18T14:00:00Z",
        "updated_at": "2026-04-18T14:30:00Z",
    },
}


@pytest.fixture
def contract_file(tmp_path):
    """Write sample contract to temp dir."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    contract_path = claude_dir / "design-contract.json"
    contract_path.write_text(json.dumps(SAMPLE_CONTRACT))
    return tmp_path


@pytest.fixture
def contract(contract_file):
    return load_contract(contract_file)


@pytest.fixture
def empty_contract(tmp_path):
    return load_contract(tmp_path)  # No contract file exists


def test_no_contract_returns_requested_props_unchanged(empty_contract):
    props = {"bg": "blue", "p": "lg"}
    result = empty_contract.resolve_component("Card", requested_props=props)
    assert result == props


def test_surface_bg_overrides_requested_bg(contract):
    props = {"bg": "blue", "p": "lg"}
    result = contract.resolve_component("Card", scheme="light", requested_props=props)
    assert result["bg"] == "white"  # raised surface bg wins
    assert result["p"] == "lg"  # uncontracted prop preserved


def test_component_lock_overrides_surface(contract):
    result = contract.resolve_component("Modal", scheme="light", requested_props={})
    assert result["padding"] == "md"
    assert result["radius"] == "md"
    assert result["withCloseButton"] is True
    assert result["bg"] == "gray.0"  # overlay surface bg also applied


def test_modal_inside_appshell_resolves_to_overlay(contract):
    level = contract.infer_surface_level("Modal")
    assert level == "overlay"


def test_card_inside_modal_resolves_to_nested_in_overlay(contract):
    level = contract.infer_surface_level("Card", parent_context="overlay")
    assert level == "nested_in_overlay"


def test_dark_scheme_surfaces_independent_of_light(contract):
    light_result = contract.resolve_component("Card", scheme="light", requested_props={})
    dark_result = contract.resolve_component("Card", scheme="dark", requested_props={})
    assert light_result["bg"] == "white"
    assert dark_result["bg"] == "dark.7"


def test_unknown_component_defaults_to_base(contract):
    level = contract.infer_surface_level("UnknownWidget")
    assert level == "base"


def test_raised_surface_adds_border_props(contract):
    result = contract.resolve_component("Card", scheme="light", requested_props={})
    assert result.get("withBorder") is True
    assert result.get("borderColor") == "gray.2"


def test_is_active_false_when_no_contract(empty_contract):
    assert empty_contract.is_active() is False


def test_is_active_true_when_contract_loaded(contract):
    assert contract.is_active() is True


def test_explicit_surface_context_overrides_inference(contract):
    # Force Card to resolve as overlay instead of its default (raised)
    result = contract.resolve_component(
        "Card", scheme="light", surface_context="overlay", requested_props={}
    )
    assert result["bg"] == "gray.0"
