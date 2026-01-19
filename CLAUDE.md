# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains Claude Code plugins for project management:

1. **`projman`** - Single-repository project management plugin with Gitea integration
2. **`projman-pmo`** - Multi-project PMO coordination plugin
3. **`claude-config-maintainer`** - CLAUDE.md optimization and maintenance plugin
4. **`cmdb-assistant`** - NetBox CMDB integration for infrastructure management

These plugins transform a proven 15-sprint workflow into reusable, distributable tools for managing software development with Claude Code, Gitea, and agile methodologies.

**Status:** projman v1.0.0 complete with full Gitea integration

## File Creation Governance

### Allowed Root Files

Only these files may exist at the repository root:

- `CLAUDE.md` - This file
- `README.md` - Repository overview
- `LICENSE` - License file
- `CHANGELOG.md` - Version history
- `.gitignore` - Git ignore rules
- `.env.example` - Environment template (if needed)

### Allowed Root Directories

Only these directories may exist at the repository root:

| Directory | Purpose |
|-----------|---------|
| `.claude/` | Claude Code local settings |
| `.claude-plugin/` | Marketplace manifest |
| `.claude-plugins/` | Local marketplace definitions |
| `.scratch/` | Transient work (auto-cleaned) |
| `docs/` | Documentation |
| `hooks/` | Shared hooks (if any) |
| `plugins/` | All plugins (projman, projman-pmo, project-hygiene, cmdb-assistant, claude-config-maintainer) |
| `scripts/` | Setup and maintenance scripts |

### File Creation Rules

1. **No new root files** - Do not create files directly in the repository root unless listed above
2. **No new root directories** - Do not create top-level directories without explicit approval
3. **Transient work goes in `.scratch/`** - Any temporary files, test outputs, or exploratory work must be created in `.scratch/`
4. **Clean up after tasks** - Delete files in `.scratch/` when the task is complete
5. **Documentation location** - All documentation goes in `docs/` with appropriate subdirectory:
   - `docs/references/` - Reference specifications and summaries
   - `docs/architecture/` - Architecture diagrams (Draw.io files)
   - `docs/workflows/` - Workflow documentation
6. **No output files** - Do not leave generated output, logs, or test results outside designated directories

### Enforcement

Before creating any file, verify:

1. Is this file type allowed in the target location?
2. If temporary, am I using `.scratch/`?
3. If documentation, am I using the correct `docs/` subdirectory?
4. Will this file be cleaned up after the task?

**Violation of these rules creates technical debt and project chaos.**

## Path Verification (MANDATORY)

### Before Generating Any Prompt or Creating Any File

**This is non-negotiable. Failure to follow causes structural damage.**

1. **READ `docs/CANONICAL-PATHS.md` FIRST**
   - This file is the single source of truth
   - Never infer paths from memory or context
   - Never assume paths based on conversation history

2. **List All Paths**
   - Before generating a prompt, list every file path it will create/modify
   - Show the list to the user

3. **Verify Each Path**
   - Check each path against `docs/CANONICAL-PATHS.md`
   - If a path is not in that file, STOP and ask

4. **Show Verification**
   - Present a verification table to user:
   ```
   | Path | Matches CANONICAL-PATHS.md? |
   |------|----------------------------|
   | plugins/projman/... | ✅ Yes |
   ```

5. **Get Confirmation**
   - User must confirm paths are correct before proceeding

### Relative Path Rules

- Plugin to bundled MCP server: `${CLAUDE_PLUGIN_ROOT}/mcp-servers/{server}`
- Marketplace to plugin: `./../../../plugins/{plugin-name}`
- **ALWAYS calculate from CANONICAL-PATHS.md, never from memory**

### Recovery Protocol

If you suspect paths are wrong:
1. Read `docs/CANONICAL-PATHS.md`
2. Compare actual structure against documented structure
3. Report discrepancies
4. Generate corrective prompt if needed

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

**Gitea MCP Server** (Python) - bundled in projman plugin

**Issue Tools:**
- `list_issues` - Query issues with filters
- `get_issue` - Fetch single issue details
- `create_issue` - Create new issue with labels
- `update_issue` - Modify existing issue
- `add_comment` - Add comments to issues
- `get_labels` - Fetch org + repo label taxonomy
- `suggest_labels` - Analyze context and suggest appropriate labels

**Milestone Tools:**
- `list_milestones` - List sprint milestones
- `get_milestone` - Get milestone details
- `create_milestone` - Create sprint milestone
- `update_milestone` - Update/close milestone

**Dependency Tools:**
- `list_issue_dependencies` - Get issue dependencies
- `create_issue_dependency` - Create dependency between issues
- `get_execution_order` - Get parallel execution batches

**Wiki Tools (Gitea Wiki):**
- `list_wiki_pages` - List wiki pages
- `get_wiki_page` - Fetch specific page content
- `create_wiki_page` - Create new wiki page
- `create_lesson` - Create lessons learned document
- `search_lessons` - Search past lessons by tags

**Validation Tools:**
- `validate_repo_org` - Check repo belongs to organization
- `get_branch_protection` - Check branch protection rules
- `create_label` - Create missing required labels

**Key Architecture Points:**
- MCP servers are **bundled inside each plugin** at `plugins/{plugin}/mcp-servers/`
- This ensures plugins work when cached by Claude Code (only plugin directory is cached)
- Configuration uses hybrid approach (system-level + project-level)
- All plugins reference `${CLAUDE_PLUGIN_ROOT}/mcp-servers/` in their `.mcp.json` files

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

**Gitea Wiki Structure:**
Lessons learned are stored in the Gitea repository's built-in wiki under `lessons-learned/sprints/`.

**Workflow:**
- Orchestrator captures lessons at sprint close via Gitea Wiki MCP tools
- Planner searches relevant lessons at sprint start using `search_lessons`
- Tags enable cross-project lesson discovery
- Focus on preventable repetitions, not every detail
- Web interface available through Gitea Wiki

## Development Workflow

### Build Order

1. **Phase 1-8:** Build `projman` plugin first (single-repo)
2. **Phase 9-11:** Build `pmo` plugin second (multi-project)
3. **Phase 12:** Production deployment

See [docs/reference-material/projman-implementation-plan.md](docs/reference-material/projman-implementation-plan.md) for the complete 12-phase implementation plan.

### Repository Structure (DEFINITIVE)

⚠️ **See `docs/CANONICAL-PATHS.md` for the authoritative path reference - THIS IS THE SINGLE SOURCE OF TRUTH**

```
personal-projects/support-claude-mktplace/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/                        # ← ALL PLUGINS (with bundled MCP servers)
│   ├── projman/                    # ← PROJECT PLUGIN
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── .mcp.json               # Points to ${CLAUDE_PLUGIN_ROOT}/mcp-servers/
│   │   ├── mcp-servers/            # ← MCP servers BUNDLED IN plugin
│   │   │   └── gitea/              # Gitea + Wiki tools
│   │   │       ├── .venv/
│   │   │       ├── requirements.txt
│   │   │       ├── mcp_server/
│   │   │       └── tests/
│   │   ├── commands/
│   │   │   ├── sprint-plan.md
│   │   │   ├── sprint-start.md
│   │   │   ├── sprint-status.md
│   │   │   ├── sprint-close.md
│   │   │   ├── labels-sync.md
│   │   │   └── initial-setup.md
│   │   ├── agents/
│   │   │   ├── planner.md
│   │   │   ├── orchestrator.md
│   │   │   └── executor.md
│   │   ├── skills/
│   │   │   └── label-taxonomy/
│   │   │       └── labels-reference.md
│   │   ├── README.md
│   │   └── CONFIGURATION.md
│   ├── projman-pmo/                # ← PMO PLUGIN
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── .mcp.json
│   │   ├── commands/
│   │   ├── agents/
│   │   │   └── pmo-coordinator.md
│   │   └── README.md
│   ├── cmdb-assistant/             # ← CMDB PLUGIN
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── .mcp.json               # Points to ${CLAUDE_PLUGIN_ROOT}/mcp-servers/
│   │   ├── mcp-servers/            # ← MCP servers BUNDLED IN plugin
│   │   │   └── netbox/
│   │   │       ├── .venv/
│   │   │       ├── requirements.txt
│   │   │       └── mcp_server/
│   │   ├── commands/
│   │   └── agents/
│   └── project-hygiene/            # ← CLEANUP PLUGIN
│       └── ...
├── scripts/                        # Setup and maintenance scripts
│   ├── setup.sh
│   └── post-update.sh
└── docs/
```

### Key Design Decisions

**MCP Servers (Bundled in Plugins):**
- **Gitea MCP**: Issues, labels, wiki, milestones, dependencies (bundled in projman)
- **NetBox MCP**: Infrastructure management (bundled in cmdb-assistant)
- Servers are **bundled inside each plugin** that needs them
- This ensures plugins work when cached by Claude Code

**Python Implementation:**
- Python chosen over Node.js for MCP servers
- Better suited for configuration management and modular code
- Easier to maintain and extend
- Virtual environment (.venv) per MCP server

**Hybrid Configuration:**
- **System-level**: `~/.config/claude/gitea.env` (credentials)
- **Project-level**: `project-root/.env` (repository specification)
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

## Multi-Project Context (PMO Plugin)

The `projman-pmo` plugin coordinates interdependent projects across an organization. Example use cases:
- Main product repository
- Marketing/documentation sites
- Extracted services
- Supporting tools

PMO plugin adds:
- Cross-project issue aggregation (all repos in organization)
- Dependency tracking and visualization
- Resource allocation across projects
- Deployment coordination
- Multi-project prioritization
- Company-wide lessons learned search

**Configuration Difference:**
- PMO operates at company level (no `GITEA_REPO`)
- Accesses all repositories in organization
- Aggregates issues and lessons across projects

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
Test in a real repository with actual Gitea instance before distribution.

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
- **CLI tools forbidden** - Use MCP tools exclusively, never CLI tools like `tea` or `gh`

## CRITICAL: Rules You MUST Follow

### DO NOT MODIFY .gitignore Without Explicit Permission
- This is a **private repository** - credentials in `.env` files are intentional
- **NEVER** add `.env` or `.env.*` to .gitignore
- **NEVER** add venv patterns unless explicitly asked
- If you think something should be ignored, ASK FIRST

### Plugin Structure Requirements
- **plugin.json MUST be in `.claude-plugin/` directory** - NOT in plugin root
- Every plugin in the repo MUST be listed in the marketplace.json
- After creating/modifying a plugin, VERIFY it's in the marketplace

### Hooks Syntax (Claude Code Official)
- **Valid events**: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `Notification`, `Stop`, `SubagentStop`, `PreCompact`
- **INVALID events**: `task-completed`, `file-changed`, `git-commit-msg-needed` (these DO NOT exist)
- Hooks schema:
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "optional-pattern",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/path/to/script.sh"
          }
        ]
      }
    ]
  }
}
```

### MCP Server Configuration
- MCP servers MUST use venv python: `${CLAUDE_PLUGIN_ROOT}/../../mcp-servers/NAME/.venv/bin/python`
- NEVER use bare `python` command - always use venv path
- Test MCP servers after any config change

### Before Completing Any Plugin Work
1. Verify plugin.json is in `.claude-plugin/` directory
2. Verify plugin is listed in marketplace.json
3. Test MCP server configs load correctly
4. Verify hooks use valid event types
5. Check .gitignore wasn't modified inappropriately

## Documentation Index

This repository contains comprehensive planning documentation:

- **`docs/CANONICAL-PATHS.md`** - ⚠️ SINGLE SOURCE OF TRUTH for all paths (MANDATORY reading before any file operations)
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
- Wiki.js structure planned with configurable base path
- Repository structure designed with shared MCP servers

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
