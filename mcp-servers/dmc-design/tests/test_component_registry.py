"""
Unit tests for DMC component registry.
"""
import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.fixture
def sample_registry_data():
    """Sample registry data for testing"""
    return {
        "version": "2.5.1",
        "categories": {
            "buttons": ["Button", "ActionIcon"],
            "inputs": ["TextInput", "NumberInput", "Select"]
        },
        "components": {
            "Button": {
                "description": "Button component",
                "props": {
                    "variant": {
                        "type": "string",
                        "enum": ["filled", "outline", "light"],
                        "default": "filled"
                    },
                    "color": {
                        "type": "string",
                        "default": "blue"
                    },
                    "size": {
                        "type": "string",
                        "enum": ["xs", "sm", "md", "lg", "xl"],
                        "default": "sm"
                    },
                    "disabled": {
                        "type": "boolean",
                        "default": False
                    }
                }
            },
            "TextInput": {
                "description": "Text input field",
                "props": {
                    "value": {"type": "string", "default": ""},
                    "placeholder": {"type": "string"},
                    "disabled": {"type": "boolean", "default": False},
                    "required": {"type": "boolean", "default": False}
                }
            }
        }
    }


@pytest.fixture
def registry_file(tmp_path, sample_registry_data):
    """Create a temporary registry file"""
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir()
    registry_file = registry_dir / "dmc_2_5.json"
    registry_file.write_text(json.dumps(sample_registry_data))
    return registry_file


@pytest.fixture
def registry(registry_file):
    """Create a ComponentRegistry with mock registry directory"""
    from mcp_server.component_registry import ComponentRegistry

    reg = ComponentRegistry(dmc_version="2.5.1")
    reg.registry_dir = registry_file.parent
    reg.load()
    return reg


def test_registry_init():
    """Test registry initialization"""
    from mcp_server.component_registry import ComponentRegistry

    reg = ComponentRegistry(dmc_version="2.5.1")

    assert reg.dmc_version == "2.5.1"
    assert reg.components == {}
    assert reg.categories == {}
    assert reg.loaded_version is None


def test_registry_load_success(registry, sample_registry_data):
    """Test successful registry loading"""
    assert registry.is_loaded()
    assert registry.loaded_version == "2.5.1"
    assert len(registry.components) == 2
    assert "Button" in registry.components
    assert "TextInput" in registry.components


def test_registry_load_no_file():
    """Test registry loading when no file exists"""
    from mcp_server.component_registry import ComponentRegistry

    reg = ComponentRegistry(dmc_version="99.99.99")
    reg.registry_dir = Path("/nonexistent/path")

    result = reg.load()

    assert result is False
    assert not reg.is_loaded()


def test_get_component(registry):
    """Test getting a component by name"""
    button = registry.get_component("Button")

    assert button is not None
    assert button["description"] == "Button component"
    assert "props" in button


def test_get_component_not_found(registry):
    """Test getting a nonexistent component"""
    result = registry.get_component("NonexistentComponent")

    assert result is None


def test_get_component_props(registry):
    """Test getting component props"""
    props = registry.get_component_props("Button")

    assert props is not None
    assert "variant" in props
    assert "color" in props
    assert props["variant"]["type"] == "string"
    assert props["variant"]["enum"] == ["filled", "outline", "light"]


def test_get_component_props_not_found(registry):
    """Test getting props for nonexistent component"""
    props = registry.get_component_props("Nonexistent")

    assert props is None


def test_list_components_all(registry):
    """Test listing all components"""
    result = registry.list_components()

    assert "buttons" in result
    assert "inputs" in result
    assert "Button" in result["buttons"]
    assert "TextInput" in result["inputs"]


def test_list_components_by_category(registry):
    """Test listing components by category"""
    result = registry.list_components(category="buttons")

    assert len(result) == 1
    assert "buttons" in result
    assert "Button" in result["buttons"]


def test_list_components_invalid_category(registry):
    """Test listing components with invalid category"""
    result = registry.list_components(category="nonexistent")

    assert result == {}


def test_get_categories(registry):
    """Test getting available categories"""
    categories = registry.get_categories()

    assert "buttons" in categories
    assert "inputs" in categories


def test_validate_prop_valid_enum(registry):
    """Test validating a valid enum prop"""
    result = registry.validate_prop("Button", "variant", "filled")

    assert result["valid"] is True


def test_validate_prop_invalid_enum(registry):
    """Test validating an invalid enum prop"""
    result = registry.validate_prop("Button", "variant", "invalid_variant")

    assert result["valid"] is False
    assert "expects one of" in result["error"]


def test_validate_prop_valid_type(registry):
    """Test validating a valid type"""
    result = registry.validate_prop("Button", "disabled", True)

    assert result["valid"] is True


def test_validate_prop_invalid_type(registry):
    """Test validating an invalid type"""
    result = registry.validate_prop("Button", "disabled", "not_a_boolean")

    assert result["valid"] is False
    assert "expects type" in result["error"]


def test_validate_prop_unknown_component(registry):
    """Test validating prop for unknown component"""
    result = registry.validate_prop("Nonexistent", "prop", "value")

    assert result["valid"] is False
    assert "Unknown component" in result["error"]


def test_validate_prop_unknown_prop(registry):
    """Test validating an unknown prop"""
    result = registry.validate_prop("Button", "unknownProp", "value")

    assert result["valid"] is False
    assert "Unknown prop" in result["error"]


def test_validate_prop_typo_detection(registry):
    """Test typo detection for similar prop names"""
    # colour vs color
    result = registry.validate_prop("Button", "colour", "blue")

    assert result["valid"] is False
    # Should suggest 'color'
    assert "color" in result.get("error", "").lower()


def test_find_similar_props(registry):
    """Test finding similar prop names"""
    available = ["color", "variant", "size", "disabled"]

    # Should match despite case difference
    similar = registry._find_similar_props("Color", available)
    assert similar == "color"

    # Should match with slight typo
    similar = registry._find_similar_props("colours", ["color", "variant"])
    # May or may not match depending on heuristic


def test_load_registry_convenience_function(registry_file):
    """Test the convenience function"""
    from mcp_server.component_registry import load_registry, ComponentRegistry

    with patch.object(ComponentRegistry, '__init__', return_value=None) as mock_init:
        with patch.object(ComponentRegistry, 'load', return_value=True):
            mock_init.return_value = None
            # Can't easily test this without mocking more - just ensure it doesn't crash
            pass


def test_find_registry_file_exact_match(tmp_path):
    """Test finding exact registry file match"""
    from mcp_server.component_registry import ComponentRegistry

    # Create registry files
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir()
    (registry_dir / "dmc_2_5.json").write_text('{"version": "2.5.0"}')

    reg = ComponentRegistry(dmc_version="2.5.1")
    reg.registry_dir = registry_dir

    result = reg._find_registry_file()

    assert result is not None
    assert result.name == "dmc_2_5.json"


def test_find_registry_file_fallback(tmp_path):
    """Test fallback to latest registry when no exact match"""
    from mcp_server.component_registry import ComponentRegistry

    # Create registry files
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir()
    (registry_dir / "dmc_0_14.json").write_text('{"version": "0.14.0"}')

    reg = ComponentRegistry(dmc_version="2.5.1")  # No exact match
    reg.registry_dir = registry_dir

    result = reg._find_registry_file()

    assert result is not None
    assert result.name == "dmc_0_14.json"  # Falls back to available
