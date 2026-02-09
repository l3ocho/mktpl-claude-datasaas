---
name: data
description: Data engineering tools — type /data <action> for commands
---

# /data

Data engineering tools with pandas, PostgreSQL/PostGIS, and dbt integration.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `ingest` | `/data-platform:data-ingest` | Load data from CSV, Parquet, JSON into DataFrame |
| `profile` | `/data-platform:data-profile` | Generate data profiling report with statistics |
| `schema` | `/data-platform:data-schema` | Explore database schemas, tables, columns |
| `explain` | `/data-platform:data-explain` | Explain query execution plan |
| `lineage` | `/data-platform:data-lineage` | Show dbt model lineage and dependencies |
| `lineage-viz` | `/data-platform:data-lineage-viz` | dbt lineage visualization as Mermaid diagrams |
| `run` | `/data-platform:data-run` | Run dbt models with validation |
| `dbt-test` | `/data-platform:data-dbt-test` | Formatted dbt test runner with summary |
| `quality` | `/data-platform:data-quality` | DataFrame quality checks |
| `review` | `/data-platform:data-review` | Comprehensive data integrity audits |
| `gate` | `/data-platform:data-gate` | Binary pass/fail data integrity gates |
| `setup` | `/data-platform:data-setup` | Setup wizard for data-platform MCP servers |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/data ingest`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/data-platform:data-ingest`)
