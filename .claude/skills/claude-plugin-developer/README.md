# Claude Plugin Developer Skill

## Installation

1. Download the entire `claude-plugin-developer` folder
2. Place it in your skills directory (or wherever you manage your skills)
3. Add it to your marketplace or use it directly

## What's Included

- **SKILL.md** - The main skill file with comprehensive plugin development guidelines
- **references/** - Detailed guides for specific topics:
  - `manifest-schema.md` - Complete plugin.json schema reference
  - `command-metadata.md` - Command frontmatter specifications
  - `hook-patterns.md` - Event-based automation patterns
  - `marketplace-guide.md` - Plugin distribution strategies
  - `mcp-integration.md` - MCP server integration guide
  - `performance-guide.md` - Performance optimization tips
- **scripts/** - Helper utilities:
  - `init_plugin.py` - Generate new plugin structure
  - `validate_manifest.py` - Validate plugin.json files
  - `test_commands.py` - Automated command testing

## Quick Usage

When creating a new plugin:
```bash
python scripts/init_plugin.py my-new-plugin
```

To validate a plugin manifest:
```bash
python scripts/validate_manifest.py path/to/plugin.json
```

To test plugin commands:
```bash
python scripts/test_commands.py path/to/plugin
```

## Purpose

This skill helps you create secure, standards-compliant Claude Code plugins following Anthropic's official guidelines. Use it whenever you need to:

- Create a new plugin from scratch
- Debug plugin loading issues
- Set up marketplaces
- Develop commands, agents, hooks, or MCP servers
- Ensure security compliance
- Publish to marketplaces
