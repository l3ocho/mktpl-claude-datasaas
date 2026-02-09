# Plugin Commands Cheat Sheet

Quick reference for all commands in the Leo Claude Marketplace (v9.0.0+).

All commands follow the `/<noun> <action>` sub-command pattern.

## Invocation

Commands can be invoked in two ways:

1. **Via dispatch file:** `/doc audit` (routes through dispatch file to invoke `/doc-guardian:doc-audit`)
2. **Direct plugin-prefixed:** `/doc-guardian:doc-audit` (invokes command directly)

Both methods work identically. The dispatch file provides a user-friendly interface with `$ARGUMENTS` parsing, while the direct format bypasses the dispatcher.

If dispatch routing fails, use the direct plugin-prefixed format: `/<plugin-name>:<command-name>`.

**Examples:**
- `/sprint plan` → routes to `/projman:sprint-plan`
- `/doc audit` → routes to `/doc-guardian:doc-audit`
- `/pr review` → routes to `/pr-review:pr-review`

---

## Command Reference Table

| Plugin | Command | Auto | Manual | Description |
|--------|---------|:----:|:------:|-------------|
| **projman** | `/sprint plan` | | X | Start sprint planning with AI-guided architecture analysis and issue creation |
| **projman** | `/sprint start` | | X | Begin sprint execution with dependency analysis and parallel task coordination (requires approval or `--force`) |
| **projman** | `/sprint status` | | X | Check current sprint progress (add `--diagram` for Mermaid visualization) |
| **projman** | `/sprint review` | | X | Pre-sprint-close code quality review (debug artifacts, security, error handling) |
| **projman** | `/sprint test` | | X | Run tests (`/sprint test run`) or generate tests (`/sprint test gen <target>`) |
| **projman** | `/sprint close` | | X | Complete sprint and capture lessons learned to Gitea Wiki |
| **projman** | `/labels sync` | | X | Synchronize label taxonomy from Gitea |
| **projman** | `/projman setup` | | X | Auto-detect mode or use `--full`, `--quick`, `--sync`, `--clear-cache` |
| **projman** | `/rfc create` | | X | Create new RFC from conversation or spec |
| **projman** | `/rfc list` | | X | List all RFCs grouped by status |
| **projman** | `/rfc review` | | X | Submit RFC for maintainer review |
| **projman** | `/rfc approve` | | X | Approve RFC for sprint planning |
| **projman** | `/rfc reject` | | X | Reject RFC with documented reason |
| **projman** | `/project initiation` | | X | Discovery, source analysis, project charter |
| **projman** | `/project plan` | | X | WBS, risk register, sprint roadmap |
| **projman** | `/project status` | | X | Project health check across all sprints |
| **projman** | `/project close` | | X | Final retrospective and archival |
| **projman** | `/adr create` | | X | Create new Architecture Decision Record |
| **projman** | `/adr list` | | X | List all ADRs with status |
| **projman** | `/adr update` | | X | Update existing ADR |
| **projman** | `/adr supersede` | | X | Supersede ADR with new decision |
| **git-flow** | `/gitflow commit` | | X | Create commit with auto-generated conventional message. Flags: `--push`, `--merge`, `--sync` |
| **git-flow** | `/gitflow branch-start` | | X | Create new feature/fix/chore branch with naming conventions |
| **git-flow** | `/gitflow branch-cleanup` | | X | Remove merged branches locally and optionally on remote |
| **git-flow** | `/gitflow status` | | X | Enhanced git status with recommendations |
| **git-flow** | `/gitflow config` | | X | Configure git-flow settings for the project |
| **pr-review** | `/pr setup` | | X | Setup wizard for pr-review (shares Gitea MCP with projman) |
| **pr-review** | `/pr init` | | X | Quick project setup for PR reviews |
| **pr-review** | `/pr sync` | | X | Sync config with git remote after repo move/rename |
| **pr-review** | `/pr review` | | X | Full multi-agent PR review with confidence scoring |
| **pr-review** | `/pr summary` | | X | Quick summary of PR changes |
| **pr-review** | `/pr findings` | | X | List and filter review findings by category/severity |
| **pr-review** | `/pr diff` | | X | Formatted diff with inline review comments and annotations |
| **clarity-assist** | `/clarity clarify` | | X | Full 4-D prompt optimization with ND accommodations |
| **clarity-assist** | `/clarity quick-clarify` | | X | Rapid single-pass clarification for simple requests |
| **doc-guardian** | `/doc audit` | | X | Full documentation audit - scans for doc drift |
| **doc-guardian** | `/doc sync` | | X | Synchronize pending documentation updates |
| **doc-guardian** | `/doc changelog-gen` | | X | Generate changelog from conventional commits |
| **doc-guardian** | `/doc coverage` | | X | Documentation coverage metrics by function/class |
| **doc-guardian** | `/doc stale-docs` | | X | Flag documentation behind code changes |
| **code-sentinel** | `/sentinel scan` | | X | Full security audit (SQL injection, XSS, secrets, etc.) |
| **code-sentinel** | `/sentinel refactor` | | X | Apply refactoring patterns to improve code |
| **code-sentinel** | `/sentinel refactor-dry` | | X | Preview refactoring without applying changes |
| **code-sentinel** | *PreToolUse hook* | X | | Scans code before writing; blocks critical issues |
| **claude-config-maintainer** | `/claude-config analyze` | | X | Analyze CLAUDE.md for optimization opportunities |
| **claude-config-maintainer** | `/claude-config optimize` | | X | Optimize CLAUDE.md structure with preview/backup |
| **claude-config-maintainer** | `/claude-config init` | | X | Initialize new CLAUDE.md for a project |
| **claude-config-maintainer** | `/claude-config diff` | | X | Track CLAUDE.md changes over time with behavioral impact |
| **claude-config-maintainer** | `/claude-config lint` | | X | Lint CLAUDE.md for anti-patterns and best practices |
| **claude-config-maintainer** | `/claude-config audit-settings` | | X | Audit settings.local.json permissions (100-point score) |
| **claude-config-maintainer** | `/claude-config optimize-settings` | | X | Optimize permissions (profiles, consolidation, dry-run) |
| **claude-config-maintainer** | `/claude-config permissions-map` | | X | Visual review layer + permission coverage map |
| **cmdb-assistant** | `/cmdb setup` | | X | Setup wizard for NetBox MCP server |
| **cmdb-assistant** | `/cmdb search` | | X | Search NetBox for devices, IPs, sites |
| **cmdb-assistant** | `/cmdb device` | | X | Manage network devices (create, view, update, delete) |
| **cmdb-assistant** | `/cmdb ip` | | X | Manage IP addresses and prefixes |
| **cmdb-assistant** | `/cmdb site` | | X | Manage sites, locations, racks, and regions |
| **cmdb-assistant** | `/cmdb audit` | | X | Data quality analysis (VMs, devices, naming, roles) |
| **cmdb-assistant** | `/cmdb register` | | X | Register current machine into NetBox with running apps |
| **cmdb-assistant** | `/cmdb sync` | | X | Sync machine state with NetBox (detect drift, update) |
| **cmdb-assistant** | `/cmdb topology` | | X | Infrastructure topology diagrams (rack, network, site views) |
| **cmdb-assistant** | `/cmdb change-audit` | | X | NetBox audit trail queries with filtering |
| **cmdb-assistant** | `/cmdb ip-conflicts` | | X | Detect IP conflicts and overlapping prefixes |
| **project-hygiene** | `/hygiene check` | | X | Project file organization and cleanup check |
| **data-platform** | `/data ingest` | | X | Load data from CSV, Parquet, JSON into DataFrame |
| **data-platform** | `/data profile` | | X | Generate data profiling report with statistics |
| **data-platform** | `/data schema` | | X | Explore database schemas, tables, columns |
| **data-platform** | `/data explain` | | X | Explain query execution plan |
| **data-platform** | `/data lineage` | | X | Show dbt model lineage and dependencies |
| **data-platform** | `/data run` | | X | Run dbt models with validation |
| **data-platform** | `/data lineage-viz` | | X | dbt lineage visualization as Mermaid diagrams |
| **data-platform** | `/data dbt-test` | | X | Formatted dbt test runner with summary and failure details |
| **data-platform** | `/data quality` | | X | DataFrame quality checks (nulls, duplicates, types, outliers) |
| **data-platform** | `/data review` | | X | Comprehensive data integrity audits |
| **data-platform** | `/data gate` | | X | Binary pass/fail data integrity gates |
| **data-platform** | `/data setup` | | X | Setup wizard for data-platform MCP servers |
| **viz-platform** | `/viz setup` | | X | Setup wizard for viz-platform MCP server |
| **viz-platform** | `/viz chart` | | X | Create Plotly charts with theme integration |
| **viz-platform** | `/viz chart-export` | | X | Export charts to PNG, SVG, PDF via kaleido |
| **viz-platform** | `/viz dashboard` | | X | Create dashboard layouts with filters and grids |
| **viz-platform** | `/viz theme` | | X | Apply existing theme to visualizations |
| **viz-platform** | `/viz theme-new` | | X | Create new custom theme with design tokens |
| **viz-platform** | `/viz theme-css` | | X | Export theme as CSS custom properties |
| **viz-platform** | `/viz component` | | X | Inspect DMC component props and validation |
| **viz-platform** | `/viz accessibility-check` | | X | Color blind validation (WCAG contrast ratios) |
| **viz-platform** | `/viz breakpoints` | | X | Configure responsive layout breakpoints |
| **viz-platform** | `/viz design-review` | | X | Detailed design system audits |
| **viz-platform** | `/viz design-gate` | | X | Binary pass/fail design system validation gates |
| **contract-validator** | `/cv validate` | | X | Full marketplace compatibility validation |
| **contract-validator** | `/cv check-agent` | | X | Validate single agent definition |
| **contract-validator** | `/cv list-interfaces` | | X | Show all plugin interfaces |
| **contract-validator** | `/cv dependency-graph` | | X | Mermaid visualization of plugin dependencies |
| **contract-validator** | `/cv setup` | | X | Setup wizard for contract-validator MCP |
| **contract-validator** | `/cv status` | | X | Marketplace-wide health check (installation, MCP, configuration) |

---

## Migration from v8.x

All commands were renamed in v9.0.0 to follow `/<noun> <action>` pattern. See [MIGRATION-v9.md](./MIGRATION-v9.md) for the complete old-to-new mapping.

---

## Plugins by Category

| Category | Plugins | Primary Use |
|----------|---------|-------------|
| **Setup** | projman, pr-review, cmdb-assistant, data-platform, viz-platform, contract-validator | `/projman setup`, `/pr setup`, `/cmdb setup`, `/data setup`, `/viz setup`, `/cv setup` |
| **Task Planning** | projman, clarity-assist | Sprint management, requirement clarification |
| **Code Quality** | code-sentinel, pr-review | Security scanning, PR reviews |
| **Documentation** | doc-guardian, claude-config-maintainer | Doc sync, CLAUDE.md maintenance |
| **Git Operations** | git-flow | Commits, branches, workflow automation |
| **Infrastructure** | cmdb-assistant | NetBox CMDB management |
| **Data Engineering** | data-platform | pandas, PostgreSQL, dbt operations |
| **Visualization** | viz-platform | DMC validation, Plotly charts, theming |
| **Validation** | contract-validator | Cross-plugin compatibility checks |
| **Maintenance** | project-hygiene | Manual cleanup via `/hygiene check` |

---

## Hook-Based Automation Summary

| Plugin | Hook Event | Behavior |
|--------|------------|----------|
| **code-sentinel** | PreToolUse (Write/Edit/MultiEdit) | Scans code before writing; blocks critical security issues |
| **git-flow** | PreToolUse (Bash) | Validates branch naming and commit message conventions |
| **cmdb-assistant** | PreToolUse (MCP create/update) | Validates input data before NetBox writes |
| **clarity-assist** | UserPromptSubmit | Detects vague prompts and suggests clarification |

---

## Dev Workflow Examples

### Example 0: RFC-Driven Feature Development

Full workflow from idea to implementation using RFCs:

```
1. /clarity clarify            # Clarify the feature idea
2. /rfc create                 # Create RFC from clarified spec
   ... refine RFC content ...
3. /rfc review 0001            # Submit RFC for review
   ... review discussion ...
4. /rfc approve 0001           # Approve RFC for implementation
5. /sprint plan                # Select approved RFC for sprint
   ... implement feature ...
6. /sprint close               # Complete sprint, RFC marked Implemented
```

### Example 1: Starting a New Feature Sprint

A typical workflow for planning and executing a feature sprint:

```
1. /clarity clarify             # Clarify requirements if vague
2. /sprint plan                 # Plan the sprint with architecture analysis
3. /labels sync                 # Ensure labels are up-to-date
4. /sprint start                # Begin execution with dependency ordering
5. /gitflow branch-start feat/...  # Create feature branch
   ... implement features ...
6. /gitflow commit              # Commit with conventional message
7. /sprint status --diagram     # Check progress with visualization
8. /sprint review               # Pre-close quality review
9. /sprint test run             # Verify test coverage
10. /sprint close               # Capture lessons learned
```

### Example 2: Daily Development Cycle

Quick daily workflow with git-flow:

```
1. /gitflow status              # Check current state
2. /gitflow branch-start fix/...  # Start bugfix branch
   ... make changes ...
3. /gitflow commit              # Auto-generate commit message
4. /gitflow commit --push       # Commit and push to remote
5. /gitflow branch-cleanup      # Clean merged branches
```

### Example 3: Pull Request Review Workflow

Reviewing a PR before merge:

```
1. /pr summary                  # Quick overview of changes
2. /pr review                   # Full multi-agent review
3. /pr findings                 # Filter findings by severity
4. /sentinel scan               # Deep security audit if needed
```

### Example 4: Documentation Maintenance

Keeping docs in sync:

```
1. /doc audit                   # Scan for documentation drift
2. /doc sync                    # Apply pending updates
3. /claude-config analyze       # Check CLAUDE.md health
4. /claude-config optimize      # Optimize if needed
```

### Example 5: Code Refactoring Session

Safe refactoring with preview:

```
1. /sentinel refactor-dry       # Preview opportunities
2. /sentinel scan               # Baseline security check
3. /sentinel refactor           # Apply improvements
4. /sprint test run             # Verify nothing broke
5. /gitflow commit              # Commit with descriptive message
```

### Example 6: Infrastructure Documentation

Managing infrastructure with CMDB:

```
1. /cmdb search "server"        # Find existing devices
2. /cmdb device view X          # Check device details
3. /cmdb ip list                # List available IPs
4. /cmdb site view Y            # Check site info
```

### Example 6b: Data Engineering Workflow

Working with data pipelines:

```
1. /data ingest file.csv        # Load data into DataFrame
2. /data profile                # Generate data profiling report
3. /data schema                 # Explore database schemas
4. /data lineage model_name     # View dbt model dependencies
5. /data run model_name         # Execute dbt models
6. /data explain "SELECT ..."   # Analyze query execution plan
```

### Example 7: First-Time Setup (New Machine)

Setting up the marketplace for the first time:

```
1. /projman setup --full        # Full setup: MCP + system config + project
   # → Follow prompts for Gitea URL, org
   # → Add token manually when prompted
   # → Confirm repository name
2. # Restart Claude Code session
3. /labels sync                 # Sync Gitea labels
4. /sprint plan                 # Plan first sprint
```

### Example 8: New Project Setup (System Already Configured)

Adding a new project when system config exists:

```
1. /projman setup --quick       # Quick project setup (auto-detected)
   # → Confirms detected repo name
   # → Creates .env
2. /labels sync                 # Sync Gitea labels
3. /sprint plan                 # Plan first sprint
```

---

## Quick Tips

- **Hooks run automatically** - code-sentinel and git-flow protect you without manual invocation
- **Use `/gitflow commit` over `git commit`** - generates better commit messages following conventions
- **Run `/sprint review` before `/sprint close`** - catches issues before closing the sprint
- **Use `/clarity clarify` for vague requests** - especially helpful for complex requirements
- **`/sentinel refactor-dry` is safe** - always preview before applying refactoring changes
- **`/gitflow commit --push`** replaces the old `/git-commit-push` - fewer commands to remember

---

## MCP Server Requirements

Some plugins require MCP server connectivity:

| Plugin | MCP Server | Purpose |
|--------|------------|---------|
| projman | Gitea | Issues, PRs, wiki, labels, milestones |
| pr-review | Gitea | PR operations and reviews |
| cmdb-assistant | NetBox | Infrastructure CMDB |
| data-platform | pandas, PostgreSQL, dbt | DataFrames, database queries, dbt builds |
| viz-platform | viz-platform | DMC validation, charts, layouts, themes, pages |
| contract-validator | contract-validator | Plugin interface parsing, compatibility validation |

Ensure credentials are configured in `~/.config/claude/gitea.env`, `~/.config/claude/netbox.env`, or `~/.config/claude/postgres.env`.

---

*Last Updated: 2026-02-06*
