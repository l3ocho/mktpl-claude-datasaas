# Topology Generation Skill

Generate Mermaid diagrams from NetBox data.

## Prerequisites

Load skill: `mcp-tools-reference`

## View: Rack Elevation

### Data Collection

1. Find rack: `dcim_list_racks name=<name>`
2. Get devices: `dcim_list_devices rack_id=<id>`
3. Note for each: `position`, `u_height`, `face`, `name`, `role`

### Mermaid Template

```mermaid
graph TB
    subgraph rack["Rack: <rack-name> (U<height>)"]
        direction TB
        u42["U42: empty"]
        u41["U41: empty"]
        u40["U40: server-01 (Server)"]
        u39["U39: server-01 (cont.)"]
        u38["U38: switch-01 (Switch)"]
    end
```

### Rules

- Mark top U with device name and role
- Mark subsequent Us as "(cont.)" for multi-U devices
- Empty Us show "empty"

## View: Network Topology

### Data Collection

1. List sites: `dcim_list_sites`
2. List devices: `dcim_list_devices site_id=<id>`
3. List cables: `dcim_list_cables`
4. List interfaces: `dcim_list_interfaces device_id=<id>`

### Mermaid Template

```mermaid
graph TD
    subgraph site1["Site: Home"]
        router1[("core-router-01<br/>Router")]
        switch1[["dist-switch-01<br/>Switch"]]
        server1["web-server-01<br/>Server"]
        server2["db-server-01<br/>Server"]
    end

    router1 -->|"eth0 - eth1"| switch1
    switch1 -->|"gi0/1 - eth0"| server1
    switch1 -->|"gi0/2 - eth0"| server2
```

### Node Shapes by Role

| Role | Shape | Mermaid Syntax |
|------|-------|----------------|
| Router | Cylinder | `[(" ")]` |
| Switch | Double brackets | `[[ ]]` |
| Server | Rectangle | `[ ]` |
| Firewall | Hexagon | `{{ }}` |
| Other | Rectangle | `[ ]` |

### Edge Labels

Show interface names: `A-side - B-side`

## View: Site Overview

### Data Collection

1. Get site: `dcim_get_site id=<id>`
2. List racks: `dcim_list_racks site_id=<id>`
3. Count devices per rack: `dcim_list_devices rack_id=<id>`

### Mermaid Template

```mermaid
graph TB
    subgraph site["Site: Headquarters"]
        subgraph row1["Row 1"]
            rack1["Rack A1<br/>12/42 U used<br/>5 devices"]
            rack2["Rack A2<br/>20/42 U used<br/>8 devices"]
        end
        subgraph row2["Row 2"]
            rack3["Rack B1<br/>8/42 U used<br/>3 devices"]
        end
    end
```

## View: Full Infrastructure

### Data Collection

1. List regions: `dcim_list_regions`
2. List sites: `dcim_list_sites`
3. Count devices: `dcim_list_devices status=active`

### Mermaid Template

```mermaid
graph TB
    subgraph region1["Region: Americas"]
        site1["Headquarters<br/>3 racks, 25 devices"]
        site2["Branch Office<br/>1 rack, 5 devices"]
    end
    subgraph region2["Region: Europe"]
        site3["EU Datacenter<br/>10 racks, 100 devices"]
    end

    site1 -.->|"WAN Link"| site3
```

## Output Format

Always provide:

1. **Summary** - Brief description of diagram content
2. **Mermaid Code Block** - The diagram code
3. **Legend** - Explanation of shapes and colors
4. **Data Notes** - Any data quality issues

### Example Output

```markdown
## Network Topology: Home Site

This diagram shows network connections between 4 devices at Home site.

```mermaid
graph TD
    router1[("core-router<br/>Router")]
    switch1[["main-switch<br/>Switch"]]
    server1["homelab-01<br/>Server"]

    router1 -->|"eth0 - gi0/24"| switch1
    switch1 -->|"gi0/1 - eth0"| server1
```

**Legend:**
- Cylinder shape: Routers
- Double brackets: Switches
- Rectangle: Servers

**Data Notes:**
- 1 device (nas-01) has no cable connections documented
```
