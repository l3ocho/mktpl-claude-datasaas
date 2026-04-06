# DMC Domain Reference Files

These `.txt` files contain curated Dash Mantine Components documentation split by domain
to minimize context window usage when loading into Claude Code sessions.

## Files

| File | Domain | Load When |
|---|---|---|
| `dmc-layout.txt` | Layout & shell components | Always |
| `dmc-ui.txt` | Buttons, inputs, navigation, typography | Always |
| `dmc-charts.txt` | Chart components | Only if chart components in wireframe |
| `dmc-feedback.txt` | Alerts, modals, loaders, date pickers | Only if feedback components in wireframe |
| `dmc-theme.txt` | MantineProvider, theme configuration | Only if theme components in wireframe |

## IMPORTANT: Do Not Edit Manually

These files are **AUTO-GENERATED** by `scripts/generate-dmc-refs.py`.
Any manual edits will be overwritten the next time the script is run.

## How to Regenerate

```bash
# From the marketplace root:
python scripts/generate-dmc-refs.py --project /path/to/consumer-project

# Dry run (preview without writing):
python scripts/generate-dmc-refs.py --project /path/to/consumer-project --dry-run

# Verbose (show each component matched):
python scripts/generate-dmc-refs.py --project /path/to/consumer-project --verbose
```

## Consumer Project Setup

Consumer projects control which components are included via two files:

**1. `.env` (project root) — declares the DMC version URL:**
```bash
DMC_LLMS_JSON_URL=https://www.dash-mantine-components.com/assets/llms.json
```

**2. `.claude/dmc-components.json` — declares which components to include:**
```json
{
  "components": ["AppShell", "Grid", "Button", "TextInput", "Select"],
  "categories": ["layout", "inputs"]
}
```

Both `components` and `categories` are additive (union). If neither is specified, all
components are included (generates a large file — not recommended).

See `docs/CONFIGURATION.md` under "DMC Reference Generation" for full schema documentation.
