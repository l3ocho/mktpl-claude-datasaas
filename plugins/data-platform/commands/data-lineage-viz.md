---
name: data lineage-viz
description: [data-platform] Visualize dataset lineage as a graph
---

# /data lineage-viz - Mermaid Lineage Visualization

## Skills to Load
- skills/lineage-analysis/SKILL.md
- skills/mcp-tools-reference/SKILL.md
- skills/visual-header/SKILL.md

## Visual Output

Display header: `DATA-PLATFORM - Lineage Visualization`

## Usage

```
/data lineage-viz <model_name> [--direction TB|LR] [--depth N]
```

## Workflow

1. **Get lineage data**: Use `dbt_lineage` to fetch model dependencies
2. **Build Mermaid graph**: Apply node shapes from `skills/lineage-analysis/SKILL.md`
3. **Output**: Render copy-paste ready Mermaid flowchart

## Options

| Flag | Description |
|------|-------------|
| `--direction TB` | Top-to-bottom layout (default: LR) |
| `--depth N` | Limit lineage depth |

## Examples

```
/data lineage-viz dim_customers
/data lineage-viz fct_orders --direction TB
/data lineage-viz rpt_revenue --depth 2
```

## Required MCP Tools

- `dbt_lineage` - Get model dependencies (REQUIRED)
- `dbt_ls` - List dbt resources
- `dbt_docs_generate` - Generate full manifest if needed
