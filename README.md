# Claude Code Marketplace - Bandit Labs

A collection of Claude Code plugins and MCP servers for project management, infrastructure automation, and development workflows.

## Plugins

### [projman](./plugins/projman/README.md)
**Sprint Planning and Project Management**

AI-guided sprint planning with Gitea and Wiki.js integration. Transforms a proven 15-sprint workflow into a distributable plugin.

- Three-agent model: Planner, Orchestrator, Executor
- Intelligent label suggestions from 44-label taxonomy
- Lessons learned capture to prevent repeated mistakes
- Branch-aware security (development/staging/production)

**Commands:** `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close`, `/labels-sync`

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
- Identifies orphaned supporting files (`test_*`, `debug_*`, `*_backup.*`)
- Logs actions to `.dev/logs/`
- Configurable via `.hygiene.json`

**Hook:** `task-completed`

## MCP Servers

Shared Model Context Protocol servers that provide plugins with external service access.

### [Gitea MCP Server](./mcp-servers/gitea/README.md)
Issue management, label operations, and repository tracking for Gitea.

| Tool | Description |
|------|-------------|
| `list_issues` | Query issues with filters |
| `create_issue` | Create issue with labels |
| `get_labels` | Fetch org + repo labels |
| `suggest_labels` | Intelligent label suggestions |

**Status:** Production Ready

### [Wiki.js MCP Server](./mcp-servers/wikijs/README.md)
Documentation management and lessons learned capture via GraphQL.

| Tool | Description |
|------|-------------|
| `search_pages` | Search by keywords/tags |
| `create_page` | Create markdown pages |
| `create_lesson` | Capture sprint lessons |
| `search_lessons` | Find relevant insights |

**Status:** Production Ready

### [NetBox MCP Server](./mcp-servers/netbox/README.md)
Comprehensive NetBox REST API integration for infrastructure management.

| Module | Coverage |
|--------|----------|
| DCIM | Sites, Racks, Devices, Interfaces, Cables |
| IPAM | Prefixes, IPs, VLANs, VRFs |
| Circuits | Providers, Circuits, Terminations |
| Virtualization | Clusters, VMs, Interfaces |
| Extras | Tags, Custom Fields, Audit Log |

**Status:** Production Ready

## Installation

### Prerequisites

- Claude Code installed
- Python 3.10+
- Access to target services (Gitea, Wiki.js, NetBox as needed)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone ssh://git@hotserv.tailc9b278.ts.net:2222/bandit/support-claude-mktplace.git
   cd support-claude-mktplace
   ```

2. **Install MCP server dependencies:**
   ```bash
   # Gitea MCP
   cd mcp-servers/gitea && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

   # Wiki.js MCP
   cd ../wikijs && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

   # NetBox MCP
   cd ../netbox && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```

3. **Configure credentials:**
   ```bash
   mkdir -p ~/.config/claude

   # Gitea
   cat > ~/.config/claude/gitea.env << 'EOF'
   GITEA_API_URL=https://gitea.example.com/api/v1
   GITEA_API_TOKEN=your_token
   GITEA_OWNER=your_org
   EOF

   # Wiki.js
   cat > ~/.config/claude/wikijs.env << 'EOF'
   WIKIJS_API_URL=https://wiki.example.com/graphql
   WIKIJS_API_TOKEN=your_token
   WIKIJS_BASE_PATH=/your-namespace
   EOF

   # NetBox
   cat > ~/.config/claude/netbox.env << 'EOF'
   NETBOX_API_URL=https://netbox.example.com/api
   NETBOX_API_TOKEN=your_token
   EOF

   chmod 600 ~/.config/claude/*.env
   ```

4. **Add marketplace to Claude Code:**
   ```bash
   claude plugin add ./.claude-plugins/projman-marketplace
   ```

## Repository Structure

```
support-claude-mktplace/
├── plugins/                    # All plugins
│   ├── projman/               # Sprint management plugin
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   └── skills/
│   ├── projman-pmo/           # PMO coordination plugin
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   └── agents/
│   ├── project-hygiene/       # Cleanup automation plugin
│   │   ├── .claude-plugin/
│   │   └── hooks/
│   └── cmdb-assistant/        # NetBox CMDB integration
│       ├── .claude-plugin/
│       ├── commands/
│       └── agents/
├── mcp-servers/               # Shared MCP servers
│   ├── gitea/
│   ├── wikijs/
│   └── netbox/
├── .claude-plugins/           # Marketplace definitions
│   └── projman-marketplace/
├── docs/                      # Reference documentation
│   └── references/
└── .claude/                   # Claude Code skills
    └── skills/
```

## Documentation

### Reference Material

| Document | Description |
|----------|-------------|
| [PROJECT-SUMMARY.md](./docs/references/PROJECT-SUMMARY.md) | Architecture overview and design decisions |
| [PLUGIN-PROJMAN.md](./docs/references/PLUGIN-PROJMAN.md) | Detailed projman plugin specification |
| [PLUGIN-PMO.md](./docs/references/PLUGIN-PMO.md) | Multi-project PMO plugin specification |
| [MCP-GITEA.md](./docs/references/MCP-GITEA.md) | Gitea MCP server API reference |
| [MCP-WIKIJS.md](./docs/references/MCP-WIKIJS.md) | Wiki.js MCP server API reference |

### Testing & Validation

| Document | Description |
|----------|-------------|
| [PROJMAN_TESTING_COMPLETE.md](./docs/PROJMAN_TESTING_COMPLETE.md) | Test results and validation |
| [LIVE_API_TEST_RESULTS.md](./docs/LIVE_API_TEST_RESULTS.md) | Live API integration tests |
| [TEST_EXECUTION_REPORT.md](./docs/TEST_EXECUTION_REPORT.md) | Full test execution report |

### Configuration Guides

| Document | Description |
|----------|-------------|
| [projman/CONFIGURATION.md](./plugins/projman/CONFIGURATION.md) | Projman setup guide |
| [CREATE_LABELS_GUIDE.md](./docs/CREATE_LABELS_GUIDE.md) | Gitea label taxonomy setup |

## Development

### Adding New Plugins

1. Create plugin directory in `plugins/` with `.claude-plugin/plugin.json`
2. Add commands, agents, or hooks as needed
3. Reference shared MCP servers via `.mcp.json` (use `../../mcp-servers/`)
4. Add to marketplace in `.claude-plugins/projman-marketplace/`
5. Document in plugin `README.md`

### Testing

```bash
# MCP server unit tests
cd mcp-servers/gitea && pytest -v
cd mcp-servers/wikijs && pytest -v

# Plugin validation
claude plugin list
claude --debug
```

## Roadmap

- [x] **Phase 1-2**: MCP servers and commands (Complete)
- [ ] **Phase 3**: Agent system implementation
- [ ] **Phase 4**: Lessons learned integration
- [ ] **Phase 5-8**: Testing, documentation, production
- [ ] **Phase 9-11**: PMO plugin for multi-project coordination
- [ ] **Phase 12**: Public marketplace distribution

## License

MIT License - Bandit Labs

## Support

- **Issues**: Contact repository maintainer
- **Repository**: `ssh://git@hotserv.tailc9b278.ts.net:2222/bandit/support-claude-mktplace.git`
