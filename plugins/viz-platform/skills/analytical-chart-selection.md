---
name: analytical-chart-selection
description: Maps analytical questions to Plotly graph_objects trace types with configuration guidance
---

# Analytical Chart Selection

## Purpose

Guides selection of the right Plotly `graph_objects` trace type for each analytical question. This skill covers the full `go.*` API — far beyond what the viz-platform MCP `chart_create` tool supports (which is limited to line, bar, scatter, pie, heatmap, histogram, area).

Load this skill when generating visualizations in Jupyter notebooks or any context using `plotly.graph_objects` directly.

**Reference:** https://plotly.com/python-api-reference/plotly.graph_objects.html

---

## Decision Framework

**Always start with the analytical question, not the chart type.** The question determines the chart.

### Distribution Analysis — "How is X spread?"

| Scenario | Trace Type | Why This One |
|---|---|---|
| Single variable distribution | `go.Histogram` | Shows frequency shape, bin edges reveal gaps |
| Compare distributions across groups | `go.Violin` | Shows density shape per group — richer than Box |
| Distribution with outlier emphasis | `go.Box` | Quartiles + outlier dots, compact for many groups |
| 2D density (where do points concentrate?) | `go.Histogram2dContour` or `go.Contour` | Reveals concentration patterns invisible in scatter |

**Key config:**
```python
# Violin with box inside
go.Violin(box_visible=True, meanline_visible=True, points='outliers')

# Histogram with controlled bins
go.Histogram(nbinsx=30, histnorm='probability density')
```

### Relationship Analysis — "How does X relate to Y?"

| Scenario | Trace Type | Why This One |
|---|---|---|
| Two numeric variables | `go.Scatter` or `go.Scattergl` (>5k points) | Classic correlation view, add trendline via numpy |
| Relationship with third variable | `go.Scatter` with `marker.color` mapped to Z | Color encodes the third dimension |
| Correlation matrix (many variables) | `go.Heatmap` | Overview of all pairwise relationships at once |
| Ranked relationship (ordinal data) | `go.Scatter` with jitter | Avoid overplotting on discrete values |

**Key config:**
```python
# Scatter with regression line (compute manually)
slope, intercept, r, p, se = scipy.stats.linregress(x, y)
fig.add_trace(go.Scatter(x=x_range, y=slope*x_range + intercept,
    mode='lines', line=dict(dash='dash', color='#FF6B6B'),
    name=f'r={r:.3f}, p={p:.2e}'))

# Heatmap correlation matrix
go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.index,
    colorscale='RdBu', zmid=0, text=corr_matrix.round(2).values,
    texttemplate='%{text}', textfont=dict(size=10))
```

### Composition Analysis — "What makes up the whole?"

| Scenario | Trace Type | Why This One |
|---|---|---|
| Hierarchical breakdown (2+ levels) | `go.Treemap` | Shows both hierarchy and proportion |
| Hierarchical with radial layout | `go.Sunburst` | Good for 3+ level hierarchies |
| Hierarchical exploration (top-down) | `go.Icicle` | Linear layout, easier to read for deep hierarchies |
| Flow between categories | `go.Sankey` | Shows how entities move between states/groups |
| Component breakdown (additive) | `go.Waterfall` | Shows how parts sum to a total |

**NEVER use `go.Pie` or donut charts.** Treemap and Sunburst encode the same information with better perceptual accuracy and scale to hierarchical data.

**Key config:**
```python
# Treemap
go.Treemap(labels=labels, parents=parents, values=values,
    branchvalues='total', textinfo='label+percent parent',
    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Share: %{percentParent:.1%}<extra></extra>')

# Sankey
go.Sankey(node=dict(label=node_labels, color=node_colors),
    link=dict(source=sources, target=targets, value=values,
    color=link_colors, hovertemplate='%{source.label} → %{target.label}: %{value}<extra></extra>'))
```

### Temporal & Range Analysis — "How did X change?"

| Scenario | Trace Type | Why This One |
|---|---|---|
| Trend over time | `go.Scatter` (mode='lines') | Clean trend line |
| Range per period (min/Q1/median/Q3/max) | `go.Candlestick` or `go.Ohlc` | Shows full range distribution per period |
| Cumulative change | `go.Waterfall` | Running total with positive/negative contributions |

**Key config:**
```python
# Candlestick for income range analysis (repurposed from finance)
go.Candlestick(x=periods, open=q1_values, high=max_values,
    low=min_values, close=q3_values,
    increasing_line_color='#00D4AA', decreasing_line_color='#FF6B6B')
```

### Spatial Analysis — "Where are the patterns?"

| Scenario | Trace Type | Why This One |
|---|---|---|
| Choropleth with GeoJSON | `go.Choroplethmapbox` | Neighbourhood-level thematic maps |
| Point locations on map | `go.Scattermapbox` | Individual locations with popups |
| Density overlay | `go.Densitymapbox` | Continuous heat surface |

**Key config:**
```python
# Choroplethmapbox
go.Choroplethmapbox(geojson=geojson, locations=ids, z=values,
    featureidkey='properties.neighbourhood_id',
    colorscale='Viridis', marker_opacity=0.8, marker_line_width=0.5,
    hovertemplate='<b>%{text}</b><br>Value: %{z:.1f}<extra></extra>')

# Layout for mapbox
fig.update_layout(mapbox=dict(style='carto-darkmatter',
    center=dict(lat=43.7, lon=-79.4), zoom=10))
```

### Summary & KPI — "What's the headline number?"

| Scenario | Trace Type | Why This One |
|---|---|---|
| Single KPI with delta | `go.Indicator` | Dashboard-style metric cards |
| Multiple KPIs in grid | Multiple `go.Indicator` in subplots | Compact overview |

**Key config:**
```python
go.Indicator(mode='number+delta',
    value=current_value,
    delta=dict(reference=previous_value, valueformat='.1f', prefix='$'),
    title=dict(text='Median Income (2021)'),
    number=dict(valueformat='$,.0f'))
```

---

## Hover Template Standard

Every trace must have a `hovertemplate` that answers three questions:

1. **What am I looking at?** — entity name, category, label
2. **What's the value?** — with proper formatting and units
3. **How does it compare?** — rank, percentile, vs average, vs previous period

```python
hovertemplate=(
    "<b>%{customdata[0]}</b><br>"          # What: neighbourhood name
    "Median Income: $%{y:,.0f}<br>"        # Value: formatted with units
    "City Rank: %{customdata[1]} of 158<br>"  # Compare: rank
    "vs City Avg: %{customdata[2]:+.1f}%"    # Compare: delta
    "<extra></extra>"                        # Remove trace name box
)
```

Use `customdata` arrays to inject comparison metrics that aren't on the axes.

---

## Chart Selection Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Using bar charts for everything | Bars are for categorical comparison, not distributions or correlations | Match the question type to the chart type above |
| Same chart type back-to-back | Reader fatigue, suggests lazy analysis | Vary chart types — if two consecutive findings need the same type, consider combining them |
| Exotic chart for simple data | Sankey diagram showing 2 categories is overkill | Use the simplest chart that reveals the pattern |
| 3D charts | Almost never improve comprehension, often obscure data | Stick to 2D; use color for the third dimension |
| Pie/donut for any reason | Poor perceptual accuracy for comparing slices | Treemap (proportional) or Bar (comparison) |
