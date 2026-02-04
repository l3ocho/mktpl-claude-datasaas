---
description: Create a Plotly chart with theme integration
---

# Create Chart

## Skills to Load
- skills/mcp-tools-reference.md
- skills/chart-types.md

## Visual Output

```
+------------------------------------------------------------------+
|  VIZ-PLATFORM - Chart Builder                                    |
+------------------------------------------------------------------+
```

Create a Plotly chart with automatic theme token application.

## Usage

```
/chart {type}
```

## Arguments

- `type` (required): line, bar, scatter, pie, area, histogram, box, heatmap, sunburst, treemap

## Tool Mapping

```python
chart_create(chart_type="line", data_ref="df", x="date", y="value", theme=None)
```

## Related Commands

- `/chart-export {format}` - Export chart to image
- `/theme {name}` - Apply theme to charts
- `/dashboard` - Create layout with charts
