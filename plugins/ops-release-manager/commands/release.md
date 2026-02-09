---
name: release
description: Release management — type /release <action> for commands
---

# /release

Release management with semantic versioning, changelog generation, and tag management.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `setup` | `/ops-release-manager:release-setup` | Setup wizard — detect version locations and release conventions |
| `prepare` | `/ops-release-manager:release-prepare` | Prepare release: bump versions, update changelog, create branch |
| `validate` | `/ops-release-manager:release-validate` | Pre-release checks — verify versions, changelog, dependencies |
| `tag` | `/ops-release-manager:release-tag` | Create and push git tag with release notes |
| `rollback` | `/ops-release-manager:release-rollback` | Revert a release — remove tag, revert version bump |
| `status` | `/ops-release-manager:release-status` | Show current version and unreleased changes |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/release prepare`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/ops-release-manager:release-prepare`)
