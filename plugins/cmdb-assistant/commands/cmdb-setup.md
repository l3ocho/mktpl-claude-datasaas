---
name: cmdb setup
description: Interactive setup wizard for cmdb-assistant plugin
---

# /cmdb setup

Configure the cmdb-assistant plugin with NetBox integration.

## Skills to Load

- `skills/visual-header.md`

## Important Context

- **Uses Bash, Read, Write, AskUserQuestion tools** - NOT MCP tools
- **MCP tools unavailable until after setup + session restart**

## Usage

```
/cmdb setup
```

## Instructions

Execute `skills/visual-header.md` with context "Setup Wizard".

### Phase 1: Environment Validation

```bash
python3 --version
```
If below 3.10, stop and inform user.

### Phase 2: MCP Server Setup

1. Locate NetBox MCP server in marketplace
2. Check virtual environment exists
3. Create venv if missing: `python3 -m venv .venv && pip install -r requirements.txt`

### Phase 3: System Configuration

1. Create config directory: `mkdir -p ~/.config/claude`
2. Check `~/.config/claude/netbox.env` exists
3. If missing, ask user for NetBox API URL (must include `/api`)
4. Create config file with placeholder token
5. Instruct user to add API token manually

### Phase 4: Validation

1. Test API connection if token was added
2. Report result (200=success, 403=invalid token)
3. Display completion summary
4. Remind user to restart session for MCP tools

## Completion Summary

```
CMDB-ASSISTANT SETUP COMPLETE
MCP Server (NetBox):   Ready
System Config:         ~/.config/claude/netbox.env

Restart your Claude Code session for MCP tools.

After restart, try:
- /cmdb device <hostname>
- /cmdb ip <address>
- /cmdb site <name>
- /cmdb search <query>
```

## User Request

$ARGUMENTS
