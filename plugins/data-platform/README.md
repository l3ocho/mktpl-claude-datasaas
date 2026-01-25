# data-platform Plugin

Data engineering tools with pandas, PostgreSQL/PostGIS, and dbt integration for Claude Code.

## Features

- **pandas Operations**: Load, transform, and export DataFrames with persistent data_ref system
- **PostgreSQL/PostGIS**: Database queries with connection pooling and spatial data support
- **dbt Integration**: Build tool wrapper with pre-execution validation

## Installation

This plugin is part of the leo-claude-mktplace. Install via:

```bash
# From marketplace
claude plugins install leo-claude-mktplace/data-platform

# Setup MCP server venv
cd ~/.claude/plugins/marketplaces/leo-claude-mktplace/mcp-servers/data-platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

### PostgreSQL (Optional)

Create `~/.config/claude/postgres.env`:

```env
POSTGRES_URL=postgresql://user:password@host:5432/database
```

### dbt (Optional)

Add to project `.env`:

```env
DBT_PROJECT_DIR=/path/to/dbt/project
DBT_PROFILES_DIR=~/.dbt
```

## Commands

| Command | Description |
|---------|-------------|
| `/initial-setup` | Interactive setup wizard for PostgreSQL and dbt configuration |
| `/ingest` | Load data from files or database |
| `/profile` | Generate data profile and statistics |
| `/schema` | Show database/DataFrame schema |
| `/explain` | Explain dbt model lineage |
| `/lineage` | Visualize data dependencies |
| `/run` | Execute dbt models |

## Agents

| Agent | Description |
|-------|-------------|
| `data-ingestion` | Data loading and transformation specialist |
| `data-analysis` | Exploration and profiling specialist |

## data_ref System

All DataFrame operations use a `data_ref` system for persistence:

```
# Load returns a reference
read_csv("data.csv") → {"data_ref": "sales_data"}

# Use reference in subsequent operations
filter("sales_data", "amount > 100") → {"data_ref": "sales_data_filtered"}
describe("sales_data_filtered") → {statistics}
```

## Example Workflow

```
/ingest data/sales.csv
# → Loaded 50,000 rows as "sales_data"

/profile sales_data
# → Statistical summary, null counts, quality assessment

/schema orders
# → Column names, types, constraints

/lineage fct_orders
# → Dependency graph showing upstream/downstream models

/run dim_customers
# → Pre-validates then executes dbt model
```

## Tools Summary

### pandas (14 tools)
`read_csv`, `read_parquet`, `read_json`, `to_csv`, `to_parquet`, `describe`, `head`, `tail`, `filter`, `select`, `groupby`, `join`, `list_data`, `drop_data`

### PostgreSQL (6 tools)
`pg_connect`, `pg_query`, `pg_execute`, `pg_tables`, `pg_columns`, `pg_schemas`

### PostGIS (4 tools)
`st_tables`, `st_geometry_type`, `st_srid`, `st_extent`

### dbt (8 tools)
`dbt_parse`, `dbt_run`, `dbt_test`, `dbt_build`, `dbt_compile`, `dbt_ls`, `dbt_docs_generate`, `dbt_lineage`

## Memory Management

- Default limit: 100,000 rows per DataFrame
- Configure via `DATA_PLATFORM_MAX_ROWS` environment variable
- Use `chunk_size` parameter for large files
- Monitor with `list_data` tool

## SessionStart Hook

On session start, the plugin checks PostgreSQL connectivity and displays a warning if unavailable. This is non-blocking - pandas and dbt tools remain available.
