# Chart Types Reference

## Available Chart Types

| Type | Best For |
|------|----------|
| `line` | Time series, trends |
| `bar` | Comparisons, categories |
| `scatter` | Correlations, distributions |
| `pie` | Part-to-whole relationships |
| `area` | Cumulative trends |
| `histogram` | Frequency distributions |
| `box` | Statistical distributions |
| `heatmap` | Matrix correlations |
| `sunburst` | Hierarchical data |
| `treemap` | Hierarchical proportions |

## Theme Integration

Charts automatically inherit from active theme:
- Primary color for main data
- Color palette for multi-series
- Font family and sizes
- Background colors

Override with explicit theme:
```python
chart_create(chart_type="bar", ..., theme="my-dark-theme")
```

## Export Formats

| Format | Best For | File Size |
|--------|----------|-----------|
| `png` | Web, presentations, general use | Medium |
| `svg` | Scalable graphics, editing | Small |
| `pdf` | Print, documents, archival | Large |

## Resolution Options

### Scale Factor
- `1` - Standard resolution (72 DPI)
- `2` - Retina/HiDPI (144 DPI)
- `3` - Print quality (216 DPI)
- `4` - High-quality print (288 DPI)

## Export Requirements

Requires `kaleido` package:
```bash
pip install kaleido
```

## Output

Charts return Plotly figure JSON that can be:
- Rendered in a Dash app
- Saved as HTML/PNG/SVG/PDF
- Embedded in a layout component
