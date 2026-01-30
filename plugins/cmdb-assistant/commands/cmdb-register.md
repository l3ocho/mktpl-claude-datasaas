---
description: Register the current machine into NetBox with all running applications
---

# CMDB Machine Registration

Register the current machine into NetBox, including hardware info, network interfaces, and running applications.

## Skills to Load

- `skills/visual-header.md`
- `skills/device-registration.md`
- `skills/system-discovery.md`
- `skills/netbox-patterns/SKILL.md`
- `skills/mcp-tools-reference.md`

## Usage

```
/cmdb-register [--site <site-name>] [--tenant <tenant-name>] [--role <role-name>]
```

**Options:**
- `--site <name>`: Site to assign (will prompt if not provided)
- `--tenant <name>`: Tenant for resource isolation (optional)
- `--role <name>`: Device role (default: auto-detect based on services)

## Instructions

Execute `skills/visual-header.md` with context "Machine Registration".

Execute `skills/device-registration.md` which covers:
1. System discovery via Bash (use `skills/system-discovery.md`)
2. Pre-registration checks (device exists?, site?, platform?, role?)
3. Device creation via MCP
4. Interface and IP creation
5. Container registration (if Docker found)
6. Journal entry documentation

## Error Handling

| Error | Action |
|-------|--------|
| Device already exists | Suggest `/cmdb-sync` or ask to proceed |
| Site not found | List available sites, offer to create new |
| Docker not available | Skip container registration, note in summary |
| Permission denied | Note which operations failed, suggest fixes |

## User Request

$ARGUMENTS
