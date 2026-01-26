# Leo Claude Marketplace - v5.0.0

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

**Commands:** `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close`, `/labels-sync`, `/initial-setup`, `/project-init`, `/project-sync`, `/review`, `/test-check`, `/test-gen`, `/debug-report`, `/debug-review`

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

**Commands:** `/pr-review`, `/pr-summary`, `/pr-findings`, `/initial-setup`, `/project-init`, `/project-sync`

#### [claude-config-maintainer](./plugins/claude-config-maintainer/README.md)
**CLAUDE.md Optimization and Maintenance**

Analyze, optimize, and create CLAUDE.md configuration files for Claude Code projects.

**Commands:** `/config-analyze`, `/config-optimize`, `/config-init`

#### [contract-validator](./plugins/contract-validator/README.md) *NEW in v5.0.0*
**Cross-Plugin Compatibility Validation**

Validate plugin marketplaces for command conflicts, tool overlaps, and broken agent references.

- Interface parsing from plugin README.md files
- Agent extraction from CLAUDE.md definitions
- Pairwise compatibility checks between all plugins
- Data flow validation for agent sequences
- Markdown or JSON reports with actionable suggestions

**Commands:** `/validate-contracts`, `/check-agent`, `/list-interfaces`, `/initial-setup`

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

**Commands:** `/initial-setup`, `/cmdb-search`, `/cmdb-device`, `/cmdb-ip`, `/cmdb-site`

### Data Engineering

#### [data-platform](./plugins/data-platform/README.md) *NEW in v4.0.0*
**pandas, PostgreSQL/PostGIS, and dbt Integration**

Comprehensive data engineering toolkit with persistent DataFrame storage.

- 14 pandas tools with Arrow IPC data_ref system
- 10 PostgreSQL/PostGIS tools with connection pooling
- 8 dbt tools with automatic pre-validation
- 100k row limit with chunking support
- Auto-detection of dbt projects

**Commands:** `/ingest`, `/profile`, `/schema`, `/explain`, `/lineage`, `/run`

### Visualization

#### [viz-platform](./plugins/viz-platform/README.md) *NEW in v4.0.0*
**Dash Mantine Components Validation and Theming**

Visualization toolkit with version-locked component validation and design token theming.

- 3 DMC tools with static JSON registry (prevents prop hallucination)
- 2 Chart tools with Plotly and theme integration
- 5 Layout tools for dashboard composition
- 6 Theme tools with design token system
- 5 Page tools for multi-page app structure
- Dual theme storage: user-level and project-level

**Commands:** `/chart`, `/dashboard`, `/theme`, `/theme-new`, `/theme-css`, `/component`, `/initial-setup`

## MCP Servers

MCP servers are **shared at repository root** with **symlinks** from plugins that use them.

### Gitea MCP Server (shared)

Full Gitea API integration for project management.

| Category | Tools |
|----------|-------|
| Issues | `list_issues`, `get_issue`, `create_issue`, `update_issue`, `add_comment`, `aggregate_issues` |
| Labels | `get_labels`, `suggest_labels`, `create_label`, `create_label_smart` |
| Wiki | `list_wiki_pages`, `get_wiki_page`, `create_wiki_page`, `update_wiki_page`, `create_lesson`, `search_lessons` |
| Milestones | `list_milestones`, `get_milestone`, `create_milestone`, `update_milestone`, `delete_milestone` |
| Dependencies | `list_issue_dependencies`, `create_issue_dependency`, `remove_issue_dependency`, `get_execution_order` |
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

### Data Platform MCP Server (shared) *NEW in v4.0.0*

pandas, PostgreSQL/PostGIS, and dbt integration for data engineering.

| Category | Tools |
|----------|-------|
| pandas | `read_csv`, `read_parquet`, `read_json`, `to_csv`, `to_parquet`, `describe`, `head`, `tail`, `filter`, `select`, `groupby`, `join`, `list_data`, `drop_data` |
| PostgreSQL | `pg_connect`, `pg_query`, `pg_execute`, `pg_tables`, `pg_columns`, `pg_schemas` |
| PostGIS | `st_tables`, `st_geometry_type`, `st_srid`, `st_extent` |
| dbt | `dbt_parse`, `dbt_run`, `dbt_test`, `dbt_build`, `dbt_compile`, `dbt_ls`, `dbt_docs_generate`, `dbt_lineage` |

### Viz Platform MCP Server (shared) *NEW in v4.0.0*

Dash Mantine Components validation and visualization tools.

| Category | Tools |
|----------|-------|
| DMC | `list_components`, `get_component_props`, `validate_component` |
| Chart | `chart_create`, `chart_configure_interaction` |
| Layout | `layout_create`, `layout_add_filter`, `layout_set_grid`, `layout_get`, `layout_add_section` |
| Theme | `theme_create`, `theme_extend`, `theme_validate`, `theme_export_css`, `theme_list`, `theme_activate` |
| Page | `page_create`, `page_add_navbar`, `page_set_auth`, `page_list`, `page_get_app_config` |

### Contract Validator MCP Server (shared) *NEW in v5.0.0*

Cross-plugin compatibility validation tools.

| Category | Tools |
|----------|-------|
| Parse | `parse_plugin_interface`, `parse_claude_md_agents` |
| Validation | `validate_compatibility`, `validate_agent_refs`, `validate_data_flow` |
| Report | `generate_compatibility_report`, `list_issues` |

## Installation

### Prerequisites

- Claude Code installed
- Python 3.10+
- Access to target services (Gitea, NetBox as needed)

### Add Marketplace to Claude Code

**Option 1 - CLI command (recommended):**
```bash
/plugin marketplace add https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace.git
```

**Option 2 - Settings file (for team distribution):**

Add to `.claude/settings.json` in your target project:
```json
{
  "extraKnownMarketplaces": {
    "leo-claude-mktplace": {
      "source": {
        "source": "git",
        "url": "https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace.git"
      }
    }
  }
}
```

### Run Interactive Setup

After installing plugins, run the setup wizard:

```
/initial-setup
```

The wizard handles everything:
- Sets up MCP server (Python venv + dependencies)
- Creates system config (`~/.config/claude/gitea.env`)
- Guides you through adding your API token
- Detects and validates your repository via API
- Creates project config (`.env`)

**For new projects** (when system is already configured):
```
/project-init
```

**After moving a repository:**
```
/project-sync
```

See [docs/CONFIGURATION.md](./docs/CONFIGURATION.md) for manual setup and advanced options.

## Verifying Plugin Installation

After installing plugins, the `/plugin` command may show `(no content)` - this is normal Claude Code behavior and doesn't indicate an error.

**To verify a plugin is installed correctly:**

1. **Check installed plugins list:**
   ```
   /plugin list
   ```
   Look for `✔ plugin-name · Installed`

2. **Test a plugin command directly:**
   ```
   /git-flow:git-status
   /projman:sprint-status
   /clarity-assist:clarify
   ```
   If the command executes and shows output, the plugin is working.

3. **Check for loading errors:**
   ```
   /plugin list
   ```
   Look for any `Plugin Loading Errors` section - this indicates manifest issues.

**Command format:** All plugin commands use the format `/plugin-name:command-name`

| Plugin | Test Command |
|--------|--------------|
| git-flow | `/git-flow:git-status` |
| projman | `/projman:sprint-status` |
| pr-review | `/pr-review:pr-summary` |
| clarity-assist | `/clarity-assist:clarify` |
| doc-guardian | `/doc-guardian:doc-audit` |
| code-sentinel | `/code-sentinel:security-scan` |
| claude-config-maintainer | `/claude-config-maintainer:config-analyze` |
| cmdb-assistant | `/cmdb-assistant:cmdb-search` |
| data-platform | `/data-platform:ingest` |
| viz-platform | `/viz-platform:chart` |
| contract-validator | `/contract-validator:validate-contracts` |

## Repository Structure

```
leo-claude-mktplace/
├── .claude-plugin/                # Marketplace manifest
│   └── marketplace.json
├── mcp-servers/                   # SHARED MCP servers (v3.0.0+)
│   ├── gitea/                     # Gitea MCP (issues, PRs, wiki)
│   ├── netbox/                    # NetBox MCP (CMDB)
│   ├── data-platform/             # Data engineering (pandas, PostgreSQL, dbt)
│   ├── viz-platform/              # Visualization (DMC, Plotly, theming)
│   └── contract-validator/        # Cross-plugin validation (v5.0.0)
├── plugins/                       # All plugins
│   ├── projman/                   # Sprint management
│   ├── git-flow/                  # Git workflow automation
│   ├── pr-review/                 # PR review
│   ├── clarity-assist/            # Prompt optimization
│   ├── data-platform/             # Data engineering
│   ├── viz-platform/              # Visualization
│   ├── contract-validator/        # Cross-plugin validation (NEW)
│   ├── claude-config-maintainer/  # CLAUDE.md optimization
│   ├── cmdb-assistant/            # NetBox CMDB integration
│   ├── doc-guardian/              # Documentation drift detection
│   ├── code-sentinel/             # Security scanning
│   └── project-hygiene/           # Cleanup automation
├── docs/                          # Documentation
│   ├── CANONICAL-PATHS.md         # Path reference
│   └── CONFIGURATION.md           # Setup guide
├── scripts/                       # Setup scripts
└── CHANGELOG.md                   # Version history
```

## Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](./CLAUDE.md) | Main project instructions |
| [CONFIGURATION.md](./docs/CONFIGURATION.md) | Centralized setup guide |
| [COMMANDS-CHEATSHEET.md](./docs/COMMANDS-CHEATSHEET.md) | All commands quick reference |
| [UPDATING.md](./docs/UPDATING.md) | Update guide for the marketplace |
| [CANONICAL-PATHS.md](./docs/CANONICAL-PATHS.md) | Authoritative path reference |
| [DEBUGGING-CHECKLIST.md](./docs/DEBUGGING-CHECKLIST.md) | Systematic troubleshooting guide |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |

## License

MIT License

## Support

- **Issues**: Contact repository maintainer
- **Repository**: `https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace.git`
