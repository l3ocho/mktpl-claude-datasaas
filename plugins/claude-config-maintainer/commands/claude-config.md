---
name: claude-config
description: CLAUDE.md and settings optimization — type /claude-config <action> for commands
---

# /claude-config

CLAUDE.md and settings.local.json optimization for Claude Code projects.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `analyze` | `/claude-config-maintainer:claude-config-analyze` | Analyze CLAUDE.md for optimization opportunities |
| `optimize` | `/claude-config-maintainer:claude-config-optimize` | Optimize CLAUDE.md structure with preview/backup |
| `init` | `/claude-config-maintainer:claude-config-init` | Initialize new CLAUDE.md for a project |
| `diff` | `/claude-config-maintainer:claude-config-diff` | Track CLAUDE.md changes over time with behavioral impact |
| `lint` | `/claude-config-maintainer:claude-config-lint` | Lint CLAUDE.md for anti-patterns and best practices |
| `audit-settings` | `/claude-config-maintainer:claude-config-audit-settings` | Audit settings.local.json permissions (100-point score) |
| `optimize-settings` | `/claude-config-maintainer:claude-config-optimize-settings` | Optimize permissions (profiles, consolidation, dry-run) |
| `permissions-map` | `/claude-config-maintainer:claude-config-permissions-map` | Visual review layer + permission coverage map |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/claude-config analyze`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/claude-config-maintainer:claude-config-analyze`)
