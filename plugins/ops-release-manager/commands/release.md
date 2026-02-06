---
description: Release management — version bumping, changelog updates, tag creation
---

# /release

Release management with semantic versioning, changelog generation, and tag management.

## Sub-commands

| Sub-command | Description |
|-------------|-------------|
| `/release setup` | Setup wizard — detect version locations and release conventions |
| `/release prepare` | Prepare release: bump versions, update changelog, create branch |
| `/release validate` | Pre-release checks — verify versions, changelog, dependencies |
| `/release tag` | Create and push git tag with release notes |
| `/release rollback` | Revert a release — remove tag, revert version bump |
| `/release status` | Show current version and unreleased changes |
