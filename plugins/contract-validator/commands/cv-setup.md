---
name: cv setup
description: Interactive setup wizard for contract-validator plugin
---

# /cv setup

## Skills to Load
- skills/visual-output.md
- skills/mcp-tools-reference.md

**Important:** This command uses Bash, Read, Write tools - NOT MCP tools (they work only after setup + restart).

## Workflow

1. **Display header** per `skills/visual-output.md`

2. **Check Python version**:
   ```bash
   python3 --version
   ```
   Requires 3.10+. Stop if below.

3. **Locate MCP server**:
   - Installed: `~/.claude/plugins/marketplaces/mktpl-claude-datasaas/mcp-servers/contract-validator/`
   - Source: `~/claude-plugins-work/mcp-servers/contract-validator/`

4. **Check/create venv**:
   ```bash
   ls .venv/bin/python || (python3 -m venv .venv && .venv/bin/pip install -r requirements.txt)
   ```

5. **Verify MCP server**:
   ```bash
   .venv/bin/python -c "from mcp_server.server import ContractValidatorMCPServer; print('OK')"
   ```

6. **Display success** per `skills/visual-output.md`

7. **Inform user**: Session restart required for MCP tools.

## Post-Setup Commands

- `/cv validate` - Full marketplace validation
- `/cv check-agent` - Validate single agent
- `/cv list-interfaces` - Show all plugin interfaces

## No Configuration Required

This plugin reads plugin manifests and README files directly - no credentials needed.
