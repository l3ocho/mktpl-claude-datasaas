# Accessibility Rules

## WCAG Contrast Standards

| Level | Ratio | Use Case |
|-------|-------|----------|
| AA (normal text) | 4.5:1 | Body text, labels |
| AA (large text) | 3:1 | Headings, 14pt+ bold |
| AAA (enhanced) | 7:1 | Highest accessibility |

## Color Blindness Types

| Type | Affected Colors | Population |
|------|-----------------|------------|
| **Deuteranopia** | Red-Green (green-blind) | ~6% males, 0.4% females |
| **Protanopia** | Red-Green (red-blind) | ~2.5% males, 0.05% females |
| **Tritanopia** | Blue-Yellow | ~0.01% total |

## Color-Blind Safe Palettes

### IBM Design Colors
```
#648FFF #785EF0 #DC267F #FE6100 #FFB000
```

### Tableau Colorblind 10
```
#006BA4 #FF800E #ABABAB #595959 #5F9ED1
#C85200 #898989 #A2C8EC #FFBC79 #CFCFCF
```

### Okabe-Ito
```
#E69F00 #56B4E9 #009E73 #F0E442 #0072B2
#D55E00 #CC79A7 #000000
```

### Safe Palette Categories

```json
{
  "categorical": ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"],
  "sequential": ["#FEE0D2", "#FC9272", "#DE2D26"],
  "diverging": ["#4575B4", "#FFFFBF", "#D73027"]
}
```

## Best Practices

1. **Don't rely on color alone** - Use shapes, patterns, or labels
2. **Test with simulation** - View through color blindness simulators
3. **Use sufficient contrast** - Minimum 4.5:1 for text, 3:1 for large elements
4. **Limit color count** - Fewer colors = easier to distinguish
5. **Use semantic colors** - Blue for information, red for errors (with icons)

## Accessibility Scoring

| Grade | Description |
|-------|-------------|
| A | Excellent - All WCAG AAA standards met |
| B | Good - WCAG AA standards met with minor warnings |
| C | Acceptable - WCAG AA met but improvements recommended |
| D | Poor - Some WCAG AA failures |
| F | Failing - Major accessibility issues |
