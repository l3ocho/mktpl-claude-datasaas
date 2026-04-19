---
name: viz setup
description: Interactive setup wizard for viz-platform plugin
---

# /viz setup

## Skills to Load
- skills/mcp-tools-reference.md
- skills/theming-system.md
- skills/dmc-components.md

Sets up viz-platform with DMC validation, theming, and design contract.

**Note:** Uses Bash/Read/Write tools - NOT MCP tools. Restart session after setup.

## Phase 1: Environment Validation

Check Python 3.10+ and DMC installation:
```bash
python3 --version
python3 -c "import dash_mantine_components as dmc; print(dmc.__version__)"
```

## Phase 2: MCP Server Setup

Locate and create venv if missing:
```bash
cd /path/to/mcp-servers/viz-platform && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

## Phase 2b: DMC Reference URL

Ask the user for the `DMC_LLMS_JSON_URL` value. Pre-fill with the stable default:

```
https://www.dash-mantine-components.com/assets/llms.json
```

Explain: _"This URL should point to the llms.json for the DMC version installed in your
project's .venv. Use the default unless you are pinning an older DMC version."_

Write the value to the consumer project's `.env`:
```bash
# Append to <project-root>/.env (create if missing)
echo "DMC_LLMS_JSON_URL=<user-provided-url>" >> .env
```

After writing, remind the user to run:
```bash
python scripts/generate-dmc-refs.py --project <project-root>
```
to regenerate DMC reference files for this project.

## Phase 3: Design Contract Builder

Build the project's surface hierarchy contract at `.claude/design-contract.json`.

Ask the user each question in sequence:

**3a. Scheme mode**
> "What color schemes will this project use?"
> Options: `light` / `dark` / `dual` (both)

For each active scheme, prompt for surface background tokens:

| Surface | Semantic meaning | Example (light) | Example (dark) |
|---------|-----------------|-----------------|----------------|
| `base` | App shell, main page background | `white` | `dark.8` |
| `raised` | Cards, panels elevated above base | `white` + border `gray.2` | `dark.7` + border `dark.5` |
| `overlay` | Modals, drawers, popovers | `gray.0` | `dark.6` |
| `nested_in_overlay` | Content inside modals | `white` | `dark.7` |

**3b. Interaction tokens**
> "Configure interaction defaults:"
- `hover_delta`: shade shift on hover (default: `-1`)
- `focus_ring size`: px (default: `2`)
- `focus_ring color_token`: (default: `primary.5`)
- `disabled_opacity`: 0–1 (default: `0.55`)
- `error_token`: (default: `red.6`)

**3c. Density**
> "Choose component density:"
> Options: `compact` (tighter padding/spacing) / `comfortable` (default Mantine spacing)

**3d. Write contract**

Create `.claude/design-contract.json` in the consumer project root:

```json
{
  "schemes": {
    "light": {
      "surfaces": {
        "base":              { "bg": "<user-value>", "border": null, "variant": null },
        "raised":            { "bg": "<user-value>", "border": "<user-value>", "variant": "outline" },
        "overlay":           { "bg": "<user-value>", "border": null, "variant": null },
        "nested_in_overlay": { "bg": "<user-value>", "border": null, "variant": null }
      }
    }
  },
  "component_locks": {},
  "interaction": {
    "hover_delta": -1,
    "focus_ring": { "size": 2, "color_token": "primary.5" },
    "disabled_opacity": 0.55,
    "error_token": "red.6"
  },
  "density": "comfortable",
  "meta": {
    "version": "1.0.0",
    "created_at": "<ISO-timestamp>",
    "updated_at": "<ISO-timestamp>"
  }
}
```

## Phase 4: Validation

Verify MCP server loads, display summary, prompt session restart.

## Related Commands

- `/viz chart {type}` - Create a chart
- `/viz theme apply {name}` - Apply a theme
