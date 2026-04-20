"""
Unit tests for DMC validation tools.
"""
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_registry():
    """Create a mock component registry"""
    registry = MagicMock()
    registry.is_loaded.return_value = True
    registry.loaded_version = "2.5.1"

    registry.categories = {
        "buttons": ["Button", "ActionIcon"],
        "inputs": ["TextInput", "Select"]
    }

    registry.list_components.return_value = registry.categories
    registry.get_categories.return_value = ["buttons", "inputs"]

    # Mock Button component
    registry.get_component.side_effect = lambda name: {
        "Button": {
            "description": "Button component",
            "props": {
                "variant": {"type": "string", "enum": ["filled", "outline"], "default": "filled"},
                "color": {"type": "string", "default": "blue"},
                "size": {"type": "string", "enum": ["xs", "sm", "md", "lg"], "default": "sm"},
                "disabled": {"type": "boolean", "default": False, "required": False}
            }
        },
        "TextInput": {
            "description": "Text input",
            "props": {
                "value": {"type": "string", "required": True},
                "placeholder": {"type": "string"}
            }
        }
    }.get(name)

    registry.get_component_props.side_effect = lambda name: {
        "Button": {
            "variant": {"type": "string", "enum": ["filled", "outline"], "default": "filled"},
            "color": {"type": "string", "default": "blue"},
            "size": {"type": "string", "enum": ["xs", "sm", "md", "lg"], "default": "sm"},
            "disabled": {"type": "boolean", "default": False}
        },
        "TextInput": {
            "value": {"type": "string", "required": True},
            "placeholder": {"type": "string"}
        }
    }.get(name)

    registry.validate_prop.side_effect = lambda comp, prop, val: (
        {"valid": True} if prop in ["variant", "color", "size", "disabled", "value", "placeholder"]
        else {"valid": False, "error": f"Unknown prop '{prop}'"}
    )

    return registry


@pytest.fixture
def dmc_tools(mock_registry):
    """Create DMCTools instance with mock registry"""
    from mcp_server.dmc_tools import DMCTools

    tools = DMCTools(registry=mock_registry)
    tools._initialized = True
    return tools


@pytest.fixture
def uninitialized_tools():
    """Create uninitialized DMCTools instance"""
    from mcp_server.dmc_tools import DMCTools
    return DMCTools()


@pytest.mark.asyncio
async def test_list_components_all(dmc_tools):
    """Test listing all components"""
    result = await dmc_tools.list_components()

    assert "components" in result
    assert "categories" in result
    assert "version" in result
    assert result["version"] == "2.5.1"


@pytest.mark.asyncio
async def test_list_components_by_category(dmc_tools, mock_registry):
    """Test listing components by category"""
    mock_registry.list_components.return_value = {"buttons": ["Button", "ActionIcon"]}

    result = await dmc_tools.list_components(category="buttons")

    assert "buttons" in result["components"]
    mock_registry.list_components.assert_called_with("buttons")


@pytest.mark.asyncio
async def test_list_components_not_initialized(uninitialized_tools):
    """Test listing components when not initialized"""
    result = await uninitialized_tools.list_components()

    assert "error" in result
    assert result["total_count"] == 0


@pytest.mark.asyncio
async def test_get_component_props_success(dmc_tools):
    """Test getting component props"""
    result = await dmc_tools.get_component_props("Button")

    assert result["component"] == "Button"
    assert "props" in result
    assert result["prop_count"] > 0


@pytest.mark.asyncio
async def test_get_component_props_not_found(dmc_tools, mock_registry):
    """Test getting props for nonexistent component"""
    mock_registry.get_component.return_value = None

    result = await dmc_tools.get_component_props("Nonexistent")

    assert "error" in result
    assert "not found" in result["error"]


@pytest.mark.asyncio
async def test_get_component_props_not_initialized(uninitialized_tools):
    """Test getting props when not initialized"""
    result = await uninitialized_tools.get_component_props("Button")

    assert "error" in result
    assert result["prop_count"] == 0


@pytest.mark.asyncio
async def test_validate_component_valid(dmc_tools, mock_registry):
    """Test validating valid component props"""
    props = {
        "variant": "filled",
        "color": "blue",
        "size": "md"
    }

    result = await dmc_tools.validate_component("Button", props)

    assert result["valid"] is True
    assert len(result["errors"]) == 0
    assert result["component"] == "Button"


@pytest.mark.asyncio
async def test_validate_component_invalid_prop(dmc_tools, mock_registry):
    """Test validating with invalid prop name"""
    mock_registry.validate_prop.side_effect = lambda comp, prop, val: (
        {"valid": False, "error": f"Unknown prop '{prop}'"} if prop == "unknownProp"
        else {"valid": True}
    )

    props = {"unknownProp": "value"}

    result = await dmc_tools.validate_component("Button", props)

    assert result["valid"] is False
    assert len(result["errors"]) > 0


@pytest.mark.asyncio
async def test_validate_component_missing_required(dmc_tools, mock_registry):
    """Test validating with missing required prop"""
    # TextInput has required value prop
    mock_registry.get_component.return_value = {
        "props": {
            "value": {"type": "string", "required": True}
        }
    }

    result = await dmc_tools.validate_component("TextInput", {})

    assert result["valid"] is False
    assert any("required" in e.lower() for e in result["errors"])


@pytest.mark.asyncio
async def test_validate_component_not_found(dmc_tools, mock_registry):
    """Test validating nonexistent component"""
    mock_registry.get_component.return_value = None

    result = await dmc_tools.validate_component("Nonexistent", {"prop": "value"})

    assert result["valid"] is False
    assert "Unknown component" in result["errors"][0]


@pytest.mark.asyncio
async def test_validate_component_not_initialized(uninitialized_tools):
    """Test validating when not initialized"""
    result = await uninitialized_tools.validate_component("Button", {})

    assert result["valid"] is False
    assert "not initialized" in result["errors"][0].lower()


@pytest.mark.asyncio
async def test_validate_component_skips_special_props(dmc_tools, mock_registry):
    """Test that special props (id, children, etc) are skipped"""
    props = {
        "id": "my-button",
        "children": "Click me",
        "className": "my-class",
        "style": {"color": "red"},
        "key": "btn-1"
    }

    result = await dmc_tools.validate_component("Button", props)

    # Should not error on special props
    assert result["valid"] is True


def test_find_similar_component(dmc_tools, mock_registry):
    """Test finding similar component names"""
    # Should find Button when given 'button' (case mismatch)
    similar = dmc_tools._find_similar_component("button")

    assert similar == "Button"


def test_find_similar_component_prefix(dmc_tools, mock_registry):
    """Test finding similar component with prefix match"""
    similar = dmc_tools._find_similar_component("Butt")

    assert similar == "Button"


def test_check_common_mistakes_onclick(dmc_tools):
    """Test detection of onclick event handler mistake"""
    warnings = []
    dmc_tools._check_common_mistakes("Button", {"onClick": "handler"}, warnings)

    assert len(warnings) > 0
    assert any("callback" in w.lower() for w in warnings)


def test_check_common_mistakes_class(dmc_tools):
    """Test detection of 'class' instead of 'className'"""
    warnings = []
    dmc_tools._check_common_mistakes("Button", {"class": "my-class"}, warnings)

    assert len(warnings) > 0
    assert any("classname" in w.lower() for w in warnings)


def test_check_common_mistakes_button_href(dmc_tools):
    """Test detection of Button with href but no component prop"""
    warnings = []
    dmc_tools._check_common_mistakes("Button", {"href": "/link"}, warnings)

    assert len(warnings) > 0
    assert any("component" in w.lower() for w in warnings)


def test_initialize_with_version():
    """Test initializing tools with DMC version"""
    from mcp_server.dmc_tools import DMCTools

    tools = DMCTools()

    with patch('mcp_server.dmc_tools.ComponentRegistry') as MockRegistry:
        mock_instance = MagicMock()
        mock_instance.is_loaded.return_value = True
        MockRegistry.return_value = mock_instance

        result = tools.initialize(dmc_version="2.5.1")

        MockRegistry.assert_called_once_with("2.5.1")
        assert result is True
