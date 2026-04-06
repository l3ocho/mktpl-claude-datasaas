---
name: viz setup
description: Interactive setup wizard for viz-platform plugin
---

# /viz setup

## Visual Output

```
+------------------------------------------------------------------+
|  VIZ-PLATFORM - Setup Wizard                                     |
+------------------------------------------------------------------+
```

Sets up viz-platform with DMC validation and theming.

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

## Phase 3: Theme Preferences (Optional)

Ask user about color scheme and primary color. Save to `~/.config/claude/viz-platform.env`.

## Phase 4: Validation

Verify MCP server loads, display summary, prompt session restart.

## Related Commands

- `/viz component {name}` - Inspect component props
- `/viz chart {type}` - Create a chart
