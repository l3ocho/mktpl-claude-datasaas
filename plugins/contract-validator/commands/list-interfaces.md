# /list-interfaces - Show Plugin Interfaces

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  ✅ CONTRACT-VALIDATOR · List Interfaces                         │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the interface listing.

Display what each plugin in the marketplace produces and accepts.

## Usage

```
/list-interfaces [marketplace_path]
```

## Parameters

- `marketplace_path` (optional): Path to marketplace root. Defaults to current project root.

## Workflow

1. **Discover plugins**:
   - Scan plugins directory for all plugins with `.claude-plugin/` marker
   - Read each plugin's README.md

2. **Parse interfaces**:
   - Extract commands (slash commands offered by plugin)
   - Extract agents (autonomous agents defined)
   - Extract tools (MCP tools provided)
   - Identify tool categories and features

3. **Display summary**:
   - Table of plugins with command/agent/tool counts
   - Detailed breakdown per plugin
   - Tool categories and their contents

## Output Format

```
| Plugin      | Commands | Agents | Tools |
|-------------|----------|--------|-------|
| projman     | 12       | 4      | 26    |
| data-platform| 7       | 2      | 32    |
| ...         | ...      | ...    | ...   |

## projman
- Commands: /sprint-plan, /sprint-start, ...
- Agents: Planner, Orchestrator, Executor, Code Reviewer
- Tools: list_issues, create_issue, ...
```

## Examples

```
/list-interfaces
/list-interfaces ~/claude-plugins-work
```

## Available Tools

Use these MCP tools:
- `parse_plugin_interface` - Parse individual plugin README
- `generate_compatibility_report` - Get full interface data (JSON format)
