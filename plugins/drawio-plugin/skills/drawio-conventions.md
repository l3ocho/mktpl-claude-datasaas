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

## Layer Convention

Every draw.io page (`<diagram>`) contains exactly these layers, in this order:

| Layer `value` attribute | `locked` | Contains |
|---|---|---|
| *(root — no `value` attribute, `id="1"`)* | `locked=1` | `AppShell` only — full-canvas wrapper |
| `layout` | `locked=1` | `AppShellNavbar` and `AppShellMain` structural regions only |
| `content-navbar` | `locked=1` | Navbar content group tree (Paper → Stack → NavLink items) |
| `content-pages` or `content-page` | `locked=0` | All page-specific components |

**Critical rule:** `AppShell` lives on the **root layer** (`parent="1"`), NOT inside `layout`.
The `layout` layer contains only `AppShellNavbar` and `AppShellMain` — the structural shells.
`AppShell` is the canvas-level wrapper; layout regions sit inside it.

### Layer XML Structure

Layers are `<mxCell>` elements with `vertex=1` and a `value` attribute at the top of the page XML.
The root layer always has `id="1"` and no meaningful `value`.

```xml
<!-- Root layer — contains AppShell -->
<mxCell id="1" value="" style="..." vertex="1" parent="0"/>

<!-- layout layer — contains AppShellNavbar and AppShellMain -->
<mxCell id="layer_layout" value="layout" style="locked=1;..." vertex="1" parent="0"/>

<!-- content-navbar layer — contains navbar component tree -->
<mxCell id="layer_navbar" value="content-navbar" style="locked=1;..." vertex="1" parent="0"/>

<!-- content-page layer — contains page-specific components -->
<mxCell id="layer_content" value="content-page" style="locked=0;..." vertex="1" parent="0"/>
```

---

## Object Attribute Convention

Every component in the wireframe is an `<object>` element wrapping an `<mxCell>`.
All five attributes below are recognized. Three are always required.

| Attribute | Required | Purpose |
|---|---|---|
| `component` | **Yes** | DMC class name (e.g. `AppShell`, `Paper`, `NavLink`, `Button`, `Grid`) |
| `label` | **Yes** | Display text / content. Use empty string `""` for purely structural wrappers |
| `instructions` | **Yes** | Implementation notes for Claude Code. Use `""` if nothing to note — **never omit** |
| `id` | No | Dash component `id` prop — used for callback wiring |
| `css_id` | No | CSS selector id — distinct from `id` when both stylesheet and callback targeting are needed |

### Object XML Structure

```xml
<object component="Paper" label="" instructions="navbar container, padding=0" id="navbar-paper" css_id="navbar-wrapper">
  <mxCell vertex="1" parent="layer_navbar" ...>
    <mxGeometry x="0" y="0" width="240" height="800" as="geometry"/>
  </mxCell>
</object>
```

`id` and `css_id` are **optional** — omit them entirely when not needed.
`component`, `label`, and `instructions` are always present (even if `""` for the last two).

---

## Parent Chain / Containment

Containment hierarchy is determined by the `parent` attribute on `<mxCell>`:

- `parent="1"` → element is in the root layer (only `AppShell` should be here)
- `parent="layer_layout"` → element is a direct child of the `layout` layer
- `parent="group_id"` → element is nested inside a group with that id
- Groups are `<mxCell>` elements with `vertex=1` and no `value` attribute (or a label-only value)

When parsing: walk the parent chain to reconstruct the component tree.
When generating: assign correct `parent` values to reflect intended nesting.

---

## Page Convention

- One `<diagram>` per view/route
- Page `name` attribute = route slug (e.g. `home`, `about`, `projects-toronto`)
- Every page repeats the `layout` and `content-navbar` layers (shared shell)
- Each page has its own `content-page` (or `content-pages`) layer for unique content
- Page title displayed in the app is a separate concern from the slug

---

## Minimal Worked Example

A single page with layout + navbar + one content element:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile>
  <diagram name="home">
    <mxGraphModel>
      <root>
        <!-- Root layer -->
        <mxCell id="0"/>
        <mxCell id="1" value="" style="..." vertex="1" parent="0"/>

        <!-- AppShell on root layer -->
        <object component="AppShell" label="" instructions="" >
          <mxCell id="appshell_1" vertex="1" parent="1" style="...">
            <mxGeometry x="0" y="0" width="1440" height="900" as="geometry"/>
          </mxCell>
        </object>

        <!-- layout layer -->
        <mxCell id="layer_layout" value="layout" style="locked=1;" vertex="1" parent="0"/>

        <!-- AppShellNavbar in layout layer -->
        <object component="AppShellNavbar" label="" instructions="width=240">
          <mxCell id="navbar_shell" vertex="1" parent="layer_layout" style="...">
            <mxGeometry x="0" y="0" width="240" height="900" as="geometry"/>
          </mxCell>
        </object>

        <!-- AppShellMain in layout layer -->
        <object component="AppShellMain" label="" instructions="">
          <mxCell id="main_shell" vertex="1" parent="layer_layout" style="...">
            <mxGeometry x="240" y="0" width="1200" height="900" as="geometry"/>
          </mxCell>
        </object>

        <!-- content-navbar layer -->
        <mxCell id="layer_navbar" value="content-navbar" style="locked=1;" vertex="1" parent="0"/>

        <!-- Navbar content: Paper → Stack → NavLink items -->
        <object component="Paper" label="" instructions="padding=0, radius=0">
          <mxCell id="paper_nav" vertex="1" parent="layer_navbar" style="...">
            <mxGeometry x="0" y="0" width="240" height="900" as="geometry"/>
          </mxCell>
        </object>

        <object component="Stack" label="" instructions="gap=0">
          <mxCell id="stack_nav" vertex="1" parent="paper_nav" style="...">
            <mxGeometry x="0" y="60" width="240" height="400" as="geometry"/>
          </mxCell>
        </object>

        <object component="NavLink" label="Home" instructions="" id="nav-home">
          <mxCell id="navlink_home" vertex="1" parent="stack_nav" style="...">
            <mxGeometry x="0" y="0" width="240" height="44" as="geometry"/>
          </mxCell>
        </object>

        <!-- content-page layer -->
        <mxCell id="layer_content" value="content-page" style="locked=0;" vertex="1" parent="0"/>

        <!-- Page-specific content -->
        <object component="Title" label="Welcome" instructions="order=1" id="home-title">
          <mxCell id="title_home" vertex="1" parent="layer_content" style="...">
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
2. Extract `component`, `label`, `instructions`, `id`, `css_id` from the `<object>` attributes
3. Resolve parent chain: follow `<mxCell parent="...">` up to the layer root
4. Determine layer membership: root → AppShell, `layout` → structural, `content-navbar` → navbar tree, `content-page/s` → page content
5. Skip elements with missing `component` attribute (warn, continue)
6. Do NOT infer from geometry — use the explicit parent chain only

## Generation Rules

1. Always produce a valid `<mxfile>` with one `<diagram>` per page
2. Follow layer order: root → layout → content-navbar → content-page
3. `AppShell` parent is always `"1"` (root layer cell id)
4. `AppShellNavbar` and `AppShellMain` parent is the `layout` layer cell id
5. Always include `component`, `label`, and `instructions` on every `<object>`
6. Omit `id` and `css_id` unless the user specifies them
7. Use realistic `mxGeometry` values (AppShell full canvas, navbar 240px wide, etc.)
