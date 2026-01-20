# Leo Claude Marketplace - v3.0.0

A collection of Claude Code plugins for project management, infrastructure automation, and development workflows.

## Plugins

### Development & Project Management

#### [projman](./plugins/projman/README.md)
**Sprint Planning and Project Management**

AI-guided sprint planning with full Gitea integration. Transforms a proven 15-sprint workflow into a distributable plugin.

- Four-agent model: Planner, Orchestrator, Executor, Code Reviewer
- Intelligent label suggestions from 43-label taxonomy
- Lessons learned capture via Gitea Wiki
- Native issue dependencies with parallel execution
- Milestone management for sprint organization
- Branch-aware security (development/staging/production)
- Pre-sprint-close code quality review and test verification

**Commands:** `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close`, `/labels-sync`, `/initial-setup`, `/review`, `/test-check`, `/test-gen`

#### [git-flow](./plugins/git-flow/README.md) *NEW in v3.0.0*
**Git Workflow Automation**

Smart git operations with intelligent commit messages and branch management.

- Auto-generated conventional commit messages
- Multiple workflow styles (simple, feature-branch, pr-required, trunk-based)
- Branch naming enforcement
- Merge and cleanup automation
- Protected branch awareness

**Commands:** `/commit`, `/commit-push`, `/commit-merge`, `/commit-sync`, `/branch-start`, `/branch-cleanup`, `/git-status`, `/git-config`

#### [pr-review](./plugins/pr-review/README.md) *NEW in v3.0.0*
**Multi-Agent PR Review**

Comprehensive pull request review using specialized agents.

- Multi-agent review: Security, Performance, Maintainability, Tests
- Confidence scoring (only reports HIGH/MEDIUM confidence findings)
- Actionable feedback with suggested fixes
- Gitea integration for automated review submission

**Commands:** `/pr-review`, `/pr-summary`, `/pr-findings`

#### [claude-config-maintainer](./plugins/claude-config-maintainer/README.md)
**CLAUDE.md Optimization and Maintenance**

Analyze, optimize, and create CLAUDE.md configuration files for Claude Code projects.

**Commands:** `/config-analyze`, `/config-optimize`, `/config-init`

### Productivity

#### [clarity-assist](./plugins/clarity-assist/README.md) *NEW in v3.0.0*
**Prompt Optimization with ND Accommodations**

Transform vague requests into clear specifications using structured methodology.

- 4-D methodology: Deconstruct, Diagnose, Develop, Deliver
- ND-friendly question patterns (option-based, chunked)
- Conflict detection and escalation protocols

**Commands:** `/clarify`, `/quick-clarify`

#### [doc-guardian](./plugins/doc-guardian/README.md)
**Documentation Lifecycle Management**

Automatic documentation drift detection and synchronization.

**Commands:** `/doc-audit`, `/doc-sync`

#### [project-hygiene](./plugins/project-hygiene/README.md)
**Post-Task Cleanup Automation**

Hook-based cleanup that runs after Claude completes work.

### Security

#### [code-sentinel](./plugins/code-sentinel/README.md)
**Security Scanning & Refactoring**

Security vulnerability detection and code refactoring tools.

**Commands:** `/security-scan`, `/refactor`, `/refactor-dry`

### Infrastructure

#### [cmdb-assistant](./plugins/cmdb-assistant/README.md)
**NetBox CMDB Integration**

Full CRUD operations for network infrastructure management directly from Claude Code.

**Commands:** `/cmdb-search`, `/cmdb-device`, `/cmdb-ip`, `/cmdb-site`

## MCP Servers

MCP servers are **shared at repository root** with **symlinks** from plugins that use them.

### Gitea MCP Server (shared)

Full Gitea API integration for project management.

| Category | Tools |
|----------|-------|
| Issues | `list_issues`, `get_issue`, `create_issue`, `update_issue`, `add_comment` |
| Labels | `get_labels`, `suggest_labels`, `create_label` |
| Wiki | `list_wiki_pages`, `get_wiki_page`, `create_wiki_page`, `create_lesson`, `search_lessons` |
| Milestones | `list_milestones`, `get_milestone`, `create_milestone`, `update_milestone` |
| Dependencies | `list_issue_dependencies`, `create_issue_dependency`, `get_execution_order` |
| **Pull Requests** | `list_pull_requests`, `get_pull_request`, `get_pr_diff`, `get_pr_comments`, `create_pr_review`, `add_pr_comment` *(NEW in v3.0.0)* |
| Validation | `validate_repo_org`, `get_branch_protection` |

### NetBox MCP Server (shared)

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
    "lm-claude-plugins": {
      "source": {
        "source": "git",
        "url": "https://gitea.hotserv.cloud/personal-projects/support-claude-mktplace.git"
      }
    }
  }
}
```

### Configure MCP Server Dependencies

Install dependencies for shared MCP servers:

```bash
# Gitea MCP (for projman, pr-review)
cd mcp-servers/gitea
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate

# NetBox MCP (for cmdb-assistant)
cd ../netbox
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Configure Credentials

See [docs/CONFIGURATION.md](./docs/CONFIGURATION.md) for complete setup instructions.

**Quick start:**
```bash
mkdir -p ~/.config/claude

# Gitea credentials
cat > ~/.config/claude/gitea.env << 'EOF'
GITEA_URL=https://gitea.example.com
GITEA_TOKEN=your_token
GITEA_ORG=your_org
EOF
chmod 600 ~/.config/claude/gitea.env

# Project-level settings
cat > .env << 'EOF'
GITEA_REPO=your-repository-name
EOF
```

## Repository Structure

```
lm-claude-plugins/
├── .claude-plugin/                # Marketplace manifest
│   └── marketplace.json
├── mcp-servers/                   # SHARED MCP servers (v3.0.0+)
│   ├── gitea/                     # Gitea MCP (issues, PRs, wiki)
│   └── netbox/                    # NetBox MCP (CMDB)
├── plugins/                       # All plugins
│   ├── projman/                   # Sprint management
│   ├── git-flow/                  # Git workflow automation (NEW)
│   ├── pr-review/                 # PR review (NEW)
│   ├── clarity-assist/            # Prompt optimization (NEW)
│   ├── claude-config-maintainer/  # CLAUDE.md optimization
│   ├── cmdb-assistant/            # NetBox CMDB integration
│   ├── doc-guardian/              # Documentation drift detection
│   ├── code-sentinel/             # Security scanning
│   └── project-hygiene/           # Cleanup automation
├── docs/                          # Documentation
│   ├── CANONICAL-PATHS.md         # Path reference
│   └── CONFIGURATION.md           # Setup guide
└── scripts/                       # Setup scripts
```

## Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](./CLAUDE.md) | Main project instructions |
| [CONFIGURATION.md](./docs/CONFIGURATION.md) | Centralized setup guide |
| [CANONICAL-PATHS.md](./docs/CANONICAL-PATHS.md) | Authoritative path reference |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |

## License

MIT License

## Support

- **Issues**: Contact repository maintainer
- **Repository**: `https://gitea.hotserv.cloud/personal-projects/support-claude-mktplace.git`
