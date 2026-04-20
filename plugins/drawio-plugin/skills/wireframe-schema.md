# Skill: wireframe-schema

## When to Load

Load this skill when:
- Running `/drawio parse` — defines the output format to write
- Reviewing a `WIREFRAME.md` file — defines what the fields mean
- Passing wireframe context to dmc-design — defines the contract

---

## Overview

`WIREFRAME.md` is the contract between `drawio-plugin` (producer) and `dmc-design` (consumer).
It is a human-readable, Claude-readable spec that captures the component hierarchy and
implementation notes from a `.drawio` wireframe file.

**Output location:** Same directory as the source `.drawio` file.
**Conventional location for app projects:** `docs/design/WIREFRAME.md`
**Consumer:** dmc-design uses this as the upstream input for DMC scaffolding.

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
    - {component-class} [id={component-id}] — {label}{instructions block}{style block}{callbacks block}{db-binding block}

## Page: {page-slug}
### AppShellMain
  ### content-page
    [component tree with indentation reflecting parent chain]
    - {component-class} [id={component-id}] — {label}{instructions block}{style block}{callbacks block}{db-binding block}
```

---

## Schema Rules

### Component Line Format

Each component line follows this structure:

```
- {component-class} [id={component-id}] [order={component-order}] — {label}{instructions block}{style block}{callbacks block}{db-binding block}
```

**Field rules:**
- `[id=...]` — omit entirely if no `component-id` on the `<object>`
- `[order=...]` — omit entirely if no `component-order`
- `— {label}` — always present; use `(no label)` if `label=""` and component is not a structural wrapper
- `{instructions block}` — rendered as `  → {component-instructions}` on the same line, only if `component-instructions` is non-empty
- `{style block}` — only if any style signal differs from default (see below)
- `{callbacks block}` — only if `callback-in` or `callback-out` present
- `{db-binding block}` — only if `db-binding` present

### Instructions Block

Append to the component line when `component-instructions` is non-empty:
```
  → {component-instructions}
```

### Style Signals Block

Append when any signal differs from default. Format as inline key=value pairs:
```
  [withBorder=false] [opacity=0.8] [rounded=true]
```

Only include signals that are non-default:
- `withBorder=false` — only when border is off (`strokeColor=none`)
- `opacity={float}` — only when not 1.0
- `rounded=true` — only when rounded

### Callbacks Block

When `callback-in` or `callback-out` is present, append after style block:
```
  ← {callback-in[0]}, {callback-in[1]} ({callback-in-details})
  → {callback-out[0]}, {callback-out[1]} ({callback-out-details})
```

Use `←` for inputs (callbacks this component reacts to) and `→` for outputs (callbacks this component triggers).
Omit the details parenthetical if `callback-in-details` / `callback-out-details` is empty.

### Data Binding Block

When `db-binding` is present, append:
```
  ⊕ {db-binding}
```

### Component Tree Visualization

After the per-layer component listing, include a component tree showing Dash parent-child
relationships derived from `component-parent-id`. Only include components that have explicit
`component-id` values:

```
### Component Tree
app-shell
└── nav-paper
    └── nav-stack
        ├── nav-home
        ├── nav-projects
        └── nav-about
home-content
└── home-filters
    ├── home-filters-date
    └── home-filters-region
└── home-chart
```

### What is NOT Included

- Geometry (x, y, width, height) — this is a component spec, not a pixel spec
- Internal draw.io IDs — only `component-id` from the `<object>` attributes
- Style attributes beyond the three semantic signals (withBorder, opacity, rounded)

### DMC Domain File Detection

Before building the `## DMC Domain Files Required` section:

1. List all `dmc-*.txt` files in `references/dmc/` to discover what is available.
2. Scan all `component-class` attribute values across all pages.
3. Apply these rules, but only include files that actually exist in `references/dmc/`:

| If any component matches... | Include this file |
|---|---|
| Always | `dmc-layout.txt` |
| Always | `dmc-ui.txt` |
| `Chart`, `AreaChart`, `BarChart`, `LineChart`, `DonutChart`, `PieChart`, `RadarChart`, `SparklineChart` | `dmc-charts.txt` |
| `Alert`, `Modal`, `Drawer`, `Notification`, `LoadingOverlay`, `Skeleton`, `Progress` | `dmc-feedback.txt` |
| `MantineProvider`, `ColorSchemeScript`, `theme` | `dmc-theme.txt` |

Any `dmc-*.txt` file present in `references/dmc/` but not matched by the rules above
should be omitted — only declare what the wireframe's components actually require.

### Shared Layout

Components on `app-shell` (root layer) and all `content-{region}` layers except `content-page`
are identical across all pages. Write them once under `## Shared Layout (all pages)`.
Do NOT repeat per page.

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
    - Paper — (no label)  → padding=0, radius=0  [withBorder=false]
      - Stack — (no label)  → gap=0  [withBorder=false]
        - NavLink [id=nav-home] — Home  → active page indicator  → nav-active (set active=home)
        - NavLink [id=nav-toronto] — Toronto Projects  → nav-active (set active=toronto)
        - NavLink [id=nav-about] — About  → nav-active (set active=about)

## Page: home
### AppShellMain
  ### content-page
    - Title [id=home-title] [order=1] — Welcome  [withBorder=false]
    - Text [id=home-subtitle] [order=2] — Portfolio of work  [withBorder=false]
    - Grid [id=home-grid] [order=3] — (no label)  → gap=md
      - GridCol — (no label)  → span=6
        - AreaChart [id=home-activity-chart] — Activity  → use mock data for now  ⊕ activity_log.timestamp

### Component Tree
home-title
home-subtitle
home-grid
  (no component-id children declared)

## Page: projects-toronto
### AppShellMain
  ### content-page
    - Stack [id=toronto-stack] — (no label)  → gap=md
      - Title [id=toronto-title] [order=1] — Toronto Projects  [withBorder=false]
      - Grid [id=toronto-grid] [order=2] — (no label)
        - GridCol — (no label)  → span=4, repeat 3 times
          - Card [id=toronto-card] — (no label)  → clickable=true  ← toronto-filter (filter cards by tag)

### Component Tree
toronto-stack
├── toronto-title
├── toronto-grid
│   └── toronto-card

## Page: about
### AppShellMain
  ### content-page
    - Stack — (no label)  → gap=xl  [withBorder=false]
      - Title — About  [withBorder=false]
      - Text — Bio text here
```
