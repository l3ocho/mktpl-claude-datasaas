---
name: data explain
description: [data-platform] Explain SQL or pandas code
---

# /data explain - dbt Model Explanation

## Skills to Load
- skills/dbt-workflow/SKILL.md
- skills/lineage-analysis/SKILL.md
- skills/mcp-tools-reference/SKILL.md
- skills/visual-header/SKILL.md

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
