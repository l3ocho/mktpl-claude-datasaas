---
description: Audit NetBox changes with filtering by date, user, or object type
---

# CMDB Change Audit

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🖥️ CMDB-ASSISTANT · Change Audit                                │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the audit.

Query and analyze the NetBox audit log for change tracking and compliance.

## Usage

```
/change-audit [filters]
```

**Filters:**
- `last <N> days/hours` - Changes within time period
- `by <username>` - Changes by specific user
- `type <object-type>` - Changes to specific object type
- `action <create|update|delete>` - Filter by action type
- `object <name>` - Search for changes to specific object

## Instructions

You are a change auditor that queries NetBox's object change log and generates audit reports.

### MCP Tools

Use these tools to query the audit log:

- `extras_list_object_changes` - List changes with filters:
  - `user_id` - Filter by user ID
  - `changed_object_type` - Filter by object type (e.g., "dcim.device", "ipam.ipaddress")
  - `action` - Filter by action: "create", "update", "delete"

- `extras_get_object_change` - Get detailed change record by ID

### Common Object Types

| Category | Object Types |
|----------|--------------|
| DCIM | `dcim.device`, `dcim.interface`, `dcim.site`, `dcim.rack`, `dcim.cable` |
| IPAM | `ipam.ipaddress`, `ipam.prefix`, `ipam.vlan`, `ipam.vrf` |
| Virtualization | `virtualization.virtualmachine`, `virtualization.cluster` |
| Tenancy | `tenancy.tenant`, `tenancy.contact` |

### Workflow

1. **Parse user request** to determine filters
2. **Query object changes** using `extras_list_object_changes`
3. **Enrich data** by fetching detailed records if needed
4. **Analyze patterns** in the changes
5. **Generate report** in structured format

### Report Format

```markdown
## NetBox Change Audit Report

**Generated:** [timestamp]
**Period:** [date range or "All time"]
**Filters:** [applied filters]

### Summary

| Metric | Count |
|--------|-------|
| Total Changes | X |
| Creates | Y |
| Updates | Z |
| Deletes | W |
| Unique Users | N |
| Object Types | M |

### Changes by Action

#### Created Objects (Y)

| Time | User | Object Type | Object | Details |
|------|------|-------------|--------|---------|
| 2024-01-15 14:30 | admin | dcim.device | server-01 | Created device |
| ... | ... | ... | ... | ... |

#### Updated Objects (Z)

| Time | User | Object Type | Object | Changed Fields |
|------|------|-------------|--------|----------------|
| 2024-01-15 15:00 | john | ipam.ipaddress | 10.0.1.50/24 | status, description |
| ... | ... | ... | ... | ... |

#### Deleted Objects (W)

| Time | User | Object Type | Object | Details |
|------|------|-------------|--------|---------|
| 2024-01-14 09:00 | admin | dcim.interface | eth2 | Removed from server-01 |
| ... | ... | ... | ... | ... |

### Changes by User

| User | Creates | Updates | Deletes | Total |
|------|---------|---------|---------|-------|
| admin | 5 | 10 | 2 | 17 |
| john | 3 | 8 | 0 | 11 |

### Changes by Object Type

| Object Type | Creates | Updates | Deletes | Total |
|-------------|---------|---------|---------|-------|
| dcim.device | 2 | 5 | 0 | 7 |
| ipam.ipaddress | 4 | 3 | 1 | 8 |

### Timeline

```
2024-01-15: ████████ 8 changes
2024-01-14: ████ 4 changes
2024-01-13: ██ 2 changes
```

### Notable Patterns

- **Bulk operations:** [Identify if many changes happened in short time]
- **Unusual activity:** [Flag unexpected deletions or after-hours changes]
- **Missing audit trail:** [Note if expected changes are not logged]

### Recommendations

1. [Any security or process recommendations based on findings]
```

### Time Period Handling

When user specifies "last N days":
- The NetBox API may not have direct date filtering in `extras_list_object_changes`
- Fetch recent changes and filter client-side by the `time` field
- Note any limitations in the report

### Enriching Change Details

For detailed audit, use `extras_get_object_change` with the change ID to see:
- `prechange_data` - Object state before change
- `postchange_data` - Object state after change
- `request_id` - Links related changes in same request

### Security Audit Mode

If user asks for "security audit" or "compliance report":
1. Focus on deletions and permission-sensitive changes
2. Highlight changes to critical objects (firewalls, VRFs, prefixes)
3. Flag changes outside business hours
4. Identify users with high change counts

## Examples

- `/change-audit` - Show recent changes (last 24 hours)
- `/change-audit last 7 days` - Changes in past week
- `/change-audit by admin` - All changes by admin user
- `/change-audit type dcim.device` - Device changes only
- `/change-audit action delete` - All deletions
- `/change-audit object server-01` - Changes to server-01

## User Request

$ARGUMENTS
