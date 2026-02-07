# data-platform Plugin - CLAUDE.md Integration

Add this section to your project's CLAUDE.md to enable data-platform plugin features.

## Suggested CLAUDE.md Section

```markdown
## Data Platform Integration

This project uses the data-platform plugin for data engineering workflows.

### Configuration

**PostgreSQL**: Credentials in `~/.config/claude/postgres.env`
**dbt**: Project path auto-detected from `dbt_project.yml`

### Available Commands

| Command | Purpose |
|---------|---------|
| `/data ingest` | Load data from files or database |
| `/data profile` | Generate statistical profile |
| `/data schema` | Show schema information |
| `/data explain` | Explain dbt model |
| `/data lineage` | Show data lineage |
| `/data run` | Execute dbt models |

### data_ref Convention

DataFrames are stored with references. Use meaningful names:
- `raw_*` for source data
- `stg_*` for staged/cleaned data
- `dim_*` for dimension tables
- `fct_*` for fact tables
- `rpt_*` for reports

### dbt Workflow

1. Always validate before running: `/data run` includes automatic `dbt_parse`
2. For dbt 1.9+, check for deprecated syntax before commits
3. Use `/data lineage` to understand impact of changes

### Database Access

PostgreSQL tools require POSTGRES_URL configuration:
- Read-only queries: `pg_query`
- Write operations: `pg_execute`
- Schema exploration: `pg_tables`, `pg_columns`

PostGIS spatial data:
- List spatial tables: `st_tables`
- Check geometry: `st_geometry_type`, `st_srid`, `st_extent`
```

## Environment Variables

Add to project `.env` if needed:

```env
# dbt configuration
DBT_PROJECT_DIR=./transform
DBT_PROFILES_DIR=~/.dbt

# Memory limits
DATA_PLATFORM_MAX_ROWS=100000
```

## Typical Workflows

### Data Exploration
```
/data ingest data/raw_customers.csv
/data profile raw_customers
/data schema
```

### ETL Development
```
/data schema orders              # Understand source
/data explain stg_orders         # Understand transformation
/data run stg_orders             # Test the model
/data lineage fct_orders         # Check downstream impact
```

### Database Analysis
```
/data schema                     # List all tables
pg_columns orders           # Detailed schema
st_tables                   # Find spatial data
```
