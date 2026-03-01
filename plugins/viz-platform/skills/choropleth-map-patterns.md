---
name: choropleth-map-patterns
description: Canonical patterns for go.Choroplethmap tile-based maps — background control, valid styles, and failure modes
---

# Choropleth Map Patterns (`go.Choroplethmap`)

## Critical Architecture Fact

`go.Choroplethmap` renders on a **tile-based map canvas**, not a standard Plotly canvas.

- `paper_bgcolor` and `plot_bgcolor` style the HTML container **only** — they have zero effect on the map tile area.
- The map background **is** the tile layer. To control it, you control the map style and/or inject a fill layer.

Do not attempt to change map background via `paper_bgcolor`/`plot_bgcolor` alone. It will not work.

---

## Pattern 1: Solid Dark Background (Recommended)

Use `white-bg` style (renders no tiles — blank canvas) with a GeoJSON fill layer painted over it.

```python
fig.update_layout(
    map={
        'style': 'white-bg',
        'center': {'lat': 43.70, 'lon': -79.375},
        'zoom': 10,
        'bearing': -17,
        'layers': [{
            'below': 'traces',
            'sourcetype': 'geojson',
            'source': {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-180, -90], [180, -90],
                            [180, 90], [-180, 90], [-180, -90]
                        ]]
                    },
                    "properties": {}
                }]
            },
            'type': 'fill',
            'color': '#000000',   # ← change this to any solid color
            'opacity': 1.0,
        }],
    },
    paper_bgcolor='#000000',   # styles the outer container only
    plot_bgcolor='#000000',
)
```

**Why this works:** `white-bg` suppresses all tile rendering. The world-polygon fill layer paints the canvas. Choropleth data renders on top via `below: 'traces'`.

---

## Pattern 2: Transparent Background

Use `white-bg` with no fill layer. The map area becomes transparent, revealing whatever is behind the Plotly component (notebook cell background, Dash layout background, etc.).

```python
fig.update_layout(
    map={
        'style': 'white-bg',
        'center': {'lat': 43.70, 'lon': -79.375},
        'zoom': 10,
        'bearing': -17,
        # No 'layers' key — no fill layer
    },
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
```

---

## Pattern 3: Standard Tile Map (Light)

Use when you want a real street/terrain base map visible behind the choropleth.

```python
fig.update_layout(
    map={
        'style': 'open-street-map',   # reliable, no token required
        'center': {'lat': 43.70, 'lon': -79.375},
        'zoom': 10,
    },
)
```

---

## Valid Map Styles (Current Plotly — No Token Required)

| Style | Description |
|-------|-------------|
| `white-bg` | Blank canvas — no tiles. Use for custom backgrounds via fill layer. |
| `open-street-map` | Full street map — light background. Reliable. |
| `carto-positron` | Minimal light map. |
| `carto-positron-nolabels` | Minimal light, no labels. |
| `carto-darkmatter` | Dark map tiles. |
| `carto-darkmatter-nolabels` | Dark map, no labels. |

## Dead / Broken Styles — Never Use

| Style | Reason |
|-------|--------|
| `stamen-toner` | Stamen tile service shut down — renders blank. |
| `stamen-toner-background` | Same — dead. |
| `stamen-terrain` | Same — dead. |
| `carto-voyager` | Unreliable in current Plotly versions. |

---

## Common Failure Modes

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Map disappears entirely | Switched to a dead/broken tile style | Use `open-street-map` or `white-bg` |
| Background is wrong color despite setting `paper_bgcolor` | `paper_bgcolor` doesn't affect tile canvas | Use Pattern 1 (fill layer) or Pattern 2 (transparent) |
| Background is blue (water) | Using a tile style with ocean rendering | Switch to `white-bg` + fill layer |
| Choropleth invisible after style change | Fill layer `below: 'traces'` missing or set wrong | Ensure `'below': 'traces'` in the layers config |
| Dark map but data looks washed out | Map tile style is dark AND choropleth opacity is low | Set `marker.opacity` to 0.8–1.0 |

---

## Colorbar Transparency

The built-in Plotly colorbar background is controlled via `colorbar.bgcolor`:

```python
colorbar={
    'bgcolor': 'rgba(0,0,0,0)',   # transparent
    ...
}
```

This is independent of the map background. Both can be set independently.

---

## Integration with Notebook Design System

This skill extends `notebook-design-system`. Color values (`COLORS['seq_low']`, etc.) from that design system apply here. Use `COLORS` tokens for `fill.color`, `paper_bgcolor`, and `marker.line.color` — never hardcode hex values that duplicate design tokens.
