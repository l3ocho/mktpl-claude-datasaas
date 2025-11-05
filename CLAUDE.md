# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains development of two Claude Code plugins for project management:

1. **`projman`** - Single-repository project management plugin (build first)
2. **`pmo`** - Multi-project PMO coordination plugin (build second)

These plugins transform a proven 15-sprint workflow into reusable, distributable tools for managing software development with Claude Code, Gitea, and agile methodologies.

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

Both plugins use a Gitea MCP server (`mcp-server/`) to expose Gitea API as tools:

**Core Tools:**
- `list_issues` - Query issues with filters
- `get_issue` - Fetch single issue details
- `create_issue` - Create new issue with labels
- `update_issue` - Modify existing issue
- `add_comment` - Add comments to issues
- `get_labels` - Fetch org + repo label taxonomy
- `suggest_labels` - Analyze context and suggest appropriate labels

Configuration lives in `.mcp.json` and uses environment variables for Gitea credentials.

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

**Structure:**
```
docs/lessons-learned/
├── INDEX.md                    # Master index with searchable tags
├── sprints/                    # Per-sprint lessons
├── patterns/                   # Recurring patterns (deployment, architecture, Claude issues)
└── templates/                  # Lesson template
```

**Workflow:**
- Orchestrator captures lessons at sprint close
- Planner searches relevant lessons at sprint start
- INDEX.md maintained automatically
- Focus on preventable repetitions, not every detail

## Development Workflow

### Build Order

1. **Phase 1-8:** Build `projman` plugin first (single-repo)
2. **Phase 9-11:** Build `pmo` plugin second (multi-project)
3. **Phase 12:** Production deployment

See [docs/reference-material/projman-implementation-plan.md](docs/reference-material/projman-implementation-plan.md) for the complete 12-phase implementation plan.

### Plugin Structure

```
projman/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── commands/                 # Slash commands (user entry points)
│   ├── sprint-plan.md
│   ├── sprint-start.md
│   ├── sprint-status.md
│   ├── sprint-close.md
│   ├── issue-create.md
│   ├── issue-list.md
│   ├── labels-sync.md
│   └── deploy-check.md
├── agents/                   # Agent personalities and workflows
│   ├── planner.md
│   ├── orchestrator.md
│   └── executor.md
├── skills/                   # Supporting knowledge (not orchestrators)
│   ├── gitea-api/
│   ├── label-taxonomy/
│   ├── lessons-learned/
│   ├── agile-pm/
│   └── branch-strategy/
├── hooks/                    # Automation (post-task sync, staging guards)
│   └── hooks.json
├── .mcp.json                 # MCP server configuration
├── mcp-server/               # Gitea API integration
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
└── README.md
```

### Key Design Decisions

**MCP vs Direct API:**
- Use MCP Server for Gitea integration
- Allows agents to use tools naturally in conversation
- Easier to test independently
- Future-proof for additional integrations

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

The `pmo` plugin will coordinate interdependent projects:
- **CuisineFlow** - Main product
- **CuisineFlow-Site** - Demo sync + customer gateway
- **Intuit Engine Service** - API aggregator extraction (imminent)
- **HHL-Site** - Company presence

PMO plugin adds:
- Cross-project issue aggregation
- Dependency tracking and visualization
- Resource allocation across projects
- Deployment coordination
- Multi-project prioritization

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
