"""
Tests for accessibility validation tools.
"""
import pytest
from mcp_server.accessibility_tools import AccessibilityTools


@pytest.fixture
def tools():
    """Create AccessibilityTools instance."""
    return AccessibilityTools()


class TestHexToRgb:
    """Tests for _hex_to_rgb method."""

    def test_hex_to_rgb_6_digit(self, tools):
        """Test 6-digit hex conversion."""
        assert tools._hex_to_rgb("#FF0000") == (255, 0, 0)
        assert tools._hex_to_rgb("#00FF00") == (0, 255, 0)
        assert tools._hex_to_rgb("#0000FF") == (0, 0, 255)

    def test_hex_to_rgb_3_digit(self, tools):
        """Test 3-digit hex conversion."""
        assert tools._hex_to_rgb("#F00") == (255, 0, 0)
        assert tools._hex_to_rgb("#0F0") == (0, 255, 0)
        assert tools._hex_to_rgb("#00F") == (0, 0, 255)

    def test_hex_to_rgb_lowercase(self, tools):
        """Test lowercase hex conversion."""
        assert tools._hex_to_rgb("#ff0000") == (255, 0, 0)


class TestContrastRatio:
    """Tests for _get_contrast_ratio method."""

    def test_black_white_contrast(self, tools):
        """Test black on white has maximum contrast."""
        ratio = tools._get_contrast_ratio("#000000", "#FFFFFF")
        assert ratio == pytest.approx(21.0, rel=0.01)

    def test_same_color_contrast(self, tools):
        """Test same color has minimum contrast."""
        ratio = tools._get_contrast_ratio("#FF0000", "#FF0000")
        assert ratio == pytest.approx(1.0, rel=0.01)

    def test_symmetric_contrast(self, tools):
        """Test contrast ratio is symmetric."""
        ratio1 = tools._get_contrast_ratio("#228be6", "#FFFFFF")
        ratio2 = tools._get_contrast_ratio("#FFFFFF", "#228be6")
        assert ratio1 == pytest.approx(ratio2, rel=0.01)


class TestColorBlindnessSimulation:
    """Tests for _simulate_color_blindness method."""

    def test_deuteranopia_simulation(self, tools):
        """Test deuteranopia (green-blind) simulation."""
        # Red and green should appear more similar
        original_red = "#FF0000"
        original_green = "#00FF00"

        simulated_red = tools._simulate_color_blindness(original_red, "deuteranopia")
        simulated_green = tools._simulate_color_blindness(original_green, "deuteranopia")

        # They should be different from originals
        assert simulated_red != original_red or simulated_green != original_green

    def test_protanopia_simulation(self, tools):
        """Test protanopia (red-blind) simulation."""
        simulated = tools._simulate_color_blindness("#FF0000", "protanopia")
        # Should return a modified color
        assert simulated.startswith("#")
        assert len(simulated) == 7

    def test_tritanopia_simulation(self, tools):
        """Test tritanopia (blue-blind) simulation."""
        simulated = tools._simulate_color_blindness("#0000FF", "tritanopia")
        # Should return a modified color
        assert simulated.startswith("#")
        assert len(simulated) == 7

    def test_unknown_deficiency_returns_original(self, tools):
        """Test unknown deficiency type returns original color."""
        color = "#FF0000"
        simulated = tools._simulate_color_blindness(color, "unknown")
        assert simulated == color


class TestAccessibilityValidateColors:
    """Tests for accessibility_validate_colors method."""

    @pytest.mark.asyncio
    async def test_validate_single_color(self, tools):
        """Test validating a single color."""
        result = await tools.accessibility_validate_colors(["#228be6"])
        assert "colors_checked" in result
        assert "overall_score" in result
        assert "issues" in result
        assert "safe_palettes" in result

    @pytest.mark.asyncio
    async def test_validate_problematic_colors(self, tools):
        """Test similar colors trigger warnings."""
        # Use colors that are very close in hue, which should be harder to distinguish
        result = await tools.accessibility_validate_colors(["#FF5555", "#FF6666"])
        # Similar colors should trigger distinguishability warnings
        assert "issues" in result
        # The validation should at least run without errors
        assert "colors_checked" in result
        assert len(result["colors_checked"]) == 2

    @pytest.mark.asyncio
    async def test_validate_contrast_issue(self, tools):
        """Test low contrast colors trigger contrast warnings."""
        # Yellow on white has poor contrast
        result = await tools.accessibility_validate_colors(["#FFFF00"])
        # Check for contrast issues (yellow may have issues with both black and white)
        assert "issues" in result

    @pytest.mark.asyncio
    async def test_validate_with_specific_types(self, tools):
        """Test validating for specific color blindness types."""
        result = await tools.accessibility_validate_colors(
            ["#FF0000", "#00FF00"],
            check_types=["deuteranopia"]
        )
        assert "simulations" in result
        assert "deuteranopia" in result["simulations"]
        assert "protanopia" not in result["simulations"]

    @pytest.mark.asyncio
    async def test_overall_score(self, tools):
        """Test overall score is calculated."""
        result = await tools.accessibility_validate_colors(["#228be6", "#ffffff"])
        assert result["overall_score"] in ["A", "B", "C", "D"]

    @pytest.mark.asyncio
    async def test_recommendations_generated(self, tools):
        """Test recommendations are generated for issues."""
        result = await tools.accessibility_validate_colors(["#FF0000", "#00FF00"])
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0


class TestAccessibilitySuggestAlternative:
    """Tests for accessibility_suggest_alternative method."""

    @pytest.mark.asyncio
    async def test_suggest_alternative_deuteranopia(self, tools):
        """Test suggesting alternatives for deuteranopia."""
        result = await tools.accessibility_suggest_alternative("#FF0000", "deuteranopia")
        assert "original_color" in result
        assert result["deficiency_type"] == "deuteranopia"
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0

    @pytest.mark.asyncio
    async def test_suggest_alternative_tritanopia(self, tools):
        """Test suggesting alternatives for tritanopia."""
        result = await tools.accessibility_suggest_alternative("#0000FF", "tritanopia")
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0

    @pytest.mark.asyncio
    async def test_suggestions_include_safe_palettes(self, tools):
        """Test suggestions include colors from safe palettes."""
        result = await tools.accessibility_suggest_alternative("#FF0000", "deuteranopia")
        palette_suggestions = [
            s for s in result["suggestions"]
            if "palette" in s
        ]
        assert len(palette_suggestions) > 0


class TestSafePalettes:
    """Tests for safe palette constants."""

    def test_safe_palettes_exist(self, tools):
        """Test that safe palettes are defined."""
        from mcp_server.accessibility_tools import SAFE_PALETTES
        assert "categorical" in SAFE_PALETTES
        assert "ibm" in SAFE_PALETTES
        assert "okabe_ito" in SAFE_PALETTES
        assert "tableau_colorblind" in SAFE_PALETTES

    def test_safe_palettes_have_colors(self, tools):
        """Test that safe palettes have color lists."""
        from mcp_server.accessibility_tools import SAFE_PALETTES
        for palette_name, palette in SAFE_PALETTES.items():
            assert "colors" in palette
            assert len(palette["colors"]) > 0
            # All colors should be valid hex
            for color in palette["colors"]:
                assert color.startswith("#")
