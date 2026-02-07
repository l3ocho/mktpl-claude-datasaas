# Leo Claude Marketplace — v9.1.2

A plugin marketplace for Claude Code providing sprint management, code review, security scanning, infrastructure automation, and development workflow tools. 20 plugins across 5 domains, backed by 5 shared MCP servers.

## Plugins

### Core (9 plugins — v9.0.1)

| Plugin | Description |
|--------|-------------|
| `projman` | Sprint planning and project management with Gitea integration |
| `git-flow` | Git workflow automation with intelligent commit messages and branch management |
| `pr-review` | Multi-agent pull request review with confidence scoring |
| `code-sentinel` | Security scanning and code refactoring tools |
| `doc-guardian` | Documentation drift detection and synchronization |
| `clarity-assist` | Prompt optimization with ND-friendly accommodations |
| `contract-validator` | Cross-plugin compatibility validation and agent verification |
| `claude-config-maintainer` | CLAUDE.md and settings.local.json optimization |
| `project-hygiene` | Manual project file cleanup checks |

### Data (3 plugins)

| Plugin | Version | Description |
|--------|---------|-------------|
| `data-platform` | 9.0.1 | pandas, PostgreSQL/PostGIS, and dbt integration |
| `viz-platform` | 9.0.1 | Dash Mantine Components validation, Plotly charts, and theming |
| `data-seed` | 0.1.0 — scaffold | Test data generation and database seeding |

### Ops (3 plugins)

| Plugin | Version | Description |
|--------|---------|-------------|
| `cmdb-assistant` | 9.0.1 | NetBox CMDB integration with data quality validation |
| `ops-release-manager` | 0.1.0 — scaffold | Release management with SemVer and changelog automation |
| `ops-deploy-pipeline` | 0.1.0 — scaffold | Deployment pipeline for Docker Compose and systemd |

### SaaS (4 plugins — v0.1.0 scaffolds)

| Plugin | Description |
|--------|-------------|
| `saas-api-platform` | REST/GraphQL API scaffolding for FastAPI and Express |
| `saas-db-migrate` | Database migration management for Alembic, Prisma, raw SQL |
| `saas-react-platform` | React frontend toolkit for Next.js and Vite |
| `saas-test-pilot` | Test automation for pytest, Jest, Vitest, Playwright |

### Debug (1 plugin — v0.1.0 scaffold)

| Plugin | Description |
|--------|-------------|
| `debug-mcp` | MCP server debugging, inspection, and development toolkit |

## Quick Start

### Launch with profiles

```bash
./scripts/claude-launch.sh [profile] [extra-args...]
```

| Profile | Plugins Loaded | Use Case |
|---------|----------------|----------|
| `sprint` | projman, git-flow, pr-review, code-sentinel, doc-guardian, clarity-assist | Default. Sprint planning and development |
| `review` | pr-review, code-sentinel | Lightweight code review |
| `data` | data-platform, viz-platform | Data engineering and visualization |
| `infra` | cmdb-assistant | Infrastructure/CMDB management |
| `full` | All 20 plugins | When you need everything |

```bash
./scripts/claude-launch.sh                    # Default sprint profile
./scripts/claude-launch.sh data --model opus  # Data profile with Opus
./scripts/claude-launch.sh full               # Load all plugins
```

### Common commands

```bash
/sprint plan                  # Plan a sprint with architecture analysis
/sprint start                 # Begin sprint execution
/gitflow commit --push        # Commit with auto-generated message and push
/pr review                    # Full multi-agent PR review
/sentinel scan                # Security audit
/doc audit                    # Check for documentation drift
/cv status                    # Marketplace health check
```

## Repository Structure

```
leo-claude-mktplace/
├── .claude-plugin/                # Marketplace manifest
│   ├── marketplace.json
│   ├── marketplace-lean.json      # Lean profile (6 core plugins)
│   └── marketplace-full.json      # Full profile (all plugins)
├── mcp-servers/                   # Shared MCP servers
│   ├── gitea/                     # Gitea (issues, PRs, wiki)
│   ├── netbox/                    # NetBox (DCIM, IPAM)
│   ├── data-platform/             # pandas, PostgreSQL, dbt
│   ├── viz-platform/              # DMC, Plotly, theming
│   └── contract-validator/        # Plugin compatibility validation
├── plugins/                       # All plugins (20 total)
│   ├── projman/                   # [core] Sprint management
│   ├── git-flow/                  # [core] Git workflow automation
│   ├── pr-review/                 # [core] PR review
│   ├── clarity-assist/            # [core] Prompt optimization
│   ├── doc-guardian/              # [core] Documentation drift detection
│   ├── code-sentinel/             # [core] Security scanning
│   ├── claude-config-maintainer/  # [core] CLAUDE.md optimization
│   ├── contract-validator/        # [core] Cross-plugin validation
│   ├── project-hygiene/           # [core] Manual cleanup checks
│   ├── cmdb-assistant/            # [ops] NetBox CMDB integration
│   ├── data-platform/             # [data] Data engineering
│   ├── viz-platform/              # [data] Visualization
│   ├── data-seed/                 # [data] Test data generation (scaffold)
│   ├── saas-api-platform/         # [saas] API scaffolding (scaffold)
│   ├── saas-db-migrate/           # [saas] DB migrations (scaffold)
│   ├── saas-react-platform/       # [saas] React toolkit (scaffold)
│   ├── saas-test-pilot/           # [saas] Test automation (scaffold)
│   ├── ops-release-manager/       # [ops] Release management (scaffold)
│   ├── ops-deploy-pipeline/       # [ops] Deployment pipeline (scaffold)
│   └── debug-mcp/                 # [debug] MCP debugging (scaffold)
├── scripts/                       # Setup and maintenance
│   ├── setup.sh                   # Initial setup (create venvs, config)
│   ├── post-update.sh             # Post-update (clear cache, changelog)
│   ├── setup-venvs.sh             # MCP server venv management (cache-based)
│   ├── validate-marketplace.sh    # Marketplace compliance validation
│   ├── verify-hooks.sh            # Hook inventory verification
│   ├── release.sh                 # Release automation with version bumping
│   ├── claude-launch.sh           # Profile-based launcher
│   ├── install-plugin.sh          # Install plugin to consumer project
│   ├── list-installed.sh          # Show installed plugins in a project
│   └── uninstall-plugin.sh        # Remove plugin from consumer project
├── docs/                          # Documentation
│   ├── ARCHITECTURE.md            # System architecture & plugin reference
│   ├── CANONICAL-PATHS.md         # Authoritative path reference
│   ├── COMMANDS-CHEATSHEET.md     # All commands quick reference
│   ├── CONFIGURATION.md           # Centralized setup guide
│   ├── DEBUGGING-CHECKLIST.md     # Systematic troubleshooting guide
│   ├── MIGRATION-v9.md            # v8.x to v9.0.0 migration guide
│   └── UPDATING.md               # Update guide
├── CLAUDE.md                      # Project instructions for Claude Code
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

## MCP Servers

All MCP servers are shared at repository root and configured in `.mcp.json`.

| Server | Used By | External System |
|--------|---------|-----------------|
| gitea | projman, pr-review | Gitea (issues, PRs, wiki, milestones) |
| netbox | cmdb-assistant | NetBox (DCIM, IPAM) |
| data-platform | data-platform | PostgreSQL, dbt |
| viz-platform | viz-platform | DMC component registry |
| contract-validator | contract-validator | Internal validation |

## Installation

### Prerequisites

- Claude Code installed
- Python 3.10+
- Access to target services (Gitea, NetBox as needed)

### Add marketplace to Claude Code

```bash
/plugin marketplace add https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace.git
```

Or add to `.claude/settings.json`:

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

### Setup MCP servers

After installing, create Python venvs for MCP servers:

```bash
cd ~/.claude/plugins/marketplaces/leo-claude-mktplace && ./scripts/setup.sh
```

Then restart Claude Code and run the interactive setup:

```
/projman setup
```

See [CONFIGURATION.md](./docs/CONFIGURATION.md) for manual setup and advanced options.

### Install to consumer projects

```bash
./scripts/install-plugin.sh <plugin-name> /path/to/project
./scripts/list-installed.sh /path/to/project
./scripts/uninstall-plugin.sh <plugin-name> /path/to/project
```

## Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](./CLAUDE.md) | Project instructions for Claude Code |
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | System architecture and plugin reference |
| [COMMANDS-CHEATSHEET.md](./docs/COMMANDS-CHEATSHEET.md) | All commands quick reference |
| [CONFIGURATION.md](./docs/CONFIGURATION.md) | Centralized setup guide |
| [DEBUGGING-CHECKLIST.md](./docs/DEBUGGING-CHECKLIST.md) | Systematic troubleshooting guide |
| [UPDATING.md](./docs/UPDATING.md) | Update guide for the marketplace |
| [MIGRATION-v9.md](./docs/MIGRATION-v9.md) | v8.x to v9.0.0 migration guide |
| [CANONICAL-PATHS.md](./docs/CANONICAL-PATHS.md) | Authoritative path reference |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |

## Validation

```bash
./scripts/validate-marketplace.sh    # Marketplace compliance (manifests, domains, paths)
./scripts/verify-hooks.sh            # Hook inventory (4 PreToolUse + 1 UserPromptSubmit)
```

## License

MIT License

## Support

- **Repository**: https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace.git
