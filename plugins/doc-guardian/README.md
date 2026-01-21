# doc-guardian

Automatic documentation drift detection and synchronization for Claude Code projects.

## Problem Solved

Documentation gets outdated. Functions get renamed, configs change, versions bump—but docs lag behind. This creates:
- Multiple review cycles finding stale references
- Unnecessary commits fixing docs piecemeal
- User confusion from outdated instructions

## Solution

doc-guardian watches your code changes and automatically:
1. Detects when changes affect documentation
2. Queues updates silently (doesn't interrupt your flow)
3. Syncs all doc changes in a single commit when ready

## Commands

| Command | Description |
|---------|-------------|
| `/doc-audit` | Full project scan - reports all drift without changing anything |
| `/doc-sync` | Apply all pending documentation updates in one commit |

## Hooks

- **PostToolUse (Write\|Edit)**: Silently checks if code changes affect docs
- **Stop**: Reminds you of pending doc updates before session ends

## What It Detects

- **Broken References**: Function/class renamed but docs still use old name
- **Version Drift**: Python 3.9 in docs but 3.11 in pyproject.toml
- **Missing Docs**: Public functions without docstrings
- **Stale Examples**: CLI examples that no longer work

## Installation

This plugin is part of the Leo Claude Marketplace.

```bash
/plugin marketplace add https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace.git
/plugin install doc-guardian
```

## Integration

See claude-md-integration.md for CLAUDE.md additions.
