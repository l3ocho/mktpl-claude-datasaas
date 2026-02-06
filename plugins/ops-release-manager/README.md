# ops-release-manager

Release management with semantic versioning, changelog generation, and tag management.

## Overview

ops-release-manager automates the release process: version bumping across all project files, changelog updates following Keep a Changelog format, git tag creation with release notes, and rollback capabilities. It supports Node.js, Python, Rust, and Claude marketplace projects.

## Commands

| Command | Description |
|---------|-------------|
| `/release setup` | Detect version locations and configure release workflow |
| `/release prepare` | Bump versions, update changelog, create release branch |
| `/release validate` | Pre-release checks (versions, changelog, dependencies) |
| `/release tag` | Create annotated git tag with release notes |
| `/release rollback` | Revert a release (remove tag, revert version bump) |
| `/release status` | Show current version and unreleased changes |

## Agents

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| release-coordinator | sonnet | acceptEdits | Version bumping, changelog, tags, branches |
| release-validator | haiku | plan (read-only) | Pre-release validation and dependency checks |

## Skills

| Skill | Purpose |
|-------|---------|
| version-detection | Find version in package.json, pyproject.toml, Cargo.toml, README, etc. |
| semver-rules | SemVer bump logic, conventional commit analysis |
| changelog-conventions | Keep a Changelog format, Unreleased section management |
| release-workflow | Branch-based and tag-based release patterns, rollback procedures |
| visual-header | Consistent command output headers |

## Supported Ecosystems

| Ecosystem | Version File | Lock File |
|-----------|-------------|-----------|
| Node.js | package.json | package-lock.json |
| Python | pyproject.toml, setup.cfg | poetry.lock, requirements.txt |
| Rust | Cargo.toml | Cargo.lock |
| Claude Marketplace | marketplace.json, plugin.json | N/A |

## Release Flow

```
/release status     -> See what is unreleased
/release prepare    -> Bump versions + changelog
/release validate   -> Pre-release checks
/release tag        -> Create git tag
```

If something goes wrong:
```
/release rollback   -> Revert the release
```

## Installation

This plugin is part of the Leo Claude Marketplace. It is installed automatically when the marketplace is configured.

## License

MIT
