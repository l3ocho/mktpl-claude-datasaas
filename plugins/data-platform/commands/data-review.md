---
description: Audit data integrity, schema validity, and dbt compliance
arguments:
  - name: path
    description: File, directory, or dbt project to audit
    required: true
---

# /data-review

Comprehensive data integrity audit producing a detailed report with findings at all severity levels. For human review and standalone codebase auditing.

## Usage

```
/data-review <path>
```

**Examples:**
```
/data-review ./dbt/
/data-review ./portfolio_app/toronto/
/data-review ./dbt/models/marts/
```

## What It Does

1. **Activates** the `data-advisor` agent in review mode
2. **Scans target path** to determine scope:
   - Identifies dbt project files (.sql models, schema.yml, sources.yml)
   - Identifies Python files with database operations
   - Identifies migration files
   - Identifies PostGIS usage
3. **Runs all check categories:**
   - Schema validity (PostgreSQL tables, columns, types)
   - dbt project health (parse, compile, test, lineage)
   - PostGIS compliance (SRID, geometry types, extent)
   - Data type consistency
   - Code patterns (unsafe SQL, hardcoded queries)
4. **Produces detailed report** with all severity levels (FAIL, WARN, INFO)
5. **Provides actionable recommendations** for each finding

## Output Format

```
+----------------------------------------------------------------------+
|  DATA-PLATFORM - Data Integrity Audit                                 |
|  /path/to/project                                                     |
+----------------------------------------------------------------------+

Target: /path/to/project
Scope: N files scanned, N models checked, N tables verified

FINDINGS

FAIL (N)
  1. [location] violation description
     Fix: actionable fix

WARN (N)
  1. [location] warning description
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

## When to Use

### Before Sprint Planning
Audit data layer health to identify tech debt and inform sprint scope.
```
/data-review ./dbt/
```

### During Code Review
Get detailed data integrity findings alongside code review comments.
```
/data-review ./dbt/models/staging/stg_new_source.sql
```

### After Migrations
Verify schema changes didn't break anything downstream.
```
/data-review ./migrations/
```

### Periodic Health Checks
Regular data infrastructure audits for proactive maintenance.
```
/data-review ./data_pipeline/
```

### New Project Onboarding
Understand the current state of data architecture.
```
/data-review .
```

## Severity Levels

| Level | Meaning | Gate Impact |
|-------|---------|-------------|
| **FAIL** | Blocking issues that will cause runtime errors | Would block `/data-gate` |
| **WARN** | Quality issues that should be addressed | Does not block gate |
| **INFO** | Suggestions for improvement | Does not block gate |

## Differences from /data-gate

`/data-review` gives you the full picture. `/data-gate` gives the orchestrator a yes/no.

| Aspect | /data-gate | /data-review |
|--------|------------|--------------|
| Output | Binary PASS/FAIL | Detailed report |
| Severity | FAIL only | FAIL + WARN + INFO |
| Purpose | Automation | Human review |
| Verbosity | Minimal | Comprehensive |
| Speed | Fast (skips INFO) | Thorough |

Use `/data-review` when you want to understand.
Use `/data-gate` when you want to automate.

## Requirements

- data-platform MCP server must be running
- For dbt checks: dbt project must be configured (auto-detected via `dbt_project.yml`)
- For PostgreSQL checks: connection configured in `~/.config/claude/postgres.env`

**Graceful degradation:** If database or dbt unavailable, applicable checks are skipped with a note in the report rather than failing entirely.

## Skills Used

- `skills/data-integrity-audit.md` - Audit rules and patterns
- `skills/mcp-tools-reference.md` - MCP tool reference

## Related Commands

- `/data-gate` - Binary pass/fail for automation
- `/data-lineage` - Visualize dbt model dependencies
- `/data-schema` - Explore database schema
