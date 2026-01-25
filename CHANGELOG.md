# Changelog

All notable changes to the Leo Claude Marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

#### New Plugin: data-platform v1.0.0
- **pandas MCP Tools** (14 tools): DataFrame operations with Arrow IPC data_ref persistence
  - `read_csv`, `read_parquet`, `read_json` - Load data with chunking support
  - `to_csv`, `to_parquet` - Export to various formats
  - `describe`, `head`, `tail` - Data exploration
  - `filter`, `select`, `groupby`, `join` - Data transformation
  - `list_data`, `drop_data` - Memory management

- **PostgreSQL MCP Tools** (10 tools): Database operations with asyncpg connection pooling
  - `pg_connect`, `pg_query`, `pg_execute` - Core database operations
  - `pg_tables`, `pg_columns`, `pg_schemas` - Schema exploration
  - `st_tables`, `st_geometry_type`, `st_srid`, `st_extent` - PostGIS spatial support

- **dbt MCP Tools** (8 tools): Build tool wrapper with pre-execution validation
  - `dbt_parse` - Pre-flight validation (catches dbt 1.9+ deprecations)
  - `dbt_run`, `dbt_test`, `dbt_build` - Execution with auto-validation
  - `dbt_compile`, `dbt_ls`, `dbt_docs_generate`, `dbt_lineage` - Analysis tools

- **Commands**: `/ingest`, `/profile`, `/schema`, `/explain`, `/lineage`, `/run`
- **Agents**: `data-ingestion` (loading/transformation), `data-analysis` (exploration/profiling)
- **SessionStart Hook**: Graceful PostgreSQL connection check (non-blocking warning)

- **Key Features**:
  - data_ref system for DataFrame persistence across tool calls
  - 100k row limit with chunking support for large datasets
  - Hybrid configuration (system: `~/.config/claude/postgres.env`, project: `.env`)
  - Auto-detection of dbt projects
  - Arrow IPC format for efficient memory management

---

## [3.2.0] - 2026-01-24

### Added
- **git-flow:** `/commit` now detects protected branches before committing
  - Warns when on protected branch (main, master, development, staging, production)
  - Offers to create feature branch automatically instead of committing directly
  - Configurable via `GIT_PROTECTED_BRANCHES` environment variable
- **netbox:** Platform and primary_ip parameters added to device update tools
- **claude-config-maintainer:** Auto-enforce mandatory behavior rules via SessionStart hook
- **scripts:** `release.sh` - Versioning workflow script for consistent releases
- **scripts:** `verify-hooks.sh` - Verify all hooks are command type

### Changed
- **doc-guardian:** Hook switched from `prompt` type to `command` type
  - Prompt hooks unreliable - Claude ignores explicit instructions
  - New `notify.sh` bash script guarantees exact output behavior
  - Only notifies for config file changes (commands/, agents/, skills/, hooks/)
  - Silent exit for all other files - no blocking possible
- **All hooks:** Converted to command type with stricter plugin prefix enforcement
  - All hooks now mandate `[plugin-name]` prefix with "NO EXCEPTIONS" rule
  - Simplified output formats with word limits
  - Consistent structure across projman, pr-review, code-sentinel, doc-guardian
- **CLAUDE.md:** Replaced destructive "ALWAYS CLEAR CACHE" rule with "VERIFY AND RESTART"
  - Cache clearing mid-session breaks MCP tools
  - Added guidance for proper plugin development workflow

### Fixed
- **cmdb-assistant:** Complete MCP tool schemas for update operations (#138)
- **netbox:** Shorten tool names to meet 64-char API limit (#134)
- **cmdb-assistant:** Correct NetBox API URL format in setup wizard (#132)
- **gitea/projman:** Type safety for `create_label_smart`, curl-based debug-report (#124)
- **netbox:** Add diagnostic logging for JSON parse errors (#121)
- **labels:** Add duplicate check before creating labels (#116)
- **hooks:** Convert ALL hooks to command type with proper prefixes (#114)
- Protected branch workflow: Claude no longer commits directly to protected branches (fixes #109)
- doc-guardian hook no longer blocks workflow (fixes #110)

---

## [3.1.1] - 2026-01-22

### Added
- **git-flow:** `/commit-sync` now prunes stale remote-tracking branches with `git fetch --prune`
- **git-flow:** `/commit-sync` detects and reports local branches with deleted upstreams
- **git-flow:** `/branch-cleanup` now handles stale branches (upstream gone) separately from merged branches
- **git-flow:** New `GIT_CLEANUP_STALE` environment variable for stale branch cleanup control

### Changed
- **All hooks:** Added `[plugin-name]` prefix to all hook messages for better identification
  - `[projman]`, `[pr-review]`, `[code-sentinel]`, `[doc-guardian]` prefixes
- **doc-guardian:** Hook now notification-only (no file reads or blocking operations)
  - Suggests running `/doc-sync` instead of performing inline checks
  - Significantly reduces workflow interruption

### Fixed
- doc-guardian hook no longer stalls workflow with deep file analysis

---

## [3.1.0] - 2026-01-21

### Added

#### Debug Workflow Commands (projman)
- **`/debug-report`** - Run diagnostics in test projects, create structured issues in marketplace
  - Runs 5 diagnostic MCP tool tests with explicit repo parameter
  - Captures full project context (git remote, cwd, branch)
  - Generates structured issue with hypothesis and investigation steps
  - Creates issue in configured marketplace repository automatically

- **`/debug-review`** - Investigate diagnostic issues with human approval gates
  - Lists open diagnostic issues for triage
  - Maps errors to relevant code files using error-to-file mapping
  - MANDATORY: Reads relevant files before proposing any fix
  - Three approval gates: investigation summary, fix approach, PR creation
  - Creates feature branch, commits, and PR with proper linking

#### MCP Server Improvements
- Dynamic label format detection in `suggest_labels`
  - Supports slash format (`Type/Bug`) and colon-space format (`Type: Bug`)
  - Fetches actual labels from repo and matches suggestions to real format
  - Handles Effort/Efforts singular/plural normalization

### Changed
- **`/labels-sync`** completely rewritten with explicit execution steps
  - Step 1 now explicitly requires running `git remote get-url origin` via Bash
  - All MCP tool calls show required `repo` parameter
  - Added "DO NOT" section preventing common mistakes
  - Removed confusing "Label Reference" section that caused file creation prompts

### Fixed
- MCP tools no longer fail with "Use 'owner/repo' format" error
  - Root cause: MCP server is sandboxed and cannot auto-detect project directory
  - Solution: Command documentation now instructs Claude to detect repo via Bash first

---

## [3.0.1] - 2026-01-21

### Added
- `/project-init` command for quick project setup when system is already configured
- `/project-sync` command to sync .env with git remote after repository move/rename
- SessionStart hooks for automatic mismatch detection between git remote and .env
- Interactive setup wizard (`/initial-setup`) redesigned to use Claude tools instead of bash script

### Changed
- `GITEA_ORG` moved from system-level to project-level configuration (different projects may belong to different organizations)
- Environment variables renamed to match MCP server expectations:
  - `GITEA_URL` → `GITEA_API_URL` (must include `/api/v1`)
  - `GITEA_TOKEN` → `GITEA_API_TOKEN`
  - `NETBOX_URL` → `NETBOX_API_URL` (must include `/api`)
  - `NETBOX_TOKEN` → `NETBOX_API_TOKEN`
- Setup commands now validate repository via Gitea API before saving configuration
- README.md simplified to show only wizard setup path (manual setup moved to CONFIGURATION.md)

### Fixed
- API URL paths in curl commands (removed redundant `/api/v1` since it's now in the URL variable)
- Documentation now correctly references environment variable names

---

## [3.0.0] - 2026-01-20

### Added

#### New Plugins
- **clarity-assist** v1.0.0 - Prompt optimization with ND accommodations
  - `/clarify` command for full 4-D methodology optimization
  - `/quick-clarify` command for rapid single-pass clarification
  - clarity-coach agent with ND-friendly questioning patterns
  - prompt-patterns skill with optimization rules

- **git-flow** v1.0.0 - Git workflow automation
  - `/commit` command with smart conventional commit messages
  - `/commit-push`, `/commit-merge`, `/commit-sync` workflow commands
  - `/branch-start`, `/branch-cleanup` branch management commands
  - `/git-status` enhanced status with recommendations
  - `/git-config` interactive configuration
  - git-assistant agent for complex operations
  - workflow-patterns skill with branching strategies

- **pr-review** v1.0.0 - Multi-agent pull request review
  - `/pr-review` command for comprehensive multi-agent review
  - `/pr-summary` command for quick PR overview
  - `/pr-findings` command for filtering review findings
  - coordinator agent for orchestrating reviews
  - security-reviewer, performance-analyst, maintainability-auditor, test-validator agents
  - review-patterns skill with confidence scoring rules

#### Gitea MCP Server Enhancements
- 6 new Pull Request tools:
  - `list_pull_requests` - List PRs with filters
  - `get_pull_request` - Get PR details
  - `get_pr_diff` - Get PR diff
  - `get_pr_comments` - Get PR comments
  - `create_pr_review` - Create review (approve, request changes, comment)
  - `add_pr_comment` - Add comment to PR

#### Documentation
- `docs/CONFIGURATION.md` - Centralized configuration guide for all plugins

### Changed
- **BREAKING:** Marketplace renamed from `claude-code-marketplace` to `leo-claude-mktplace`
- **BREAKING:** MCP servers moved from plugin directories to shared `mcp-servers/` at repository root
- All plugins now have `category`, `tags`, and `license` fields in marketplace.json
- Plugin MCP dependencies now use symlinks to shared servers
- projman version bumped to 3.0.0 (includes PR tools integration)
- projman CONFIGURATION.md slimmed down, links to central docs

### Removed
- Standalone MCP server directories inside plugins (replaced with symlinks)

---

## [2.3.0] - 2026-01-20

### Added

#### New Plugins
- **doc-guardian** v1.0.0 - Documentation lifecycle management
  - `/doc-audit` command for full project documentation drift analysis
  - `/doc-sync` command to batch apply pending documentation updates
  - PostToolUse hook for automatic drift detection
  - Stop hook reminder for pending updates
  - doc-analyzer agent for cross-reference analysis
  - doc-patterns skill for documentation structure knowledge

- **code-sentinel** v1.0.0 - Security scanning and refactoring
  - `/security-scan` command for comprehensive security audit
  - `/refactor` command to apply refactoring patterns
  - `/refactor-dry` command to preview refactoring opportunities
  - PreToolUse hook for real-time security scanning
  - security-reviewer agent for vulnerability analysis
  - refactor-advisor agent for code structure improvements
  - security-patterns skill for vulnerability detection rules

#### projman Enhancements
- `/test-gen` command - Generate unit, integration, and e2e tests for specified code

### Changed
- Marketplace version bumped to 2.3.0
- projman version bumped to 2.3.0

## [2.2.0] - 2026-01-20

### Added
- `/review` command for pre-sprint-close code quality checks (projman)
- `/test-check` command for test verification before sprint close (projman)
- `code-reviewer` agent for structured code review workflow (projman)
- Validation script (`scripts/validate-marketplace.sh`) for marketplace compliance
- `homepage` and `repository` fields to all plugin entries in marketplace.json
- `metadata` wrapper for description/version in marketplace.json
- Keywords to all plugin manifests for better discoverability
- `commands` and `agents` directory references to plugin manifests
- Versioning rule: version displayed only in main README.md title

### Changed
- Updated marketplace.json with required fields per Claude Code spec
- Fixed installation documentation to use official Claude Code methods
- Prioritized public HTTPS URL over Tailscale SSH URL in documentation
- Updated all plugin manifests with author, homepage, repository, license fields
- Consolidated version display to main README.md title only
- Removed version numbers from plugin documentation titles

### Fixed
- Plugin manifests now include all required fields per Claude Code spec
- Installation section uses `extraKnownMarketplaces` instead of undocumented `pluginMarketplace`

### Removed
- `docs/references/` directory (obsolete planning documents)
- Version numbers from individual plugin README titles
- Version section from plugins/projman/README.md

## [2.1.0] - 2026-01-15

### Added
- `docs/CANONICAL-PATHS.md` - Single source of truth for all file paths
- Path verification rules in CLAUDE.md (mandatory pre-flight check)
- Recovery protocol for path issues
- Installation script (`scripts/setup.sh`) for new users
- Post-update script (`scripts/post-update.sh`) for updates
- Update documentation (`docs/UPDATING.md`)
- `/initial-setup` slash command
- File creation governance rules in CLAUDE.md
- `.scratch/` directory for transient work
- `scripts/` directory for setup automation

### Changed
- Replaced `docs/CORRECT-ARCHITECTURE.md` reference with `docs/CANONICAL-PATHS.md`
- Added mandatory path verification section to CLAUDE.md
- Updated CLAUDE.md with file creation governance

### Fixed
- Removed dead reference to non-existent `docs/CORRECT-ARCHITECTURE.md`

### Removed
- Organization/workspace GID variable (no longer needed)
- Development output files (test scripts, status reports)
- IDE-specific workspace files
- Stray files from project root

## [2.0.0] - 2026-01-06

### Added
- Full Gitea integration with wiki, milestones, dependencies
- Parallel execution batching via dependency graph
- Wiki tools for lessons learned (`create_lesson`, `search_lessons`)
- Milestone tools (`list_milestones`, `create_milestone`, `update_milestone`)
- Dependency tools (`list_issue_dependencies`, `create_issue_dependency`, `get_execution_order`)
- Validation tools (`validate_repo_org`, `get_branch_protection`)
- MCP servers bundled inside plugins (not shared at root)

### Changed
- MCP server architecture: bundled in plugins instead of shared at root
- Configuration uses `${CLAUDE_PLUGIN_ROOT}/mcp-servers/` paths

## [1.0.0] - 2025-12-15

### Added
- projman plugin with basic sprint commands
- `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close` commands
- `/labels-sync` command for label taxonomy synchronization
- Three-agent model (planner, orchestrator, executor)
- Gitea MCP server with issue and label tools
- 43-label taxonomy system
- Hybrid configuration system (system + project level)
- Branch-aware security model

## [0.1.0] - 2025-12-01

### Added
- Initial repository structure
- projman plugin structure (planned)
- projman-pmo plugin structure (planned)
- project-hygiene plugin for cleanup automation
- claude-config-maintainer plugin structure
- cmdb-assistant plugin structure
- Basic marketplace manifest
