# doc-guardian

Automatic documentation drift detection and synchronization for Claude Code projects.

## Problem Solved

Documentation gets outdated. Functions get renamed, configs change, versions bump—but docs lag behind. This creates:
- Multiple review cycles finding stale references
- Unnecessary commits fixing docs piecemeal
- User confusion from outdated instructions

## Solution

doc-guardian monitors your code changes via hooks:
1. Detects when changes might affect documentation
2. Alerts you to potential drift (doesn't interrupt your flow)
3. Provides commands to audit and sync docs when ready

## Commands

| Command | Description |
|---------|-------------|
| `/doc-audit` | Full project scan - reports all drift without changing anything |
| `/doc-sync` | Apply all pending documentation updates in one commit |

## Hooks

- **PostToolUse (Write|Edit)**: Silently checks if code changes affect docs

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
