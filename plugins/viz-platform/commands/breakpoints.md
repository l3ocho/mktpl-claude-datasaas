---
description: Configure responsive breakpoints for dashboard layouts
---

# Configure Breakpoints

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🎨 VIZ-PLATFORM · Breakpoints                                    │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the configuration.

Configure responsive breakpoints for a layout to support mobile-first design across different screen sizes.

## Usage

```
/breakpoints {layout_ref}
```

## Arguments

- `layout_ref` (required): Layout name to configure breakpoints for

## Examples

```
/breakpoints my-dashboard
/breakpoints sales-report
```

## Tool Mapping

This command uses the `layout_set_breakpoints` MCP tool:

```python
layout_set_breakpoints(
    layout_ref="my-dashboard",
    breakpoints={
        "xs": {"cols": 1, "spacing": "xs"},    # < 576px (mobile)
        "sm": {"cols": 2, "spacing": "sm"},    # >= 576px (large mobile)
        "md": {"cols": 6, "spacing": "md"},    # >= 768px (tablet)
        "lg": {"cols": 12, "spacing": "md"},   # >= 992px (desktop)
        "xl": {"cols": 12, "spacing": "lg"}    # >= 1200px (large desktop)
    },
    mobile_first=True
)
```

## Workflow

1. **User invokes**: `/breakpoints my-dashboard`
2. **Agent asks**: Which breakpoints to customize? (shows current settings)
3. **Agent asks**: Mobile column count? (xs, typically 1-2)
4. **Agent asks**: Tablet column count? (md, typically 4-6)
5. **Agent applies**: Breakpoint configuration
6. **Agent returns**: Complete responsive configuration

## Breakpoint Sizes

| Name | Min Width | Common Devices |
|------|-----------|----------------|
| `xs` | 0px | Small phones (portrait) |
| `sm` | 576px | Large phones, small tablets |
| `md` | 768px | Tablets (portrait) |
| `lg` | 992px | Tablets (landscape), laptops |
| `xl` | 1200px | Desktops, large screens |

## Mobile-First Approach

When `mobile_first=True` (default), styles cascade up:
- Define base styles for `xs` (mobile)
- Override only what changes at larger breakpoints
- Smaller CSS footprint, better performance

```python
# Mobile-first example
{
    "xs": {"cols": 1},      # Stack everything on mobile
    "md": {"cols": 6},      # Two-column on tablet
    "lg": {"cols": 12}      # Full grid on desktop
}
```

When `mobile_first=False`, styles cascade down:
- Define base styles for `xl` (desktop)
- Override for smaller screens
- Traditional "desktop-first" approach

## Grid Configuration per Breakpoint

Each breakpoint can configure:

| Property | Description | Values |
|----------|-------------|--------|
| `cols` | Grid column count | 1-24 |
| `spacing` | Gap between items | xs, sm, md, lg, xl |
| `gutter` | Outer padding | xs, sm, md, lg, xl |
| `grow` | Items grow to fill | true, false |

## Common Patterns

### Dashboard (Charts & Filters)
```python
{
    "xs": {"cols": 1, "spacing": "xs"},   # Full-width cards
    "sm": {"cols": 2, "spacing": "sm"},   # 2 cards per row
    "md": {"cols": 3, "spacing": "md"},   # 3 cards per row
    "lg": {"cols": 4, "spacing": "md"},   # 4 cards per row
    "xl": {"cols": 6, "spacing": "lg"}    # 6 cards per row
}
```

### Data Table
```python
{
    "xs": {"cols": 1, "scroll": true},    # Horizontal scroll
    "md": {"cols": 1, "scroll": false},   # Full table visible
    "lg": {"cols": 1}                     # Same as md
}
```

### Form Layout
```python
{
    "xs": {"cols": 1},                    # Single column
    "md": {"cols": 2},                    # Two columns
    "lg": {"cols": 3}                     # Three columns
}
```

### Sidebar Layout
```python
{
    "xs": {"sidebar": "hidden"},          # No sidebar on mobile
    "md": {"sidebar": "collapsed"},       # Icon-only sidebar
    "lg": {"sidebar": "expanded"}         # Full sidebar
}
```

## Component Span

Control how many columns a component spans at each breakpoint:

```python
# A chart that spans full width on mobile, half on desktop
{
    "component": "sales-chart",
    "span": {
        "xs": 1,     # Full width (1/1)
        "md": 3,     # Half width (3/6)
        "lg": 6      # Half width (6/12)
    }
}
```

## DMC Grid Integration

This maps to Dash Mantine Components Grid:

```python
dmc.Grid(
    children=[
        dmc.GridCol(
            children=[chart],
            span={"base": 12, "sm": 6, "lg": 4}  # Responsive span
        )
    ],
    gutter="md"
)
```

## Output

```json
{
  "layout_ref": "my-dashboard",
  "breakpoints": {
    "xs": {"cols": 1, "spacing": "xs", "min_width": "0px"},
    "sm": {"cols": 2, "spacing": "sm", "min_width": "576px"},
    "md": {"cols": 6, "spacing": "md", "min_width": "768px"},
    "lg": {"cols": 12, "spacing": "md", "min_width": "992px"},
    "xl": {"cols": 12, "spacing": "lg", "min_width": "1200px"}
  },
  "mobile_first": true,
  "css_media_queries": [
    "@media (min-width: 576px) { ... }",
    "@media (min-width: 768px) { ... }",
    "@media (min-width: 992px) { ... }",
    "@media (min-width: 1200px) { ... }"
  ]
}
```

## Related Commands

- `/dashboard {template}` - Create layout with default breakpoints
- `/layout-set-grid` - Configure grid without responsive settings
- `/theme {name}` - Theme includes default spacing values
