---
name: chart export
description: [dmc-design] Export a Plotly chart to PNG, SVG, or PDF format
---

# /chart export

Export a Plotly chart to static image formats.

## Usage

```
/chart export {format}
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
- `/viz theme apply {name}` - Apply theme before export
