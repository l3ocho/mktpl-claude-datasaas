# Component Map - Draw.io Specification

**Target File:** `docs/architecture/component-map.drawio`

**Purpose:** Shows all plugins, MCP servers, hooks and their relationships.

---

## NODES

### Plugins (Blue - #4A90D9)

| ID | Label | Type | Color | Position |
|----|-------|------|-------|----------|
| projman | projman | rectangle | #4A90D9 | top-center |
| projman-pmo | projman-pmo | rectangle | #4A90D9 | top-right |
| project-hygiene | project-hygiene | rectangle | #4A90D9 | top-left |

### MCP Servers (Green - #7CB342)

| ID | Label | Type | Color | Position |
|----|-------|------|-------|----------|
| gitea-mcp | Gitea MCP Server | rectangle | #7CB342 | middle-left |
| wikijs-mcp | Wiki.js MCP Server | rectangle | #7CB342 | middle-right |

### External Systems (Gray - #9E9E9E)

| ID | Label | Type | Color | Position |
|----|-------|------|-------|----------|
| gitea-instance | Gitea\ngitea.hotserv.cloud | cylinder | #9E9E9E | bottom-left |
| wikijs-instance | Wiki.js\nwikijs.hotserv.cloud | cylinder | #9E9E9E | bottom-right |

### Configuration (Orange - #FF9800)

| ID | Label | Type | Color | Position |
|----|-------|------|-------|----------|
| system-config | System Config\n~/.config/claude/ | rectangle | #FF9800 | far-left |
| project-config | Project Config\n.env | rectangle | #FF9800 | far-right |

---

## EDGES

### Plugin to MCP Server Connections

| From | To | Label | Style | Arrow |
|------|----|-------|-------|-------|
| projman | gitea-mcp | uses | solid | forward |
| projman | wikijs-mcp | uses | solid | forward |
| projman-pmo | gitea-mcp | uses (company-wide) | solid | forward |
| projman-pmo | wikijs-mcp | uses (company-wide) | solid | forward |

### Plugin Dependencies

| From | To | Label | Style | Arrow |
|------|----|-------|-------|-------|
| projman-pmo | projman | depends on | dashed | forward |

### MCP Server to External System Connections

| From | To | Label | Style | Arrow |
|------|----|-------|-------|-------|
| gitea-mcp | gitea-instance | REST API | solid | forward |
| wikijs-mcp | wikijs-instance | GraphQL | solid | forward |

### Configuration Connections

| From | To | Label | Style | Arrow |
|------|----|-------|-------|-------|
| system-config | gitea-mcp | credentials | dashed | forward |
| system-config | wikijs-mcp | credentials | dashed | forward |
| project-config | gitea-mcp | repo context | dashed | forward |
| project-config | wikijs-mcp | project path | dashed | forward |

---

## GROUPS

| ID | Label | Contains | Style |
|----|-------|----------|-------|
| plugins-group | Plugins | projman, projman-pmo, project-hygiene | light blue border |
| mcp-group | Shared MCP Servers | gitea-mcp, wikijs-mcp | light green border |
| external-group | External Services | gitea-instance, wikijs-instance | light gray border |
| config-group | Configuration | system-config, project-config | light orange border |

---

## LAYOUT NOTES

```
+------------------------------------------------------------------+
|                         PLUGINS GROUP                             |
|  +----------------+  +----------------+  +-------------------+    |
|  | project-       |  |    projman     |  |   projman-pmo    |    |
|  | hygiene        |  |                |  |                   |    |
|  +----------------+  +-------+--------+  +--------+----------+    |
|                              |                    |               |
+------------------------------------------------------------------+
                               |                    |
                               v                    v
+------------------------------------------------------------------+
|                      MCP SERVERS GROUP                            |
|  +-------------------+              +-------------------+         |
|  |  Gitea MCP Server |              | Wiki.js MCP Server|         |
|  +--------+----------+              +---------+---------+         |
+------------------------------------------------------------------+
           |                                     |
           v                                     v
+------------------------------------------------------------------+
|                    EXTERNAL SERVICES GROUP                        |
|  +-------------------+              +-------------------+         |
|  |      Gitea        |              |     Wiki.js       |         |
|  | gitea.hotserv.cloud              | wikijs.hotserv.cloud        |
|  +-------------------+              +-------------------+         |
+------------------------------------------------------------------+

CONFIG GROUP (left side):           CONFIG GROUP (right side):
+-------------------+               +-------------------+
| System Config     |               | Project Config    |
| ~/.config/claude/ |               | .env              |
+-------------------+               +-------------------+
```

---

## COLOR LEGEND

| Color | Hex | Meaning |
|-------|-----|---------|
| Blue | #4A90D9 | Plugins |
| Green | #7CB342 | MCP Servers |
| Gray | #9E9E9E | External Systems |
| Orange | #FF9800 | Configuration |
