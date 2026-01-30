# Skill: Interface Parsing

Parse plugin interfaces from README.md and agent definitions from CLAUDE.md.

## Interface Components

| Component | Source | Description |
|-----------|--------|-------------|
| Commands | README.md | Slash commands offered by plugin |
| Agents | README.md, CLAUDE.md | Autonomous agents defined |
| Tools | README.md | MCP tools provided |
| Categories | README.md | Tool groupings and features |

## Parsing README.md

Extract from these sections:

1. **Commands section**: Look for tables with `| Command |` or lists of `/command-name`
2. **Tools section**: Look for tables with `| Tool |` or code blocks with tool names
3. **Agents section**: Look for "Four-Agent Model" or "Agents" headings

## Parsing CLAUDE.md

Extract agent definitions from:

1. **Four-Agent Model table**: `| Agent | Personality | Responsibilities |`
2. **Agent sections**: Headings like `### Planner Agent` or `## Agents`
3. **Tool sequences**: Lists of tools in workflow steps

## Agent Definition Structure

```yaml
agent:
  name: "Planner"
  personality: "Thoughtful, methodical"
  responsibilities:
    - "Sprint planning"
    - "Architecture analysis"
  tools:
    - "create_issue"
    - "search_lessons"
  workflow:
    - step: "Analyze requirements"
      tools: ["list_issues", "get_issue"]
```

## MCP Tools

| Tool | Purpose |
|------|---------|
| `parse_plugin_interface` | Extract interface from README.md |
| `parse_claude_md_agents` | Extract agents and tool sequences from CLAUDE.md |
