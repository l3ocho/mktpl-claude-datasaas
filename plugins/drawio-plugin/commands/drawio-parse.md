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
- `skills/drawio-conventions.md` — XML structure, layer naming, attribute schema
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
Find all `<mxCell>` elements with `vertex=1` and a `value` attribute that matches a known layer name:
- Root layer: `id="1"`, no meaningful value
- `layout` layer: `value="layout"`
- `content-navbar` layer: `value="content-navbar"`
- `content-page` / `content-pages` layer: `value` starts with `content-page`

**3b. Extract components:**
Walk all `<object>` elements. For each, extract:
- `component` attribute — required; if missing, warn and skip: `Warning: <object> at id={id} missing component attribute — skipped`
- `label` attribute — required but may be `""`
- `instructions` attribute — required but may be `""`
- `id` attribute — optional, omit from output if absent
- `css_id` attribute — optional, omit from output if absent

**3c. Resolve parent chain:**
For each `<object>`, find its `<mxCell>` child and read its `parent` attribute.
Walk the parent chain: `object → mxCell.parent → ... → layer cell`
Record which layer (root, layout, content-navbar, content-page) the element belongs to.
Record the nesting depth within that layer for indentation in output.

**3d. Classify:**
- Elements parented to root layer (`id="1"`) → AppShell section
- Elements parented to `layout` layer → shared layout structural components
- Elements parented to `content-navbar` layer → shared navbar content tree
- Elements parented to `content-page/s` layer → per-page content tree

### Step 4 — Detect DMC Domain Files

Collect all unique `component` attribute values across ALL pages.
Apply the component → domain file mapping from `skills/dmc-domain-files.md`.
Always include `dmc-layout.txt` and `dmc-ui.txt`.

### Step 5 — Write WIREFRAME.md

Write `WIREFRAME.md` to the same directory as the source `.drawio` file.
Follow the schema defined in `skills/wireframe-schema.md` exactly.

Shared layout (AppShell, AppShellNavbar tree) is written once.
Each page's `AppShellMain` content is written separately.

### Step 6 — Print Summary

After writing the file, print:

```
Parsed: {drawio_file_path}
Output: {wireframe_md_path}

Pages found:     {N} ({comma-separated page names})
Components found: {N} total across all pages
DMC domain files: {list of declared files}
```

If any warnings were generated (missing `component` attributes), list them at the end.

---

## Edge Cases

| Condition | Behavior |
|---|---|
| Page has no `content-page` layer | Note in output: `(no content-page layer found)`, still parse shared layout |
| `<object>` missing `component` attribute | Warn and skip — do not stop parsing |
| Multiple pages with identical names | Parse all; append `_2`, `_3` suffix to disambiguate in output |
| Empty `.drawio` file or no `<diagram>` elements | Fail with clear message |
| `content-pages` vs `content-page` layer name variant | Both are valid — treat identically |
