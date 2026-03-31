---
name: drawio-parse
description: Parse a .drawio XML file into a WIREFRAME.md spec with DMC domain file declarations
---

# /drawio parse

Parse a `.drawio` wireframe file into a `WIREFRAME.md` specification.
Outputs a structured component spec and declares which DMC domain files viz-platform
should load for the session.

## Usage

```
/drawio parse {drawio_file_path}
```

## Parameters

| Parameter | Required | Description |
|---|---|---|
| `drawio_file_path` | Yes | Relative or absolute path to the `.drawio` file |

---

## Execution Flow

### Step 1 — Load Skills

Load the following skills before proceeding:
- `skills/drawio-conventions.md` — XML structure, layer naming, attribute schema, style signals
- `skills/wireframe-schema.md` — WIREFRAME.md output format
- `skills/dmc-domain-files.md` — component → domain file mapping

### Step 2 — Read the File

Read the `.drawio` XML file at `{drawio_file_path}`.

**Error:** If file not found, fail immediately with:
```
Error: File not found at {drawio_file_path}
Expected a .drawio XML file. Check the path and try again.
```

### Step 3 — Parse Each Page

For each `<diagram>` element (one per page/view):

**3a. Identify layers:**
Find all `<mxCell>` elements with `vertex=1` and a `value` attribute that matches a known layer pattern:
- Root layer: `id="1"`, no meaningful value → treat as `app-shell`
- `content-navbar` layer: `value="content-navbar"`
- `content-header` layer: `value="content-header"` (if present)
- `content-footer` layer: `value="content-footer"` (if present)
- `content-aside` layer: `value="content-aside"` (if present)
- `content-page` layer: `value` starts with `content-page`
- Any layer whose `value` starts with `content-` is a content layer

**3b. Extract components:**
Walk all `<object>` elements. For each, extract:
- `component-class` — required; if missing, warn and skip: `Warning: <object> at id={id} missing component-class attribute — skipped`
- `label` — required but may be `""`
- `component-id` — optional; if present, validate naming convention (`{prefix}-{descriptor}` two segments, max three). Warn if invalid, do not fail.
- `component-parent-id` — optional; collect for parent-child tree building
- `component-instructions` — optional
- `component-order` — optional integer
- `callback-in` — optional; split on commas → list
- `callback-in-details` — optional
- `callback-out` — optional; split on commas → list
- `callback-out-details` — optional
- `db-binding` — optional; expected format `table_name.column_name`

**3c. Extract style signals:**
For each `<object>`, read its `<mxCell style="...">` string and extract:
- `strokeColor`: `none` → `withBorder: false`; any other value → `withBorder: true`
- `opacity`: parse integer value, convert to float (80 → 0.8). Omit if 100 (default).
- `rounded`: `1` → `true`, `0` or absent → `false`. Ignore `arcSize`. Omit if false (default).

Only record style signals that differ from defaults (withBorder: true, opacity: 1.0, rounded: false).

**3d. Resolve parent chain:**
For each `<object>`, find its `<mxCell>` child and read its `parent` attribute.
Walk the parent chain: `object → mxCell.parent → ... → layer cell`
Record which layer (app-shell, content-navbar, content-header, content-footer, content-aside, content-page) the element belongs to.
Record the nesting depth within that layer for indentation in output.

**3e. Build component tree:**
Use `component-parent-id` references to build the explicit Dash parent-child tree.
Where `component-parent-id` is absent, use XML `parent` chain as fallback for tree structure.

**3f. Classify:**
- Elements parented to root layer (`id="1"`) → app-shell section (AppShell + region containers)
- Elements parented to `content-navbar` layer → shared navbar content tree
- Elements parented to `content-header` layer → shared header content
- Elements parented to `content-footer` layer → shared footer content
- Elements parented to `content-aside` layer → shared aside content
- Elements parented to `content-page` layer → per-page content tree

### Step 4 — Detect DMC Domain Files

Collect all unique `component-class` attribute values across ALL pages.
Apply the component → domain file mapping from `skills/dmc-domain-files.md`.
Always include `dmc-layout.txt` and `dmc-ui.txt`.

### Step 5 — Write WIREFRAME.md

Write `WIREFRAME.md` to the same directory as the source `.drawio` file.
Follow the schema defined in `skills/wireframe-schema.md` exactly.

Shared layout (AppShell, AppShellNavbar tree, and any other shared region trees) is written once.
Each page's content-page content is written separately.

### Step 6 — Print Summary

After writing the file, print:

```
Parsed: {drawio_file_path}
Output: {wireframe_md_path}

Pages found:      {N} ({comma-separated page names})
Components found: {N} total across all pages
Layers detected:  app-shell{, content-navbar}{, content-header}{, content-footer}{, content-aside}, content-page
DMC domain files: {list of declared files}
```

If any warnings were generated (missing `component-class`, invalid `component-id` naming), list them at the end.

---

## Edge Cases

| Condition | Behavior |
|---|---|
| Page has no `content-page` layer | Note in output: `(no content-page layer found)`, still parse shared layout |
| `<object>` missing `component-class` attribute | Warn and skip — do not stop parsing |
| `<object>` has old attribute `component` instead of `component-class` | Warn: `Warning: old attribute 'component' found at id={id} — update to 'component-class'`. Use value as-is. |
| Multiple pages with identical names | Parse all; append `_2`, `_3` suffix to disambiguate in output |
| Empty `.drawio` file or no `<diagram>` elements | Fail with clear message |
| `content-pages` vs `content-page` layer name variant | Both are valid — treat identically |
| `callback-in` or `callback-out` contains a single value (no comma) | Treat as a list with one element |
| `db-binding` format is not `table.column` | Warn: `Warning: db-binding "{value}" at {id} does not follow table_name.column_name format` |
