# Changelog

All notable changes to support-claude-mktplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
