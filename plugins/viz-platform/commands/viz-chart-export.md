---
name: viz chart-export
description: Export a Plotly chart to PNG, SVG, or PDF format
---

# /viz chart-export

## Skills to Load
- skills/mcp-tools-reference.md
- skills/chart-types.md

## Visual Output

```
+------------------------------------------------------------------+
|  VIZ-PLATFORM - Chart Export                                     |
+------------------------------------------------------------------+
```

Export a Plotly chart to static image formats.

## Usage

```
/viz chart-export {format}
```

## Arguments

- `format` (required): png, svg, or pdf

## Tool Mapping

```python
chart_export(figure=figure_json, format="png", width=1200, height=800, scale=2)
```

Requires `kaleido` package: `pip install kaleido`

## Related Commands

- `/viz chart {type}` - Create a chart
- `/viz theme {name}` - Apply theme before export
