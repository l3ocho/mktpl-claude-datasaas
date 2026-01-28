"""
Accessibility validation tools for color blindness and WCAG compliance.

Provides tools for validating color palettes against color blindness
simulations and WCAG contrast requirements.
"""
import logging
import math
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)


# Color-blind safe palettes
SAFE_PALETTES = {
    "categorical": {
        "name": "Paul Tol's Qualitative",
        "colors": ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"],
        "description": "Distinguishable for all types of color blindness"
    },
    "ibm": {
        "name": "IBM Design",
        "colors": ["#648FFF", "#785EF0", "#DC267F", "#FE6100", "#FFB000"],
        "description": "IBM's accessible color palette"
    },
    "okabe_ito": {
        "name": "Okabe-Ito",
        "colors": ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"],
        "description": "Optimized for all color vision deficiencies"
    },
    "tableau_colorblind": {
        "name": "Tableau Colorblind 10",
        "colors": ["#006BA4", "#FF800E", "#ABABAB", "#595959", "#5F9ED1",
                   "#C85200", "#898989", "#A2C8EC", "#FFBC79", "#CFCFCF"],
        "description": "Industry-standard accessible palette"
    }
}


# Simulation matrices for color blindness (LMS color space transformation)
# These approximate how colors appear to people with different types of color blindness
SIMULATION_MATRICES = {
    "deuteranopia": {
        # Green-blind (most common)
        "severity": "common",
        "population": "6% males, 0.4% females",
        "description": "Difficulty distinguishing red from green (green-blind)",
        "matrix": [
            [0.625, 0.375, 0.0],
            [0.700, 0.300, 0.0],
            [0.0, 0.300, 0.700]
        ]
    },
    "protanopia": {
        # Red-blind
        "severity": "common",
        "population": "2.5% males, 0.05% females",
        "description": "Difficulty distinguishing red from green (red-blind)",
        "matrix": [
            [0.567, 0.433, 0.0],
            [0.558, 0.442, 0.0],
            [0.0, 0.242, 0.758]
        ]
    },
    "tritanopia": {
        # Blue-blind (rare)
        "severity": "rare",
        "population": "0.01% total",
        "description": "Difficulty distinguishing blue from yellow",
        "matrix": [
            [0.950, 0.050, 0.0],
            [0.0, 0.433, 0.567],
            [0.0, 0.475, 0.525]
        ]
    }
}


class AccessibilityTools:
    """
    Color accessibility validation tools.

    Validates colors for WCAG compliance and color blindness accessibility.
    """

    def __init__(self, theme_store=None):
        """
        Initialize accessibility tools.

        Args:
            theme_store: Optional ThemeStore for theme color extraction
        """
        self.theme_store = theme_store

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c * 2 for c in hex_color])
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color."""
        return '#{:02x}{:02x}{:02x}'.format(
            max(0, min(255, int(rgb[0]))),
            max(0, min(255, int(rgb[1]))),
            max(0, min(255, int(rgb[2])))
        )

    def _get_relative_luminance(self, rgb: Tuple[int, int, int]) -> float:
        """
        Calculate relative luminance per WCAG 2.1.

        https://www.w3.org/WAI/GL/wiki/Relative_luminance
        """
        def channel_luminance(value: int) -> float:
            v = value / 255
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

        r, g, b = rgb
        return (
            0.2126 * channel_luminance(r) +
            0.7152 * channel_luminance(g) +
            0.0722 * channel_luminance(b)
        )

    def _get_contrast_ratio(self, color1: str, color2: str) -> float:
        """
        Calculate contrast ratio between two colors per WCAG 2.1.

        Returns ratio between 1:1 and 21:1.
        """
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)

        l1 = self._get_relative_luminance(rgb1)
        l2 = self._get_relative_luminance(rgb2)

        lighter = max(l1, l2)
        darker = min(l1, l2)

        return (lighter + 0.05) / (darker + 0.05)

    def _simulate_color_blindness(
        self,
        hex_color: str,
        deficiency_type: str
    ) -> str:
        """
        Simulate how a color appears with a specific color blindness type.

        Uses linear RGB transformation approximation.
        """
        if deficiency_type not in SIMULATION_MATRICES:
            return hex_color

        rgb = self._hex_to_rgb(hex_color)
        matrix = SIMULATION_MATRICES[deficiency_type]["matrix"]

        # Apply transformation matrix
        r = rgb[0] * matrix[0][0] + rgb[1] * matrix[0][1] + rgb[2] * matrix[0][2]
        g = rgb[0] * matrix[1][0] + rgb[1] * matrix[1][1] + rgb[2] * matrix[1][2]
        b = rgb[0] * matrix[2][0] + rgb[1] * matrix[2][1] + rgb[2] * matrix[2][2]

        return self._rgb_to_hex((r, g, b))

    def _get_color_distance(self, color1: str, color2: str) -> float:
        """
        Calculate perceptual color distance (CIE76 approximation).

        Returns a value where < 20 means colors may be hard to distinguish.
        """
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)

        # Simple Euclidean distance in RGB space (approximation)
        # For production, should use CIEDE2000
        return math.sqrt(
            (rgb1[0] - rgb2[0]) ** 2 +
            (rgb1[1] - rgb2[1]) ** 2 +
            (rgb1[2] - rgb2[2]) ** 2
        )

    async def accessibility_validate_colors(
        self,
        colors: List[str],
        check_types: Optional[List[str]] = None,
        min_contrast_ratio: float = 4.5
    ) -> Dict[str, Any]:
        """
        Validate a list of colors for accessibility.

        Args:
            colors: List of hex colors to validate
            check_types: Color blindness types to check (default: all)
            min_contrast_ratio: Minimum WCAG contrast ratio (default: 4.5 for AA)

        Returns:
            Dict with:
                - issues: List of accessibility issues found
                - simulations: How colors appear under each deficiency
                - recommendations: Suggestions for improvement
                - safe_palettes: Color-blind safe palette suggestions
        """
        check_types = check_types or list(SIMULATION_MATRICES.keys())
        issues = []
        simulations = {}

        # Normalize colors
        normalized_colors = [c.upper() if c.startswith('#') else f'#{c.upper()}' for c in colors]

        # Simulate each color blindness type
        for deficiency in check_types:
            if deficiency not in SIMULATION_MATRICES:
                continue

            simulated = [self._simulate_color_blindness(c, deficiency) for c in normalized_colors]
            simulations[deficiency] = {
                "original": normalized_colors,
                "simulated": simulated,
                "info": SIMULATION_MATRICES[deficiency]
            }

            # Check if any color pairs become indistinguishable
            for i in range(len(normalized_colors)):
                for j in range(i + 1, len(normalized_colors)):
                    distance = self._get_color_distance(simulated[i], simulated[j])
                    if distance < 30:  # Threshold for distinguishability
                        issues.append({
                            "type": "distinguishability",
                            "severity": "warning" if distance > 15 else "error",
                            "colors": [normalized_colors[i], normalized_colors[j]],
                            "affected_by": [deficiency],
                            "simulated_colors": [simulated[i], simulated[j]],
                            "distance": round(distance, 1),
                            "message": f"Colors may be hard to distinguish for {deficiency} ({SIMULATION_MATRICES[deficiency]['description']})"
                        })

        # Check contrast ratios against white and black backgrounds
        for color in normalized_colors:
            white_contrast = self._get_contrast_ratio(color, "#FFFFFF")
            black_contrast = self._get_contrast_ratio(color, "#000000")

            if white_contrast < min_contrast_ratio and black_contrast < min_contrast_ratio:
                issues.append({
                    "type": "contrast_ratio",
                    "severity": "error",
                    "colors": [color],
                    "white_contrast": round(white_contrast, 2),
                    "black_contrast": round(black_contrast, 2),
                    "required": min_contrast_ratio,
                    "message": f"Insufficient contrast against both white ({white_contrast:.1f}:1) and black ({black_contrast:.1f}:1) backgrounds"
                })

        # Generate recommendations
        recommendations = self._generate_recommendations(issues)

        # Calculate overall score
        error_count = sum(1 for i in issues if i["severity"] == "error")
        warning_count = sum(1 for i in issues if i["severity"] == "warning")

        if error_count == 0 and warning_count == 0:
            score = "A"
        elif error_count == 0 and warning_count <= 2:
            score = "B"
        elif error_count <= 2:
            score = "C"
        else:
            score = "D"

        return {
            "colors_checked": normalized_colors,
            "overall_score": score,
            "issue_count": len(issues),
            "issues": issues,
            "simulations": simulations,
            "recommendations": recommendations,
            "safe_palettes": SAFE_PALETTES
        }

    async def accessibility_validate_theme(
        self,
        theme_name: str
    ) -> Dict[str, Any]:
        """
        Validate a theme's colors for accessibility.

        Args:
            theme_name: Theme name to validate

        Returns:
            Dict with accessibility validation results
        """
        if not self.theme_store:
            return {
                "error": "Theme store not configured",
                "theme_name": theme_name
            }

        theme = self.theme_store.get_theme(theme_name)
        if not theme:
            available = self.theme_store.list_themes()
            return {
                "error": f"Theme '{theme_name}' not found. Available: {available}",
                "theme_name": theme_name
            }

        # Extract colors from theme
        colors = []
        tokens = theme.get("tokens", {})
        color_tokens = tokens.get("colors", {})

        def extract_colors(obj, prefix=""):
            """Recursively extract color values."""
            if isinstance(obj, str) and (obj.startswith('#') or len(obj) == 6):
                colors.append(obj if obj.startswith('#') else f'#{obj}')
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    extract_colors(value, f"{prefix}.{key}")
            elif isinstance(obj, list):
                for item in obj:
                    extract_colors(item, prefix)

        extract_colors(color_tokens)

        # Validate extracted colors
        result = await self.accessibility_validate_colors(colors)
        result["theme_name"] = theme_name

        # Add theme-specific checks
        primary = color_tokens.get("primary")
        background = color_tokens.get("background", {})
        text = color_tokens.get("text", {})

        if primary and background:
            bg_color = background.get("base") if isinstance(background, dict) else background
            if bg_color:
                contrast = self._get_contrast_ratio(primary, bg_color)
                if contrast < 4.5:
                    result["issues"].append({
                        "type": "primary_contrast",
                        "severity": "error",
                        "colors": [primary, bg_color],
                        "ratio": round(contrast, 2),
                        "required": 4.5,
                        "message": f"Primary color has insufficient contrast ({contrast:.1f}:1) against background"
                    })

        return result

    async def accessibility_suggest_alternative(
        self,
        color: str,
        deficiency_type: str
    ) -> Dict[str, Any]:
        """
        Suggest accessible alternative colors.

        Args:
            color: Original hex color
            deficiency_type: Type of color blindness to optimize for

        Returns:
            Dict with alternative color suggestions
        """
        rgb = self._hex_to_rgb(color)

        suggestions = []

        # Suggest shifting hue while maintaining saturation and brightness
        # For red-green deficiency, shift toward blue or yellow
        if deficiency_type in ["deuteranopia", "protanopia"]:
            # Shift toward blue
            blue_shift = self._rgb_to_hex((
                max(0, rgb[0] - 50),
                max(0, rgb[1] - 30),
                min(255, rgb[2] + 80)
            ))
            suggestions.append({
                "color": blue_shift,
                "description": "Blue-shifted alternative",
                "preserves": "approximate brightness"
            })

            # Shift toward yellow/orange
            yellow_shift = self._rgb_to_hex((
                min(255, rgb[0] + 50),
                min(255, rgb[1] + 30),
                max(0, rgb[2] - 80)
            ))
            suggestions.append({
                "color": yellow_shift,
                "description": "Yellow-shifted alternative",
                "preserves": "approximate brightness"
            })

        elif deficiency_type == "tritanopia":
            # For blue-yellow deficiency, shift toward red or green
            red_shift = self._rgb_to_hex((
                min(255, rgb[0] + 60),
                max(0, rgb[1] - 20),
                max(0, rgb[2] - 40)
            ))
            suggestions.append({
                "color": red_shift,
                "description": "Red-shifted alternative",
                "preserves": "approximate brightness"
            })

        # Add safe palette suggestions
        for palette_name, palette in SAFE_PALETTES.items():
            # Find closest color in safe palette
            min_distance = float('inf')
            closest = None
            for safe_color in palette["colors"]:
                distance = self._get_color_distance(color, safe_color)
                if distance < min_distance:
                    min_distance = distance
                    closest = safe_color

            if closest:
                suggestions.append({
                    "color": closest,
                    "description": f"From {palette['name']} palette",
                    "palette": palette_name
                })

        return {
            "original_color": color,
            "deficiency_type": deficiency_type,
            "suggestions": suggestions[:5]  # Limit to 5 suggestions
        }

    def _generate_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations based on issues."""
        recommendations = []

        # Check for distinguishability issues
        distinguishability_issues = [i for i in issues if i["type"] == "distinguishability"]
        if distinguishability_issues:
            affected_types = set()
            for issue in distinguishability_issues:
                affected_types.update(issue.get("affected_by", []))

            if "deuteranopia" in affected_types or "protanopia" in affected_types:
                recommendations.append(
                    "Avoid using red and green as the only differentiators - "
                    "add patterns, shapes, or labels"
                )

            recommendations.append(
                "Consider using a color-blind safe palette like Okabe-Ito or IBM Design"
            )

        # Check for contrast issues
        contrast_issues = [i for i in issues if i["type"] in ["contrast_ratio", "primary_contrast"]]
        if contrast_issues:
            recommendations.append(
                "Increase contrast by darkening colors for light backgrounds "
                "or lightening for dark backgrounds"
            )
            recommendations.append(
                "Use WCAG contrast checker tools to verify text readability"
            )

        # General recommendations
        if len(issues) > 0:
            recommendations.append(
                "Add secondary visual cues (icons, patterns, labels) "
                "to not rely solely on color"
            )

        if not recommendations:
            recommendations.append(
                "Color palette appears accessible! Consider adding patterns "
                "for additional distinguishability"
            )

        return recommendations
