# Leo Claude Marketplace - v7.0.0

A collection of Claude Code plugins for project management, infrastructure automation, and development workflows.

## Quick Start

Use the launcher script to load only the plugins you need, reducing token overhead from ~22K to ~4-6K tokens:

```bash
./scripts/claude-launch.sh [profile] [extra-args...]
```

| Profile | Plugins Loaded | Use Case |
|---------|----------------|----------|
| `sprint` | projman, git-flow, pr-review, code-sentinel, doc-guardian, clarity-assist | Default. Sprint planning and development |
| `review` | pr-review, code-sentinel | Lightweight code review |
| `data` | data-platform, viz-platform | Data engineering and visualization |
| `infra` | cmdb-assistant | Infrastructure/CMDB management |
| `full` | All 12 plugins via marketplace.json | When you need everything |

**Examples:**
```bash
./scripts/claude-launch.sh                    # Default sprint profile
./scripts/claude-launch.sh data --model opus  # Data profile with Opus
./scripts/claude-launch.sh full               # Load all plugins
```

The script enables `ENABLE_TOOL_SEARCH=true` for MCP lazy loading.

## Plugins

### Development & Project Management

#### [projman](./plugins/projman)
**Sprint Planning and Project Management**

AI-guided sprint planning with full Gitea integration. Transforms a proven 15-sprint workflow into a distributable plugin.

- Four-agent model: Planner, Orchestrator, Executor, Code Reviewer
- Plan-then-batch execution: skills loaded once per phase, API calls batched for ~80% token savings
- Intelligent label suggestions from 43-label taxonomy
- Lessons learned capture via Gitea Wiki
- Native issue dependencies with parallel execution
- Milestone management for sprint organization
- Branch-aware security (development/staging/production)
- Pre-sprint-close code quality review and test verification

**Commands:** `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close`, `/labels-sync`, `/pm-setup`, `/pm-review`, `/pm-test`, `/pm-debug`, `/suggest-version`, `/proposal-status`, `/rfc`

#### [git-flow](./plugins/git-flow) *NEW in v3.0.0*
**Git Workflow Automation**

Smart git operations with intelligent commit messages and branch management.

- Auto-generated conventional commit messages
- Multiple workflow styles (simple, feature-branch, pr-required, trunk-based)
- Branch naming enforcement
- Merge and cleanup automation
- Protected branch awareness

**Commands:** `/git-commit`, `/git-commit-push`, `/git-commit-merge`, `/git-commit-sync`, `/branch-start`, `/branch-cleanup`, `/git-status`, `/git-config`

#### [pr-review](./plugins/pr-review) *NEW in v3.0.0*
**Multi-Agent PR Review**

Comprehensive pull request review using specialized agents.

- Multi-agent review: Security, Performance, Maintainability, Tests
- Confidence scoring (only reports HIGH/MEDIUM confidence findings)
- Actionable feedback with suggested fixes
- Gitea integration for automated review submission

**Commands:** `/pr-review`, `/pr-summary`, `/pr-findings`, `/pr-diff`, `/pr-setup`, `/project-init`, `/project-sync`

#### [claude-config-maintainer](./plugins/claude-config-maintainer)
**CLAUDE.md and Settings Optimization**

Analyze, optimize, and create CLAUDE.md configuration files. Audit and optimize settings.local.json permissions.

**Commands:** `/analyze`, `/optimize`, `/init`, `/config-diff`, `/config-lint`, `/config-audit-settings`, `/config-optimize-settings`, `/config-permissions-map`

#### [contract-validator](./plugins/contract-validator) *NEW in v5.0.0*
**Cross-Plugin Compatibility Validation**

Validate plugin marketplaces for command conflicts, tool overlaps, and broken agent references.

- Interface parsing from plugin README.md files
- Agent extraction from CLAUDE.md definitions
- Pairwise compatibility checks between all plugins
- Data flow validation for agent sequences
- Markdown or JSON reports with actionable suggestions

**Commands:** `/validate-contracts`, `/check-agent`, `/list-interfaces`, `/dependency-graph`, `/cv-setup`

### Productivity

#### [clarity-assist](./plugins/clarity-assist) *NEW in v3.0.0*
**Prompt Optimization with ND Accommodations**

Transform vague requests into clear specifications using structured methodology.

- 4-D methodology: Deconstruct, Diagnose, Develop, Deliver
- ND-friendly question patterns (option-based, chunked)
- Conflict detection and escalation protocols

**Commands:** `/clarify`, `/quick-clarify`

#### [doc-guardian](./plugins/doc-guardian)
**Documentation Lifecycle Management**

Automatic documentation drift detection and synchronization.

**Commands:** `/doc-audit`, `/doc-sync`, `/changelog-gen`, `/doc-coverage`, `/stale-docs`

#### [project-hygiene](./plugins/project-hygiene)
**Post-Task Cleanup Automation**

Hook-based cleanup that runs after Claude completes work.

### Security

#### [code-sentinel](./plugins/code-sentinel)
**Security Scanning & Refactoring**

Security vulnerability detection and code refactoring tools.

**Commands:** `/security-scan`, `/refactor`, `/refactor-dry`

### Infrastructure

#### [cmdb-assistant](./plugins/cmdb-assistant)
**NetBox CMDB Integration**

Full CRUD operations for network infrastructure management directly from Claude Code.

**Commands:** `/cmdb-setup`, `/cmdb-search`, `/cmdb-device`, `/cmdb-ip`, `/cmdb-site`, `/cmdb-audit`, `/cmdb-register`, `/cmdb-sync`, `/cmdb-topology`, `/change-audit`, `/ip-conflicts`

### Data Engineering

#### [data-platform](./plugins/data-platform) *NEW in v4.0.0*
**pandas, PostgreSQL/PostGIS, and dbt Integration**

Comprehensive data engineering toolkit with persistent DataFrame storage.

- 14 pandas tools with Arrow IPC data_ref system
- 10 PostgreSQL/PostGIS tools with connection pooling
- 8 dbt tools with automatic pre-validation
- 100k row limit with chunking support
- Auto-detection of dbt projects

**Commands:** `/data-ingest`, `/data-profile`, `/data-schema`, `/data-explain`, `/data-lineage`, `/lineage-viz`, `/data-run`, `/dbt-test`, `/data-quality`, `/data-review`, `/data-gate`, `/data-setup`

### Visualization

#### [viz-platform](./plugins/viz-platform) *NEW in v4.0.0*
**Dash Mantine Components Validation and Theming**

Visualization toolkit with version-locked component validation and design token theming.

- 3 DMC tools with static JSON registry (prevents prop hallucination)
- 2 Chart tools with Plotly and theme integration
- 5 Layout tools for dashboard composition
- 6 Theme tools with design token system
- 5 Page tools for multi-page app structure
- Dual theme storage: user-level and project-level

**Commands:** `/viz-chart`, `/viz-chart-export`, `/viz-dashboard`, `/viz-theme`, `/viz-theme-new`, `/viz-theme-css`, `/viz-component`, `/accessibility-check`, `/viz-breakpoints`, `/design-review`, `/design-gate`, `/viz-setup`

## Domain Advisory Pattern

The marketplace supports cross-plugin domain advisory integration:

- **Domain Detection**: projman automatically detects when issues involve specialized domains (frontend/viz, data engineering)
- **Acceptance Criteria**: Domain-specific acceptance criteria are added to issues during planning
- **Execution Gates**: Domain validation gates (`/design-gate`, `/data-gate`) run before issue completion
- **Extensible**: New domains can be added by creating advisory agents and gate commands

**Current Domains:**
| Domain | Plugin | Gate Command |
|--------|--------|--------------|
| Visualization | viz-platform | `/design-gate` |
| Data | data-platform | `/data-gate` |

## MCP Servers

MCP servers are **shared at repository root** and configured in `.mcp.json`.

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
| Validation | `validate_compatibility`, `validate_agent_refs`, `validate_data_flow`, `validate_workflow_integration` |
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
/pm-setup
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
| claude-config-maintainer | `/claude-config-maintainer:analyze` |
| cmdb-assistant | `/cmdb-assistant:cmdb-search` |
| data-platform | `/data-platform:data-ingest` |
| viz-platform | `/viz-platform:viz-chart` |
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
