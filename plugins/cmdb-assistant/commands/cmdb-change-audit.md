---
name: cmdb change-audit
description: Audit NetBox changes with filtering by date, user, or object type
---

# /cmdb change-audit

Query and analyze the NetBox audit log for change tracking and compliance.

## Skills to Load

- `skills/visual-header.md`
- `skills/change-audit.md`
- `skills/mcp-tools-reference.md`

## Usage

```
/cmdb change-audit [filters]
```

**Filters:**
- `last <N> days/hours` - Changes within time period
- `by <username>` - Changes by specific user
- `type <object-type>` - Changes to specific object type
- `action <create|update|delete>` - Filter by action type
- `object <name>` - Search for changes to specific object

## Instructions

Execute `skills/visual-header.md` with context "Change Audit".

Execute `skills/change-audit.md` which covers:
1. Parse user request for filters
2. Query object changes via MCP
3. Enrich data with detailed records
4. Analyze patterns
5. Generate report

## Security Audit Mode

If user asks for "security audit" or "compliance report":
- Focus on deletions and permission-sensitive changes
- Highlight changes to critical objects (firewalls, VRFs, prefixes)
- Flag changes outside business hours
- Identify users with high change counts

## Examples

- `/cmdb change-audit` - Recent changes (last 24 hours)
- `/cmdb change-audit last 7 days` - Past week
- `/cmdb change-audit by admin` - All changes by admin
- `/cmdb change-audit type dcim.device` - Device changes only
- `/cmdb change-audit action delete` - All deletions

## User Request

$ARGUMENTS
