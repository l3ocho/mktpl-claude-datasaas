# Design: ops-release-manager

**Domain:** `ops`
**Target Version:** v9.6.0

## Purpose

Release management automation including semantic versioning, changelog generation, release branch creation, and tag management. Coordinates the release process across git, changelogs, and package manifests.

## Target Users

- Project maintainers managing releases
- Teams following SemVer and conventional commits
- Projects with multiple version locations to keep in sync

## Commands

| Command | Description |
|---------|-------------|
| `/release setup` | Setup wizard — detect version locations, configure release flow |
| `/release prepare` | Prepare release: bump versions, update changelog, create branch |
| `/release validate` | Pre-release checks (clean tree, tests pass, changelog has content) |
| `/release tag` | Create and push git tag with release notes |
| `/release rollback` | Revert a release (delete tag, revert version bump commit) |
| `/release status` | Show current version, unreleased changes, next version suggestion |

## Agent Architecture

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| `release-coordinator` | sonnet | acceptEdits | Version bumping, changelog updates, branch/tag creation |
| `release-validator` | haiku | plan | Pre-release validation, dependency checks |

## Skills

| Skill | Purpose |
|-------|---------|
| `version-detection` | Find version locations (package.json, pyproject.toml, marketplace.json, etc.) |
| `semver-rules` | SemVer bump logic based on conventional commits |
| `changelog-conventions` | Keep a Changelog format, unreleased section management |
| `release-workflow` | Branch-based vs tag-based release patterns |
| `visual-header` | Standard command output headers |

## MCP Server

**Not required.** All operations are git and file-based.

## Integration Points

| Plugin | Integration |
|--------|-------------|
| git-flow | `/release prepare` uses gitflow conventions for branch creation |
| doc-guardian | `/release validate` checks documentation is up to date |
| projman | Sprint close can trigger `/release prepare` for sprint-based releases |
| ops-deploy-pipeline | Release tags trigger deployment pipeline |

## Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| `claude-md-integration.md` | ~600 |
| Dispatch file (`release.md`) | ~200 |
| 6 commands (avg) | ~3,600 |
| 2 agents | ~1,200 |
| 5 skills | ~2,000 |
| **Total** | **~7,600** |

## Open Questions

- Should this subsume the existing `release.sh` script in this repo?
- Support for GitHub Releases / Gitea Releases API via MCP?
