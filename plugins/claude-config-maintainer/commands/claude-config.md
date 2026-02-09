---
name: claude-config
description: CLAUDE.md and settings optimization — type /claude-config <action> for commands
---

# /claude-config

CLAUDE.md and settings.local.json optimization for Claude Code projects.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/claude-config analyze` | Analyze CLAUDE.md for optimization opportunities |
| `/claude-config optimize` | Optimize CLAUDE.md structure with preview/backup |
| `/claude-config init` | Initialize new CLAUDE.md for a project |
| `/claude-config diff` | Track CLAUDE.md changes over time with behavioral impact |
| `/claude-config lint` | Lint CLAUDE.md for anti-patterns and best practices |
| `/claude-config audit-settings` | Audit settings.local.json permissions (100-point score) |
| `/claude-config optimize-settings` | Optimize permissions (profiles, consolidation, dry-run) |
| `/claude-config permissions-map` | Visual review layer + permission coverage map |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
