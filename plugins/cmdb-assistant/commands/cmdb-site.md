---
name: cmdb site
---

# /cmdb site

Manage sites and locations in NetBox.

## Skills to Load

- `skills/visual-header.md`
- `skills/mcp-tools-reference.md`

## Usage

```
/cmdb site <action> [options]
```

## Instructions

Execute `skills/visual-header.md` with context "Site Management".

### Actions

**Sites:**
- `list` - List all sites: `dcim_list_sites`
- `show <name>` - Get site details: `dcim_get_site`
- `create <name>` - Create new site: `dcim_create_site`
- `update <name>` - Update site: `dcim_update_site`
- `delete <name>` - Delete site (with confirmation)

**Locations:**
- `locations at <site>` - List locations: `dcim_list_locations`
- `create location <name> at <site>` - Create location

**Racks:**
- `racks at <site>` - List racks: `dcim_list_racks`
- `create rack <name> at <site>` - Create rack

**Regions:**
- `regions` - List regions: `dcim_list_regions`
- `create region <name>` - Create region

## Examples

- `/cmdb site list`
- `/cmdb site show headquarters`
- `/cmdb site create branch-office-nyc`
- `/cmdb site racks at headquarters`

## User Request

$ARGUMENTS
