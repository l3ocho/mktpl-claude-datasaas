---
description: Export a Plotly chart to PNG, SVG, or PDF format
---

# Export Chart

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🎨 VIZ-PLATFORM · Chart Export                                   │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the export.

Export a Plotly chart to static image formats for sharing, embedding, or printing.

## Usage

```
/chart-export {format}
```

## Arguments

- `format` (required): Output format - one of: png, svg, pdf

## Examples

```
/chart-export png
/chart-export svg
/chart-export pdf
```

## Tool Mapping

This command uses the `chart_export` MCP tool:

```python
chart_export(
    figure=figure_json,           # Plotly figure JSON from chart_create
    format="png",                 # Output format: png, svg, pdf
    width=1200,                   # Optional: image width in pixels
    height=800,                   # Optional: image height in pixels
    scale=2,                      # Optional: resolution scale factor
    output_path=None              # Optional: save to file path
)
```

## Workflow

1. **User invokes**: `/chart-export png`
2. **Agent asks**: Which chart to export? (if multiple charts in context)
3. **Agent asks**: Image dimensions? (optional, uses chart defaults)
4. **Agent exports**: Chart with `chart_export` tool
5. **Agent returns**: Base64 image data or file path

## Output Formats

| Format | Best For | File Size |
|--------|----------|-----------|
| `png` | Web, presentations, general use | Medium |
| `svg` | Scalable graphics, editing | Small |
| `pdf` | Print, documents, archival | Large |

## Resolution Options

### Width & Height
Specify exact pixel dimensions:
```python
chart_export(figure, format="png", width=1920, height=1080)
```

### Scale Factor
Increase resolution for high-DPI displays:
```python
chart_export(figure, format="png", scale=3)  # 3x resolution
```

Common scale values:
- `1` - Standard resolution (72 DPI)
- `2` - Retina/HiDPI (144 DPI)
- `3` - Print quality (216 DPI)
- `4` - High-quality print (288 DPI)

## Output Options

### Return as Base64
Default behavior - returns base64-encoded image data:
```python
result = chart_export(figure, format="png")
# result["image_data"] contains base64 string
```

### Save to File
Specify output path to save directly:
```python
chart_export(figure, format="png", output_path="/path/to/chart.png")
# result["file_path"] contains the saved path
```

## Requirements

This tool requires the `kaleido` package for rendering:
```bash
pip install kaleido
```

Kaleido is a cross-platform library that renders Plotly figures without a browser.

## Error Handling

Common issues:
- **Kaleido not installed**: Install with `pip install kaleido`
- **Invalid figure**: Ensure figure is valid Plotly JSON
- **Permission denied**: Check write permissions for output path

## Related Commands

- `/chart {type}` - Create a chart
- `/theme {name}` - Apply theme before export
- `/dashboard` - Create layout containing charts
