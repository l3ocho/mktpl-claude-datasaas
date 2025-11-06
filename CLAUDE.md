# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains development of two Claude Code plugins for project management:

1. **`projman`** - Single-repository project management plugin (build first)
2. **`projman-pmo`** - Multi-project PMO coordination plugin (build second)

These plugins transform a proven 15-sprint workflow into reusable, distributable tools for managing software development with Claude Code, Gitea, Wiki.js, and agile methodologies.

**Status:** Planning phase complete, ready for implementation (Phase 1)

## Core Architecture

### Three-Agent Model

The plugins implement a three-agent architecture that mirrors the proven workflow:

**Planner Agent** (`agents/planner.md`)
- Performs architecture analysis and sprint planning
- Creates detailed planning documents
- Makes architectural decisions
- Creates Gitea issues with appropriate labels
- Personality: Asks clarifying questions, thinks through edge cases, never rushes

**Orchestrator Agent** (`agents/orchestrator.md`)
- Coordinates sprint execution
- Generates lean execution prompts (not full docs)
- Tracks progress and updates documentation
- Handles Git operations (commit, merge, cleanup)
- Manages task dependencies
- Personality: Concise, action-oriented, tracks details meticulously

**Executor Agent** (`agents/executor.md`)
- Implements features according to execution prompts
- Writes clean, tested code
- Follows architectural decisions from planning
- Generates completion reports
- Personality: Implementation-focused, follows specs precisely

### MCP Server Integration

Both plugins use **two shared MCP servers** at repository root level (`mcp-servers/`):

**1. Gitea MCP Server** (Python)
- `list_issues` - Query issues with filters
- `get_issue` - Fetch single issue details
- `create_issue` - Create new issue with labels
- `update_issue` - Modify existing issue
- `add_comment` - Add comments to issues
- `get_labels` - Fetch org + repo label taxonomy
- `suggest_labels` - Analyze context and suggest appropriate labels

**2. Wiki.js MCP Server** (Python, GraphQL)
- `search_pages` - Search Wiki.js pages by keywords/tags
- `get_page` - Fetch specific page content
- `create_page` - Create new Wiki page
- `update_page` - Modify existing page
- `list_pages` - List pages in a path
- `create_lesson` - Create lessons learned document
- `search_lessons` - Search past lessons by tags
- `tag_lesson` - Add tags to lessons learned

**Key Architecture Points:**
- MCP servers are **shared** by both plugins at `mcp-servers/gitea` and `mcp-servers/wikijs`
- Each MCP server detects its mode (project-scoped vs company-wide) based on environment variables
- Configuration uses hybrid approach (system-level + project-level)
- Both plugins reference `../mcp-servers/` in their `.mcp.json` files

## Branch-Aware Security Model

Plugin behavior adapts to the current Git branch to prevent accidental changes:

**Development Mode** (`development`, `feat/*`)
- Full access to all operations
- Can create Gitea issues
- Can modify all files

**Staging Mode** (`staging`)
- Read-only for application code
- Can modify `.env` files
- Can create issues to document needed fixes
- Warns on attempted code changes

**Production Mode** (`main`)
- Read-only for application code
- Emergency-only `.env` modifications
- Can create incident issues
- Blocks code changes

This behavior is implemented in both CLAUDE.md (file-level) and plugin agents (tool-level).

## Label Taxonomy System

The project uses a sophisticated 43-label taxonomy at organization level:

**Organization Labels (27):**
- Agent/2, Complexity/3, Efforts/5, Priority/4, Risk/3, Source/4, Type/6

**Repository Labels (16):**
- Component/9, Tech/7

**Important Labels:**
- `Type/Refactor` - For architectural changes and code restructuring (exclusive Type label)
- Used for service extraction, architecture modifications, technical debt

The label system includes:
- `skills/label-taxonomy/labels-reference.md` - Local reference synced from Gitea
- Label suggestion logic that detects appropriate labels from context
- `/labels-sync` command to review and sync changes from Gitea

## Lessons Learned System

**Critical Feature:** After 15 sprints without lesson capture, repeated mistakes occurred (e.g., Claude Code infinite loops on similar issues 2-3 times).

**Wiki.js Structure:**
```
Wiki.js: https://wiki.hyperhivelabs.com
└── /hyper-hive-labs/
    ├── projects/                       # Project-specific documentation
    │   ├── cuisineflow/
    │   │   ├── lessons-learned/
    │   │   │   ├── sprints/
    │   │   │   ├── patterns/
    │   │   │   └── INDEX.md
    │   │   └── documentation/
    │   ├── cuisineflow-site/
    │   ├── intuit-engine/
    │   └── hhl-site/
    ├── company/                        # Company-wide documentation
    │   ├── processes/
    │   ├── standards/
    │   └── tools/
    └── shared/                         # Cross-project resources
        ├── architecture-patterns/
        ├── best-practices/
        └── tech-stack/
```

**Workflow:**
- Orchestrator captures lessons at sprint close via Wiki.js MCP
- Planner searches relevant lessons at sprint start using GraphQL search
- INDEX.md maintained automatically via Wiki.js API
- Tags enable cross-project lesson discovery
- Focus on preventable repetitions, not every detail
- Web interface for team review and editing

## Development Workflow

### Build Order

1. **Phase 1-8:** Build `projman` plugin first (single-repo)
2. **Phase 9-11:** Build `pmo` plugin second (multi-project)
3. **Phase 12:** Production deployment

See [docs/reference-material/projman-implementation-plan.md](docs/reference-material/projman-implementation-plan.md) for the complete 12-phase implementation plan.

### Repository Structure (DEFINITIVE)

⚠️ **See `docs/CORRECT-ARCHITECTURE.md` for the authoritative structure reference**

```
hyperhivelabs/claude-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── mcp-servers/                    # ← SHARED BY BOTH PLUGINS
│   ├── gitea/
│   │   ├── .venv/
│   │   ├── requirements.txt        # Python dependencies
│   │   ├── mcp_server/
│   │   │   ├── __init__.py
│   │   │   ├── server.py
│   │   │   ├── config.py           # Mode detection (project/company)
│   │   │   ├── gitea_client.py
│   │   │   └── tools/
│   │   │       ├── issues.py
│   │   │       └── labels.py
│   │   └── tests/
│   └── wikijs/
│       ├── .venv/
│       ├── requirements.txt        # Python + GraphQL dependencies
│       ├── mcp_server/
│       │   ├── __init__.py
│       │   ├── server.py
│       │   ├── config.py           # Mode detection (project/company)
│       │   ├── wikijs_client.py    # GraphQL client
│       │   └── tools/
│       │       ├── pages.py
│       │       ├── lessons_learned.py
│       │       └── documentation.py
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

### Key Design Decisions

**Two MCP Servers (Shared Architecture):**
- **Gitea MCP**: Issues, labels, repository management
- **Wiki.js MCP**: Documentation, lessons learned, knowledge base
- Servers are **shared** between both plugins at repository root
- Mode detection based on environment variables (project vs company-wide)
- Benefits: Single source of truth, fix bugs once, professional architecture

**Python Implementation:**
- Python chosen over Node.js for MCP servers
- Better suited for configuration management and modular code
- Easier to maintain and extend
- Virtual environment (.venv) per MCP server

**Hybrid Configuration:**
- **System-level**: `~/.config/claude/gitea.env` and `wikijs.env` (credentials)
- **Project-level**: `project-root/.env` (repository and path specification)
- Merge strategy: project overrides system
- Benefits: Single token per service, easy multi-project setup

**Skills as Knowledge, Not Orchestrators:**
- Skills provide supporting knowledge loaded when relevant
- Agents are the primary interface
- Reduces token usage
- Makes knowledge reusable across agents

**Branch Detection:**
- Two layers: CLAUDE.md (file access) + Plugin agents (tool usage)
- Defense in depth approach
- Plugin works with or without CLAUDE.md

**Plugin Development:**
- Use `claude-plugin-developer` skill for all plugin-related work
- Reference when creating/updating plugin manifests, commands, agents, hooks, or MCP servers
- Ensures compliance with Anthropic's security requirements and best practices
- Provides templates, validation tools, and troubleshooting guidance
- Critical for proper plugin structure, path safety, and marketplace publication

## Multi-Project Context (PMO Plugin)

The `projman-pmo` plugin will coordinate interdependent projects:
- **CuisineFlow** - Main product
- **CuisineFlow-Site** - Demo sync + customer gateway
- **Intuit Engine Service** - API aggregator extraction (imminent)
- **HHL-Site** - Company presence

PMO plugin adds:
- Cross-project issue aggregation (all repos in organization)
- Dependency tracking and visualization
- Resource allocation across projects
- Deployment coordination
- Multi-project prioritization
- Company-wide lessons learned search

**Configuration Difference:**
- PMO operates at company level (no `GITEA_REPO` or `WIKIJS_PROJECT`)
- Accesses entire `/hyper-hive-labs` Wiki.js namespace
- Queries all repositories in organization

Build PMO plugin AFTER projman is working and validated.

## Testing Approach

**Local Marketplace:**
Create local marketplace for plugin development:
```
~/projman-dev-marketplace/
├── .claude-plugin/
│   └── marketplace.json
└── projman/              # Symlink to plugin directory
```

**Integration Testing:**
Test in real CuisineFlow repository with actual Gitea instance before distribution.

**Success Metrics:**
- Sprint planning time reduced 40%
- Manual steps eliminated: 10+ per sprint
- Lessons learned capture rate: 100% (vs 0% before)
- Label accuracy on issues: 90%+
- User satisfaction: Better than current manual workflow

## Important Notes

- **Never modify docker-compose files with 'version' attribute** - It's obsolete
- **Focus on implementation, not over-engineering** - This system has been validated over 15 sprints
- **Lessons learned is critical** - Prevents repeated mistakes (e.g., Claude infinite loops)
- **Type/Refactor label** - Newly implemented at org level for architectural work
- **Branch detection must be 100% reliable** - Prevents production accidents
- **Python for MCP servers** - Use Python 3.8+ with virtual environments
- **Wiki.js structure** - All HHL content under `/hyper-hive-labs` namespace

## Documentation Index

This repository contains comprehensive planning documentation:

- **`docs/CORRECT-ARCHITECTURE.md`** - ⚠️ DEFINITIVE repository structure reference
- **`docs/DOCUMENT-INDEX.md`** - Complete guide to all planning documents
- **`docs/projman-implementation-plan-updated.md`** - Full 12-phase implementation plan
- **`docs/projman-python-quickstart.md`** - Python-specific implementation guide
- **`docs/two-mcp-architecture-guide.md`** - Deep dive into two-MCP architecture

**Start with:** `docs/DOCUMENT-INDEX.md` for navigation guidance

## Recent Updates (Updated: 2025-06-11)

### Planning Phase Complete
- Comprehensive 12-phase implementation plan finalized
- Architecture decisions documented and validated
- Two-MCP-server approach confirmed (Gitea + Wiki.js)
- Python selected for MCP server implementation
- Hybrid configuration strategy defined (system + project level)
- Wiki.js structure planned at `/hyper-hive-labs`
- Repository structure designed with shared MCP servers
- `claude-plugin-developer` skill added to project

### Key Architectural Decisions Made
1. **Shared MCP Servers**: Both plugins use the same MCP codebase at `mcp-servers/`
2. **Mode Detection**: MCP servers detect project vs company-wide mode via environment variables
3. **Python Implementation**: MCP servers written in Python (not Node.js) for better configuration handling
4. **Wiki.js Integration**: Lessons learned and documentation moved to Wiki.js for better collaboration
5. **Hybrid Config**: System-level credentials + project-level paths for flexibility

### Next Steps
- Begin Phase 1.1a: Gitea MCP Server implementation
- Set up Python virtual environments
- Create configuration loaders
- Implement core Gitea tools (issues, labels)
- Write integration tests
