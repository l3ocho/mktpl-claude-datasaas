# Data Platform MCP Server

MCP Server providing pandas, PostgreSQL/PostGIS, and dbt tools for Claude Code.

## Features

- **pandas Tools**: DataFrame operations with Arrow IPC data_ref persistence
- **PostgreSQL Tools**: Database queries with asyncpg connection pooling
- **PostGIS Tools**: Spatial data operations
- **dbt Tools**: Build tool wrapper with pre-execution validation

## Installation

```bash
cd mcp-servers/data-platform
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

### System-Level (PostgreSQL credentials)

Create `~/.config/claude/postgres.env`:

```env
POSTGRES_URL=postgresql://user:password@host:5432/database
```

### Project-Level (dbt paths)

Create `.env` in your project root:

```env
DBT_PROJECT_DIR=/path/to/dbt/project
DBT_PROFILES_DIR=/path/to/.dbt
DATA_PLATFORM_MAX_ROWS=100000
```

## Tools

### pandas Tools (14 tools)

| Tool | Description |
|------|-------------|
| `read_csv` | Load CSV file into DataFrame |
| `read_parquet` | Load Parquet file into DataFrame |
| `read_json` | Load JSON/JSONL file into DataFrame |
| `to_csv` | Export DataFrame to CSV file |
| `to_parquet` | Export DataFrame to Parquet file |
| `describe` | Get statistical summary of DataFrame |
| `head` | Get first N rows of DataFrame |
| `tail` | Get last N rows of DataFrame |
| `filter` | Filter DataFrame rows by condition |
| `select` | Select specific columns from DataFrame |
| `groupby` | Group DataFrame and aggregate |
| `join` | Join two DataFrames |
| `list_data` | List all stored DataFrames |
| `drop_data` | Remove a DataFrame from storage |

### PostgreSQL Tools (6 tools)

| Tool | Description |
|------|-------------|
| `pg_connect` | Test connection and return status |
| `pg_query` | Execute SELECT, return as data_ref |
| `pg_execute` | Execute INSERT/UPDATE/DELETE |
| `pg_tables` | List all tables in schema |
| `pg_columns` | Get column info for table |
| `pg_schemas` | List all schemas |

### PostGIS Tools (4 tools)

| Tool | Description |
|------|-------------|
| `st_tables` | List PostGIS-enabled tables |
| `st_geometry_type` | Get geometry type of column |
| `st_srid` | Get SRID of geometry column |
| `st_extent` | Get bounding box of geometries |

### dbt Tools (8 tools)

| Tool | Description |
|------|-------------|
| `dbt_parse` | Validate project (pre-execution) |
| `dbt_run` | Run models with selection |
| `dbt_test` | Run tests |
| `dbt_build` | Run + test |
| `dbt_compile` | Compile SQL without executing |
| `dbt_ls` | List resources |
| `dbt_docs_generate` | Generate documentation |
| `dbt_lineage` | Get model dependencies |

## data_ref System

All DataFrame operations use a `data_ref` system to persist data across tool calls:

1. **Load data**: Returns a `data_ref` string (e.g., `"df_a1b2c3d4"`)
2. **Use data_ref**: Pass to other tools (filter, join, export)
3. **List data**: Use `list_data` to see all stored DataFrames
4. **Clean up**: Use `drop_data` when done

### Example Flow

```
read_csv("data.csv") → {"data_ref": "sales_data", "rows": 1000}
filter("sales_data", "amount > 100") → {"data_ref": "sales_data_filtered"}
describe("sales_data_filtered") → {statistics}
to_parquet("sales_data_filtered", "output.parquet") → {success}
```

## Memory Management

- Default row limit: 100,000 rows per DataFrame
- Configure via `DATA_PLATFORM_MAX_ROWS` environment variable
- Use chunked processing for large files (`chunk_size` parameter)
- Monitor with `list_data` tool (shows memory usage)

## Running

```bash
python -m mcp_server.server
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
