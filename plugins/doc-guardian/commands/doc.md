---
name: doc
description: Documentation management and drift detection — type /doc <action> for commands
---

# /doc

Documentation management, drift detection, and synchronization.

When invoked without a sub-command or with `$ARGUMENTS`, handle as follows:

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `audit` | `/doc-guardian:doc-audit` | Full documentation audit - scans for doc drift |
| `sync` | `/doc-guardian:doc-sync` | Synchronize pending documentation updates |
| `changelog-gen` | `/doc-guardian:doc-changelog-gen` | Generate changelog from conventional commits |
| `coverage` | `/doc-guardian:doc-coverage` | Documentation coverage metrics by function/class |
| `stale-docs` | `/doc-guardian:doc-stale-docs` | Flag documentation behind code changes |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/doc audit`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/doc-guardian:doc-audit`)
