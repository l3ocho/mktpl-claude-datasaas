---
description: Audit NetBox data quality and identify consistency issues
---

# CMDB Data Quality Audit

Analyze NetBox data for quality issues and best practice violations.

## Usage

```
/cmdb-audit [scope]
```

**Scopes:**
- `all` (default) - Full audit across all categories
- `vms` - Virtual machines only
- `devices` - Physical devices only
- `naming` - Naming convention analysis
- `roles` - Role fragmentation analysis

## Instructions

You are a data quality auditor for NetBox. Your job is to identify consistency issues and best practice violations.

**IMPORTANT:** Load the `netbox-patterns` skill for best practice reference.

### Phase 1: Data Collection

Run these MCP tool calls to gather data for analysis:

```
1. virt_list_vms (no filters - get all)
2. dcim_list_devices (no filters - get all)
3. virt_list_clusters (no filters)
4. dcim_list_sites
5. tenancy_list_tenants
6. dcim_list_device_roles
7. dcim_list_platforms
```

Store the results for analysis.

### Phase 2: Quality Checks

Analyze collected data for these issues by severity:

#### CRITICAL Issues (must fix immediately)

| Check | Detection |
|-------|-----------|
| VMs without cluster | `cluster` field is null AND `site` field is null |
| Devices without site | `site` field is null |
| Active devices without primary IP | `status=active` AND `primary_ip4` is null AND `primary_ip6` is null |

#### HIGH Issues (should fix soon)

| Check | Detection |
|-------|-----------|
| VMs without site | VM has no site (neither direct nor via cluster.site) |
| VMs without tenant | `tenant` field is null |
| Devices without platform | `platform` field is null |
| Clusters not scoped to site | `site` field is null on cluster |
| VMs without role | `role` field is null |

#### MEDIUM Issues (plan to address)

| Check | Detection |
|-------|-----------|
| Inconsistent naming | Names don't match patterns: devices=`{role}-{site}-{num}`, VMs=`{env}-{app}-{num}` |
| Role fragmentation | More than 10 device roles with <3 assignments each |
| Missing tags on production | Active resources without any tags |
| Mixed naming separators | Some names use `_`, others use `-` |

#### LOW Issues (informational)

| Check | Detection |
|-------|-----------|
| Docker containers as VMs | Cluster type is "Docker Compose" - document this modeling choice |
| VMs without description | `description` field is empty |
| Sites without physical address | `physical_address` is empty |
| Devices without serial | `serial` field is empty |

### Phase 3: Naming Convention Analysis

For naming scope, analyze patterns:

1. **Extract naming patterns** from existing objects
2. **Identify dominant patterns** (most common conventions)
3. **Flag outliers** that don't match dominant patterns
4. **Suggest standardization** based on best practices

**Expected Patterns:**
- Devices: `{role}-{location}-{number}` (e.g., `web-dc1-01`)
- VMs: `{prefix}_{service}` or `{env}-{app}-{number}` (e.g., `prod-api-01`)
- Clusters: `{site}-{type}` (e.g., `home-docker`)

### Phase 4: Role Analysis

For roles scope, analyze fragmentation:

1. **List all device roles** with assignment counts
2. **Identify single-use roles** (only 1 device/VM)
3. **Identify similar roles** that could be consolidated
4. **Suggest consolidation** based on patterns

**Red Flags:**
- More than 15 highly specific roles
- Roles with technology in name (use platform instead)
- Roles that duplicate functionality

### Phase 5: Report Generation

Present findings in this structure:

```markdown
## CMDB Data Quality Audit Report

**Generated:** [timestamp]
**Scope:** [scope parameter]

### Summary

| Metric | Count |
|--------|-------|
| Total VMs | X |
| Total Devices | Y |
| Total Clusters | Z |
| **Total Issues** | **N** |

| Severity | Count |
|----------|-------|
| Critical | A |
| High | B |
| Medium | C |
| Low | D |

### Critical Issues

[List each with specific object names and IDs]

**Example:**
- VM `HotServ` (ID: 1) - No cluster or site assignment
- Device `server-01` (ID: 5) - No site assignment

### High Issues

[List each with specific object names]

### Medium Issues

[Grouped by category with counts]

### Recommendations

1. **[Most impactful fix]** - affects N objects
2. **[Second priority]** - affects M objects
...

### Quick Fixes

Commands to fix common issues:

```
# Assign site to VM
virt_update_vm id=X site=Y

# Assign platform to device
dcim_update_device id=X platform=Y
```

### Next Steps

- Run `/cmdb-register` to properly register new machines
- Use `/cmdb-sync` to update existing registrations
- Consider bulk updates via NetBox web UI for >10 items
```

## Scope-Specific Instructions

### For `vms` scope:
Focus only on Virtual Machine checks. Skip device and role analysis.

### For `devices` scope:
Focus only on Device checks. Skip VM and cluster analysis.

### For `naming` scope:
Focus on naming convention analysis across all objects. Generate detailed pattern report.

### For `roles` scope:
Focus on role fragmentation analysis. Generate consolidation recommendations.

## User Request

$ARGUMENTS
