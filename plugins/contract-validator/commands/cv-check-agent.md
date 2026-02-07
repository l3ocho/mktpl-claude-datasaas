---
name: cv check-agent
---

# /cv check-agent

## Skills to Load
- skills/visual-output.md
- skills/interface-parsing.md
- skills/validation-rules.md
- skills/mcp-tools-reference.md

## Usage

```
/cv check-agent <agent_name> [claude_md_path]
```

## Parameters

- `agent_name` (required): Agent to validate (e.g., "Planner", "Orchestrator")
- `claude_md_path` (optional): Path to CLAUDE.md. Defaults to `./CLAUDE.md`

## Workflow

1. **Display header** per `skills/visual-output.md`

2. **Parse agent** per `skills/interface-parsing.md`
   - Use `parse_claude_md_agents` to extract agent definition
   - Get responsibilities, tool references, workflow steps

3. **Validate** per `skills/validation-rules.md`
   - Use `validate_agent_refs` - check all tools exist
   - Use `validate_data_flow` - verify producer/consumer order

4. **Report findings**:
   - Tool references found
   - Missing tools (with suggestions)
   - Data flow issues
   - Recommendations

## Examples

```
/cv check-agent Planner
/cv check-agent Orchestrator ./CLAUDE.md
/cv check-agent data-analysis ~/project/CLAUDE.md
```
