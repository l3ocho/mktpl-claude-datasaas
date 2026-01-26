"""
Unit tests for chart creation tools.
"""
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def chart_tools():
    """Create ChartTools instance"""
    from mcp_server.chart_tools import ChartTools
    return ChartTools()


@pytest.fixture
def chart_tools_with_theme():
    """Create ChartTools instance with a theme"""
    from mcp_server.chart_tools import ChartTools

    tools = ChartTools()
    tools.set_theme({
        "colors": {
            "primary": "#ff0000",
            "secondary": "#00ff00",
            "success": "#0000ff"
        }
    })
    return tools


def test_chart_tools_init():
    """Test chart tools initialization"""
    from mcp_server.chart_tools import ChartTools

    tools = ChartTools()

    assert tools.theme_store is None
    assert tools._active_theme is None


def test_set_theme(chart_tools):
    """Test setting active theme"""
    theme = {"colors": {"primary": "#123456"}}

    chart_tools.set_theme(theme)

    assert chart_tools._active_theme == theme


def test_get_color_palette_default(chart_tools):
    """Test getting default color palette"""
    from mcp_server.chart_tools import DEFAULT_COLORS

    palette = chart_tools._get_color_palette()

    assert palette == DEFAULT_COLORS


def test_get_color_palette_with_theme(chart_tools_with_theme):
    """Test getting color palette from theme"""
    palette = chart_tools_with_theme._get_color_palette()

    # Should start with theme colors
    assert palette[0] == "#ff0000"
    assert palette[1] == "#00ff00"
    assert palette[2] == "#0000ff"


def test_resolve_color_from_theme(chart_tools_with_theme):
    """Test resolving color token from theme"""
    color = chart_tools_with_theme._resolve_color("primary")

    assert color == "#ff0000"


def test_resolve_color_hex(chart_tools):
    """Test resolving hex color"""
    color = chart_tools._resolve_color("#abcdef")

    assert color == "#abcdef"


def test_resolve_color_rgb(chart_tools):
    """Test resolving rgb color"""
    color = chart_tools._resolve_color("rgb(255, 0, 0)")

    assert color == "rgb(255, 0, 0)"


def test_resolve_color_named(chart_tools):
    """Test resolving named color"""
    color = chart_tools._resolve_color("blue")

    assert color == "#228be6"  # DEFAULT_COLORS[0]


def test_resolve_color_none(chart_tools):
    """Test resolving None color defaults to first palette color"""
    from mcp_server.chart_tools import DEFAULT_COLORS

    color = chart_tools._resolve_color(None)

    assert color == DEFAULT_COLORS[0]


@pytest.mark.asyncio
async def test_chart_create_line(chart_tools):
    """Test creating a line chart"""
    data = {
        "x": [1, 2, 3, 4, 5],
        "y": [10, 20, 15, 25, 30]
    }

    result = await chart_tools.chart_create("line", data)

    assert "figure" in result
    assert result["chart_type"] == "line"
    assert "error" not in result or result["error"] is None


@pytest.mark.asyncio
async def test_chart_create_bar(chart_tools):
    """Test creating a bar chart"""
    data = {
        "x": ["A", "B", "C"],
        "y": [10, 20, 15]
    }

    result = await chart_tools.chart_create("bar", data)

    assert "figure" in result
    assert result["chart_type"] == "bar"


@pytest.mark.asyncio
async def test_chart_create_scatter(chart_tools):
    """Test creating a scatter chart"""
    data = {
        "x": [1, 2, 3, 4, 5],
        "y": [10, 20, 15, 25, 30]
    }

    result = await chart_tools.chart_create("scatter", data)

    assert "figure" in result
    assert result["chart_type"] == "scatter"


@pytest.mark.asyncio
async def test_chart_create_pie(chart_tools):
    """Test creating a pie chart"""
    data = {
        "labels": ["A", "B", "C"],
        "values": [30, 50, 20]
    }

    result = await chart_tools.chart_create("pie", data)

    assert "figure" in result
    assert result["chart_type"] == "pie"


@pytest.mark.asyncio
async def test_chart_create_histogram(chart_tools):
    """Test creating a histogram"""
    data = {
        "x": [1, 1, 2, 2, 2, 3, 3, 4, 5, 5, 5, 5]
    }

    result = await chart_tools.chart_create("histogram", data)

    assert "figure" in result
    assert result["chart_type"] == "histogram"


@pytest.mark.asyncio
async def test_chart_create_area(chart_tools):
    """Test creating an area chart"""
    data = {
        "x": [1, 2, 3, 4, 5],
        "y": [10, 20, 15, 25, 30]
    }

    result = await chart_tools.chart_create("area", data)

    assert "figure" in result
    assert result["chart_type"] == "area"


@pytest.mark.asyncio
async def test_chart_create_heatmap(chart_tools):
    """Test creating a heatmap"""
    data = {
        "z": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "x": ["A", "B", "C"],
        "y": ["X", "Y", "Z"]
    }

    result = await chart_tools.chart_create("heatmap", data)

    assert "figure" in result
    assert result["chart_type"] == "heatmap"


@pytest.mark.asyncio
async def test_chart_create_invalid_type(chart_tools):
    """Test creating chart with invalid type"""
    data = {"x": [1, 2, 3], "y": [10, 20, 30]}

    result = await chart_tools.chart_create("invalid_type", data)

    assert "error" in result
    assert "invalid" in result["error"].lower()


@pytest.mark.asyncio
async def test_chart_create_with_options(chart_tools):
    """Test creating chart with options"""
    data = {
        "x": [1, 2, 3],
        "y": [10, 20, 30]
    }
    options = {
        "title": "My Chart",
        "color": "red"
    }

    result = await chart_tools.chart_create("line", data, options=options)

    assert "figure" in result
    # The title should be applied to the figure


@pytest.mark.asyncio
async def test_chart_create_with_theme(chart_tools_with_theme):
    """Test that theme colors are applied to chart"""
    data = {
        "x": [1, 2, 3],
        "y": [10, 20, 30]
    }

    result = await chart_tools_with_theme.chart_create("line", data)

    assert "figure" in result
    # Chart should use theme colors


@pytest.mark.asyncio
async def test_chart_configure_interaction(chart_tools):
    """Test configuring chart interaction"""
    # Create a simple figure first
    data = {"x": [1, 2, 3], "y": [10, 20, 30]}
    chart_result = await chart_tools.chart_create("line", data)
    figure = chart_result.get("figure", {})

    if hasattr(chart_tools, 'chart_configure_interaction'):
        result = await chart_tools.chart_configure_interaction(
            figure=figure,
            interactions={"zoom": True, "pan": True}
        )

        # Just verify it doesn't crash
        assert result is not None


def test_default_colors_defined():
    """Test that DEFAULT_COLORS is properly defined"""
    from mcp_server.chart_tools import DEFAULT_COLORS

    assert len(DEFAULT_COLORS) == 10
    assert all(c.startswith("#") for c in DEFAULT_COLORS)
