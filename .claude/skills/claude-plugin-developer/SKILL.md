---
name: claude-plugin-developer
description: Comprehensive guide for developing secure, standards-compliant Claude Code plugins. Use when creating new plugins, debugging plugin issues, setting up marketplaces, developing commands/agents/hooks/MCP servers, or ensuring plugins follow Anthropic's security requirements and best practices for (1) Plugin structure and manifests, (2) Command development, (3) Agent development, (4) Hook automation, (5) MCP server integration, (6) Security validation, (7) Marketplace publication
license: MIT
---

# Claude Plugin Developer

Expert guidance for creating secure, standards-compliant Claude Code plugins following Anthropic's official guidelines.

## Quick Start

### Plugin Structure
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json        # Required manifest
├── commands/              # Slash commands (.md files)
├── agents/                # Subagents (.md files)  
├── hooks/                 # Event handlers
│   └── hooks.json
├── .mcp.json             # MCP server config
└── scripts/              # Supporting scripts
```

### Creating Your First Plugin

1. **Initialize structure**: Use `scripts/init_plugin.py` template
2. **Create manifest**: Fill in `.claude-plugin/plugin.json`
3. **Add components**: Commands, agents, hooks, or MCP servers
4. **Test locally**: `claude --debug` to verify loading
5. **Publish**: Add to marketplace or share directly

## Component Development

### Commands
- **Location**: `commands/` directory at plugin root
- **Format**: Markdown files with structured metadata
- **Naming**: Use kebab-case (e.g., `deploy-app.md`)
- **Organization**: Use subdirectories for related commands

### Agents
- **Location**: `agents/` directory at plugin root  
- **Format**: Markdown with agent instructions
- **Integration**: Referenced in commands via `_agent` field

### Hooks
- **Configuration**: `hooks/hooks.json` file
- **Events**: `file-changed`, `git-commit-msg-needed`, `task-completed`
- **Scripts**: Place in `hooks/` directory

### MCP Servers
- **Configuration**: `.mcp.json` at plugin root
- **Integration**: External tool connections
- **Security**: Follow sandboxing requirements

## Security Requirements

### Path Safety
- Always use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths
- Never use absolute paths or parent directory traversal
- Validate all user inputs before file operations

### Command Security
```json
{
  "default_shell": "bash",
  "require_safety_check": true,
  "allowed_operations": ["read", "write", "execute"]
}
```

### Marketplace Security
- Sign commits when publishing to marketplaces
- Include proper licensing information
- Document all external dependencies
- Follow semantic versioning

## Validation & Testing

### Local Testing
```bash
# Debug plugin loading
claude --debug

# Test specific command
/plugin-name command-name

# Verify marketplace
claude plugin list
```

### Common Issues
- **JSON syntax errors**: Validate with `jq` or online validator
- **File permissions**: Ensure scripts are executable
- **Path resolution**: Use relative paths from plugin root
- **Missing dependencies**: Document in plugin.json

## Advanced Topics

### Plugin Manifest Schema
See `references/manifest-schema.md` for complete JSON schema

### Command Metadata Format
See `references/command-metadata.md` for frontmatter specifications

### Hook Development Patterns
See `references/hook-patterns.md` for event handling examples

### MCP Server Integration
See `references/mcp-integration.md` for server configuration

### Marketplace Publication
See `references/marketplace-guide.md` for distribution strategies

## Best Practices

### Naming Conventions
- Plugin names: `kebab-case`
- Commands: `action-object` pattern
- Variables: `${SCREAMING_SNAKE_CASE}`
- Functions: `camelCase` in scripts

### Documentation
- Include examples in every command
- Document environment variables
- Provide troubleshooting sections
- Keep README concise

### Performance
- Lazy load heavy dependencies
- Cache expensive operations
- Minimize startup time
- Use async where possible

### User Experience
- Clear error messages with solutions
- Progress indicators for long operations
- Confirmation prompts for destructive actions
- Helpful command descriptions

## Resource Organization

### Scripts Usage
- `scripts/init_plugin.py`: Generate plugin structure
- `scripts/validate_manifest.py`: Check plugin.json
- `scripts/test_commands.py`: Automated testing

### References Content
- Detailed schemas and specifications
- Advanced patterns and examples
- Troubleshooting guides
- API documentation

### Assets Purpose
- Command templates
- Example configurations
- Boilerplate code
- Icon assets

## When to Reference Additional Files

- **Creating complex commands**: See `references/command-patterns.md`
- **Setting up CI/CD**: See `references/ci-cd-integration.md`
- **Multi-language support**: See `references/i18n-guide.md`
- **Team collaboration**: See `references/team-workflows.md`
- **Performance optimization**: See `references/performance-guide.md`