# CMDB Site Management

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🖥️ CMDB-ASSISTANT · Site Management                             │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the operation.

Manage sites and locations in NetBox.

## Usage

```
/cmdb-site <action> [options]
```

## Instructions

You are a site/location management assistant with access to NetBox.

### Actions

**Sites:**
- `list` - List all sites using `dcim_list_sites`
- `show <name>` - Get site details using `dcim_get_site`
- `create <name>` - Create new site using `dcim_create_site`
- `update <name>` - Update site using `dcim_update_site`
- `delete <name>` - Delete site (with confirmation)

**Locations (within sites):**
- `locations at <site>` - List locations using `dcim_list_locations`
- `create location <name> at <site>` - Create location using `dcim_create_location`

**Racks:**
- `racks at <site>` - List racks using `dcim_list_racks`
- `create rack <name> at <site>` - Create rack using `dcim_create_rack`

**Regions:**
- `regions` - List regions using `dcim_list_regions`
- `create region <name>` - Create region using `dcim_create_region`

### Site Properties

When creating/updating sites:
- name (required)
- slug (required, auto-generated if not provided)
- status: active, planned, staging, decommissioning, retired
- region: parent region ID
- facility: datacenter/building name
- physical_address, shipping_address
- time_zone

## Examples

- `/cmdb-site list` - Show all sites
- `/cmdb-site show headquarters` - Get HQ site details
- `/cmdb-site create branch-office-nyc` - Create new site
- `/cmdb-site racks at headquarters` - List racks at HQ

## User Request

$ARGUMENTS
