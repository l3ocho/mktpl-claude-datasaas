# /ingest - Data Ingestion

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  📊 DATA-PLATFORM · Ingest                                        │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the ingestion.

Load data from files or database into the data platform.

## Usage

```
/ingest [source]
```

## Workflow

1. **Identify data source**:
   - If source is a file path, determine format (CSV, Parquet, JSON)
   - If source is "db" or a table name, query PostgreSQL

2. **Load data**:
   - For files: Use `read_csv`, `read_parquet`, or `read_json`
   - For database: Use `pg_query` with appropriate SELECT

3. **Validate**:
   - Check row count against limits
   - If exceeds 100k rows, suggest chunking or filtering

4. **Report**:
   - Show data_ref, row count, columns, and memory usage
   - Preview first few rows

## Examples

```
/ingest data/sales.csv
/ingest data/customers.parquet
/ingest "SELECT * FROM orders WHERE created_at > '2024-01-01'"
```

## Available Tools

Use these MCP tools:
- `read_csv` - Load CSV files
- `read_parquet` - Load Parquet files
- `read_json` - Load JSON/JSONL files
- `pg_query` - Query PostgreSQL database
- `list_data` - List loaded DataFrames
