---
name: doc
description: Documentation management and drift detection — type /doc <action> for commands
---

# /doc

Documentation management, drift detection, and synchronization.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/doc audit` | Full documentation audit - scans for doc drift |
| `/doc sync` | Synchronize pending documentation updates |
| `/doc changelog-gen` | Generate changelog from conventional commits |
| `/doc coverage` | Documentation coverage metrics by function/class |
| `/doc stale-docs` | Flag documentation behind code changes |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
