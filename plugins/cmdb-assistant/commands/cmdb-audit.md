---
name: cmdb audit
description: Audit NetBox data quality and identify consistency issues
---

# /cmdb audit

Analyze NetBox data for quality issues and best practice violations.

## Skills to Load

- `skills/visual-header.md`
- `skills/audit-workflow.md`
- `skills/netbox-patterns/SKILL.md`
- `skills/mcp-tools-reference.md`

## Usage

```
/cmdb audit [scope]
```

**Scopes:**
- `all` (default) - Full audit across all categories
- `vms` - Virtual machines only
- `devices` - Physical devices only
- `naming` - Naming convention analysis
- `roles` - Role fragmentation analysis

## Instructions

Execute `skills/visual-header.md` with context "Data Quality Audit".

Execute `skills/audit-workflow.md` which covers:
1. Data collection via MCP
2. Quality checks by severity (CRITICAL, HIGH, MEDIUM, LOW)
3. Naming convention analysis
4. Role fragmentation analysis
5. Report generation with recommendations

## Scope-Specific Focus

| Scope | Focus |
|-------|-------|
| `all` | Full audit across all categories |
| `vms` | Virtual Machine checks only |
| `devices` | Device checks only |
| `naming` | Naming convention analysis |
| `roles` | Role fragmentation analysis |

## Examples

- `/cmdb audit` - Full audit
- `/cmdb audit vms` - VM-specific checks
- `/cmdb audit naming` - Naming conventions

## User Request

$ARGUMENTS
