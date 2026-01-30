---
description: Generate infrastructure topology diagrams from NetBox data
---

# CMDB Topology Visualization

Generate Mermaid diagrams showing infrastructure topology from NetBox.

## Skills to Load

- `skills/visual-header.md`
- `skills/topology-generation.md`
- `skills/mcp-tools-reference.md`

## Usage

```
/cmdb-topology <view> [scope]
```

**Views:**
- `rack <rack-name>` - Rack elevation showing devices and positions
- `network [site]` - Network topology showing device connections
- `site <site-name>` - Site overview with racks and device counts
- `full` - Full infrastructure overview

## Instructions

Execute `skills/visual-header.md` with context "Topology".

Execute `skills/topology-generation.md` which covers:
- Data collection via MCP for each view type
- Mermaid diagram generation with proper shapes
- Legend and data notes

## Output Format

Always provide:
1. **Summary** - Brief description
2. **Mermaid Code Block** - The diagram
3. **Legend** - Shape explanations
4. **Data Notes** - Quality issues found

## Examples

- `/cmdb-topology rack server-rack-01` - Rack elevation
- `/cmdb-topology network` - All network connections
- `/cmdb-topology network Home` - Network for Home site
- `/cmdb-topology site Headquarters` - Site overview
- `/cmdb-topology full` - Full infrastructure

## User Request

$ARGUMENTS
