# /validate-contracts - Full Contract Validation

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  ✅ CONTRACT-VALIDATOR · Full Validation                         │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the validation.

Run comprehensive cross-plugin compatibility validation for the entire marketplace.

## Usage

```
/validate-contracts [marketplace_path]
```

## Parameters

- `marketplace_path` (optional): Path to marketplace root. Defaults to current project root.

## Workflow

1. **Discover plugins**:
   - Scan plugins directory for all plugins with `.claude-plugin/` marker
   - Parse each plugin's README.md to extract interface

2. **Run compatibility checks**:
   - Perform pairwise compatibility validation between all plugins
   - Check for command name conflicts
   - Check for tool name overlaps
   - Identify interface mismatches

3. **Validate CLAUDE.md agents**:
   - Parse agent definitions from CLAUDE.md
   - Validate all tool references exist
   - Check data flow through agent sequences

4. **Generate report**:
   - Summary statistics (plugins, commands, tools, issues)
   - Detailed findings by severity (error, warning, info)
   - Actionable suggestions for each issue

## Examples

```
/validate-contracts
/validate-contracts ~/claude-plugins-work
```

## Available Tools

Use these MCP tools:
- `generate_compatibility_report` - Generate full marketplace report
- `list_issues` - Filter issues by severity or type
- `parse_plugin_interface` - Parse individual plugin interface
- `validate_compatibility` - Check two plugins for conflicts
