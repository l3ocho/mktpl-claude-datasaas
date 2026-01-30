# /dependency-graph - Generate Dependency Visualization

## Skills to Load
- skills/visual-output.md
- skills/plugin-discovery.md
- skills/interface-parsing.md
- skills/dependency-analysis.md
- skills/mcp-tools-reference.md

## Usage

```
/dependency-graph [marketplace_path] [--format <mermaid|text>] [--show-tools]
```

## Parameters

- `marketplace_path` (optional): Path to marketplace root. Defaults to current project root.
- `--format` (optional): Output format - `mermaid` (default) or `text`
- `--show-tools` (optional): Include individual tool nodes in the graph

## Workflow

1. **Display header** per `skills/visual-output.md`

2. **Discover plugins** per `skills/plugin-discovery.md`

3. **Parse interfaces** per `skills/interface-parsing.md`
   - Use `parse_plugin_interface` for each plugin
   - Use `parse_claude_md_agents` for CLAUDE.md

4. **Analyze dependencies** per `skills/dependency-analysis.md`
   - Identify shared MCP servers
   - Detect data producers/consumers
   - Categorize as required or optional

5. **Generate output**:
   - Mermaid: Create flowchart TD diagram with styled edges
   - Text: Create text summary with counts and lists

## Examples

```
/dependency-graph
/dependency-graph --show-tools
/dependency-graph --format text
/dependency-graph ~/claude-plugins-work
```

## Integration

Use with `/validate-contracts`:
1. Run `/dependency-graph` to visualize
2. Run `/validate-contracts` to find issues
3. Fix and regenerate
