# Changelog

All notable changes to support-claude-mktplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Installation script (`scripts/setup.sh`) for new users
- Post-update script (`scripts/post-update.sh`) for updates
- Update documentation (`docs/UPDATING.md`)
- `/initial-setup` slash command
- File creation governance rules in CLAUDE.md
- Architecture diagram specifications in `docs/architecture/`
- `.scratch/` directory for transient work
- `scripts/` directory for setup automation
- `docs/architecture/` for Draw.io diagrams
- `docs/workflows/` for workflow documentation

### Changed
- Reorganized documentation into `docs/references/`, `docs/architecture/`, `docs/workflows/`
- Updated CLAUDE.md with file creation governance

### Removed
- Organization/workspace GID variable (no longer needed)
- Deprecated `cmdb-assistant/` plugin
- Development output files (test scripts, status reports)
- IDE-specific workspace files
- Stray files from project root

## [0.1.0] - Initial Release

### Added
- projman plugin for sprint management
- projman-pmo plugin structure (planned)
- project-hygiene plugin for cleanup automation
- Gitea MCP server
- Wiki.js MCP server
- 43-label taxonomy system
- Lessons learned capture system
- Hybrid configuration system (system + project level)
- Three-agent model (planner, orchestrator, executor)
- Branch-aware security model
