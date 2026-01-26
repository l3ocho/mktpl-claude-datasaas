---
description: Interactive setup wizard for contract-validator plugin - verifies MCP server and shows capabilities
---

# Contract-Validator Setup Wizard

This command sets up the contract-validator plugin for cross-plugin compatibility validation.

## Important Context

- **This command uses Bash, Read, Write, and AskUserQuestion tools** - NOT MCP tools
- **MCP tools won't work until after setup + session restart**
- **No external credentials required** - this plugin validates local files only

---

## Phase 1: Environment Validation

### Step 1.1: Check Python Version

```bash
python3 --version
```

Requires Python 3.10+. If below, stop setup and inform user:
```
Python 3.10 or higher is required. Please install it and run /initial-setup again.
```

---

## Phase 2: MCP Server Setup

### Step 2.1: Locate Contract-Validator MCP Server

```bash
# If running from installed marketplace
ls -la ~/.claude/plugins/marketplaces/leo-claude-mktplace/mcp-servers/contract-validator/ 2>/dev/null || echo "NOT_FOUND_INSTALLED"

# If running from source
ls -la ~/claude-plugins-work/mcp-servers/contract-validator/ 2>/dev/null || echo "NOT_FOUND_SOURCE"
```

Determine which path exists and use that as the MCP server path.

### Step 2.2: Check Virtual Environment

```bash
ls -la /path/to/mcp-servers/contract-validator/.venv/bin/python 2>/dev/null && echo "VENV_EXISTS" || echo "VENV_MISSING"
```

### Step 2.3: Create Virtual Environment (if missing)

```bash
cd /path/to/mcp-servers/contract-validator && python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && deactivate
```

**If pip install fails:**
- Show the error to the user
- Suggest: "Check your internet connection and try again."

---

## Phase 3: Validation

### Step 3.1: Verify MCP Server

```bash
cd /path/to/mcp-servers/contract-validator && .venv/bin/python -c "from mcp_server.server import ContractValidatorMCPServer; print('MCP Server OK')"
```

If this fails, check the error and report it to the user.

### Step 3.2: Summary

Display:

```
╔════════════════════════════════════════════════════════════════╗
║          CONTRACT-VALIDATOR SETUP COMPLETE                      ║
╠════════════════════════════════════════════════════════════════╣
║ MCP Server:        ✓ Ready                                      ║
║ Parse Tools:       ✓ Available (2 tools)                        ║
║ Validation Tools:  ✓ Available (3 tools)                        ║
║ Report Tools:      ✓ Available (2 tools)                        ║
╚════════════════════════════════════════════════════════════════╝
```

### Step 3.3: Session Restart Notice

---

**Session Restart Required**

Restart your Claude Code session for MCP tools to become available.

**After restart, you can:**
- Run `/validate-contracts` to check all plugins for compatibility issues
- Run `/check-agent` to validate a single agent definition
- Run `/list-interfaces` to see all plugin commands and tools

---

## Available Tools

| Category | Tools | Description |
|----------|-------|-------------|
| Parse | `parse_plugin_interface`, `parse_claude_md_agents` | Extract interfaces from README.md and agents from CLAUDE.md |
| Validation | `validate_compatibility`, `validate_agent_refs`, `validate_data_flow` | Check conflicts, tool references, and data flows |
| Report | `generate_compatibility_report`, `list_issues` | Generate reports and filter issues |

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/validate-contracts` | Full marketplace compatibility validation |
| `/check-agent` | Validate single agent definition |
| `/list-interfaces` | Show all plugin interfaces |

---

## Use Cases

### 1. Pre-Release Validation
Run `/validate-contracts` before releasing a new marketplace version to catch:
- Command name conflicts between plugins
- Missing tool references in agents
- Broken data flows

### 2. Agent Development
Run `/check-agent` when creating or modifying agents to verify:
- All referenced tools exist
- Data flows are valid
- No undeclared dependencies

### 3. Plugin Audit
Run `/list-interfaces` to get a complete view of:
- All commands across plugins
- All tools available
- Potential overlap areas

---

## No Configuration Required

This plugin doesn't require any configuration files. It reads plugin manifests and README files directly from the filesystem.

**Paths it scans:**
- Marketplace: `~/.claude/plugins/marketplaces/leo-claude-mktplace/plugins/`
- Source (if available): `~/claude-plugins-work/plugins/`
