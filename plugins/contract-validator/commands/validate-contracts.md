# /validate-contracts - Full Contract Validation

## Skills to Load
- skills/visual-output.md
- skills/plugin-discovery.md
- skills/interface-parsing.md
- skills/validation-rules.md
- skills/mcp-tools-reference.md

## Usage

```
/validate-contracts [marketplace_path]
```

## Parameters

- `marketplace_path` (optional): Path to marketplace root. Defaults to current project root.

## Workflow

1. **Display header** per `skills/visual-output.md`

2. **Discover plugins** per `skills/plugin-discovery.md`

3. **Parse interfaces** per `skills/interface-parsing.md`
   - Use `parse_plugin_interface` for each plugin

4. **Run validations** per `skills/validation-rules.md`
   - Use `validate_compatibility` for pairwise checks
   - Use `validate_agent_refs` for CLAUDE.md agents
   - Use `validate_data_flow` for data sequences
   - Use `validate_workflow_integration` for domain plugin advisory interfaces

5. **Generate report**:
   - Use `generate_compatibility_report` for full report
   - Use `list_issues` to filter by severity
   - Display summary and actionable suggestions

## Examples

```
/validate-contracts
/validate-contracts ~/claude-plugins-work
```
