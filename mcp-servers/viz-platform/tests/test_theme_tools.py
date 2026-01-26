"""
Unit tests for theme management tools.
"""
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def theme_store():
    """Create a fresh ThemeStore instance"""
    from mcp_server.theme_store import ThemeStore
    store = ThemeStore()
    store._themes = {}  # Clear any existing themes
    return store


@pytest.fixture
def theme_tools(theme_store):
    """Create ThemeTools instance with fresh store"""
    from mcp_server.theme_tools import ThemeTools
    return ThemeTools(store=theme_store)


def test_theme_store_init():
    """Test theme store initialization"""
    from mcp_server.theme_store import ThemeStore

    store = ThemeStore()

    # Should have default theme
    assert store.get_theme("default") is not None


def test_default_theme_structure():
    """Test default theme has required structure"""
    from mcp_server.theme_store import DEFAULT_THEME

    assert "name" in DEFAULT_THEME
    assert "tokens" in DEFAULT_THEME
    assert "colors" in DEFAULT_THEME["tokens"]
    assert "spacing" in DEFAULT_THEME["tokens"]
    assert "typography" in DEFAULT_THEME["tokens"]
    assert "radii" in DEFAULT_THEME["tokens"]


def test_default_theme_colors():
    """Test default theme has required color tokens"""
    from mcp_server.theme_store import DEFAULT_THEME

    colors = DEFAULT_THEME["tokens"]["colors"]

    assert "primary" in colors
    assert "secondary" in colors
    assert "success" in colors
    assert "warning" in colors
    assert "error" in colors
    assert "background" in colors
    assert "text" in colors


@pytest.mark.asyncio
async def test_theme_create(theme_tools):
    """Test creating a new theme"""
    tokens = {
        "colors": {
            "primary": "#ff0000"
        }
    }

    result = await theme_tools.theme_create("my-theme", tokens)

    assert result["name"] == "my-theme"
    assert "tokens" in result
    assert result["tokens"]["colors"]["primary"] == "#ff0000"


@pytest.mark.asyncio
async def test_theme_create_merges_with_defaults(theme_tools):
    """Test that new theme merges with default tokens"""
    tokens = {
        "colors": {
            "primary": "#ff0000"
        }
    }

    result = await theme_tools.theme_create("partial-theme", tokens)

    # Should have primary from our tokens
    assert result["tokens"]["colors"]["primary"] == "#ff0000"
    # Should inherit secondary from defaults
    assert "secondary" in result["tokens"]["colors"]


@pytest.mark.asyncio
async def test_theme_create_duplicate_name(theme_tools, theme_store):
    """Test creating theme with existing name fails"""
    # Create first theme
    await theme_tools.theme_create("existing", {"colors": {}})

    # Try to create with same name
    result = await theme_tools.theme_create("existing", {"colors": {}})

    assert "error" in result
    assert "already exists" in result["error"]


@pytest.mark.asyncio
async def test_theme_extend(theme_tools, theme_store):
    """Test extending an existing theme"""
    # Create base theme
    await theme_tools.theme_create("base", {
        "colors": {"primary": "#0000ff"}
    })

    # Extend it
    result = await theme_tools.theme_extend(
        base_theme="base",
        overrides={"colors": {"secondary": "#00ff00"}},
        new_name="extended"
    )

    assert result["name"] == "extended"
    # Should have base primary
    assert result["tokens"]["colors"]["primary"] == "#0000ff"
    # Should have override secondary
    assert result["tokens"]["colors"]["secondary"] == "#00ff00"


@pytest.mark.asyncio
async def test_theme_extend_nonexistent_base(theme_tools):
    """Test extending nonexistent theme fails"""
    result = await theme_tools.theme_extend(
        base_theme="nonexistent",
        overrides={},
        new_name="new"
    )

    assert "error" in result
    assert "not found" in result["error"]


@pytest.mark.asyncio
async def test_theme_extend_default_name(theme_tools, theme_store):
    """Test extending creates default name if not provided"""
    await theme_tools.theme_create("base", {"colors": {}})

    result = await theme_tools.theme_extend(
        base_theme="base",
        overrides={}
        # No new_name provided
    )

    assert result["name"] == "base_extended"


@pytest.mark.asyncio
async def test_theme_validate(theme_tools, theme_store):
    """Test theme validation"""
    await theme_tools.theme_create("test-theme", {
        "colors": {"primary": "#ff0000"},
        "spacing": {"md": "16px"}
    })

    result = await theme_tools.theme_validate("test-theme")

    assert "complete" in result or "validation" in result


@pytest.mark.asyncio
async def test_theme_validate_nonexistent(theme_tools):
    """Test validating nonexistent theme"""
    result = await theme_tools.theme_validate("nonexistent")

    assert "error" in result


@pytest.mark.asyncio
async def test_theme_export_css(theme_tools, theme_store):
    """Test exporting theme as CSS"""
    await theme_tools.theme_create("css-theme", {
        "colors": {"primary": "#ff0000"},
        "spacing": {"md": "16px"}
    })

    result = await theme_tools.theme_export_css("css-theme")

    assert "css" in result
    # CSS should contain custom properties
    assert "--" in result["css"]


@pytest.mark.asyncio
async def test_theme_export_css_nonexistent(theme_tools):
    """Test exporting nonexistent theme"""
    result = await theme_tools.theme_export_css("nonexistent")

    assert "error" in result


@pytest.mark.asyncio
async def test_theme_list(theme_tools, theme_store):
    """Test listing themes"""
    await theme_tools.theme_create("theme1", {"colors": {}})
    await theme_tools.theme_create("theme2", {"colors": {}})

    result = await theme_tools.theme_list()

    assert "themes" in result
    assert "theme1" in result["themes"]
    assert "theme2" in result["themes"]


@pytest.mark.asyncio
async def test_theme_activate(theme_tools, theme_store):
    """Test activating a theme"""
    await theme_tools.theme_create("active-theme", {"colors": {}})

    result = await theme_tools.theme_activate("active-theme")

    assert result.get("active_theme") == "active-theme" or result.get("success") is True


@pytest.mark.asyncio
async def test_theme_activate_nonexistent(theme_tools):
    """Test activating nonexistent theme"""
    result = await theme_tools.theme_activate("nonexistent")

    assert "error" in result


def test_theme_store_get_theme(theme_store):
    """Test getting theme from store"""
    from mcp_server.theme_store import DEFAULT_THEME

    # Add a theme first, then retrieve it
    theme_store._themes["test-theme"] = {"name": "test-theme", "tokens": {}}
    result = theme_store.get_theme("test-theme")

    assert result is not None
    assert result["name"] == "test-theme"


def test_theme_store_list_themes(theme_store):
    """Test listing themes from store"""
    result = theme_store.list_themes()

    assert isinstance(result, list)


def test_deep_merge(theme_tools):
    """Test deep merging of token dicts"""
    base = {
        "colors": {
            "primary": "#000",
            "secondary": "#111"
        },
        "spacing": {"sm": "8px"}
    }

    override = {
        "colors": {
            "primary": "#fff"
        }
    }

    result = theme_tools._deep_merge(base, override)

    # primary should be overridden
    assert result["colors"]["primary"] == "#fff"
    # secondary should remain
    assert result["colors"]["secondary"] == "#111"
    # spacing should remain
    assert result["spacing"]["sm"] == "8px"


def test_validate_tokens(theme_tools):
    """Test token validation"""
    from mcp_server.theme_store import REQUIRED_TOKEN_CATEGORIES

    tokens = {
        "colors": {"primary": "#000"},
        "spacing": {"md": "16px"},
        "typography": {"fontFamily": "Inter"},
        "radii": {"md": "8px"}
    }

    result = theme_tools._validate_tokens(tokens)

    assert "complete" in result
    # Check for either "missing" or "missing_required" key
    assert "missing" in result or "missing_required" in result or "missing_optional" in result


def test_validate_tokens_incomplete(theme_tools):
    """Test validation of incomplete tokens"""
    tokens = {
        "colors": {"primary": "#000"}
        # Missing spacing, typography, radii
    }

    result = theme_tools._validate_tokens(tokens)

    # Should flag missing categories
    assert result["complete"] is False or len(result.get("missing", [])) > 0
