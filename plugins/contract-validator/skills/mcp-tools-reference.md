# Skill: MCP Tools Reference

Available MCP tools for contract-validator operations.

## Tool Categories

### Parse Tools
| Tool | Description |
|------|-------------|
| `parse_plugin_interface` | Extract interface from plugin README.md |
| `parse_claude_md_agents` | Extract agents and tool sequences from CLAUDE.md |

### Validation Tools
| Tool | Description |
|------|-------------|
| `validate_compatibility` | Check two plugins for conflicts |
| `validate_agent_refs` | Check agent tool references exist |
| `validate_data_flow` | Verify data flow through agent sequence |

### Report Tools
| Tool | Description |
|------|-------------|
| `generate_compatibility_report` | Generate full marketplace report (JSON) |
| `list_issues` | Filter issues by severity or type |

## Tool Usage Patterns

### Full Marketplace Validation
```
1. generate_compatibility_report(marketplace_path)
2. list_issues(severity="ERROR")  # Get critical issues
3. list_issues(severity="WARNING")  # Get warnings
```

### Single Agent Check
```
1. parse_claude_md_agents(claude_md_path)
2. validate_agent_refs(agent_name, agents_data)
3. validate_data_flow(agent_workflow)
```

### Interface Listing
```
1. For each plugin:
   parse_plugin_interface(readme_path)
2. Aggregate results into summary table
```

### Dependency Graph
```
1. generate_compatibility_report(marketplace_path)
2. validate_data_flow(cross_plugin_flows)
3. Build Mermaid diagram from results
```

## Error Handling

If MCP tools fail:
1. Check if `/initial-setup` has been run
2. Verify session was restarted after setup
3. Check MCP server venv exists and is valid
