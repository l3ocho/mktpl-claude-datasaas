---
name: drawio-generate
description: Generate .drawio XML from a natural language UI description following DMC layer conventions
---

# /drawio generate

Generate a valid `.drawio` XML file from a natural language description of a UI.
Output follows Leo's established layer/group/attribute conventions exactly.

## Usage

```
/drawio generate {description} [--pages page1,page2,...] [--output path/to/output.drawio]
```

## Parameters

| Parameter | Required | Description |
|---|---|---|
| `description` | Yes | Natural language description of the UI to generate |
| `--pages` | No | Comma-separated list of page slugs to generate (default: inferred from description) |
| `--output` | No | Output file path. If omitted, Claude will prompt for it. |

---

## Execution Flow

### Step 1 — Load Skill

Load `skills/drawio-conventions.md` before proceeding.

### Step 2 — Parse Description

Analyze `{description}` to identify:

- **Pages needed:** Explicit (`--pages`) or inferred from description (e.g., "a home page and an about page" → `home`, `about`)
- **Layout type:** Default to AppShell. Determine which regions exist (navbar, header, footer, aside) from description.
- **Navbar items:** Extract any navigation items mentioned (e.g., "with links to Home, Projects, About")
- **Per-page components:** Group described components by page
- **Callbacks:** Note any interaction descriptions that imply callback relationships

If description is too vague to determine pages, default to a single page named `home`.

### Step 3 — Generate XML

For each page, generate XML following the layer/group/attribute conventions exactly.

#### XML Structure Per Page

Every `<diagram>` must contain these layers in this order. Only generate `content-{region}` layers
that exist in this project's layout:

**Root layer (`id="1"`, app-shell):**
- `<object component-class="AppShell">` with:
  - `label=""`
  - `<mxGeometry x="0" y="0" width="1440" height="900"/>`
- `<object component-class="AppShellNavbar">` (if navbar): `component-instructions="width=240"` (default)
- `<object component-class="AppShellMain">` always present
- `<object component-class="AppShellHeader">` (if header exists)
- `<object component-class="AppShellFooter">` (if footer exists)
- `<object component-class="AppShellAside">` (if aside exists)
- All region containers parented to `id="1"` (root layer)

**`content-navbar` layer (`value="content-navbar"`, `locked=1`)** — if navbar exists:
- Standard navbar structure:
  ```
  Paper (component-instructions="padding=0, radius=0") → Stack (component-instructions="gap=0") → NavLink items
  ```
- Each NavLink: `label="{nav item name}"`, `component-id="nav-{slug}"`, no callbacks unless user specified

**`content-header` layer** — if header exists (locked=1)

**`content-footer` layer** — if footer exists (locked=1)

**`content-aside` layer** — if aside exists (locked=1)

**`content-page` layer (`value="content-page"`, `locked=0`):**
- Components described for this page
- Reasonable component choices based on description:
  - Text content → `Title`, `Text`
  - Data display → `Table`, `Card`, `Grid`
  - User input → `TextInput`, `Select`, `Button`
  - Charts/graphs → `AreaChart`, `BarChart`, `LineChart` (or note: "use dcc.Graph with Plotly figure")
  - Layout grouping → `Stack`, `Group`, `Grid` / `GridCol`
- Use groups within `content-page` for logical sections (forms, tables, charts) — not sub-layers

#### Attribute Convention

Every `<object>` element MUST have:
- `component-class` — the DMC class name
- `label` — display text, or `""` for structural wrappers

Include when relevant:
- `component-id` — when the component participates in callbacks or needs CSS targeting. Follow `{prefix}-{descriptor}` naming.
- `component-instructions` — when there are meaningful implementation notes. Omit entirely if nothing to note.
- `component-order` — when ordering within a parent matters
- `callback-out` / `callback-out-details` — when the component triggers actions
- `callback-in` / `callback-in-details` — when the component reacts to callbacks
- `db-binding` — when the component is bound to a database column (`table_name.column_name`)

**Do NOT generate:** `component`, `instructions`, `dash_id`, `css_id` — these are old attributes. Always use the new names.

#### Geometry Guidelines

Use consistent, realistic values:

| Component | Typical Width | Typical Height |
|---|---|---|
| AppShell (canvas) | 1440 | 900 |
| AppShellNavbar | 240 | 900 |
| AppShellMain | 1200 | 900 |
| Paper (navbar) | 240 | 900 |
| NavLink | 240 | 44 |
| Title (h1) | 600 | 48 |
| Title (h2) | 400 | 36 |
| Text | 600 | 24 |
| Button | 120 | 36 |
| Card | 320 | 200 |
| Grid row | 1120 | 200 |
| GridCol (3-col) | 360 | 200 |

Stack children vertically with appropriate spacing (e.g., y increments of 60px for navbar items).

### Step 4 — Determine Output Path

If `--output` was provided, write to that path.

If not provided, prompt:
```
Where should I write the .drawio file?
Suggested: docs/design/{project-name}.drawio
```

Wait for user response before writing.

### Step 5 — Write File

Write the generated XML to the output path.
Ensure the parent directory exists — if not, note the `mkdir` command needed.

### Step 6 — Confirm

Print:
```
Generated: {output_path}
Pages:     {N} ({comma-separated page names})
Components: {N} total

Open in draw.io to review and refine the layout.
Run `/drawio parse {output_path}` to generate WIREFRAME.md when ready.
```

---

## Generation Quality Rules

1. **Completeness over brevity** — generate all mentioned components, even if structural
2. **Follow conventions exactly** — no spatial inference, parent chain is the authority
3. **Placeholder content** — use realistic placeholder labels (e.g., `"Home"`, `"Projects"`, `"Chart Title"`)
4. **Instructions are guidance, not code** — keep `component-instructions` values brief and human-readable
5. **New attributes only** — only `component-class`, `label`, `component-id`, `component-parent-id`, `component-instructions`, `component-order`, `callback-in`, `callback-in-details`, `callback-out`, `callback-out-details`, `db-binding` on `<object>` elements
6. **Valid XML** — output must be parseable by draw.io without modification
7. **Omit optional attributes** — do not include empty optional attributes; omit entirely when not needed

---

## Example

Input:
```
/drawio generate "Portfolio app with home and about pages. Navbar with links to Home, Projects, About. Home page has a title and a grid of 3 project cards."
```

Output: A `.drawio` XML file with:
- 2 pages: `home`, `about`
- Root layer (app-shell): AppShell, AppShellNavbar, AppShellMain
- Shared navbar (content-navbar): Paper → Stack → NavLink ×3 (nav-home, nav-projects, nav-about)
- `home` page (content-page): Title [component-id=home-title] + Grid → GridCol ×3 → Card ×3
- `about` page (content-page): Title [component-id=about-title] + Text (placeholder)
