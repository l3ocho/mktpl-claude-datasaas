# Release Manager Integration

Add to your project's CLAUDE.md:

## Release Management

This project uses ops-release-manager for versioning and release automation.

### Commands
- `/release setup` - Detect version locations and configure release workflow
- `/release status` - Show current version and unreleased changes
- `/release prepare <major|minor|patch>` - Bump versions and update changelog
- `/release validate` - Pre-release checks before tagging
- `/release tag` - Create annotated git tag with release notes
- `/release rollback` - Revert a release if needed

### Versioning
- Follows [SemVer](https://semver.org/) (MAJOR.MINOR.PATCH)
- Version locations: package.json, README.md, CHANGELOG.md (auto-detected)
- Changelog follows [Keep a Changelog](https://keepachangelog.com) format

### Release Process
1. All changes documented under `[Unreleased]` in CHANGELOG.md
2. Run `/release prepare minor` (or major/patch) when ready
3. Run `/release validate` to verify readiness
4. Run `/release tag --push` to finalize

### Conventions
- Tag format: `vX.Y.Z` (annotated tags with release notes)
- Branch format: `release/X.Y.Z` (for major/minor releases)
- Commit message: `chore(release): prepare vX.Y.Z`
