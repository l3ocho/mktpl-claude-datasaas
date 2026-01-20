# Claude Code Marketplace

A collection of Claude Code plugins for project management, infrastructure automation, and development workflows.

## Plugins

### [projman](./plugins/projman/README.md) v2.2.0
**Sprint Planning and Project Management**

AI-guided sprint planning with full Gitea integration. Transforms a proven 15-sprint workflow into a distributable plugin.

- Three-agent model: Planner, Orchestrator, Executor, Code Reviewer
- Intelligent label suggestions from 43-label taxonomy
- Lessons learned capture via Gitea Wiki
- Native issue dependencies with parallel execution
- Milestone management for sprint organization
- Branch-aware security (development/staging/production)
- Pre-sprint-close code quality review and test verification

**Commands:** `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close`, `/labels-sync`, `/initial-setup`, `/review`, `/test-check`

### [claude-config-maintainer](./plugins/claude-config-maintainer/README.md)
**CLAUDE.md Optimization and Maintenance**

Analyze, optimize, and create CLAUDE.md configuration files for Claude Code projects.

- Structure and clarity scoring (100-point system)
- Automatic optimization with preview and backup
- Project-aware initialization with stack detection
- Best practices enforcement

**Commands:** `/config-analyze`, `/config-optimize`, `/config-init`

### [cmdb-assistant](./plugins/cmdb-assistant/README.md)
**NetBox CMDB Integration**

Full CRUD operations for network infrastructure management directly from Claude Code.

- Device, IP, site, and rack management
- Smart search across all NetBox modules
- Conversational infrastructure queries
- Audit trail and change tracking

**Commands:** `/cmdb-search`, `/cmdb-device`, `/cmdb-ip`, `/cmdb-site`

### [project-hygiene](./plugins/project-hygiene/README.md)
**Post-Task Cleanup Automation**

Hook-based cleanup that runs after Claude completes work.

- Deletes temp files (`*.tmp`, `*.bak`, `__pycache__`, etc.)
- Warns about unexpected files in project root
- Identifies orphaned supporting files
- Configurable via `.hygiene.json`

## MCP Servers

MCP servers are **bundled inside each plugin** that needs them. This ensures plugins work when cached by Claude Code.

### Gitea MCP Server (bundled in projman)

Full Gitea API integration for project management.

| Category | Tools |
|----------|-------|
| Issues | `list_issues`, `get_issue`, `create_issue`, `update_issue`, `add_comment` |
| Labels | `get_labels`, `suggest_labels`, `create_label` |
| Wiki | `list_wiki_pages`, `get_wiki_page`, `create_wiki_page`, `create_lesson`, `search_lessons` |
| Milestones | `list_milestones`, `get_milestone`, `create_milestone`, `update_milestone` |
| Dependencies | `list_issue_dependencies`, `create_issue_dependency`, `get_execution_order` |
| Validation | `validate_repo_org`, `get_branch_protection` |

### NetBox MCP Server (bundled in cmdb-assistant)

Comprehensive NetBox REST API integration for infrastructure management.

| Module | Coverage |
|--------|----------|
| DCIM | Sites, Racks, Devices, Interfaces, Cables |
| IPAM | Prefixes, IPs, VLANs, VRFs |
| Circuits | Providers, Circuits, Terminations |
| Virtualization | Clusters, VMs, Interfaces |
| Extras | Tags, Custom Fields, Audit Log |

## Installation

### Prerequisites

- Claude Code installed
- Python 3.10+
- Access to target services (Gitea, NetBox as needed)

### Add Marketplace to Claude Code

**Option 1 - CLI command (recommended):**
```bash
/plugin marketplace add https://gitea.hotserv.cloud/personal-projects/support-claude-mktplace.git
```

**Option 2 - Settings file (for team distribution):**

Add to `.claude/settings.json` in your target project:
```json
{
  "extraKnownMarketplaces": {
    "support-claude-mktplace": {
      "source": {
        "source": "git",
        "url": "https://gitea.hotserv.cloud/personal-projects/support-claude-mktplace.git"
      }
    }
  }
}
```

**Option 3 - Local development:**
```bash
# Clone the repository first
git clone https://gitea.hotserv.cloud/personal-projects/support-claude-mktplace.git

# Then add from local path
/plugin marketplace add /path/to/support-claude-mktplace
```

**Alternative SSH URL (for authenticated access):**
```
ssh://git@hotserv.tailc9b278.ts.net:2222/personal-projects/support-claude-mktplace.git
```

### Configure MCP Server Dependencies

If using plugins with MCP servers (projman, cmdb-assistant), install dependencies:

```bash
# Gitea MCP (for projman)
cd plugins/projman/mcp-servers/gitea
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate

# NetBox MCP (for cmdb-assistant)
cd ../../../cmdb-assistant/mcp-servers/netbox
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Configure Credentials

**System-level credentials:**
```bash
mkdir -p ~/.config/claude

# Gitea credentials
cat > ~/.config/claude/gitea.env << 'EOF'
GITEA_URL=https://gitea.example.com
GITEA_TOKEN=your_token
GITEA_ORG=your_org
EOF

# NetBox credentials
cat > ~/.config/claude/netbox.env << 'EOF'
NETBOX_API_URL=https://netbox.example.com/api
NETBOX_API_TOKEN=your_token
EOF

chmod 600 ~/.config/claude/*.env
```

**Project-level settings:**
```bash
# In your target project root
cat > .env << 'EOF'
GITEA_REPO=your-repository-name
EOF
```

## Repository Structure

```
support-claude-mktplace/
├── .claude-plugin/                # Marketplace manifest
│   └── marketplace.json
├── plugins/                       # All plugins (with bundled MCP servers)
│   ├── projman/                   # Sprint management plugin
│   │   ├── .claude-plugin/
│   │   ├── .mcp.json
│   │   ├── mcp-servers/           # Bundled MCP server
│   │   │   └── gitea/
│   │   ├── commands/
│   │   ├── agents/
│   │   └── skills/
│   ├── claude-config-maintainer/  # CLAUDE.md optimization plugin
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   └── agents/
│   ├── cmdb-assistant/            # NetBox CMDB integration
│   │   ├── .claude-plugin/
│   │   ├── .mcp.json
│   │   ├── mcp-servers/           # Bundled MCP server
│   │   │   └── netbox/
│   │   ├── commands/
│   │   └── agents/
│   ├── projman-pmo/               # PMO coordination plugin (planned)
│   └── project-hygiene/           # Cleanup automation plugin
├── docs/                          # Reference documentation
│   ├── CANONICAL-PATHS.md         # Single source of truth for paths
│   └── references/
└── scripts/                       # Setup and maintenance scripts
    └── validate-marketplace.sh    # Marketplace compliance validation
```

## Key Features (v2.2.0)

### Parallel Execution
Tasks are batched by dependency graph for optimal parallel execution:
```
Batch 1 (parallel): Task A, Task B, Task C
Batch 2 (parallel): Task D, Task E  (depend on Batch 1)
Batch 3 (sequential): Task F        (depends on Batch 2)
```

### Naming Conventions
- **Tasks:** `[Sprint XX] <type>: <description>`
- **Branches:** `feat/`, `fix/`, `debug/` prefixes with issue numbers

### CLI Tools Blocked
All agents use MCP tools exclusively. CLI tools like `tea` or `gh` are forbidden to ensure consistent, auditable operations.

## Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](./CLAUDE.md) | Main project instructions |
| [CANONICAL-PATHS.md](./docs/CANONICAL-PATHS.md) | Authoritative path reference |
| [projman/CONFIGURATION.md](./plugins/projman/CONFIGURATION.md) | Projman setup guide |

## License

MIT License

## Support

- **Issues**: Contact repository maintainer
- **Repository**: `https://gitea.hotserv.cloud/personal-projects/support-claude-mktplace.git`
- **SSH URL**: `ssh://git@hotserv.tailc9b278.ts.net:2222/personal-projects/support-claude-mktplace.git`
