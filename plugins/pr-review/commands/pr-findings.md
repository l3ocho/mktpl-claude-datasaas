# /pr-findings - Filter Review Findings

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔍 PR-REVIEW · Findings                                          │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the findings display.

## Purpose

List and filter findings from a previous PR review by category, severity, or confidence level.

## Usage

```
/pr-findings <pr-number> [filters]
```

### Filters

```
--category <cat>      Filter by category (security, performance, maintainability, tests)
--severity <sev>      Filter by severity (critical, major, minor, suggestion)
--confidence <min>    Minimum confidence score (0.0-1.0)
--file <pattern>      Filter by file path pattern
```

## Examples

```
# Show only security findings
/pr-findings 123 --category security

# Show critical and major issues only
/pr-findings 123 --severity critical,major

# Show high-confidence findings only
/pr-findings 123 --confidence 0.8

# Show findings in specific files
/pr-findings 123 --file src/api/*
```

## Behavior

### Without Previous Review

If no review exists for this PR:

```
No review found for PR #123.

Would you like to:
1. Run full /pr-review now
2. Run quick /pr-summary
3. Cancel
```

### With Previous Review

Display filtered findings:

```
═══════════════════════════════════════════════════
PR #123 Findings (filtered: security)
═══════════════════════════════════════════════════

Showing 3 of 8 total findings

───────────────────────────────────────────────────

[SEC-001] SQL Injection Vulnerability
Confidence: 0.95 (HIGH) | Severity: Critical
File: src/api/users.ts:45

The query uses string interpolation without parameterization.

Fix: Use parameterized queries.

───────────────────────────────────────────────────

[SEC-002] Missing Input Validation
Confidence: 0.88 (MEDIUM) | Severity: Major
File: src/api/auth.ts:23

User input is passed directly to database without validation.

Fix: Add input validation middleware.

───────────────────────────────────────────────────

[SEC-003] Sensitive Data in Logs
Confidence: 0.72 (MEDIUM) | Severity: Minor
File: src/utils/logger.ts:15

Password field may be logged in debug mode.

Fix: Sanitize sensitive fields before logging.

═══════════════════════════════════════════════════
```

## Output Formats

### Default (Detailed)

Full finding details with descriptions and fixes.

### Compact (--compact)

```
SEC-001 | Critical | 0.95 | src/api/users.ts:45 | SQL Injection
SEC-002 | Major    | 0.88 | src/api/auth.ts:23  | Missing Validation
SEC-003 | Minor    | 0.72 | src/utils/logger.ts | Sensitive Logs
```

### JSON (--json)

```json
{
  "pr": 123,
  "findings": [
    {
      "id": "SEC-001",
      "category": "security",
      "severity": "critical",
      "confidence": 0.95,
      "file": "src/api/users.ts",
      "line": 45,
      "title": "SQL Injection Vulnerability",
      "description": "...",
      "fix": "..."
    }
  ]
}
```

## Use Cases

- Focus on specific issue types
- Track resolution of findings
- Export findings for tracking
- Quick reference during fixes
