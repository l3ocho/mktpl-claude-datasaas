# data-platform Plugin — CLAUDE.md Integration

Install with: `./scripts/install-plugin.sh data-platform <target> [--profile default|readonly]`

Profiles:
- **default** — Full access: read/write database, dbt operations, data ingestion
- **readonly** — Read-only: schema exploration and query only (for webapp consumers)

<!-- BEGIN data-platform:default -->

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
| `/data lineage-viz` | Visual lineage diagram |
| `/data run` | Execute dbt models |
| `/data dbt-test` | Run dbt tests |
| `/data quality` | Data quality checks |
| `/data review` | Comprehensive data audit |
| `/data gate` | Pass/fail data quality gate |

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

### Environment Variables

```env
# dbt configuration
DBT_PROJECT_DIR=./transform
DBT_PROFILES_DIR=~/.dbt

# Memory limits
DATA_PLATFORM_MAX_ROWS=100000
```

<!-- END data-platform:default -->

<!-- BEGIN data-platform:readonly -->

## Data Platform Integration (Read-Only)

This project consumes data produced by a separate data pipeline. Database access is **read-only** — no write operations, no dbt execution.

### Configuration

**PostgreSQL**: Credentials in `~/.config/claude/postgres.env`

### Available Commands

| Command | Purpose |
|---------|---------|
| `/data schema` | Show schema information |

### Database Access (Read-Only)

PostgreSQL tools available (read-only):
- Queries: `pg_query`
- Schema exploration: `pg_tables`, `pg_columns`, `pg_schemas`

PostGIS spatial data:
- List spatial tables: `st_tables`
- Check geometry: `st_geometry_type`, `st_srid`, `st_extent`

### ⛔ Not Available in This Profile

The following are **not available** in read-only mode. Use the data pipeline repository for these operations:
- `pg_execute` (write operations)
- All `dbt_*` tools (dbt_parse, dbt_run, dbt_test, dbt_build, dbt_compile, dbt_ls, dbt_lineage, dbt_docs_generate)
- `/data ingest`, `/data profile`, `/data explain`, `/data lineage`, `/data run`, `/data dbt-test`, `/data quality`, `/data review`, `/data gate`
- `DBT_PROJECT_DIR` environment variable

### Environment Variables

```env
# No dbt configuration needed — this project does not run dbt
# DATA_PLATFORM_MAX_ROWS=100000  # Optional: limit query results
```

<!-- END data-platform:readonly -->
