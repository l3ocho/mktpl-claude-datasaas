# Configuration Guide - Projman Plugin

For comprehensive configuration instructions, see the **[Centralized Configuration Guide](../../docs/CONFIGURATION.md)**.

## Quick Reference

### Required Configuration

**System-level** (`~/.config/claude/gitea.env`):
```bash
GITEA_URL=https://gitea.example.com
GITEA_TOKEN=your_token
GITEA_ORG=your_organization
```

**Project-level** (`.env` in project root):
```bash
GITEA_REPO=your-repo-name
```

### MCP Server Installation

```bash
cd mcp-servers/gitea
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Verification

```bash
/initial-setup
/labels-sync
```

---

For detailed setup instructions, troubleshooting, and security best practices, see [docs/CONFIGURATION.md](../../docs/CONFIGURATION.md).
