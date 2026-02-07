---
name: data gate
description: Data integrity compliance gate (pass/fail) for sprint execution
gate_contract: v1
arguments:
  - name: path
    description: File or directory to validate
    required: true
---

# /data gate

Binary pass/fail validation for data integrity compliance. Used by projman orchestrator during sprint execution to gate issue completion.

## Usage

```
/data gate <path>
```

**Examples:**
```
/data gate ./dbt/models/staging/
/data gate ./portfolio_app/toronto/parsers/
/data gate ./dbt/
```

## What It Does

1. **Activates** the `data-advisor` agent in gate mode
2. **Loads** the `skills/data-integrity-audit.md` skill
3. **Determines scope** from target path:
   - dbt project directory: full dbt validation (parse, compile, test, lineage)
   - Python files with database operations: schema validation
   - SQL files: dbt model validation
   - Mixed: all applicable checks
4. **Checks only FAIL-level violations:**
   - dbt parse failures (project broken)
   - dbt compilation errors (SQL invalid)
   - Missing tables/columns referenced in code
   - Data type mismatches that cause runtime errors
   - Broken lineage (orphaned model references)
   - PostGIS SRID mismatches
5. **Returns binary result:**
   - `PASS` - No blocking violations found
   - `FAIL` - One or more blocking violations

## Output

### On PASS
```
DATA GATE: PASS
No blocking data integrity violations found.
```

### On FAIL
```
DATA GATE: FAIL

Blocking Issues (2):
1. dbt/models/staging/stg_census.sql - Compilation error: column 'census_yr' not found
   Fix: Column was renamed to 'census_year' in source table. Update model.

2. portfolio_app/toronto/loaders/census.py:67 - References table 'census_raw' which does not exist
   Fix: Table was renamed to 'census_demographics' in migration 003.

Run /data review for full audit report.
```

## Integration with projman

This command is automatically invoked by the projman orchestrator when:

1. An issue has the `Domain/Data` label
2. The orchestrator is about to mark the issue as complete
3. The orchestrator passes the path of changed files

**Gate behavior:**
- PASS: Issue can be marked complete
- FAIL: Issue stays open, blocker comment added with failure details

## Differences from /data review

| Aspect | /data gate | /data review |
|--------|------------|--------------|
| Output | Binary PASS/FAIL | Detailed report with all severities |
| Severity | FAIL only | FAIL + WARN + INFO |
| Purpose | Automation gate | Human review |
| Verbosity | Minimal | Comprehensive |
| Speed | Skips INFO checks | Full scan |

## When to Use

- **Sprint execution**: Automatic quality gates via projman
- **CI/CD pipelines**: Automated data integrity checks
- **Quick validation**: Fast pass/fail without full report
- **Pre-merge checks**: Verify data changes before integration

For detailed findings including warnings and suggestions, use `/data review` instead.

## Requirements

- data-platform MCP server must be running
- For dbt checks: dbt project must be configured (auto-detected via `dbt_project.yml`)
- For PostgreSQL checks: connection configured in `~/.config/claude/postgres.env`
- If database or dbt unavailable: applicable checks skipped with warning (non-blocking degradation)
