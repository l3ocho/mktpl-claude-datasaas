# /data-ingest - Data Ingestion

## Skills to Load
- skills/mcp-tools-reference.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-PLATFORM - Ingest`

## Usage

```
/data-ingest [source]
```

## Workflow

1. **Identify source**:
   - File path: determine format (CSV, Parquet, JSON)
   - SQL query or table name: query PostgreSQL

2. **Load data**:
   - Files: `read_csv`, `read_parquet`, `read_json`
   - Database: `pg_query`

3. **Validate**: Check row count against 100k limit

4. **Report**: data_ref, row count, columns, memory usage, preview

## Examples

```
/data-ingest data/sales.csv
/data-ingest data/customers.parquet
/data-ingest "SELECT * FROM orders WHERE created_at > '2024-01-01'"
```

## Required MCP Tools

- `read_csv` - Load CSV files
- `read_parquet` - Load Parquet files
- `read_json` - Load JSON/JSONL files
- `pg_query` - Query PostgreSQL database
- `list_data` - List loaded DataFrames
