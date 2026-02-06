---
description: Marketplace-wide health check across all installed plugins
---

# /cv status

## Purpose

Quick health check showing installed plugin status. For each marketplace plugin, reports installation state, MCP connectivity, and configuration status.

## Usage

```
/cv status                    # Full status table
/cv status --plugin projman   # Single plugin check
```

## Workflow

### Step 1: Enumerate Plugins
Read `.claude-plugin/marketplace.json` to get the full plugin list.

### Step 2: Check Each Plugin
For each plugin, verify:
- **Installed:** `plugin.json` exists and is valid JSON
- **MCP Connected:** If plugin has MCP servers (check `metadata.json`), verify server is responding
- **Configured:** Required config files present
- **Version:** Read from `plugin.json`
- **Domain:** Read from `plugin.json`

### Step 3: Display Results

```
| Plugin                   | Domain | Version | Installed | MCP | Configured |
|--------------------------|--------|---------|-----------|-----|------------|
| projman                  | core   | 3.4.0   | Y         | Y   | Y          |
| git-flow                 | core   | 1.2.0   | Y         | -   | Y          |
| cmdb-assistant           | ops    | 1.2.0   | Y         | N   | N          |

Summary: 12/12 installed, 4/5 MCP connected, 11/12 configured
```

## Notes

- MCP column shows `-` for plugins without MCP servers
- `N` in MCP means the server is defined but not responding
- `N` in Configured means the setup check found issues
