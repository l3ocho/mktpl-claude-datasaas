---
name: pr setup
description: Interactive setup wizard for pr-review plugin
---

# /pr setup - PR Review Setup Wizard

## Visual Output

Display header: `PR-REVIEW - Setup Wizard`

## Skills to Load

- skills/setup-workflow.md
- skills/mcp-tools-reference.md
- skills/output-formats.md

## Important Context

- Uses Bash, Read, Write, AskUserQuestion - NOT MCP tools
- MCP tools won't work until after setup + session restart
- Shares Gitea MCP server with projman plugin

## Workflow

### Phase 1: Check Existing Setup

Check `~/.config/claude/gitea.env`. If valid, skip to Phase 3.

### Phase 2: System Setup (if needed)

Execute `skills/setup-workflow.md`: verify Python, create gitea.env, prompt for token

### Phase 3: Project Configuration

Execute `skills/setup-workflow.md`: auto-detect org/repo, validate via API, create .env

### Phase 4: Validation

Test API connection, display completion summary, remind to restart session

## Available Commands After Setup

- `/pr review <number>` - Full multi-agent review
- `/pr summary <number>` - Quick summary
- `/pr findings <number>` - List findings
