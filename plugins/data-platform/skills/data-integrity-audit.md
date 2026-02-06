---
name: data-integrity-audit
description: Rules and patterns for auditing data integrity, schema validity, and dbt compliance
---

# Data Integrity Audit

## Purpose

Defines what "data valid" means for the data-platform domain. This skill is loaded by the `data-advisor` agent for both review and gate modes during sprint execution and standalone audits.

---

## What to Check

| Check Category | What It Validates | MCP Tools Used |
|----------------|-------------------|----------------|
| **Schema Validity** | Tables exist, columns have correct types, constraints present, no orphaned columns | `pg_tables`, `pg_columns`, `pg_schemas` |
| **dbt Project Health** | Project parses without errors, models compile, tests defined for critical models | `dbt_parse`, `dbt_compile`, `dbt_test`, `dbt_ls` |
| **Lineage Integrity** | No orphaned models (referenced but missing), no circular dependencies, upstream sources exist | `dbt_lineage`, `dbt_ls` |
| **Data Type Consistency** | DataFrame dtypes match expected schema, no silent type coercion, date formats consistent | `describe`, `head`, `pg_columns` |
| **PostGIS Compliance** | Spatial tables have correct SRID, geometry types match expectations, extent is reasonable | `st_tables`, `st_geometry_type`, `st_srid`, `st_extent` |
| **Query Safety** | SELECT queries used for reads (not raw SQL for mutations), parameterized patterns | Code review - manual pattern check |

---

## Common Violations

### FAIL-Level Violations (Block Gate)

| Violation | Detection Method | Example |
|-----------|-----------------|---------|
| dbt parse failure | `dbt_parse` returns error | Project YAML invalid, missing ref targets |
| dbt compilation error | `dbt_compile` fails | SQL syntax error, undefined column reference |
| Missing table/column | `pg_tables`, `pg_columns` lookup | Code references `census_raw` but table doesn't exist |
| Type mismatch | Compare `pg_columns` vs dbt schema | Column is `varchar` in DB but model expects `integer` |
| Broken lineage | `dbt_lineage` shows orphaned refs | Model references `stg_old_format` which doesn't exist |
| PostGIS SRID mismatch | `st_srid` returns unexpected value | Geometry column has SRID 0 instead of 4326 |
| Unreasonable spatial extent | `st_extent` returns global bbox | Toronto data shows coordinates in China |

### WARN-Level Violations (Report, Don't Block)

| Violation | Detection Method | Example |
|-----------|-----------------|---------|
| Missing dbt tests | `dbt_ls` shows model without test | `dim_customers` has no `unique` test on `customer_id` |
| Undocumented columns | dbt schema.yml missing descriptions | Model columns have no documentation |
| Schema drift | `pg_columns` vs dbt schema.yml | Column exists in DB but not in dbt YAML |
| Hardcoded SQL | Scan Python for string concatenation | `f"SELECT * FROM {table}"` without parameterization |
| Orphaned model | `dbt_lineage` shows no downstream | `stg_legacy` has no consumers and no exposure |

### INFO-Level Violations (Suggestions Only)

| Violation | Detection Method | Example |
|-----------|-----------------|---------|
| Missing indexes | Query pattern suggests need | Frequent filter on non-indexed column |
| Documentation gaps | dbt docs incomplete | Missing model description |
| Unused models | `dbt_ls` vs actual queries | Model exists but never selected |
| Optimization opportunity | `describe` shows data patterns | Column has low cardinality, could be enum |

---

## Severity Classification

| Severity | When to Apply | Gate Behavior |
|----------|--------------|---------------|
| **FAIL** | Broken lineage, models that won't compile, missing tables/columns, data type mismatches that cause runtime errors, invalid SRID | Blocks issue completion |
| **WARN** | Missing dbt tests, undocumented columns, schema drift, hardcoded SQL, orphaned models | Does NOT block gate, included in review report |
| **INFO** | Optimization opportunities, documentation gaps, unused models | Review report only |

### Severity Decision Tree

```
Is the dbt project broken (parse/compile fails)?
  YES -> FAIL
  NO -> Does code reference non-existent tables/columns?
    YES -> FAIL
    NO -> Would this cause a runtime error?
      YES -> FAIL
      NO -> Does it violate data quality standards?
        YES -> WARN
        NO -> Is it an optimization/documentation suggestion?
          YES -> INFO
          NO -> Not a violation
```

---

## Scanning Strategy

### For dbt Projects

1. **Parse validation** (ALWAYS FIRST)
   ```
   dbt_parse → if fails, immediate FAIL (project is broken)
   ```

2. **Catalog resources**
   ```
   dbt_ls → list all models, tests, sources, exposures
   ```

3. **Lineage check**
   ```
   dbt_lineage on changed models → check upstream/downstream integrity
   ```

4. **Compilation check**
   ```
   dbt_compile on changed models → verify SQL renders correctly
   ```

5. **Test execution**
   ```
   dbt_test --select <changed_models> → verify tests pass
   ```

6. **Test coverage audit**
   ```
   Cross-reference dbt_ls tests against model list → flag models without tests (WARN)
   ```

### For PostgreSQL Schema Changes

1. **Table verification**
   ```
   pg_tables → verify expected tables exist
   ```

2. **Column validation**
   ```
   pg_columns on affected tables → verify types match expectations
   ```

3. **Schema comparison**
   ```
   Compare pg_columns output against dbt schema.yml → flag drift
   ```

### For PostGIS/Spatial Data

1. **Spatial table scan**
   ```
   st_tables → list tables with geometry columns
   ```

2. **SRID validation**
   ```
   st_srid → verify SRID is correct for expected region
   Expected: 4326 (WGS84) for GPS data, local projections for regional data
   ```

3. **Geometry type check**
   ```
   st_geometry_type → verify expected types (Point, Polygon, etc.)
   ```

4. **Extent sanity check**
   ```
   st_extent → verify bounding box is reasonable for expected region
   Toronto data should be ~(-79.6 to -79.1, 43.6 to 43.9)
   ```

### For DataFrame/pandas Operations

1. **Data quality check**
   ```
   describe → check for unexpected nulls, type issues, outliers
   ```

2. **Structure verification**
   ```
   head → verify data structure matches expectations
   ```

3. **Memory management**
   ```
   list_data → verify no stale DataFrames from previous failed runs
   ```

### For Python Code (Manual Scan)

1. **SQL injection patterns**
   - Scan for f-strings with table/column names
   - Check for string concatenation in queries
   - Look for `.format()` calls with SQL

2. **Mutation safety**
   - `pg_execute` usage should be intentional, not accidental
   - Verify DELETE/UPDATE have WHERE clauses

3. **Credential exposure**
   - No hardcoded connection strings
   - No credentials in code (check for `.env` usage)

---

## Report Templates

### Gate Mode (Compact)

```
DATA GATE: PASS
No blocking data integrity violations found.
```

or

```
DATA GATE: FAIL

Blocking Issues (N):
1. <location> - <violation description>
   Fix: <actionable fix>

2. <location> - <violation description>
   Fix: <actionable fix>

Run /data review for full audit report.
```

### Review Mode (Detailed)

```
+----------------------------------------------------------------------+
|  DATA-PLATFORM - Data Integrity Audit                                 |
|  [Target Path]                                                        |
+----------------------------------------------------------------------+

Target: <scanned path or project>
Scope: N files scanned, N models checked, N tables verified

FINDINGS

FAIL (N)
  1. [location] violation description
     Fix: actionable fix

  2. [location] violation description
     Fix: actionable fix

WARN (N)
  1. [location] warning description
     Suggestion: improvement suggestion

  2. [location] warning description
     Suggestion: improvement suggestion

INFO (N)
  1. [location] info description
     Note: context

SUMMARY
  Schema:   Valid | N issues
  Lineage:  Intact | N orphaned
  dbt:      Passes | N failures
  PostGIS:  Valid | N issues | Not applicable

VERDICT: PASS | FAIL (N blocking issues)
```

---

## Skip Patterns

Do not flag violations in:

- `**/tests/**` - Test files may have intentional violations
- `**/__pycache__/**` - Compiled files
- `**/fixtures/**` - Test fixtures
- `**/.scratch/**` - Temporary working files
- Files with `# noqa: data-audit` comment
- Migration files marked as historical

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Database not reachable (`pg_connect` fails) | WARN, skip PostgreSQL checks, continue with file-based |
| dbt not configured (no `dbt_project.yml`) | Skip dbt checks entirely, not an error |
| No PostGIS tables found | Skip PostGIS checks, not an error |
| MCP tool call fails | Report as WARN with tool name, continue with remaining checks |
| No data files in scanned path | Report "No data artifacts found" - PASS (nothing to fail) |
| Empty directory | Report "No files found in path" - PASS |

---

## Integration Notes

### projman Orchestrator

When called as a domain gate:
1. Orchestrator detects `Domain/Data` label on issue
2. Orchestrator identifies changed files
3. Orchestrator invokes `/data gate <path>`
4. Agent runs gate mode scan
5. Returns PASS/FAIL to orchestrator
6. Orchestrator decides whether to complete issue

### Standalone Usage

For manual audits:
1. User runs `/data review <path>`
2. Agent runs full review mode scan
3. Returns detailed report with all severity levels
4. User decides on actions
