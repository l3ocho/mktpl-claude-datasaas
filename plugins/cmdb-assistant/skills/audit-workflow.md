# Audit Workflow Skill

How to audit NetBox data quality.

## Prerequisites

Load these skills:
- `netbox-patterns` - Best practices reference
- `mcp-tools-reference` - MCP tool reference

## Data Collection

```
virt_list_vms
dcim_list_devices
virt_list_clusters
dcim_list_sites
tenancy_list_tenants
dcim_list_device_roles
dcim_list_platforms
```

## Quality Checks by Severity

### CRITICAL (must fix immediately)

| Check | Detection |
|-------|-----------|
| VMs without cluster | `cluster` is null AND `site` is null |
| Devices without site | `site` is null |
| Active devices without primary IP | `status=active` AND `primary_ip4` is null AND `primary_ip6` is null |

### HIGH (should fix soon)

| Check | Detection |
|-------|-----------|
| VMs without site | No site (neither direct nor via cluster.site) |
| VMs without tenant | `tenant` is null |
| Devices without platform | `platform` is null |
| Clusters not scoped to site | `site` is null on cluster |
| VMs without role | `role` is null |

### MEDIUM (plan to address)

| Check | Detection |
|-------|-----------|
| Inconsistent naming | Names don't match patterns |
| Role fragmentation | >10 device roles with <3 assignments each |
| Missing tags on production | Active resources without tags |
| Mixed naming separators | Some `_`, others `-` |

### LOW (informational)

| Check | Detection |
|-------|-----------|
| Docker containers as VMs | Cluster type is "Docker Compose" |
| VMs without description | `description` is empty |
| Sites without physical address | `physical_address` is empty |
| Devices without serial | `serial` is empty |

## Naming Convention Analysis

### Expected Patterns

| Object Type | Pattern | Example |
|-------------|---------|---------|
| Devices | `{role}-{location}-{number}` | `web-dc1-01` |
| VMs | `{env}-{app}-{number}` | `prod-api-01` |
| Clusters | `{site}-{type}` | `home-docker` |

### Analysis Steps

1. Extract naming patterns from existing objects
2. Identify dominant patterns (most common)
3. Flag outliers that don't match
4. Suggest standardization

## Role Fragmentation Analysis

### Red Flags

- More than 15 highly specific roles
- Roles with technology in name (use platform instead)
- Roles that duplicate functionality
- Single-use roles (only 1 device/VM)

### Recommended Consolidation

Use general roles + platform/tags for specificity:
- Instead of `nginx-web-server`, use `web-server` + platform `nginx`

## Report Template

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

- VM `HotServ` (ID: 1) - No cluster or site assignment
- Device `server-01` (ID: 5) - No site assignment

### High Issues

[List each with specific object names]

### Medium Issues

[Grouped by category with counts]

### Recommendations

1. **[Most impactful fix]** - affects N objects
2. **[Second priority]** - affects M objects

### Quick Fixes

Commands to fix common issues:

```
# Assign site to VM
virt_update_vm id=X site=Y

# Assign platform to device
dcim_update_device id=X platform=Y
```

### Next Steps

- Run `/cmdb register` to properly register new machines
- Use `/cmdb sync` to update existing registrations
- Consider bulk updates via NetBox web UI for >10 items
```

## Scope-Specific Focus

| Scope | Focus |
|-------|-------|
| `all` | Full audit across all categories |
| `vms` | Virtual Machine checks only |
| `devices` | Device checks only |
| `naming` | Naming convention analysis |
| `roles` | Role fragmentation analysis |
