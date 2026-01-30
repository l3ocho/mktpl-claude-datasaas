# Skill: Plugin Discovery

Discover plugins in a marketplace by scanning for `.claude-plugin/` markers.

## Discovery Process

1. **Identify marketplace root**:
   - Use provided path or default to current project root
   - Look for `plugins/` subdirectory

2. **Scan for plugins**:
   - Find all directories containing `.claude-plugin/plugin.json`
   - Each is a valid plugin

3. **Build plugin list**:
   - Extract plugin name from directory name
   - Record path to plugin root

## Standard Paths

| Context | Path |
|---------|------|
| Installed | `~/.claude/plugins/marketplaces/leo-claude-mktplace/plugins/` |
| Source | `~/claude-plugins-work/plugins/` |

## Expected Structure

```
plugins/
  plugin-name/
    .claude-plugin/
      plugin.json       # Required marker
    commands/           # Command definitions
    agents/             # Agent definitions (optional)
    hooks/              # Hook definitions (optional)
    skills/             # Skill files (optional)
    README.md           # Interface documentation
```

## MCP Tool

Use `parse_plugin_interface` with each discovered plugin's README.md path.
