# /schema - Schema Exploration

## Skills to Load
- skills/mcp-tools-reference.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-PLATFORM - Schema Explorer`

## Usage

```
/schema [table_name | data_ref]
```

## Workflow

1. **Determine target**:
   - DataFrame: show pandas schema via `describe`
   - Database table: query via `pg_columns`
   - No argument: list all tables and DataFrames

2. **For DataFrames**: Show dtypes, null counts, sample values

3. **For database tables**: Show columns, types, constraints, indexes

4. **For PostGIS**: Include geometry type and SRID via `st_tables`

## Examples

```
/schema                    # List all tables and DataFrames
/schema customers          # Show table schema
/schema sales_data         # Show DataFrame schema
```

## Required MCP Tools

- `pg_tables` - List database tables
- `pg_columns` - Get column info
- `pg_schemas` - List schemas
- `st_tables` - List PostGIS tables
- `describe` - Get DataFrame info
- `list_data` - List DataFrames
