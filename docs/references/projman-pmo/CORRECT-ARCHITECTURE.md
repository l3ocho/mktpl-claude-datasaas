# DEFINITIVE ARCHITECTURE - FINAL CORRECT VERSION

## ⚠️ THIS IS THE ONLY CORRECT STRUCTURE ⚠️

If you see ANY other structure in ANY other document, **THIS ONE IS CORRECT**.

---

## Repository Structure (FINAL)

```
your-gitea/hyperhivelabs/claude-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── mcp-servers/                    # ← SHARED BY BOTH PLUGINS
│   ├── gitea/
│   │   ├── .venv/
│   │   ├── requirements.txt
│   │   ├── mcp_server/
│   │   │   ├── __init__.py
│   │   │   ├── server.py
│   │   │   ├── config.py
│   │   │   ├── gitea_client.py
│   │   │   └── tools/
│   │   │       ├── __init__.py
│   │   │       ├── issues.py
│   │   │       └── labels.py
│   │   └── tests/
│   │       ├── test_config.py
│   │       ├── test_gitea_client.py
│   │       └── test_tools.py
│   └── wikijs/
│       ├── .venv/
│       ├── requirements.txt
│       ├── mcp_server/
│       │   ├── __init__.py
│       │   ├── server.py
│       │   ├── config.py
│       │   ├── wikijs_client.py
│       │   └── tools/
│       │       ├── __init__.py
│       │       ├── pages.py
│       │       ├── lessons_learned.py
│       │       └── documentation.py
│       └── tests/
│           ├── test_config.py
│           ├── test_wikijs_client.py
│           └── test_tools.py
├── projman/                        # ← PROJECT PLUGIN
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── .mcp.json                   # Points to ../mcp-servers/
│   ├── commands/
│   │   ├── sprint-plan.md
│   │   ├── sprint-start.md
│   │   ├── sprint-status.md
│   │   ├── sprint-close.md
│   │   └── labels-sync.md
│   ├── agents/
│   │   ├── planner.md
│   │   ├── orchestrator.md
│   │   └── executor.md
│   ├── skills/
│   │   └── label-taxonomy/
│   │       └── labels-reference.md
│   ├── README.md
│   └── CONFIGURATION.md
└── projman-pmo/                    # ← PMO PLUGIN
    ├── .claude-plugin/
    │   └── plugin.json
    ├── .mcp.json                   # Points to ../mcp-servers/
    ├── commands/
    │   ├── pmo-status.md
    │   ├── pmo-priorities.md
    │   ├── pmo-dependencies.md
    │   └── pmo-schedule.md
    ├── agents/
    │   └── pmo-coordinator.md
    └── README.md
```

---

## Key Points

### 1. MCP Servers Are SHARED
- Location: `mcp-servers/` at repository root
- NOT inside `projman/` or `projman-pmo/`
- Built ONCE, used by BOTH plugins

### 2. Plugins Reference MCP Servers
- Both plugins use `.mcp.json` to point to `../mcp-servers/`
- No MCP code inside plugin directories
- Only commands, agents, and skills in plugin directories

### 3. Mode Detection
- MCP servers detect mode based on environment variables
- Project mode: When `GITEA_REPO` and `WIKIJS_PROJECT` present
- Company mode: When those variables absent (PMO)

---

## Configuration Files

### projman/.mcp.json

```json
{
  "mcpServers": {
    "gitea-projman": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea",
        "GITEA_API_URL": "${GITEA_API_URL}",
        "GITEA_API_TOKEN": "${GITEA_API_TOKEN}",
        "GITEA_OWNER": "${GITEA_OWNER}",
        "GITEA_REPO": "${GITEA_REPO}"
      }
    },
    "wikijs-projman": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
        "WIKIJS_API_URL": "${WIKIJS_API_URL}",
        "WIKIJS_API_TOKEN": "${WIKIJS_API_TOKEN}",
        "WIKIJS_BASE_PATH": "${WIKIJS_BASE_PATH}",
        "WIKIJS_PROJECT": "${WIKIJS_PROJECT}"
      }
    }
  }
}
```

### projman-pmo/.mcp.json

```json
{
  "mcpServers": {
    "gitea-pmo": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea",
        "GITEA_API_URL": "${GITEA_API_URL}",
        "GITEA_API_TOKEN": "${GITEA_API_TOKEN}",
        "GITEA_OWNER": "${GITEA_OWNER}"
      }
    },
    "wikijs-pmo": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
        "WIKIJS_API_URL": "${WIKIJS_API_URL}",
        "WIKIJS_API_TOKEN": "${WIKIJS_API_TOKEN}",
        "WIKIJS_BASE_PATH": "${WIKIJS_BASE_PATH}"
      }
    }
  }
}
```

**Critical:** Both plugins point to `../mcp-servers/` using relative paths.

---

## Setup Instructions

### 1. System Configuration

```bash
# Create config directory
mkdir -p ~/.config/claude

# Gitea config
cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
GITEA_API_TOKEN=your_token
GITEA_OWNER=hyperhivelabs
EOF

# Wiki.js config
cat > ~/.config/claude/wikijs.env << EOF
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_token
WIKIJS_BASE_PATH=/hyper-hive-labs
EOF

# Secure files
chmod 600 ~/.config/claude/*.env
```

### 2. Project Configuration

```bash
# In each project root
cat > .env << EOF
GITEA_REPO=cuisineflow
WIKIJS_PROJECT=projects/cuisineflow
EOF

# Add to .gitignore
echo ".env" >> .gitignore
```

### 3. Install MCP Servers (ONE TIME)

```bash
# Gitea MCP Server
cd /path/to/claude-plugins/mcp-servers/gitea
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Wiki.js MCP Server
cd /path/to/claude-plugins/mcp-servers/wikijs
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## What Makes This Work

### Mode Detection in config.py

```python
# mcp-servers/gitea/mcp_server/config.py
def load(self):
    # ... load configs ...
    
    self.repo = os.getenv('GITEA_REPO')  # Optional
    
    if self.repo:
        self.mode = 'project'
        logger.info(f"Running in project mode: {self.repo}")
    else:
        self.mode = 'company'
        logger.info("Running in company-wide mode (PMO)")
    
    return {
        'api_url': self.api_url,
        'api_token': self.api_token,
        'owner': self.owner,
        'repo': self.repo,
        'mode': self.mode
    }
```

### Same MCP Code, Different Behavior

The SAME MCP server code runs differently based on environment variables:

**When projman calls it:**
- Has `GITEA_REPO` → operates on single repository
- Has `WIKIJS_PROJECT` → operates on single project path

**When projman-pmo calls it:**
- No `GITEA_REPO` → operates on all repositories
- No `WIKIJS_PROJECT` → operates on entire company namespace

---

## Visual Path Flow

### projman Plugin Flow
```
projman/.mcp.json
    ↓ (cwd: ../mcp-servers/gitea)
mcp-servers/gitea/mcp_server/server.py
    ↓ (loads config)
mcp-servers/gitea/mcp_server/config.py
    ↓ (detects GITEA_REPO present)
    → PROJECT MODE
```

### projman-pmo Plugin Flow
```
projman-pmo/.mcp.json
    ↓ (cwd: ../mcp-servers/gitea)
mcp-servers/gitea/mcp_server/server.py
    ↓ (loads config)
mcp-servers/gitea/mcp_server/config.py
    ↓ (detects NO GITEA_REPO)
    → COMPANY MODE
```

---

## File Paths Quick Reference

### Gitea MCP Server Files
- Config loader: `mcp-servers/gitea/mcp_server/config.py`
- API client: `mcp-servers/gitea/mcp_server/gitea_client.py`
- Server entry: `mcp-servers/gitea/mcp_server/server.py`
- Issue tools: `mcp-servers/gitea/mcp_server/tools/issues.py`
- Label tools: `mcp-servers/gitea/mcp_server/tools/labels.py`

### Wiki.js MCP Server Files
- Config loader: `mcp-servers/wikijs/mcp_server/config.py`
- API client: `mcp-servers/wikijs/mcp_server/wikijs_client.py`
- Server entry: `mcp-servers/wikijs/mcp_server/server.py`
- Page tools: `mcp-servers/wikijs/mcp_server/tools/pages.py`
- Lessons tools: `mcp-servers/wikijs/mcp_server/tools/lessons_learned.py`

### Plugin Files
- projman config: `projman/.mcp.json`
- projman-pmo config: `projman-pmo/.mcp.json`

---

## This Is The Truth

**If ANY other document shows MCP servers inside plugin directories, that document is WRONG.**

**THIS document shows the CORRECT, FINAL architecture.**

Use this as your reference. Period.