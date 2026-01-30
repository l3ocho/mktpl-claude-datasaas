# Responsive Design

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
{
    "xs": {"cols": 1},      # Stack everything on mobile
    "md": {"cols": 6},      # Two-column on tablet
    "lg": {"cols": 12}      # Full grid on desktop
}
```

When `mobile_first=False`, styles cascade down (desktop-first).

## Grid Configuration

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
    "xs": {"cols": 1, "spacing": "xs"},
    "sm": {"cols": 2, "spacing": "sm"},
    "md": {"cols": 3, "spacing": "md"},
    "lg": {"cols": 4, "spacing": "md"},
    "xl": {"cols": 6, "spacing": "lg"}
}
```

### Data Table
```python
{
    "xs": {"cols": 1, "scroll": true},
    "md": {"cols": 1, "scroll": false},
    "lg": {"cols": 1}
}
```

### Form Layout
```python
{
    "xs": {"cols": 1},
    "md": {"cols": 2},
    "lg": {"cols": 3}
}
```

### Sidebar Layout
```python
{
    "xs": {"sidebar": "hidden"},
    "md": {"sidebar": "collapsed"},
    "lg": {"sidebar": "expanded"}
}
```

## Component Span

Control how many columns a component spans:

```python
{
    "component": "sales-chart",
    "span": {
        "xs": 1,     # Full width (1/1)
        "md": 3,     # Half width (3/6)
        "lg": 6      # Half width (6/12)
    }
}
```

## CSS Media Queries

Generated for each breakpoint:
```css
@media (min-width: 576px) { ... }
@media (min-width: 768px) { ... }
@media (min-width: 992px) { ... }
@media (min-width: 1200px) { ... }
```
