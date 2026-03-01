---
name: notebook-design-system
description: Reusable dark-theme design system for Plotly graph_objects in Jupyter notebooks
---

# Notebook Design System

## Purpose

Defines a complete visual design system for Plotly `graph_objects` in Jupyter notebooks. This is NOT for Dash dashboards (which use viz-platform themes and DMC components). This is specifically for standalone notebook visualizations.

Load this skill when generating Jupyter notebooks with Plotly visualizations.

---

## Layout Template

Copy this template into the first code cell of every notebook:

```python
LAYOUT_TEMPLATE = dict(
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font=dict(family='Inter, Arial, sans-serif', color='#FFFFFF', size=12),
    title=dict(font=dict(size=16, color='#FFFFFF'), x=0.5, xanchor='center'),
    xaxis=dict(showgrid=False, color='#B0B0B0', zeroline=False,
               tickfont=dict(size=11), title_font=dict(size=12)),
    yaxis=dict(showgrid=False, color='#B0B0B0', zeroline=False,
               tickfont=dict(size=11), title_font=dict(size=12)),
    margin=dict(l=60, r=30, t=80, b=60),
    hoverlabel=dict(bgcolor='#1a1a1a', font_size=11, font_color='#FFFFFF',
                    bordercolor='#333333'),
    coloraxis=dict(colorbar=dict(
        tickfont=dict(color='#B0B0B0'),
        title_font=dict(color='#B0B0B0')
    )),
    showlegend=False,
)

# Color palette — accessible on black backgrounds
COLORS = dict(
    primary='#00D4AA',        # Teal-green — main accent
    secondary='#7B61FF',      # Purple — secondary accent
    tertiary='#FF6B6B',       # Coral — alerts/negative
    quaternary='#FFB84D',     # Amber — warnings/highlights
    quinary='#4DABF7',        # Sky blue — info/neutral

    # Sequential for numeric scales
    seq_low='#0D1B2A',
    seq_mid='#1B4965',
    seq_high='#00D4AA',

    # Categorical palette (7 colors, WCAG AA on black)
    cat=[ '#00D4AA', '#7B61FF', '#FF6B6B', '#FFB84D', '#4DABF7',
          '#E599F7', '#69DB7C' ],

    # Diverging (negative → neutral → positive)
    div_neg='#FF6B6B',
    div_mid='#333333',
    div_pos='#00D4AA',

    # Text
    text_primary='#FFFFFF',
    text_secondary='#B0B0B0',
    text_muted='#666666',

    # Grid (use sparingly — gridlines off by default)
    grid='#1a1a1a',
    grid_emphasis='#333333',
)

# Plotly colorscales for continuous data
COLORSCALES = dict(
    sequential='Viridis',         # Default for single-direction numeric
    sequential_alt='Plasma',      # Alternative when Viridis is used elsewhere
    diverging='RdBu',             # For data centered on a meaningful zero
    spatial='Ice',                # For choropleth maps
)


def apply_layout(fig, title, subtitle=None, **overrides):
    """Apply the standard design system to any Plotly figure.

    Args:
        fig: Plotly Figure object
        title: Chart title (analytical, descriptive)
        subtitle: Optional methodology note (appears below title)
        **overrides: Any layout key to override defaults
    """
    full_title = title
    if subtitle:
        full_title = f"{title}<br><sup style='color:#B0B0B0'>{subtitle}</sup>"

    layout = {**LAYOUT_TEMPLATE}
    layout['title'] = dict(text=full_title, **LAYOUT_TEMPLATE.get('title', {}))
    layout.update(overrides)
    fig.update_layout(**layout)
    return fig
```

---

## Design Rules

### Background
- Paper and plot: `#000000`. Pure black. Not dark grey.

### Gridlines
- **OFF by default** (`showgrid=False` on both axes).
- Add back ONLY with explicit analytical justification in a markdown cell.
- When added: use `gridcolor='#1a1a1a'`, `griddash='dot'`.
- Reference lines (e.g., city average): `#333333`, `dash='dash'`.

### Titles
- Every chart gets an **analytical title** that states the finding, not the chart type.
- ✅ `"Income Distribution Reveals Bimodal Pattern (2021, CPI-adjusted)"`
- ❌ `"Income Chart"`, `"Figure 3"`, `"Bar Chart of Income"`

### Legends
- Hidden by default (`showlegend=False`).
- Show ONLY when multiple series need disambiguation.
- When shown: `legend=dict(font=dict(color='#B0B0B0'), bgcolor='rgba(0,0,0,0)')`.

### Annotations
- Font color: `#B0B0B0` for non-critical, `#FFFFFF` for emphasis.
- Arrow color: `#666666`.
- Use annotations to call out specific data points that support findings.

### Colorscales
- Sequential data: `Viridis` (default) or `Plasma` (alternative).
- Diverging data: `RdBu` with `zmid=0`.
- Spatial maps: `Ice` or `Viridis`.
- Categorical: use `COLORS['cat']` list.
- NEVER use Plotly's default color cycle (too bright for black backgrounds).

### Mapbox
- Style: `carto-darkmatter` (matches black background).
- No Mapbox token required for `carto-darkmatter`.
- For tile-based `go.Choroplethmap` background control and valid style patterns, see the `choropleth-map-patterns` skill.

---

## Absolute Prohibitions

1. **NO pie or donut charts.** Ever. Use Treemap or Sunburst.
2. **NO default Plotly templates.** Every figure gets explicit layout via `apply_layout()`.
3. **NO white or light backgrounds.** All charts on `#000000`.
4. **NO default gridlines.** Must be explicitly justified.
5. **NO charts without hover templates.** Every trace gets `hovertemplate`.
6. **NO generic titles.** Title must state the analytical finding or question.
