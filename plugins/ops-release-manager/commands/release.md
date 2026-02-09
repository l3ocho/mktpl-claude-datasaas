---
name: release
description: Release management — type /release <action> for commands
---

# /release

Release management with semantic versioning, changelog generation, and tag management.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/release setup` | Setup wizard — detect version locations and release conventions |
| `/release prepare` | Prepare release: bump versions, update changelog, create branch |
| `/release validate` | Pre-release checks — verify versions, changelog, dependencies |
| `/release tag` | Create and push git tag with release notes |
| `/release rollback` | Revert a release — remove tag, revert version bump |
| `/release status` | Show current version and unreleased changes |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
