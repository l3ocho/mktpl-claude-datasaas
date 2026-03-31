# Skill: drawio-conventions

## When to Load

Load this skill whenever:
- Parsing a `.drawio` XML file (`/drawio parse`)
- Generating `.drawio` XML from a description (`/drawio generate`)
- Answering questions about the draw.io XML structure used in this project

---

## Overview

Leo's projects use draw.io wireframes with a strict layer/group/attribute convention.
All `.drawio` files follow this schema exactly — no exceptions, no spatial inference.
Containment is expressed purely through the `parent` attribute chain in XML.

---

## Page Convention

- One `<diagram>` per view/route (tab = page)
- Page `name` attribute = route slug (e.g. `home`, `about`, `projects-toronto`)
- The AppShell and all region containers repeat identically on every tab
- Only `content-page` varies per tab — this is the only layer that differs across pages
- Page title displayed in the app is a separate concern from the slug

---

## Layer Convention

Every draw.io page (`<diagram>`) contains these layers. Only `app-shell` (root) and
`content-page` are mandatory. All other layers are project-dependent.

| Layer `value` attribute | `locked` | Required | Contains |
|---|---|---|---|
| *(root — `id="1"`, no `value` attribute)* → `app-shell` | `locked=1` | **Always** | `AppShell` + all `AppShell*` region containers (`AppShellNavbar`, `AppShellMain`, `AppShellHeader`, `AppShellFooter`, `AppShellAside`) |
| `content-navbar` | `locked=1` | If navbar exists | Navbar content group tree (Paper → Stack → NavLink items) |
| `content-header` | `locked=1` | If header exists | Header internals |
| `content-footer` | `locked=1` | If footer exists | Footer internals |
| `content-aside` | `locked=1` | If aside exists | Aside internals |
| `content-page` | `locked=0` | **Always** | Page-specific components. Groups within for logical sections (forms, tables, charts) — not sub-layers |

**Critical rule:** The root layer (`id="1"`) is the `app-shell`. It contains `AppShell` and ALL
`AppShell*` structural region containers directly. There is no separate `layout` layer.

Any layer whose `value` starts with `content-` is a content layer. Parser must detect which
`content-{region}` layers exist — they are project-dependent.

### Layer XML Structure

Layers are `<mxCell>` elements with `vertex=1` at the top of the page XML.
The root layer always has `id="1"` and no `value` (or `value=""`).

```xml
<!-- Root layer (app-shell) — contains AppShell + all region containers -->
<mxCell id="1" value="" style="locked=1;..." vertex="1" parent="0"/>

<!-- content-navbar layer — contains navbar component tree (if navbar exists) -->
<mxCell id="layer_navbar" value="content-navbar" style="locked=1;..." vertex="1" parent="0"/>

<!-- content-header layer (if header exists) -->
<mxCell id="layer_header" value="content-header" style="locked=1;..." vertex="1" parent="0"/>

<!-- content-footer layer (if footer exists) -->
<mxCell id="layer_footer" value="content-footer" style="locked=1;..." vertex="1" parent="0"/>

<!-- content-aside layer (if aside exists) -->
<mxCell id="layer_aside" value="content-aside" style="locked=1;..." vertex="1" parent="0"/>

<!-- content-page layer — contains page-specific components -->
<mxCell id="layer_content" value="content-page" style="locked=0;..." vertex="1" parent="0"/>
```

---

## Object Attribute Convention

Every component in the wireframe is an `<object>` element wrapping an `<mxCell>`.

### Frontend Component Attributes

| Attribute | Required | Purpose |
|---|---|---|
| `component-class` | **Yes** | DMC class name (e.g. `AppShell`, `Paper`, `NavLink`, `Button`, `Grid`) |
| `label` | **Yes** | Display text / content. Parser interprets per DMC class. Use `""` for purely structural wrappers |
| `component-id` | No | Dash component `id` prop — used for callback wiring and CSS selection. Two-segment: `{prefix}-{descriptor}` |
| `component-parent-id` | No | Parent component's `component-id` in the Dash component tree (for explicit tree relationships) |
| `component-instructions` | No | Implementation notes for Claude Code. Omit if nothing to note |
| `component-order` | No | Integer ordering within parent or group |

### Frontend Callback Attributes

| Attribute | Required | Purpose |
|---|---|---|
| `callback-in` | No | Comma-separated callback names that trigger an action on this component |
| `callback-in-details` | No | Behavior instructions when the callback triggers |
| `callback-out` | No | Comma-separated callback names this component triggers |
| `callback-out-details` | No | Behavior instructions when this component triggers its callbacks |

### Data Binding Attributes

| Attribute | Required | Purpose |
|---|---|---|
| `db-binding` | No | Database column this component is bound to. Format: `table_name.column_name` |

### Draw.io Native Attributes (kept as-is)

| Attribute | Purpose |
|---|---|
| `label` | Display text — draw.io native, always present. Parser interprets meaning per `component-class` |
| `id` | Structural cell ID — draw.io native. Do not use for Dash IDs (use `component-id` instead) |

### Dropped Attributes

The following attributes from v1.0.0 are no longer valid:

| Old Attribute | Replacement | Notes |
|---|---|---|
| `component` | `component-class` | Renamed |
| `instructions` | `component-instructions` | Renamed |
| `dash_id` | `component-id` | Renamed |
| `css_id` | *(dropped)* | Dash `component-id` serves as CSS selector |
| `component-children` | *(dropped)* | Derivable from `component-parent-id` references |

### Object XML Structure

```xml
<object component-class="Button" label="Submit"
        component-id="dashboard-submit"
        component-parent-id="dashboard-form"
        component-instructions="primary variant, full width"
        component-order="3"
        callback-out="submit-form"
        callback-out-details="POST /api/data on click, show LoadingOverlay while pending"
        db-binding="submissions.status">
  <mxCell vertex="1" parent="layer_content" style="rounded=1;opacity=100;strokeColor=#1c7ed6;">
    <mxGeometry x="40" y="200" width="120" height="36" as="geometry"/>
  </mxCell>
</object>
```

Omit any optional attribute entirely when not needed — do not include empty strings for optional fields.
`component-class` and `label` are always present (even if `label=""` for structural wrappers).

---

## Component ID Naming Convention

`component-id` follows a two-segment `{prefix}-{descriptor}` convention:

| Region | Prefix | Example |
|---|---|---|
| AppShell regions | `app-` | `app-shell`, `app-navbar` |
| Navbar | `nav-` | `nav-home`, `nav-about` |
| Header | `hdr-` | `hdr-title`, `hdr-search` |
| Footer | `ftr-` | `ftr-links`, `ftr-copyright` |
| Aside | `aside-` | `aside-toc`, `aside-filters` |
| Page content | `{page-slug}-` | `home-title`, `toronto-chart` |

Max **three segments** for grouped sections: `dashboard-filters-date`, `home-hero-cta`.

Warn (do not fail) if a `component-id` does not follow this convention.

---

## Style Property Signals

The parser reads three semantic signals from the `mxCell style` string.
These override default DMC behavior — include them in WIREFRAME.md output when non-default.

| Style Property | Signal | Default |
|---|---|---|
| `strokeColor=none` | `withBorder: false` | Default: `true` (border on) |
| `strokeColor=<any value>` | `withBorder: true` | Default: `true` |
| `opacity=<0-100>` | Convert to 0.0–1.0 float → DMC `opacity` prop | Default: `1.0` (100) |
| `rounded=1` | `rounded: true` | Default: `false` |
| `rounded=0` | `rounded: false` | Default: `false` |

**Important:** `arcSize` is ignored — `rounded` is boolean only. Radius comes from the design system.

Style string example:
```
style="rounded=1;opacity=80;strokeColor=none;fillColor=#ffffff;..."
```
Extracts: `withBorder: false`, `opacity: 0.8`, `rounded: true`

Only include style signals in WIREFRAME.md output when they differ from defaults.

---

## Parent Chain / Containment

Containment hierarchy is determined by the `parent` attribute on `<mxCell>`:

- `parent="1"` → element is on the root/app-shell layer
- `parent="layer_navbar"` → element is a direct child of the `content-navbar` layer
- `parent="group_id"` → element is nested inside a group with that id
- Groups within `content-page` are used for logical sections (forms, tables, charts)

When parsing: walk the parent chain to reconstruct the component tree.
When generating: assign correct `parent` values to reflect intended nesting.
The `component-parent-id` attribute expresses Dash tree relationships explicitly;
the XML `parent` chain expresses draw.io visual containment.

---

## Minimal Worked Example

A single page with AppShell + navbar + one content element:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile>
  <diagram name="home">
    <mxGraphModel>
      <root>
        <!-- Root cell (required by draw.io) -->
        <mxCell id="0"/>

        <!-- Root layer (app-shell) — AppShell + region containers -->
        <mxCell id="1" value="" style="locked=1;" vertex="1" parent="0"/>

        <!-- AppShell on root layer -->
        <object component-class="AppShell" label="">
          <mxCell id="appshell_1" vertex="1" parent="1" style="strokeColor=#dee2e6;">
            <mxGeometry x="0" y="0" width="1440" height="900" as="geometry"/>
          </mxCell>
        </object>

        <!-- AppShellNavbar on root layer -->
        <object component-class="AppShellNavbar" label=""
                component-instructions="width=240">
          <mxCell id="navbar_shell" vertex="1" parent="1" style="strokeColor=#dee2e6;">
            <mxGeometry x="0" y="0" width="240" height="900" as="geometry"/>
          </mxCell>
        </object>

        <!-- AppShellMain on root layer -->
        <object component-class="AppShellMain" label="">
          <mxCell id="main_shell" vertex="1" parent="1" style="strokeColor=#dee2e6;">
            <mxGeometry x="240" y="0" width="1200" height="900" as="geometry"/>
          </mxCell>
        </object>

        <!-- content-navbar layer -->
        <mxCell id="layer_navbar" value="content-navbar" style="locked=1;" vertex="1" parent="0"/>

        <!-- Navbar content: Paper → Stack → NavLink items -->
        <object component-class="Paper" label=""
                component-instructions="padding=0, radius=0">
          <mxCell id="paper_nav" vertex="1" parent="layer_navbar" style="strokeColor=none;">
            <mxGeometry x="0" y="0" width="240" height="900" as="geometry"/>
          </mxCell>
        </object>

        <object component-class="Stack" label=""
                component-instructions="gap=0">
          <mxCell id="stack_nav" vertex="1" parent="paper_nav" style="strokeColor=none;">
            <mxGeometry x="0" y="60" width="240" height="400" as="geometry"/>
          </mxCell>
        </object>

        <object component-class="NavLink" label="Home"
                component-id="nav-home"
                callback-out="nav-active"
                callback-out-details="set active page to home">
          <mxCell id="navlink_home" vertex="1" parent="stack_nav" style="rounded=0;strokeColor=none;">
            <mxGeometry x="0" y="0" width="240" height="44" as="geometry"/>
          </mxCell>
        </object>

        <!-- content-page layer -->
        <mxCell id="layer_content" value="content-page" style="locked=0;" vertex="1" parent="0"/>

        <!-- Page-specific content -->
        <object component-class="Title" label="Welcome"
                component-id="home-title"
                component-order="1">
          <mxCell id="title_home" vertex="1" parent="layer_content" style="strokeColor=none;">
            <mxGeometry x="40" y="40" width="600" height="48" as="geometry"/>
          </mxCell>
        </object>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## Parsing Rules

1. Walk all `<object>` elements in page order
2. Extract attributes from each `<object>`:
   - `component-class` — required; warn and skip if missing: `Warning: <object> at id={id} missing component-class — skipped`
   - `label` — required but may be `""`
   - `component-id` — optional; if present, validate naming convention (warn if invalid, do not fail)
   - `component-parent-id` — optional; use to build explicit Dash parent-child tree
   - `component-instructions` — optional
   - `component-order` — optional integer
   - `callback-in`, `callback-in-details`, `callback-out`, `callback-out-details` — optional; split `callback-in` and `callback-out` on commas into lists
   - `db-binding` — optional; expected format `table_name.column_name`
3. Extract style signals from the `<mxCell style="...">` string:
   - `strokeColor`: `none` → `withBorder=false`, any other value → `withBorder=true`
   - `opacity`: convert `0–100` integer to `0.0–1.0` float
   - `rounded`: `1` → `true`, `0` → `false`. Ignore `arcSize`.
   - Only record signals that differ from defaults (border on, opacity 1.0, not rounded)
4. Resolve parent chain: follow `<mxCell parent="...">` up to the layer root
5. Determine layer membership:
   - Root (`id="1"`) → app-shell (AppShell + region containers)
   - `value` starts with `content-` → content layer for that region
   - `content-page` (or starts with `content-page`) → page-specific content
6. Do NOT infer from geometry — use explicit parent chain only

## Generation Rules

1. Always produce a valid `<mxfile>` with one `<diagram>` per page
2. Follow layer order: root (app-shell) → content-navbar → [content-header] → [content-footer] → [content-aside] → content-page
3. `AppShell` and all `AppShell*` region containers have `parent="1"` (root layer)
4. Only include `content-{region}` layers that exist in the project
5. Always include `component-class` and `label` on every `<object>`
6. Include `component-id` when the component participates in callbacks or needs CSS targeting
7. Include `component-instructions` only when there are meaningful implementation notes
8. Include callback attributes only when callbacks are specified
9. Use realistic `mxGeometry` values (AppShell full canvas, navbar 240px wide, etc.)
