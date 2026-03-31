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
- **Layout type:** Default to AppShell. If description specifies a different layout, note it but still use AppShell as the outer wrapper.
- **Navbar items:** Extract any navigation items mentioned (e.g., "with links to Home, Projects, About")
- **Per-page components:** Group described components by page

If description is too vague to determine pages, default to a single page named `home`.

### Step 3 — Generate XML

For each page, generate XML following the layer/group/attribute conventions exactly.

#### XML Structure Per Page

Every `<diagram>` must contain these layers in this order:

**Root layer (`id="1"`):**
- One `<object component="AppShell">` element with:
  - `label=""`
  - `instructions=""` (or any noted constraints)
  - `<mxGeometry x="0" y="0" width="1440" height="900"/>`

**`layout` layer (`value="layout"`, `locked=1`):**
- `<object component="AppShellNavbar">` with `instructions="width=240"` (default)
- `<object component="AppShellMain">` with `instructions=""`
- Both parented to the layout layer cell

**`content-navbar` layer (`value="content-navbar"`, `locked=1`):**
- Standard navbar structure:
  ```
  Paper (padding=0, radius=0) → Stack (gap=0) → NavLink items (one per nav item)
  ```
- Each NavLink: `label="{nav item name}"`, `instructions=""`, no `id` unless user specified

**`content-page` layer (`value="content-page"`, `locked=0`):**
- Components described for this page
- Reasonable component choices based on description:
  - Text content → `Title`, `Text`
  - Data display → `Table`, `Card`, `Grid`
  - User input → `TextInput`, `Select`, `Button`
  - Charts/graphs → `AreaChart`, `BarChart`, `LineChart` (or note: "use dcc.Graph with Plotly figure")
  - Layout grouping → `Stack`, `Group`, `Grid` / `GridCol`

#### Attribute Completeness

Every `<object>` element MUST have:
- `component` — the DMC class name
- `label` — display text, or `""` for structural wrappers
- `instructions` — implementation notes, or `""` — **never omit this attribute**

Omit `id` and `css_id` unless the user explicitly specifies them in the description.

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
4. **Instructions are guidance, not code** — keep `instructions` attribute values brief and human-readable
5. **No custom attributes** — only `component`, `label`, `instructions`, `id`, `css_id` on `<object>` elements
6. **Valid XML** — output must be parseable by draw.io without modification

---

## Example

Input:
```
/drawio generate "Portfolio app with home and about pages. Navbar with links to Home, Projects, About. Home page has a title and a grid of 3 project cards."
```

Output: A `.drawio` XML file with:
- 2 pages: `home`, `about`
- Shared navbar: Paper → Stack → NavLink ×3 (Home, Projects, About)
- `home` page: Title + Grid → GridCol ×3 → Card ×3
- `about` page: Title + Text (placeholder)
