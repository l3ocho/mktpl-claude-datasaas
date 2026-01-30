# Skill: Dependency Analysis

Analyze dependencies between plugins including shared MCP servers and data flows.

## Dependency Types

| Type | Line Style | Meaning |
|------|------------|---------|
| Required | Solid (`-->`) | Plugin cannot function without this |
| Optional | Dashed (`-.->`) | Plugin works with reduced functionality |
| Internal | Dotted (`...>`) | Self-dependency within same plugin |
| Shared MCP | Double (`==>`) | Plugins share same MCP server instance |

## Shared MCP Server Detection

Check each plugin's `.mcp.json` for server definitions. Plugins with identical MCP server names share that server.

**Common shared servers:**
- `gitea` - Used by projman, pr-review
- `netbox` - Used by cmdb-assistant
- `data-platform` - Used by data-platform
- `viz-platform` - Used by viz-platform

## Data Flow Patterns

### Data Producers
- `read_csv`, `read_parquet`, `read_json` - File loaders
- `pg_query`, `pg_execute` - Database queries
- `filter`, `select`, `groupby`, `join` - Transformations

### Data Consumers
- `describe`, `head`, `tail` - Data inspection
- `to_csv`, `to_parquet` - File writers
- `chart_create` - Visualization

### Cross-Plugin Flows
| Producer | Consumer | Data Type |
|----------|----------|-----------|
| data-platform | viz-platform | `data_ref` |
| projman | pr-review | issues/lessons |
| gitea wiki | projman | lessons learned |

## Required vs Optional

- **Required**: Consumer has no default/fallback (ERROR if missing)
- **Optional**: Consumer works without producer (WARNING if missing)

Determined by:
- Issue severity from `validate_data_flow`
- Tool docs stating "requires" vs "uses if available"

## MCP Tools

| Tool | Purpose |
|------|---------|
| `validate_data_flow` | Verify producer/consumer relationships |
| `generate_compatibility_report` | Get full dependency data |
