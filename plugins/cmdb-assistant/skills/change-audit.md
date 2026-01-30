# Change Audit Skill

Audit NetBox changes for tracking and compliance.

## Prerequisites

Load skill: `mcp-tools-reference`

## MCP Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `extras_list_object_changes` | List changes | `user_id`, `changed_object_type`, `action` |
| `extras_get_object_change` | Get change details | `id` |

## Common Object Types

| Category | Object Types |
|----------|--------------|
| DCIM | `dcim.device`, `dcim.interface`, `dcim.site`, `dcim.rack`, `dcim.cable` |
| IPAM | `ipam.ipaddress`, `ipam.prefix`, `ipam.vlan`, `ipam.vrf` |
| Virtualization | `virtualization.virtualmachine`, `virtualization.cluster` |
| Tenancy | `tenancy.tenant`, `tenancy.contact` |

## Audit Workflow

1. **Parse user request** - Determine filters
2. **Query object changes** - `extras_list_object_changes`
3. **Enrich data** - Fetch detailed records if needed
4. **Analyze patterns** - Identify bulk operations, unusual activity
5. **Generate report** - Structured format

## Report Template

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

#### Updated Objects (Z)

| Time | User | Object Type | Object | Changed Fields |
|------|------|-------------|--------|----------------|
| 2024-01-15 15:00 | john | ipam.ipaddress | 10.0.1.50/24 | status, description |

#### Deleted Objects (W)

| Time | User | Object Type | Object | Details |
|------|------|-------------|--------|---------|
| 2024-01-14 09:00 | admin | dcim.interface | eth2 | Removed from server-01 |

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
2024-01-15: ######## 8 changes
2024-01-14: ####     4 changes
2024-01-13: ##       2 changes
```

### Notable Patterns

- **Bulk operations:** [Many changes in short time]
- **Unusual activity:** [Unexpected deletions, after-hours changes]
- **Missing audit trail:** [Expected changes not logged]

### Recommendations

1. [Security or process recommendations based on findings]
```

## Enriching Change Details

For detailed audit, use `extras_get_object_change` to see:
- `prechange_data` - Object state before change
- `postchange_data` - Object state after change
- `request_id` - Links related changes in same request

## Security Audit Mode

When user asks for "security audit" or "compliance report":

1. Focus on deletions and permission-sensitive changes
2. Highlight changes to critical objects (firewalls, VRFs, prefixes)
3. Flag changes outside business hours
4. Identify users with high change counts

## Filter Examples

| Request | Filter |
|---------|--------|
| Recent changes | None (last 24 hours default) |
| Last 7 days | Filter by `time` field |
| By user | `user_id=<id>` |
| Device changes | `changed_object_type=dcim.device` |
| All deletions | `action=delete` |
