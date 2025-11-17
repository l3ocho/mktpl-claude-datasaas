# Project Management Plugins - Project Summary

## Overview

This project builds two Claude Code plugins that transform a proven 15-sprint workflow into reusable, distributable tools for managing software development with Gitea, Wiki.js, and agile methodologies.

**Status:** Planning phase complete, ready for implementation

---

## The Two Plugins

### 1. projman (Single-Repository)

**Purpose:** Project management for individual repositories
**Users:** Developers, Team Leads
**Build Order:** Build FIRST

**Key Features:**
- Sprint planning with AI agents
- Issue creation with 43-label taxonomy
- Lessons learned capture in Wiki.js
- Branch-aware security model
- Hybrid configuration system

**Reference:** [PLUGIN-PROJMAN.md](./PLUGIN-PROJMAN.md)

### 2. projman-pmo (Multi-Project)

**Purpose:** PMO coordination across organization
**Users:** PMO Coordinators, Engineering Managers, CTOs
**Build Order:** Build SECOND (after projman validated)

**Key Features:**
- Cross-project status aggregation
- Dependency tracking and visualization
- Resource conflict detection
- Release coordination
- Company-wide lessons learned search

**Reference:** [PLUGIN-PMO.md](./PLUGIN-PMO.md)

---

## Core Architecture

### Shared MCP Servers

Both plugins share the same MCP server codebase at repository root (`mcp-servers/`):

**1. Gitea MCP Server**
- Issue management (CRUD operations)
- Label taxonomy system (43 labels)
- Mode detection (project vs company-wide)

**Reference:** [MCP-GITEA.md](./MCP-GITEA.md)

**2. Wiki.js MCP Server**
- Documentation management
- Lessons learned capture and search
- GraphQL API integration
- Company-wide knowledge base

**Reference:** [MCP-WIKIJS.md](./MCP-WIKIJS.md)

### Mode Detection

The MCP servers detect their operating mode based on environment variables:

**Project Mode (projman):**
- `GITEA_REPO` present → operates on single repository
- `WIKIJS_PROJECT` present → operates on single project path

**Company Mode (pmo):**
- No `GITEA_REPO` → operates on all repositories
- No `WIKIJS_PROJECT` → operates on entire company namespace

---

## Repository Structure

```
hhl-infra/claude-code-hhl-toolkit/
├── mcp-servers/                    # ← SHARED BY BOTH PLUGINS
│   ├── gitea/                      # Gitea MCP Server
│   │   ├── .venv/
│   │   ├── requirements.txt
│   │   ├── mcp_server/
│   │   └── tests/
│   └── wikijs/                     # Wiki.js MCP Server
│       ├── .venv/
│       ├── requirements.txt
│       ├── mcp_server/
│       └── tests/
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

## Configuration Architecture

### Hybrid Configuration System

The plugins use a hybrid configuration approach that balances security and flexibility:

**System-Level (Once per machine):**
- `~/.config/claude/gitea.env` - Gitea credentials
- `~/.config/claude/wikijs.env` - Wiki.js credentials

**Project-Level (Per repository):**
- `project-root/.env` - Repository and project paths

**Benefits:**
- Single token per service (update once)
- Project isolation
- Security (tokens never committed)
- Easy multi-project setup

### Configuration Example

**System-Level:**
```bash
# ~/.config/claude/gitea.env
GITEA_API_URL=https://gitea.hotserv.cloud/api/v1
GITEA_API_TOKEN=your_token
GITEA_OWNER=hhl-infra

# ~/.config/claude/wikijs.env
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_token
WIKIJS_BASE_PATH=/hyper-hive-labs
```

**Project-Level:**
```bash
# project-root/.env (for projman)
GITEA_REPO=cuisineflow
WIKIJS_PROJECT=projects/cuisineflow

# No .env needed for pmo (company-wide mode)
```

---

## Key Architectural Decisions

### 1. Two MCP Servers (Shared)

**Decision:** Separate Gitea and Wiki.js servers at repository root
**Why:**
- Clear separation of concerns
- Independent configuration
- Better maintainability
- Professional architecture

### 2. Python Implementation

**Decision:** Python 3.10+ for MCP servers
**Why:**
- Modern async/await improvements
- Better type hints support
- Good balance of compatibility vs features
- Widely available (released Oct 2021)
- Most production servers have 3.10+ by now

### 3. Wiki.js for Lessons Learned

**Decision:** Use Wiki.js instead of Git-based Wiki
**Why:**
- Rich editor and search
- Built-in tag system
- Version history
- Web-based collaboration
- GraphQL API
- Company-wide accessibility

### 4. Hybrid Configuration

**Decision:** System-level + project-level configuration
**Why:**
- Single token per service (security)
- Per-project customization (flexibility)
- Easy multi-project setup
- Never commit tokens to git

### 5. Mode Detection in MCP Servers

**Decision:** Detect mode based on environment variables
**Why:**
- Same codebase for both plugins
- No code duplication
- Fix bugs once, both benefit
- Clear separation of concerns

### 6. Build Order: projman First

**Decision:** Build projman completely before starting pmo
**Why:**
- Validate core functionality
- Establish patterns
- Reduce risk
- PMO builds on projman foundation

---

## The Three-Agent Model

### Projman Agents

**Planner Agent:**
- Sprint planning and architecture analysis
- Asks clarifying questions
- Suggests appropriate labels
- Creates Gitea issues
- Searches relevant lessons learned

**Orchestrator Agent:**
- Sprint progress monitoring
- Task coordination
- Blocker identification
- Git operations
- Generates lean execution prompts

**Executor Agent:**
- Implementation guidance
- Code review suggestions
- Testing strategy
- Quality standards enforcement
- Documentation

### PMO Agent

**PMO Coordinator:**
- Strategic view across all projects
- Cross-project dependency tracking
- Resource conflict detection
- Release coordination
- Delegates to projman agents for details

---

## Wiki.js Structure

```
Wiki.js: https://wiki.hyperhivelabs.com
└── /hyper-hive-labs/
    ├── projects/                       # Project-specific
    │   ├── cuisineflow/
    │   │   ├── lessons-learned/
    │   │   │   ├── sprints/
    │   │   │   ├── patterns/
    │   │   │   └── INDEX.md
    │   │   └── documentation/
    │   ├── cuisineflow-site/
    │   ├── intuit-engine/
    │   └── hhl-site/
    ├── company/                        # Company-wide
    │   ├── processes/
    │   ├── standards/
    │   └── tools/
    └── shared/                         # Cross-project
        ├── architecture-patterns/
        ├── best-practices/
        └── tech-stack/
```

**Reference:** [MCP-WIKIJS.md](./MCP-WIKIJS.md#wiki-js-structure)

---

## Label Taxonomy System

### Dynamic Label System (44 labels currently)

Labels are **fetched dynamically from Gitea** at runtime via the `/labels-sync` command:

**Organization Labels (28):**
- Agent/2
- Complexity/3
- Efforts/5
- Priority/4
- Risk/3
- Source/4
- Type/6 (Bug, Feature, Refactor, Documentation, Test, Chore)

**Repository Labels (16):**
- Component/9 (Backend, Frontend, API, Database, Auth, Deploy, Testing, Docs, Infra)
- Tech/7 (Python, JavaScript, Docker, PostgreSQL, Redis, Vue, FastAPI)

### Type/Refactor Label

**Organization-level label** for architectural work:
- Service extraction
- Architecture modifications
- Code restructuring
- Technical debt reduction

**Note:** Label count may change. Always sync from Gitea using `/labels-sync` command. When new labels are detected, the command will explain changes and update suggestion logic.

**Reference:** [PLUGIN-PROJMAN.md](./PLUGIN-PROJMAN.md#label-taxonomy-system)

---

## Build Order & Phases

### Build projman First (Phases 1-8)

**Phase 1:** Core Infrastructure (MCP servers)
**Phase 2:** Sprint Planning Commands
**Phase 3:** Agent System
**Phase 4:** Lessons Learned System
**Phase 5:** Testing & Validation
**Phase 6:** Documentation & Refinement
**Phase 7:** Marketplace Preparation
**Phase 8:** Production Hardening

**Reference:** [PLUGIN-PROJMAN.md](./PLUGIN-PROJMAN.md#implementation-phases)

### Build pmo Second (Phases 9-12)

**Phase 9:** PMO Plugin Foundation
**Phase 10:** PMO Commands & Workflows
**Phase 11:** PMO Testing & Integration
**Phase 12:** Production Deployment

**Reference:** [PLUGIN-PMO.md](./PLUGIN-PMO.md#implementation-phases)

---

## Quick Start Guide

### 1. System Configuration

```bash
# Create config directory
mkdir -p ~/.config/claude

# Gitea config
cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.hotserv.cloud/api/v1
GITEA_API_TOKEN=your_gitea_token
GITEA_OWNER=hhl-infra
EOF

# Wiki.js config
cat > ~/.config/claude/wikijs.env << EOF
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_wikijs_token
WIKIJS_BASE_PATH=/hyper-hive-labs
EOF

# Secure files
chmod 600 ~/.config/claude/*.env
```

### 2. Project Configuration

```bash
# In each project root (for projman)
cat > .env << EOF
GITEA_REPO=cuisineflow
WIKIJS_PROJECT=projects/cuisineflow
EOF

# Add to .gitignore
echo ".env" >> .gitignore
```

### 3. MCP Server Setup

```bash
# Gitea MCP Server
cd mcp-servers/gitea
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Wiki.js MCP Server
cd mcp-servers/wikijs
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Validate Setup

```bash
# Test MCP servers
python -m mcp_server.server --test  # In each MCP directory

# Test plugin loading
claude plugin test projman
claude plugin test projman-pmo
```

---

## Document Organization

This documentation is organized into 4 focused files plus this summary:

### 1. Gitea MCP Server Reference

**File:** [MCP-GITEA.md](./MCP-GITEA.md)

**Contains:**
- Configuration setup
- Python implementation
- API client code
- Issue and label tools
- Testing strategies
- Mode detection
- Performance optimization

**Use when:** Implementing or troubleshooting Gitea integration

### 2. Wiki.js MCP Server Reference

**File:** [MCP-WIKIJS.md](./MCP-WIKIJS.md)

**Contains:**
- Configuration setup
- GraphQL client implementation
- Wiki.js structure
- Lessons learned system
- Documentation tools
- Company-wide patterns
- PMO multi-project methods

**Use when:** Implementing or troubleshooting Wiki.js integration

### 3. Projman Plugin Reference

**File:** [PLUGIN-PROJMAN.md](./PLUGIN-PROJMAN.md)

**Contains:**
- Plugin structure
- Commands (sprint-plan, sprint-start, sprint-status, sprint-close, labels-sync)
- Three agents (planner, orchestrator, executor)
- Sprint workflow
- Label taxonomy
- Branch-aware security
- Implementation phases 1-8

**Use when:** Building or using the projman plugin

### 4. PMO Plugin Reference

**File:** [PLUGIN-PMO.md](./PLUGIN-PMO.md)

**Contains:**
- PMO plugin structure
- Multi-project commands
- PMO coordinator agent
- Cross-project coordination
- Dependency tracking
- Resource conflict detection
- Implementation phases 9-12

**Use when:** Building or using the projman-pmo plugin

### 5. This Summary

**File:** PROJECT-SUMMARY.md (this document)

**Contains:**
- Project overview
- Architecture decisions
- Configuration approach
- Quick start guide
- References to detailed docs

**Use when:** Getting started or need high-level overview

---

## Key Success Metrics

### Technical Metrics

- Sprint planning time reduced by 40%
- Manual steps eliminated: 10+ per sprint
- Lessons learned capture rate: 100% (vs 0% before)
- Label accuracy on issues: 90%+
- Configuration setup time: < 5 minutes

### User Metrics

- User satisfaction: Better than current manual workflow
- Learning curve: < 1 hour to basic proficiency
- Error rate: < 5% incorrect operations
- Adoption rate: 100% team adoption within 1 month

### PMO Metrics

- Cross-project visibility: 100% (vs fragmented before)
- Dependency detection: Automated (vs manual tracking)
- Resource conflict identification: Proactive (vs reactive)
- Release coordination: Streamlined (vs ad-hoc)

---

## Critical Lessons from 15 Sprints

### Why Lessons Learned Is Critical

After 15 sprints without systematic lesson capture, repeated mistakes occurred:
- Claude Code infinite loops on similar issues: 2-3 times
- Same architectural mistakes: Multiple occurrences
- Forgotten optimizations: Re-discovered each time

**Solution:** Mandatory lessons learned capture at sprint close, searchable at sprint start

### Branch Detection Must Be 100% Reliable

Production accidents are unacceptable. Branch-aware security prevents:
- Accidental code changes on production branch
- Sprint planning on wrong branch
- Deployment mistakes

**Implementation:** Two layers - CLAUDE.md (file-level) + Plugin agents (tool-level)

### Configuration Complexity Is a Blocker

Previous attempts failed due to:
- Complex per-project setup
- Token management overhead
- Multiple configuration files

**Solution:** Hybrid approach - system-level tokens + simple project-level paths

---

## Next Steps

### Immediate Actions

1. **Set up system configuration** (Gitea + Wiki.js tokens)
2. **Create Wiki.js base structure** at `/hyper-hive-labs`
3. **Begin Phase 1.1a** - Gitea MCP Server implementation
4. **Begin Phase 1.1b** - Wiki.js MCP Server implementation

### Phase Execution

1. **Phases 1-4:** Build core projman functionality
2. **Phase 5:** Validate with real sprint (e.g., Intuit Engine extraction)
3. **Phases 6-8:** Polish, document, and harden projman
4. **Phases 9-12:** Build and validate pmo plugin

### Validation Points

- **After Phase 1:** MCP servers working and tested
- **After Phase 4:** Complete projman workflow end-to-end
- **After Phase 5:** Real sprint successfully managed
- **After Phase 8:** Production-ready projman
- **After Phase 11:** Multi-project coordination validated
- **After Phase 12:** Complete system operational

---

## Implementation Decisions (Pre-Development)

These decisions were finalized before development:

### 1. Python Version: 3.10+
- **Rationale:** Balance of modern features and wide availability
- **Benefits:** Modern async, good type hints, widely deployed
- **Minimum:** Python 3.10.0

### 2. Wiki.js Base Structure: Needs Creation
- **Status:** `/hyper-hive-labs` structure does NOT exist yet
- **Action:** Run `setup_wiki_structure.py` during Phase 1.1b
- **Script:** See MCP-WIKIJS.md for complete setup script
- **Post-setup:** Verify at https://wiki.hyperhivelabs.com/hyper-hive-labs

### 3. Testing Strategy: Both Mocks and Real APIs
- **Unit tests:** Use mocks for fast feedback during development
- **Integration tests:** Use real Gitea/Wiki.js APIs for validation
- **CI/CD:** Run both test suites
- **Developers:** Can skip integration tests locally if needed
- **Markers:** Use pytest markers (`@pytest.mark.integration`)

### 4. Token Permissions: Confirmed
- **Gitea token:**
  - `repo` (all) - Read/write repositories, issues, labels
  - `read:org` - Organization information and labels
  - `read:user` - User information
- **Wiki.js token:**
  - Read/create/update pages
  - Manage tags
  - Search access

### 5. Label System: Dynamic (44 labels)
- **Current count:** 44 labels (28 org + 16 repo)
- **Approach:** Fetch dynamically via API, never hardcode
- **Sync:** `/labels-sync` command updates local reference and suggestion logic
- **New labels:** Command explains changes and asks for confirmation

### 6. Branch Detection: Defense in Depth
- **Layer 1:** MCP tools check branch and block operations
- **Layer 2:** Agent prompts check branch and warn users
- **Layer 3:** CLAUDE.md provides context (third layer)
- **Rationale:** Multiple layers prevent production accidents

---

## Important Reminders

1. **Build projman FIRST** - Don't start pmo until projman is validated
2. **MCP servers are SHARED** - Located at `mcp-servers/`, not inside plugins
3. **Lessons learned is critical** - Prevents repeated mistakes
4. **Test with real work** - Validate with actual sprints, not just unit tests
5. **Security first** - Branch detection must be 100% reliable
6. **Keep it simple** - Avoid over-engineering, focus on proven workflow
7. **Python 3.10+** - Minimum version requirement
8. **Wiki.js setup** - Must run setup script before projman works

---

## Getting Help

### Documentation Structure

**Need details on:**
- Gitea integration → [MCP-GITEA.md](./MCP-GITEA.md)
- Wiki.js integration → [MCP-WIKIJS.md](./MCP-WIKIJS.md)
- Projman usage → [PLUGIN-PROJMAN.md](./PLUGIN-PROJMAN.md)
- PMO usage → [PLUGIN-PMO.md](./PLUGIN-PMO.md)
- Overview → This document

### Quick Reference

| Question | Reference |
|----------|-----------|
| How do I set up configuration? | This document, "Quick Start Guide" |
| What's the repository structure? | This document, "Repository Structure" |
| How do Gitea tools work? | [MCP-GITEA.md](./MCP-GITEA.md) |
| How do Wiki.js tools work? | [MCP-WIKIJS.md](./MCP-WIKIJS.md) |
| How do I use sprint commands? | [PLUGIN-PROJMAN.md](./PLUGIN-PROJMAN.md#commands) |
| How do agents work? | [PLUGIN-PROJMAN.md](./PLUGIN-PROJMAN.md#three-agent-model) |
| How do I coordinate multiple projects? | [PLUGIN-PMO.md](./PLUGIN-PMO.md) |
| What's the build order? | This document, "Build Order & Phases" |

---

## Project Timeline

**Planning:** Complete ✅
**Phase 1-8 (projman):** 6-8 weeks estimated
**Phase 9-12 (pmo):** 2-4 weeks estimated
**Total:** 8-12 weeks from start to production

**Note:** No fixed deadlines - work at sustainable pace and validate thoroughly

---

## You're Ready!

You have everything you need to build the projman and projman-pmo plugins. All architectural decisions are finalized and documented.

**Start here:** [MCP-GITEA.md](./MCP-GITEA.md) - Set up Gitea MCP Server

Good luck with the build! 🚀
