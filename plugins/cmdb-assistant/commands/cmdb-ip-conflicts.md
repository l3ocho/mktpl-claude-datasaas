---
name: cmdb ip-conflicts
description: Detect IP address conflicts and overlapping prefixes in NetBox
---

# /cmdb ip-conflicts

Scan NetBox IPAM data to identify IP address conflicts and overlapping prefixes.

## Skills to Load

- `skills/visual-header.md`
- `skills/ip-management.md`
- `skills/mcp-tools-reference.md`

## Usage

```
/cmdb ip-conflicts [scope]
```

**Scopes:**
- `all` (default) - Full scan of all IP data
- `addresses` - Check for duplicate IP addresses only
- `prefixes` - Check for overlapping prefixes only
- `vrf <name>` - Scan specific VRF only
- `prefix <cidr>` - Scan within specific prefix

## Instructions

Execute `skills/visual-header.md` with context "IP Conflict Detection".

Execute conflict detection from `skills/ip-management.md`:

1. **Data Collection** - Fetch IPs, prefixes, VRFs via MCP
2. **Duplicate Detection** - Group by address+VRF, flag >1 record
3. **Overlap Detection** - Compare prefixes pairwise using CIDR math
4. **Orphan IP Detection** - Find IPs without containing prefix
5. **Generate Report** - Use template from skill

## Conflict Types

| Type | Severity |
|------|----------|
| Duplicate IP (same interface type) | CRITICAL |
| Duplicate IP (different roles) | HIGH |
| Overlapping prefixes (same status) | HIGH |
| Overlapping prefixes (container ok) | LOW |
| Orphan IP | MEDIUM |

## Examples

- `/cmdb ip-conflicts` - Full scan
- `/cmdb ip-conflicts addresses` - Duplicate IPs only
- `/cmdb ip-conflicts vrf Production` - Scan specific VRF

## User Request

$ARGUMENTS
