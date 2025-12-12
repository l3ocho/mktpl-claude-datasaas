# Changelog

All notable changes to support-claude-mktplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- `docs/CANONICAL-PATHS.md` - Single source of truth for all file paths
- Path verification rules in CLAUDE.md (mandatory pre-flight check)
- Recovery protocol for path issues
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
- Replaced `docs/CORRECT-ARCHITECTURE.md` reference with `docs/CANONICAL-PATHS.md`
- Added mandatory path verification section to CLAUDE.md
- Reorganized documentation into `docs/references/`, `docs/architecture/`, `docs/workflows/`
- Updated CLAUDE.md with file creation governance

### Fixed
- Removed dead reference to non-existent `docs/CORRECT-ARCHITECTURE.md`

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
