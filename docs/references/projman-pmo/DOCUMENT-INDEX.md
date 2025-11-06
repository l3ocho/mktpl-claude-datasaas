# ProjMan Implementation - Document Index

All documentation for building the projman and projman-pmo plugins.

---

## ⚠️ START HERE - CORRECT ARCHITECTURE

### [CORRECT-ARCHITECTURE.md](./CORRECT-ARCHITECTURE.md)
**⚠️ THIS IS THE DEFINITIVE REFERENCE ⚠️**
**Use when:** You need to verify the correct repository structure
**Contains:**
- THE ONLY CORRECT repository structure
- MCP servers are SHARED at root level (`mcp-servers/` directory)
- Configuration file examples
- Setup instructions
- Path references
- Mode detection implementation

**If any other document conflicts with this, THIS ONE IS CORRECT.**

---

## 📚 Core Implementation Documents

### [projman-implementation-plan-updated.md](./projman-implementation-plan-updated.md)
**Purpose:** Complete, detailed implementation plan
**Use when:** Actually building the plugins (your main reference)
**Contains:**
- 12 detailed implementation phases
- Configuration architecture
- Complete code examples
- Success criteria per phase
- Testing strategies
- No timelines - work at your pace
- **Length:** Comprehensive (2000+ lines)

---

## 🐍 Python-Specific Guides

### [projman-python-quickstart.md](./projman-python-quickstart.md)
**Purpose:** Python-specific implementation guide
**Use when:** Setting up Python environment, writing code
**Contains:**
- Python project structure
- Virtual environment setup
- Requirements.txt examples
- Configuration loader code
- Modular code patterns
- Testing with pytest
- Debugging tips

---

## 🏗️ Architecture Documentation

### [two-mcp-architecture-guide.md](./two-mcp-architecture-guide.md)
**Purpose:** Deep dive into two-MCP-server architecture
**Use when:** Understanding the MCP server design
**Contains:**
- Wiki.js structure at `/hyper-hive-labs`
- Complete Gitea MCP server code
- Complete Wiki.js MCP server code (GraphQL)
- Configuration examples
- Mode detection implementation
- Setup instructions
- Migration guidance

---

## 🎯 How to Use These Documents

### Phase 1: Planning & Setup
1. Read **CORRECT-ARCHITECTURE.md** to understand the definitive repository structure
2. Review **projman-implementation-plan-updated.md** Phase 1 for setup overview
3. Set up your Gitea and Wiki.js instances
4. Create system-level configuration files

### Phase 2: Starting Implementation
1. Open **projman-implementation-plan-updated.md** (your main reference for all 12 phases)
2. Start with Phase 1.1a (Gitea MCP Server)
3. Reference **projman-python-quickstart.md** for Python patterns and virtual environment setup
4. Reference **two-mcp-architecture-guide.md** for detailed MCP server code examples

### Phase 3: During Development
1. **Main reference:** projman-implementation-plan-updated.md (follow phase by phase)
2. **Structure reference:** CORRECT-ARCHITECTURE.md (when in doubt about paths)
3. **Code patterns:** projman-python-quickstart.md
4. **Architecture deep dive:** two-mcp-architecture-guide.md

### Phase 4: Troubleshooting
1. Check **CORRECT-ARCHITECTURE.md** for definitive path references
2. Review configuration examples in **two-mcp-architecture-guide.md**
3. Check Python-specific debugging in **projman-python-quickstart.md**
4. Verify setup instructions in **projman-implementation-plan-updated.md** Phase 1.3

---

## 📖 Document Relationships

```
CORRECT-ARCHITECTURE.md (definitive structure)
    ↓ (referenced by)
    ├── projman-implementation-plan-updated.md (main implementation guide)
    │       ↓ (uses Python patterns from)
    │       ├── projman-python-quickstart.md
    │       ↓ (references architecture from)
    │       └── two-mcp-architecture-guide.md
    └── DOCUMENT-INDEX.md (this file - navigation)
```

---

## 🎨 Quick Reference by Topic

### Repository Structure
- **Definitive reference:** CORRECT-ARCHITECTURE.md (lines 9-80)
- **Key point:** MCP servers are SHARED at `mcp-servers/` directory (not inside plugins)

### Configuration
- **Setup instructions:** CORRECT-ARCHITECTURE.md (lines 172-229)
- **Implementation details:** projman-implementation-plan-updated.md (Phase 1.3)
- **Python code examples:** projman-python-quickstart.md (lines 140-214)
- **Config loader:** two-mcp-architecture-guide.md (lines 281-358)

### MCP Servers
- **Architecture overview:** CORRECT-ARCHITECTURE.md (Key Points section)
- **Gitea MCP:** projman-implementation-plan-updated.md (Phase 1.1a)
- **Wiki.js MCP:** projman-implementation-plan-updated.md (Phase 1.1b)
- **Complete implementation:** two-mcp-architecture-guide.md (lines 277-680)

### Wiki.js Structure
- **Full structure:** two-mcp-architecture-guide.md (lines 13-70)
- **Path resolution:** projman-implementation-plan-updated.md (lines 110-115)
- **Integration:** projman-implementation-plan-updated.md (Phase 4.1)

### Python Patterns
- **Setup & dependencies:** projman-python-quickstart.md (lines 15-111)
- **Modular code structure:** projman-python-quickstart.md (lines 511-575)
- **Virtual environment:** projman-python-quickstart.md (lines 579-616)

### Sprint Workflow
- **Commands:** projman-implementation-plan-updated.md (Phase 2)
- **Agents:** projman-implementation-plan-updated.md (Phase 3)
- **Lessons Learned:** projman-implementation-plan-updated.md (Phase 4)

### PMO Plugin
- **Requirements:** projman-implementation-plan-updated.md (Phase 9)
- **Implementation:** projman-implementation-plan-updated.md (Phase 10-11)
- **Multi-project methods:** two-mcp-architecture-guide.md (lines 639-679)

---

## 🚀 Suggested Reading Order

### First Time (Understanding the Project)
1. **CORRECT-ARCHITECTURE.md** (15 minutes)
   - Understand the definitive repository structure
   - See MCP server placement (shared at root)
   - Review configuration approach

2. **projman-python-quickstart.md** (30 minutes)
   - Understand Python setup
   - See code patterns
   - Virtual environment setup

3. **projman-implementation-plan-updated.md** (2-3 hours)
   - Read Phase 1 in detail
   - Skim Phases 2-12 to understand the flow
   - This is your main implementation guide

4. **two-mcp-architecture-guide.md** (1 hour)
   - Deep dive into MCP server architecture
   - Complete code examples
   - Wiki.js structure and integration

### During Implementation
- Keep **projman-implementation-plan-updated.md** open (your main reference)
- Reference **CORRECT-ARCHITECTURE.md** when unsure about paths
- Use **projman-python-quickstart.md** for Python-specific code
- Use **two-mcp-architecture-guide.md** for detailed MCP implementation

### When You Need Quick Answers
- **"What's the correct repository structure?"** → CORRECT-ARCHITECTURE.md
- **"How do I set up Python?"** → projman-python-quickstart.md
- **"How does configuration work?"** → CORRECT-ARCHITECTURE.md or two-mcp-architecture-guide.md
- **"What's the full MCP server code?"** → two-mcp-architecture-guide.md
- **"What do I build in Phase X?"** → projman-implementation-plan-updated.md

---

## 📊 Document Statistics

| Document | Lines | Focus | Primary Use |
|----------|-------|-------|-------------|
| CORRECT-ARCHITECTURE.md | 325 | Definitive Structure | Reference (paths, config) |
| projman-implementation-plan-updated.md | 2081 | Complete Implementation | Main guide (building) |
| projman-python-quickstart.md | 727 | Python Patterns | Code patterns & setup |
| two-mcp-architecture-guide.md | 941 | Architecture Deep Dive | MCP implementation |

**Total:** ~4,074 lines of comprehensive documentation

---

## ✅ Pre-Implementation Checklist

Before starting Phase 1, verify you have:
- [ ] Read CORRECT-ARCHITECTURE.md (understand structure)
- [ ] Understand the two-MCP-server architecture (Gitea + Wiki.js)
- [ ] Understand shared MCP codebase at `mcp-servers/` (not in plugin dirs)
- [ ] Understand Wiki.js structure at `/hyper-hive-labs`
- [ ] Understand hybrid configuration (system + project levels)
- [ ] Python 3.11+ installed
- [ ] Access to Gitea instance
- [ ] Access to Wiki.js instance
- [ ] API tokens for both services

---

## 🎯 Key Architectural Decisions

These are the final decisions documented across all files:

1. **Two MCP Servers** - Separate Gitea and Wiki.js servers for better maintainability
2. **Shared MCP Codebase** - Located at `mcp-servers/` (root level), used by both plugins
3. **Python Implementation** - MCP servers written in Python 3.11+
4. **Hybrid Configuration** - System-level tokens + project-level paths
5. **Wiki.js for Lessons** - Superior to Git-based Wiki for documentation and search
6. **Mode Detection** - MCP servers detect project vs company-wide mode via environment variables
7. **Build Order** - projman first (Phases 1-8), then projman-pmo (Phases 9-12)

---

## 🎉 You're Ready!

You have everything you need to build the projman and projman-pmo plugins. All architectural decisions are finalized and documented.

**Start here:** [projman-implementation-plan-updated.md](./projman-implementation-plan-updated.md) - Phase 1.1a

Good luck with the build!