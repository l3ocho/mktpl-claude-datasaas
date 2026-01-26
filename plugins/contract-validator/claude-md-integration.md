# contract-validator Plugin - CLAUDE.md Integration

Add this section to your marketplace or project's CLAUDE.md to enable contract validation features.

## Suggested CLAUDE.md Section

```markdown
## Contract Validation

This marketplace uses the contract-validator plugin for cross-plugin compatibility checks.

### Available Commands

| Command | Purpose |
|---------|---------|
| `/validate-contracts` | Full marketplace compatibility validation |
| `/check-agent` | Validate single agent definition |
| `/list-interfaces` | Show all plugin interfaces |

### Validation Workflow

Run before merging plugin changes:

1. `/validate-contracts` - Check for conflicts
2. Review errors (must fix) and warnings (should review)
3. Fix issues before merging

### Interface Documentation Standards

For plugins to be validated correctly, document interfaces in README.md:

**Commands Section:**
```markdown
## Commands

| Command | Description |
|---------|-------------|
| `/my-command` | What it does |
```

**Tools Section:**
```markdown
## Tools Summary

### Category (N tools)
`tool_a`, `tool_b`, `tool_c`
```

**Agents Section:**
```markdown
## Agents

| Agent | Description |
|-------|-------------|
| `my-agent` | What it does |
```
```

## Declaring Agent Tool References

For agent validation to work, document tool usage in CLAUDE.md:

### Option 1: Four-Agent Model Table

```markdown
### Four-Agent Model

| Agent | Personality | Responsibilities |
|-------|-------------|------------------|
| **Planner** | Methodical | Planning via `create_issue`, `search_lessons` |
```

### Option 2: Agent Sections

```markdown
### Planner Agent

Uses these tools:
- `create_issue` - Create planning issues
- `search_lessons` - Find relevant lessons
```

## Best Practices for Plugin Authors

### Unique Command Names

Avoid generic names that may conflict:

```markdown
# BAD - Will conflict with other plugins
| `/setup` | Setup wizard |

# GOOD - Plugin-specific prefix
| `/data-setup` | Data platform setup wizard |
```

### Document All Tools

Ensure every MCP tool is listed in README.md:

```markdown
## Tools Summary

### pandas (14 tools)
`read_csv`, `read_parquet`, `read_json`, `to_csv`, `to_parquet`,
`describe`, `head`, `tail`, `filter`, `select`, `groupby`, `join`,
`list_data`, `drop_data`
```

### Specify Dependencies

If agents depend on tools from other plugins, document it:

```markdown
## Dependencies

This agent uses tools from:
- `projman` - Issue management (`create_issue`, `update_issue`)
- `data-platform` - Data loading (`read_csv`, `describe`)
```

## Typical Workflows

### Pre-Merge Validation

```
# Before merging new plugin
/validate-contracts

# Check specific agent after changes
/check-agent Orchestrator
```

### Plugin Development

```
# See what interfaces exist
/list-interfaces

# After adding new command, verify no conflicts
/validate-contracts
```

### CI/CD Integration

Add to your pipeline:

```yaml
- name: Validate Plugin Contracts
  run: |
    claude --skill contract-validator:validate-contracts --args "${{ github.workspace }}"
```
