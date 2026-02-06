---
name: cv list-interfaces
---

# /cv list-interfaces

## Skills to Load
- skills/visual-output.md
- skills/plugin-discovery.md
- skills/interface-parsing.md
- skills/mcp-tools-reference.md

## Usage

```
/cv list-interfaces [marketplace_path]
```

## Parameters

- `marketplace_path` (optional): Path to marketplace root. Defaults to current project root.

## Workflow

1. **Display header** per `skills/visual-output.md`

2. **Discover plugins** per `skills/plugin-discovery.md`

3. **Parse interfaces** per `skills/interface-parsing.md`
   - Use `parse_plugin_interface` for each plugin README.md
   - Extract commands, agents, tools

4. **Display summary table**:
   ```
   | Plugin      | Commands | Agents | Tools |
   |-------------|----------|--------|-------|
   | projman     | 12       | 4      | 26    |
   ```

5. **Display per-plugin details**:
   - List of commands
   - List of agents
   - Tool categories

## Examples

```
/cv list-interfaces
/cv list-interfaces ~/claude-plugins-work
```
