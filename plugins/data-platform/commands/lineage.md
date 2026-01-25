# /lineage - Data Lineage Visualization

Show data lineage for dbt models or database tables.

## Usage

```
/lineage <model_name> [--depth N]
```

## Workflow

1. **Get lineage data**:
   - Use `dbt_lineage` for dbt models
   - For database tables, trace through dbt manifest

2. **Build lineage graph**:
   - Identify all upstream sources
   - Identify all downstream consumers
   - Note materialization at each node

3. **Visualize**:
   - ASCII art dependency tree
   - List format with indentation
   - Show depth levels

4. **Report**:
   - Full dependency chain
   - Critical path identification
   - Refresh implications

## Examples

```
/lineage dim_customers
/lineage fct_orders --depth 3
```

## Output Format

```
Sources:
  └── raw_customers (source)
  └── raw_orders (source)

dim_customers (table)
  ├── upstream:
  │   └── stg_customers (view)
  │       └── raw_customers (source)
  └── downstream:
      └── fct_orders (incremental)
      └── rpt_customer_lifetime (table)
```

## Available Tools

Use these MCP tools:
- `dbt_lineage` - Get model dependencies
- `dbt_ls` - List dbt resources
- `dbt_docs_generate` - Generate full manifest
