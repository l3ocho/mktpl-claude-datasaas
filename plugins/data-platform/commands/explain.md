# /explain - dbt Model Explanation

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  📊 DATA-PLATFORM · Model Explanation                             │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the explanation.

Explain a dbt model's purpose, dependencies, and SQL logic.

## Usage

```
/explain <model_name>
```

## Workflow

1. **Get model info**:
   - Use `dbt_lineage` to get model metadata
   - Extract description, tags, materialization

2. **Analyze dependencies**:
   - Show upstream models (what this depends on)
   - Show downstream models (what depends on this)
   - Visualize as dependency tree

3. **Compile SQL**:
   - Use `dbt_compile` to get rendered SQL
   - Explain key transformations

4. **Report**:
   - Model purpose (from description)
   - Materialization strategy
   - Dependency graph
   - Key SQL logic explained

## Examples

```
/explain dim_customers
/explain fct_orders
```

## Available Tools

Use these MCP tools:
- `dbt_lineage` - Get model dependencies
- `dbt_compile` - Get compiled SQL
- `dbt_ls` - List related resources
