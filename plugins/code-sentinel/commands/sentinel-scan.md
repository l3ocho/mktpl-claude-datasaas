---
name: sentinel scan
description: Full security audit of codebase - scans all files for vulnerability patterns
---

# /sentinel scan

Comprehensive security audit of the project.

## Visual Output

```
+----------------------------------------------------------------------+
|  CODE-SENTINEL - Security Scan                                       |
+----------------------------------------------------------------------+
```

## Skills to Load

- skills/security-patterns/SKILL.md

## Process

1. **File Discovery** - Scan: .py, .js, .ts, .jsx, .tsx, .go, .rs, .java, .rb, .php, .sh
2. **Pattern Detection** - Apply patterns from skill (Critical/High/Medium severity)
3. **Report** - Group by severity, include code snippets and fixes

## Output Format

```
## Security Scan Report

### Critical (Immediate Action Required)
[red] file:line - Vulnerability Type
   Code: `problematic code`
   Fix: Recommended solution

### High / Medium / Low
[Similar format]

### Summary
- Critical: X (must fix before deploy)
- High: X (fix soon)
- Medium: X (improve when possible)
```

## Exit Guidance

- Critical findings: Block merge/deploy
- High findings: Fix before release
- Medium/Low: Informational
