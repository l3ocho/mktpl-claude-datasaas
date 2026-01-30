# Skill: Validation Rules

Rules for validating plugin compatibility and agent definitions.

## Compatibility Checks

### 1. Command Name Conflicts
- No two plugins should have identical command names
- Severity: ERROR

### 2. Tool Name Overlaps
- Tools with same name must have same signature
- Severity: WARNING (may be intentional aliasing)

### 3. Interface Mismatches
- Producer output types must match consumer input types
- Severity: ERROR

## Agent Validation

### Tool Reference Check
1. Parse agent's tool references from workflow steps
2. Verify each tool exists in available plugins
3. Report missing or misspelled tool names
4. Suggest corrections for common mistakes

### Data Flow Validation
1. Analyze sequence of tools in agent workflow
2. Verify data producers precede data consumers
3. Check for orphaned data references
4. Ensure required data is available at each step

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| ERROR | Will cause runtime failures | Must fix |
| WARNING | May cause issues | Review needed |
| INFO | Informational only | No action required |

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Missing tool | Typo or plugin not installed | Check spelling, install plugin |
| Data flow gap | Producer not called before consumer | Reorder workflow steps |
| Name conflict | Two plugins use same command | Rename one command |
| Orphan reference | Data produced but never consumed | Remove or use the data |

## MCP Tools

| Tool | Purpose |
|------|---------|
| `validate_compatibility` | Check two plugins for conflicts |
| `validate_agent_refs` | Check agent tool references |
| `validate_data_flow` | Verify data flow sequences |
| `list_issues` | Filter issues by severity or type |
