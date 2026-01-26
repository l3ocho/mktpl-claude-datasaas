# contract-validator Plugin

Cross-plugin compatibility validation and CLAUDE.md agent verification for Claude Code plugin marketplaces.

## Problem Statement

As plugin marketplaces grow, several compatibility issues emerge:

- **Command conflicts**: Multiple plugins defining the same slash command (e.g., `/initial-setup`)
- **Tool name overlaps**: Different plugins using identical tool names with incompatible interfaces
- **Undocumented dependencies**: Agents referencing tools that don't exist
- **Broken data flows**: Agent sequences that expect outputs not produced by prior steps

Contract-validator solves these by parsing plugin interfaces and validating compatibility before runtime.

## Features

- **Interface Parsing**: Extract commands, agents, and tools from plugin README.md files
- **Agent Extraction**: Parse CLAUDE.md Four-Agent Model tables and Agents sections
- **Compatibility Checks**: Pairwise validation between all plugins in a marketplace
- **Data Flow Validation**: Verify agent tool sequences have valid data producers/consumers
- **Comprehensive Reports**: Markdown or JSON reports with actionable suggestions

## Installation

This plugin is part of the leo-claude-mktplace. Install via:

```bash
# From marketplace
claude plugins install leo-claude-mktplace/contract-validator

# Setup MCP server venv
cd ~/.claude/plugins/marketplaces/leo-claude-mktplace/mcp-servers/contract-validator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Commands

| Command | Description |
|---------|-------------|
| `/validate-contracts` | Full marketplace compatibility validation |
| `/check-agent` | Validate single agent definition |
| `/list-interfaces` | Show all plugin interfaces |

## Agents

| Agent | Description |
|-------|-------------|
| `full-validation` | Complete cross-plugin compatibility validation |
| `agent-check` | Single agent definition verification |

## Tools Summary

### Parse Tools (2)
- `parse_plugin_interface` - Extract interface from plugin README.md
- `parse_claude_md_agents` - Extract agents from CLAUDE.md

### Validation Tools (3)
- `validate_compatibility` - Check two plugins for conflicts
- `validate_agent_refs` - Verify agent tool references exist
- `validate_data_flow` - Check data flow through agent sequences

### Report Tools (2)
- `generate_compatibility_report` - Full marketplace validation report
- `list_issues` - Filter issues by severity or type

## Example Workflow

```
/validate-contracts ~/claude-plugins-work

# Output:
# Contract Validation Report
#
# | Metric     | Count |
# |------------|-------|
# | Plugins    | 12    |
# | Commands   | 39    |
# | Tools      | 32    |
# | **Issues** | **7** |
# | - Errors   | 3     |
# | - Warnings | 0     |
# | - Info     | 4     |
#
# ## Issues Found
# [ERROR] Command conflict: projman and data-platform both define /initial-setup
# [ERROR] Command conflict: projman and pr-review both define /initial-setup
# ...
```

```
/check-agent Planner ./CLAUDE.md

# Output:
# Agent: Planner
# Status: VALID
#
# Tool References Found (3):
# - create_issue ✓
# - search_lessons ✓
# - get_execution_order ✓
#
# Data Flow: No issues detected
```

## Issue Types

| Type | Severity | Description |
|------|----------|-------------|
| `interface_mismatch` | ERROR | Command name conflict between plugins |
| `missing_tool` | ERROR | Agent references non-existent tool |
| `interface_mismatch` | WARNING | Tool name overlap (different plugins) |
| `optional_dependency` | WARNING | Agent uses tool from non-required plugin |
| `undeclared_output` | INFO | Agent has no documented tool references |

## Parsed Interface Structure

When parsing a plugin README.md, the following structure is extracted:

```json
{
  "plugin_name": "data-platform",
  "description": "Data engineering tools...",
  "commands": [
    {"name": "/ingest", "description": "Load data..."}
  ],
  "agents": [
    {"name": "data-analysis", "description": "..."}
  ],
  "tools": [
    {"name": "read_csv", "category": "pandas"}
  ],
  "tool_categories": {
    "pandas": ["read_csv", "to_csv", ...],
    "PostgreSQL": ["pg_query", ...]
  },
  "features": ["pandas Operations", "PostgreSQL/PostGIS", ...]
}
```

## Best Practices

### For Plugin Authors

1. **Use unique command names**: Prefix with plugin name if generic (e.g., `/data-setup` vs `/initial-setup`)
2. **Document all tools**: Include tool names in README.md with backticks
3. **Specify tool categories**: Use `### Category (N tools)` headers
4. **Declare agent tools**: List tools used by agents in their definitions

### For Marketplace Maintainers

1. **Run validation before merging**: Use `/validate-contracts` in CI/CD
2. **Review warnings**: Tool overlaps may indicate design issues
3. **Track issues over time**: Use JSON format for programmatic tracking
