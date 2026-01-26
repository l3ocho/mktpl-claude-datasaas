# /check-agent - Validate Agent Definition

Validate a single agent's tool references and data flow.

## Usage

```
/check-agent <agent_name> [claude_md_path]
```

## Parameters

- `agent_name` (required): Name of the agent to validate (e.g., "Planner", "Orchestrator")
- `claude_md_path` (optional): Path to CLAUDE.md file. Defaults to `./CLAUDE.md`

## Workflow

1. **Parse agent definition**:
   - Locate agent in CLAUDE.md (Four-Agent Model table or Agents section)
   - Extract responsibilities, tool references, workflow steps

2. **Validate tool references**:
   - Check each referenced tool exists in available plugins
   - Report missing or misspelled tool names
   - Suggest corrections for common mistakes

3. **Validate data flow**:
   - Analyze sequence of tools in agent workflow
   - Verify data producers precede data consumers
   - Check for orphaned data references

4. **Report findings**:
   - List all tool references found
   - List any missing tools
   - Data flow validation results
   - Suggestions for improvement

## Examples

```
/check-agent Planner
/check-agent Orchestrator ./CLAUDE.md
/check-agent data-analysis ~/project/CLAUDE.md
```

## Available Tools

Use these MCP tools:
- `validate_agent_refs` - Check agent tool references exist
- `validate_data_flow` - Verify data flow through agent sequence
- `parse_claude_md_agents` - Parse all agents from CLAUDE.md
