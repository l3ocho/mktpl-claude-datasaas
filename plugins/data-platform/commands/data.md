---
name: data
description: Data engineering tools — type /data <action> for commands
---

# /data

Data engineering tools with pandas, PostgreSQL/PostGIS, and dbt integration.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|-------------|-------------|
| `/data ingest` | Load data from CSV, Parquet, JSON into DataFrame |
| `/data profile` | Generate data profiling report with statistics |
| `/data schema` | Explore database schemas, tables, columns |
| `/data explain` | Explain query execution plan |
| `/data lineage` | Show dbt model lineage and dependencies |
| `/data lineage-viz` | dbt lineage visualization as Mermaid diagrams |
| `/data run` | Run dbt models with validation |
| `/data dbt-test` | Formatted dbt test runner with summary |
| `/data quality` | DataFrame quality checks |
| `/data review` | Comprehensive data integrity audits |
| `/data gate` | Binary pass/fail data integrity gates |
| `/data setup` | Setup wizard for data-platform MCP servers |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
