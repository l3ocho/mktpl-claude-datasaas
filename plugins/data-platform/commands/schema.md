# /schema - Schema Exploration

Display schema information for database tables or DataFrames.

## Usage

```
/schema [table_name | data_ref]
```

## Workflow

1. **Determine target**:
   - If argument is a loaded data_ref, show DataFrame schema
   - If argument is a table name, query database schema
   - If no argument, list all available tables and DataFrames

2. **For DataFrames**:
   - Use `describe` to get column info
   - Show dtypes, null counts, sample values

3. **For database tables**:
   - Use `pg_columns` for column details
   - Use `st_tables` to check for PostGIS columns
   - Show constraints and indexes if available

4. **Report**:
   - Column name, type, nullable, default
   - For PostGIS: geometry type, SRID
   - For DataFrames: pandas dtype, null percentage

## Examples

```
/schema                    # List all tables and DataFrames
/schema customers          # Show table schema
/schema sales_data         # Show DataFrame schema
```

## Available Tools

Use these MCP tools:
- `pg_tables` - List database tables
- `pg_columns` - Get column info
- `pg_schemas` - List schemas
- `st_tables` - List PostGIS tables
- `describe` - Get DataFrame info
- `list_data` - List DataFrames
