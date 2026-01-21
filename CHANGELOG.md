# Changelog

All notable changes to the Leo Claude Marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
