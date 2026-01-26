---
description: Create a Plotly chart with theme integration
---

# Create Chart

Create a Plotly chart with automatic theme token application.

## Usage

```
/chart {type}
```

## Arguments

- `type` (required): Chart type - one of: line, bar, scatter, pie, area, histogram, box, heatmap, sunburst, treemap

## Examples

```
/chart line
/chart bar
/chart scatter
/chart pie
```

## Tool Mapping

This command uses the `chart_create` MCP tool:

```python
chart_create(
    chart_type="line",
    data_ref="df_sales",          # Reference to loaded DataFrame
    x="date",                      # X-axis column
    y="revenue",                   # Y-axis column
    color=None,                    # Optional: column for color grouping
    title="Sales Over Time",       # Optional: chart title
    theme=None                     # Optional: theme name to apply
)
```

## Workflow

1. **User invokes**: `/chart line`
2. **Agent asks**: Which DataFrame to use? (list available with `list_data` from data-platform)
3. **Agent asks**: Which columns for X and Y axes?
4. **Agent asks**: Any grouping/color column?
5. **Agent creates**: Chart with `chart_create` tool
6. **Agent returns**: Plotly figure JSON ready for rendering

## Chart Types

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

Charts automatically inherit colors from the active theme:
- Primary color for main data
- Color palette for multi-series
- Font family and sizes
- Background colors

Override with explicit theme:
```python
chart_create(chart_type="bar", ..., theme="my-dark-theme")
```

## Output

Returns Plotly figure JSON that can be:
- Rendered in a Dash app
- Saved as HTML/PNG
- Embedded in a layout component
