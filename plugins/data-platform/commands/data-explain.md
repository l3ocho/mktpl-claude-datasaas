---
name: data explain
---

# /data explain - dbt Model Explanation

## Skills to Load
- skills/dbt-workflow.md
- skills/lineage-analysis.md
- skills/mcp-tools-reference.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-PLATFORM - Model Explanation`

## Usage

```
/data explain <model_name>
```

## Workflow

1. **Get model info**: Use `dbt_lineage` for metadata (description, tags, materialization)
2. **Analyze dependencies**: Show upstream/downstream as tree
3. **Compile SQL**: Use `dbt_compile` to get rendered SQL
4. **Report**: Purpose, materialization, dependencies, key SQL logic

## Examples

```
/data explain dim_customers
/data explain fct_orders
```

## Required MCP Tools

- `dbt_lineage` - Get model dependencies
- `dbt_compile` - Get compiled SQL
- `dbt_ls` - List related resources
