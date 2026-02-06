---
name: viz chart
description: Create a Plotly chart with theme integration
---

# /viz chart

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
/viz chart {type}
```

## Arguments

- `type` (required): line, bar, scatter, pie, area, histogram, box, heatmap, sunburst, treemap

## Tool Mapping

```python
chart_create(chart_type="line", data_ref="df", x="date", y="value", theme=None)
```

## Related Commands

- `/viz chart-export {format}` - Export chart to image
- `/viz theme {name}` - Apply theme to charts
- `/viz dashboard` - Create layout with charts
