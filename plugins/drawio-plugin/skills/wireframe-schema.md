# Skill: wireframe-schema

## When to Load

Load this skill when:
- Running `/drawio parse` — defines the output format to write
- Reviewing a `WIREFRAME.md` file — defines what the fields mean
- Passing wireframe context to viz-platform — defines the contract

---

## Overview

`WIREFRAME.md` is the contract between `drawio-plugin` (producer) and `viz-platform` (consumer).
It is a human-readable, Claude-readable spec that captures the component hierarchy and
implementation notes from a `.drawio` wireframe file.

**Output location:** Same directory as the source `.drawio` file.
**Conventional location for app projects:** `docs/design/WIREFRAME.md`
**Consumer:** viz-platform uses this as the upstream input for DMC scaffolding.

---

## WIREFRAME.md Schema

```markdown
# Wireframe Spec: {project-name}

Generated: {ISO 8601 timestamp}
Source: {drawio_file_path}

## DMC Domain Files Required
- dmc-layout.txt     ← always included
- dmc-ui.txt         ← always included
- dmc-charts.txt     ← only if Chart/AreaChart/BarChart/LineChart component found
- dmc-feedback.txt   ← only if Alert/Modal/Notification/Drawer/LoadingOverlay found
- dmc-theme.txt      ← only if MantineProvider or theme-config component found

## Pages
- {page-slug}: {page display name or slug}
- ...

## Shared Layout (all pages)
### AppShell
  navbar_width: {px from mxGeometry width of AppShellNavbar}
  main_width: {px from mxGeometry width of AppShellMain}
  ### AppShellNavbar
    [component tree with indentation reflecting parent chain]
    - {component} [id={id}] [css_id={css_id}] — {label} — {instructions}

## Page: {page-slug}
### AppShellMain
  ### {layer: content-page}
    [component tree with indentation reflecting parent chain]
    - {component} [id={id}] [css_id={css_id}] — {label} — {instructions}
```

---

## Schema Rules

### Component Tree Formatting

- Indentation depth reflects the XML `parent` chain, not visual position
- Each component line: `- {component} [id={id}] [css_id={css_id}] — {label} — {instructions}`
- `[id=...]` is omitted entirely if no `id` attribute on the `<object>`
- `[css_id=...]` is omitted entirely if no `css_id` attribute
- `instructions` text is preserved verbatim — these are notes for Claude Code
- If both `label` and `instructions` are empty strings, render as: `- {component} — (no label) — (no instructions)`

### What is NOT Included

- Geometry (x, y, width, height) — this is a component spec, not a pixel spec
- Style attributes — draw.io visual styling is irrelevant to DMC scaffolding
- Internal draw.io IDs — only `id` and `css_id` from the `<object>` attributes

### DMC Domain File Detection

Scan all `component` attribute values across all pages. Apply these rules:

| If any component matches... | Include this file |
|---|---|
| Always | `dmc-layout.txt` |
| Always | `dmc-ui.txt` |
| `Chart`, `AreaChart`, `BarChart`, `LineChart`, `DonutChart`, `PieChart`, `RadarChart`, `SparklineChart` | `dmc-charts.txt` |
| `Alert`, `Modal`, `Drawer`, `Notification`, `LoadingOverlay`, `Skeleton`, `Progress` | `dmc-feedback.txt` |
| `MantineProvider`, `ColorSchemeScript`, `theme` | `dmc-theme.txt` |

### Shared Layout

Components on `layout` and `content-navbar` layers are identical across all pages.
Write them once under `## Shared Layout (all pages)` — do NOT repeat per page.

### Pages with No content-page Layer

If a page has no `content-page` layer, note it:
```markdown
## Page: {page-slug}
### AppShellMain
  (no content-page layer found)
```
Still parse and output the shared layout sections.

---

## Example Output

```markdown
# Wireframe Spec: personal-portfolio

Generated: 2026-03-15T10:30:00Z
Source: docs/design/portfolio.drawio

## DMC Domain Files Required
- dmc-layout.txt
- dmc-ui.txt
- dmc-charts.txt

## Pages
- home: home
- projects-toronto: projects-toronto
- about: about

## Shared Layout (all pages)
### AppShell
  navbar_width: 240
  main_width: 1200
  ### AppShellNavbar
    - Paper — — padding=0, radius=0
      - Stack — — gap=0
        - NavLink [id=nav-home] — Home —
        - NavLink [id=nav-toronto] — Toronto Projects —
        - NavLink [id=nav-about] — About —

## Page: home
### AppShellMain
  ### content-page
    - Title [id=home-title] — Welcome —
    - Text — Portfolio of work —
    - Grid — —
      - GridCol — — span=6
        - AreaChart [id=chart-activity] — Activity — use mock data for now

## Page: projects-toronto
### AppShellMain
  ### content-page
    - Stack — — gap=md
      - Title [id=toronto-title] — Toronto Projects —
      - Grid — —
        - GridCol — — span=4, repeat 3 times
          - Card [id=project-card] — — clickable=true

## Page: about
### AppShellMain
  ### content-page
    - Stack — — gap=xl
      - Title — About —
      - Text — Bio text here —
```
