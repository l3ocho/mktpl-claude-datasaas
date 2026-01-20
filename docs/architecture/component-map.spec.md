# Component Map - Draw.io Specification

**Target File:** `docs/architecture/component-map.drawio`

**Purpose:** Shows all plugins, MCP servers, hooks and their relationships.

---

## NODES

### Plugins (Blue - #4A90D9)

| ID | Label | Type | Color | Position |
|----|-------|------|-------|----------|
| projman | projman | rectangle | #4A90D9 | top-center |
| projman-pmo | projman-pmo (planned) | rectangle | #4A90D9 | top-right |
| project-hygiene | project-hygiene | rectangle | #4A90D9 | top-left |
| claude-config | claude-config-maintainer | rectangle | #4A90D9 | bottom-left |
| cmdb-assistant | cmdb-assistant | rectangle | #4A90D9 | bottom-right |

### MCP Servers (Green - #7CB342)

MCP servers are **bundled inside each plugin** that needs them.

| ID | Label | Type | Color | Position | Bundled In |
|----|-------|------|-------|----------|------------|
| gitea-mcp | Gitea MCP Server | rectangle | #7CB342 | middle-left | projman |
| netbox-mcp | NetBox MCP Server | rectangle | #7CB342 | middle-right | cmdb-assistant |

### External Systems (Gray - #9E9E9E)

| ID | Label | Type | Color | Position |
|----|-------|------|-------|----------|
| gitea-instance | Gitea\n(Issues + Wiki) | cylinder | #9E9E9E | bottom-left |
| netbox-instance | NetBox | cylinder | #9E9E9E | bottom-right |

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
| projman | gitea-mcp | bundled | solid | bidirectional |
| cmdb-assistant | netbox-mcp | bundled | solid | bidirectional |

### Plugin Dependencies

| From | To | Label | Style | Arrow |
|------|----|-------|-------|-------|
| projman-pmo | projman | depends on | dashed | forward |

### MCP Server to External System Connections

| From | To | Label | Style | Arrow |
|------|----|-------|-------|-------|
| gitea-mcp | gitea-instance | REST API | solid | forward |
| netbox-mcp | netbox-instance | REST API | solid | forward |

### Configuration Connections

| From | To | Label | Style | Arrow |
|------|----|-------|-------|-------|
| system-config | gitea-mcp | credentials | dashed | forward |
| system-config | netbox-mcp | credentials | dashed | forward |
| project-config | gitea-mcp | repo context | dashed | forward |
| project-config | netbox-mcp | site context | dashed | forward |

---

## GROUPS

| ID | Label | Contains | Style |
|----|-------|----------|-------|
| plugins-group | Plugins | projman, projman-pmo, project-hygiene, claude-config, cmdb-assistant | light blue border |
| external-group | External Services | gitea-instance, netbox-instance | light gray border |
| config-group | Configuration | system-config, project-config | light orange border |

---

## LAYOUT NOTES

```
+------------------------------------------------------------------+
|                         PLUGINS GROUP                             |
|  +----------------+  +----------------+  +-------------------+    |
|  | project-       |  |    projman     |  |   projman-pmo    |    |
|  | hygiene        |  |  [gitea-mcp]   |  |    (planned)      |    |
|  +----------------+  +-------+--------+  +-------------------+    |
|                              |                                    |
|  +----------------+  +-------------------+                        |
|  | claude-config  |  |  cmdb-assistant   |                        |
|  | -maintainer    |  |   [netbox-mcp]    |                        |
|  +----------------+  +--------+----------+                        |
+------------------------------------------------------------------+
                               |
                               v
+------------------------------------------------------------------+
|                    EXTERNAL SERVICES GROUP                        |
|  +-------------------+              +-------------------+         |
|  |      Gitea        |              |     NetBox        |         |
|  |  (Issues + Wiki)  |              |                   |         |
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
| Green | #7CB342 | MCP Servers (bundled in plugins) |
| Gray | #9E9E9E | External Systems |
| Orange | #FF9800 | Configuration |

---

## ARCHITECTURE NOTES

- MCP servers are **bundled inside plugins** (not shared at root)
- Gitea provides both issue tracking AND wiki (lessons learned)
- No separate Wiki.js - all wiki functionality uses Gitea Wiki
- Each plugin is self-contained for Claude Code caching
