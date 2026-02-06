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

## Phase 3: Theme Preferences (Optional)

Ask user about color scheme and primary color. Save to `~/.config/claude/viz-platform.env`.

## Phase 4: Validation

Verify MCP server loads, display summary, prompt session restart.

## Related Commands

- `/viz component {name}` - Inspect component props
- `/viz chart {type}` - Create a chart
