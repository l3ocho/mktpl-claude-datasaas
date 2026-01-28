---
description: Validate color accessibility for color blind users
---

# Accessibility Check

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🎨 VIZ-PLATFORM · Accessibility Check                            │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the accessibility validation.

Validate theme or chart colors for color blind accessibility, checking contrast ratios and suggesting alternatives.

## Usage

```
/accessibility-check {target}
```

## Arguments

- `target` (optional): "theme" or "chart" - defaults to active theme

## Examples

```
/accessibility-check
/accessibility-check theme
/accessibility-check chart
```

## Tool Mapping

This command uses the `accessibility_validate_colors` MCP tool:

```python
accessibility_validate_colors(
    colors=["#228be6", "#40c057", "#fa5252"],  # Colors to check
    check_types=["deuteranopia", "protanopia", "tritanopia"],
    min_contrast_ratio=4.5                      # WCAG AA standard
)
```

Or validate a full theme:
```python
accessibility_validate_theme(
    theme_name="corporate"
)
```

## Workflow

1. **User invokes**: `/accessibility-check theme`
2. **Tool analyzes**: Theme color palette
3. **Tool simulates**: Color perception for each deficiency type
4. **Tool checks**: Contrast ratios between color pairs
5. **Tool returns**: Issues found and alternative suggestions

## Color Blindness Types

| Type | Affected Colors | Population |
|------|-----------------|------------|
| **Deuteranopia** | Red-Green (green-blind) | ~6% males, 0.4% females |
| **Protanopia** | Red-Green (red-blind) | ~2.5% males, 0.05% females |
| **Tritanopia** | Blue-Yellow | ~0.01% total |

## Output Example

```json
{
  "theme_name": "corporate",
  "overall_score": "B",
  "issues": [
    {
      "type": "contrast",
      "severity": "warning",
      "colors": ["#fa5252", "#40c057"],
      "affected_by": ["deuteranopia", "protanopia"],
      "message": "Red and green may be indistinguishable for red-green color blind users",
      "suggestion": "Use blue (#228be6) instead of green to differentiate from red"
    },
    {
      "type": "contrast_ratio",
      "severity": "error",
      "colors": ["#fab005", "#ffffff"],
      "ratio": 2.1,
      "required": 4.5,
      "message": "Insufficient contrast for WCAG AA compliance",
      "suggestion": "Darken yellow to #e6a200 for ratio of 4.5+"
    }
  ],
  "recommendations": [
    "Add patterns or shapes to distinguish data series, not just color",
    "Include labels directly on chart elements",
    "Consider using a color-blind safe palette"
  ],
  "safe_palettes": {
    "categorical": ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"],
    "sequential": ["#FEE0D2", "#FC9272", "#DE2D26"],
    "diverging": ["#4575B4", "#FFFFBF", "#D73027"]
  }
}
```

## WCAG Contrast Standards

| Level | Ratio | Use Case |
|-------|-------|----------|
| AA (normal text) | 4.5:1 | Body text, labels |
| AA (large text) | 3:1 | Headings, 14pt+ bold |
| AAA (enhanced) | 7:1 | Highest accessibility |

## Color-Blind Safe Palettes

The tool can suggest complete color-blind safe palettes:

### IBM Design Colors
Designed for accessibility:
```
#648FFF #785EF0 #DC267F #FE6100 #FFB000
```

### Tableau Colorblind 10
Industry-standard accessible palette:
```
#006BA4 #FF800E #ABABAB #595959 #5F9ED1
#C85200 #898989 #A2C8EC #FFBC79 #CFCFCF
```

### Okabe-Ito
Optimized for all types of color blindness:
```
#E69F00 #56B4E9 #009E73 #F0E442 #0072B2
#D55E00 #CC79A7 #000000
```

## Related Commands

- `/theme-new {name}` - Create accessible theme from the start
- `/theme-validate {name}` - General theme validation
- `/chart {type}` - Create chart (check colors after)

## Best Practices

1. **Don't rely on color alone** - Use shapes, patterns, or labels
2. **Test with simulation** - View your visualizations through color blindness simulators
3. **Use sufficient contrast** - Minimum 4.5:1 for text, 3:1 for large elements
4. **Limit color count** - Fewer colors = easier to distinguish
5. **Use semantic colors** - Blue for information, red for errors (with icons)
