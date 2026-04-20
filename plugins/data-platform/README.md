# data-platform

Data engineering toolkit for Claude Code: pandas, PostgreSQL/PostGIS, and dbt — wired up via an MCP server that gives Claude real tools, not just instructions.

## What it does

- Read and profile CSV / Parquet / pandas DataFrames
- Query PostgreSQL (and PostGIS for geospatial) with connection + column helpers
- Compile, parse, and lineage-analyze dbt projects
- Run data-quality gates

## Commands

| Command | Purpose |
|---|---|
| `/data setup` | Initialize project config |
| `/data ingest` | Ingest CSV/Parquet |
| `/data profile` | Profile a dataset (nulls, uniqueness, types) |
| `/data schema` | Extract dataset schema |
| `/data explain` | Explain SQL / pandas code |
| `/data quality` | Quality gates |
| `/data gate` | Hard-block on quality issues |
| `/data review` | Review a data pipeline |
| `/data run` | Run a dbt / pandas / SQL job |
| `/data lineage`, `/data lineage-viz` | Dataset lineage and visualization |
| `/data dbt-test` | `dbt test` with grouped output |

## Agents (3)

| Agent | Model | Role |
|---|---|---|
| `data-advisor` | sonnet | End-to-end data pipeline advice |
| `data-analysis` | sonnet (plan mode) | Read-only dataset analysis |
| `data-ingestion` | haiku | Fast ingestion scaffolding |

## MCP server

`mcp-servers/data-platform/` — real tools (`read_csv`, `read_parquet`, `pg_connect`, `pg_columns`, `st_tables`, `dbt_parse`, `dbt_compile`, `dbt_lineage`, etc.). The MCP is what makes this plugin worth having — without it, the commands would be prescriptive text.

## Configuration

`POSTGRES_URL` in `~/.config/claude/postgres.env` if you want PG tools; pandas/dbt tools work without it.
