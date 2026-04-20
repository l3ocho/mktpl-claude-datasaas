---
name: data lineage
---

# /data lineage - Data Lineage Visualization

## Skills to Load
- skills/lineage-analysis/SKILL.md
- skills/mcp-tools-reference/SKILL.md
- skills/visual-header/SKILL.md

## Visual Output

Display header: `DATA-PLATFORM - Lineage`

## Usage

```
/data lineage <model_name> [--depth N]
```

## Workflow

1. **Get lineage data**: Use `dbt_lineage` for dbt models
2. **Build lineage graph**: Identify upstream sources and downstream consumers
3. **Visualize**: ASCII tree with depth levels (see `skills/lineage-analysis/SKILL.md`)
4. **Report**: Full dependency chain and refresh implications

## Examples

```
/data lineage dim_customers
/data lineage fct_orders --depth 3
```

## Required MCP Tools

- `dbt_lineage` - Get model dependencies
- `dbt_ls` - List dbt resources
- `dbt_docs_generate` - Generate full manifest
