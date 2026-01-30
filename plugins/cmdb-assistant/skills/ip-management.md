# IP Management Skill

IP address and prefix management in NetBox.

## Prerequisites

Load skill: `mcp-tools-reference`

## IPAM Operations

### Prefix Management

| Action | Tool | Key Parameters |
|--------|------|----------------|
| List prefixes | `ipam_list_prefixes` | `prefix`, `vrf_id`, `within`, `contains` |
| Get details | `ipam_get_prefix` | `id` |
| Find available child | `ipam_list_available_prefixes` | `prefix_id` |
| Create prefix | `ipam_create_prefix` | `prefix`, `status`, `site`, `vrf` |
| Allocate child | `ipam_create_available_prefix` | `prefix_id`, `prefix_length` |

### IP Address Management

| Action | Tool | Key Parameters |
|--------|------|----------------|
| List IPs | `ipam_list_ip_addresses` | `address`, `vrf_id`, `device_id` |
| Get details | `ipam_get_ip_address` | `id` |
| Find available | `ipam_list_available_ips` | `prefix_id` |
| Create IP | `ipam_create_ip_address` | `address`, `assigned_object_type`, `assigned_object_id` |
| Allocate next | `ipam_create_available_ip` | `prefix_id` |
| Assign to interface | `ipam_update_ip_address` | `id`, `assigned_object_id` |

### VLAN and VRF

| Action | Tool |
|--------|------|
| List VLANs | `ipam_list_vlans` |
| Get VLAN | `ipam_get_vlan` |
| Create VLAN | `ipam_create_vlan` |
| List VRFs | `ipam_list_vrfs` |
| Get VRF | `ipam_get_vrf` |

## IP Allocation Workflow

1. **Find available IPs in target prefix:**
   ```
   ipam_list_available_ips prefix_id=<id>
   ```

2. **Create the IP address:**
   ```
   ipam_create_ip_address
     address=<ip/prefix>
     assigned_object_type="dcim.interface"
     assigned_object_id=<interface_id>
     status="active"
   ```

3. **Set as primary (if needed):**
   ```
   dcim_update_device id=<device_id> primary_ip4=<ip_id>
   ```

## IP Conflict Detection

### Conflict Types

1. **Duplicate IP Addresses**
   - Multiple records with same address in same VRF
   - Exception: Anycast addresses (check `role` field)

2. **Overlapping Prefixes**
   - Prefixes containing same address space in same VRF
   - Legitimate: Parent/child hierarchy, different VRFs, "container" status

3. **IPs Outside Prefix**
   - IP addresses not within any defined prefix

4. **Same Prefix in Multiple VRFs** (informational)

### Detection Workflow

1. **Duplicate Detection:**
   - Get all addresses: `ipam_list_ip_addresses`
   - Group by address + VRF
   - Flag groups with >1 record

2. **Overlap Detection:**
   - Get all prefixes: `ipam_list_prefixes`
   - For each VRF, compare prefixes pairwise
   - Check if prefix A contains prefix B or vice versa
   - Ignore legitimate hierarchies (status=container)

3. **Orphan IP Detection:**
   - For each IP, find containing prefix
   - Flag IPs with no prefix match

### CIDR Math Rules

- Prefix A **contains** Prefix B if: `A.network <= B.network AND A.broadcast >= B.broadcast`
- Two prefixes **overlap** if: `A.network <= B.broadcast AND B.network <= A.broadcast`

### Severity Levels

| Issue | Severity |
|-------|----------|
| Duplicate IP (same interface type) | CRITICAL |
| Duplicate IP (different roles) | HIGH |
| Overlapping prefixes (same status) | HIGH |
| Overlapping prefixes (container ok) | LOW |
| Orphan IP | MEDIUM |

## Conflict Report Template

```markdown
## IP Conflict Detection Report

**Generated:** [timestamp]
**Scope:** [scope parameter]

### Summary

| Check | Status | Count |
|-------|--------|-------|
| Duplicate IPs | [PASS/FAIL] | X |
| Overlapping Prefixes | [PASS/FAIL] | Y |
| Orphan IPs | [PASS/FAIL] | Z |

### Critical Issues

#### Duplicate IP Addresses

| Address | VRF | Count | Assigned To |
|---------|-----|-------|-------------|
| 10.0.1.50/24 | Global | 2 | server-01, server-02 |

**Resolution:**
- Determine which device should have the IP
- Update or remove the duplicate

#### Overlapping Prefixes

| Prefix 1 | Prefix 2 | VRF | Type |
|----------|----------|-----|------|
| 10.0.0.0/24 | 10.0.0.0/25 | Global | Unstructured |

**Resolution:**
- For legitimate hierarchies: Mark parent as status="container"
- For accidental: Consolidate or re-address

### Remediation Commands

```
# Remove duplicate IP
ipam_delete_ip_address id=123

# Mark prefix as container
ipam_update_prefix id=456 status=container

# Create missing prefix
ipam_create_prefix prefix=172.16.5.0/24 status=active
```
```
