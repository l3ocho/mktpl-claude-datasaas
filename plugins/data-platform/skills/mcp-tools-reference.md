# MCP Tools Reference

## pandas Tools

| Tool | Description |
|------|-------------|
| `read_csv` | Load CSV file into DataFrame |
| `read_parquet` | Load Parquet file into DataFrame |
| `read_json` | Load JSON/JSONL file into DataFrame |
| `to_csv` | Export DataFrame to CSV |
| `to_parquet` | Export DataFrame to Parquet |
| `describe` | Get statistical summary (count, mean, std, min, max) |
| `head` | Preview first N rows |
| `tail` | Preview last N rows |
| `filter` | Filter rows by condition |
| `select` | Select specific columns |
| `groupby` | Aggregate data by columns |
| `join` | Join two DataFrames |
| `list_data` | List all loaded DataFrames |
| `drop_data` | Remove DataFrame from memory |

## PostgreSQL Tools

| Tool | Description |
|------|-------------|
| `pg_connect` | Establish database connection |
| `pg_query` | Execute SELECT query, return DataFrame |
| `pg_execute` | Execute INSERT/UPDATE/DELETE |
| `pg_tables` | List tables in schema |
| `pg_columns` | Get column info for table |
| `pg_schemas` | List available schemas |

## PostGIS Tools

| Tool | Description |
|------|-------------|
| `st_tables` | List tables with geometry columns |
| `st_geometry_type` | Get geometry type for column |
| `st_srid` | Get SRID for geometry column |
| `st_extent` | Get bounding box for geometry |

## dbt Tools

| Tool | Description |
|------|-------------|
| `dbt_parse` | Validate project (ALWAYS RUN FIRST) |
| `dbt_run` | Execute models |
| `dbt_test` | Run tests |
| `dbt_build` | Run + test together |
| `dbt_compile` | Compile SQL without execution |
| `dbt_ls` | List dbt resources |
| `dbt_docs_generate` | Generate documentation manifest |
| `dbt_lineage` | Get model dependencies |

## Tool Selection Guidelines

**For data loading:**
- Files: `read_csv`, `read_parquet`, `read_json`
- Database: `pg_query`

**For data exploration:**
- Schema: `describe`, `pg_columns`, `st_tables`
- Preview: `head`, `tail`
- Available data: `list_data`, `pg_tables`

**For dbt operations:**
- Always start with `dbt_parse` for validation
- Use `dbt_lineage` for dependency analysis
- Use `dbt_compile` to see rendered SQL
