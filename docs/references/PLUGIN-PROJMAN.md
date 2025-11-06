# Projman Plugin Reference

## Overview

The `projman` plugin provides single-repository project management with Gitea and Wiki.js integration. It transforms the proven 15-sprint workflow into a distributable tool for managing software development with Claude Code.

**Build Order:** Build projman FIRST, then pmo
**Target Users:** Individual developers and project teams
**Scope:** Single-repository project management

**Key Features:**
- Sprint planning with planner agent
- Issue creation with label taxonomy
- Lessons learned capture in Wiki.js
- Sprint execution coordination
- Branch-aware security model
- Hybrid configuration system

---

## Plugin Structure

```
projman/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest
├── .mcp.json                      # Points to ../mcp-servers/
├── commands/
│   ├── sprint-plan.md            # Sprint planning command
│   ├── sprint-start.md           # Sprint initiation command
│   ├── sprint-status.md          # Sprint status check command
│   ├── sprint-close.md           # Sprint closing command
│   └── labels-sync.md            # Label taxonomy sync command
├── agents/
│   ├── planner.md                # Sprint planning agent
│   ├── orchestrator.md           # Sprint coordination agent
│   └── executor.md               # Implementation guidance agent
├── skills/
│   └── label-taxonomy/
│       └── labels-reference.md   # Dynamic label reference
├── README.md                      # Installation and usage guide
└── CONFIGURATION.md               # Configuration setup guide
```

---

## Plugin Manifest

**File:** `projman/.claude-plugin/plugin.json`

```json
{
  "name": "projman",
  "version": "0.1.0",
  "displayName": "Projman - Single-Repository Project Management",
  "description": "Sprint planning and project management with Gitea and Wiki.js integration",
  "author": "Hyper Hive Labs",
  "homepage": "https://gitea.hyperhivelabs.com/hyperhivelabs/claude-plugins/projman",
  "repository": {
    "type": "git",
    "url": "https://gitea.hyperhivelabs.com/hyperhivelabs/claude-plugins.git"
  },
  "license": "MIT",
  "keywords": [
    "project-management",
    "sprint-planning",
    "gitea",
    "wikijs",
    "agile"
  ],
  "minimumClaudeVersion": "1.0.0",
  "main": "commands/",
  "contributes": {
    "commands": [
      {
        "name": "sprint-plan",
        "title": "Plan Sprint",
        "description": "Start sprint planning with AI guidance",
        "file": "commands/sprint-plan.md"
      },
      {
        "name": "sprint-start",
        "title": "Start Sprint",
        "description": "Begin sprint execution with relevant lessons",
        "file": "commands/sprint-start.md"
      },
      {
        "name": "sprint-status",
        "title": "Sprint Status",
        "description": "Check current sprint progress",
        "file": "commands/sprint-status.md"
      },
      {
        "name": "sprint-close",
        "title": "Close Sprint",
        "description": "Complete sprint and capture lessons learned",
        "file": "commands/sprint-close.md"
      },
      {
        "name": "labels-sync",
        "title": "Sync Labels",
        "description": "Synchronize label taxonomy from Gitea",
        "file": "commands/labels-sync.md"
      }
    ],
    "agents": [
      {
        "name": "planner",
        "title": "Sprint Planner",
        "description": "Sprint planning and architecture analysis",
        "file": "agents/planner.md"
      },
      {
        "name": "orchestrator",
        "title": "Sprint Orchestrator",
        "description": "Sprint coordination and progress tracking",
        "file": "agents/orchestrator.md"
      },
      {
        "name": "executor",
        "title": "Sprint Executor",
        "description": "Implementation guidance and code review",
        "file": "agents/executor.md"
      }
    ],
    "skills": [
      {
        "name": "label-taxonomy",
        "title": "Label Taxonomy Reference",
        "description": "Gitea label system reference",
        "file": "skills/label-taxonomy/labels-reference.md"
      }
    ]
  },
  "configuration": {
    "required": [
      "GITEA_API_URL",
      "GITEA_API_TOKEN",
      "GITEA_OWNER",
      "GITEA_REPO",
      "WIKIJS_API_URL",
      "WIKIJS_API_TOKEN",
      "WIKIJS_BASE_PATH",
      "WIKIJS_PROJECT"
    ],
    "properties": {
      "GITEA_API_URL": {
        "type": "string",
        "description": "Gitea API base URL (e.g., https://gitea.example.com/api/v1)"
      },
      "GITEA_API_TOKEN": {
        "type": "string",
        "description": "Gitea API token with repo and org read access",
        "secret": true
      },
      "GITEA_OWNER": {
        "type": "string",
        "description": "Gitea organization or user name"
      },
      "GITEA_REPO": {
        "type": "string",
        "description": "Repository name for project-scoped operations"
      },
      "WIKIJS_API_URL": {
        "type": "string",
        "description": "Wiki.js GraphQL API URL (e.g., https://wiki.example.com/graphql)"
      },
      "WIKIJS_API_TOKEN": {
        "type": "string",
        "description": "Wiki.js API token with page management permissions",
        "secret": true
      },
      "WIKIJS_BASE_PATH": {
        "type": "string",
        "description": "Base path in Wiki.js (e.g., /company-name)"
      },
      "WIKIJS_PROJECT": {
        "type": "string",
        "description": "Project path relative to base (e.g., projects/my-project)"
      }
    }
  }
}
```

---

## How Commands Work

Commands are **markdown files** that expand when invoked. When a user types `/sprint-plan`, Claude Code:

1. Loads the markdown file from `commands/sprint-plan.md`
2. Injects the content into the conversation context
3. Claude follows the instructions in the markdown

**Example:** `commands/sprint-plan.md`

```markdown
# Sprint Planning Command

You are assisting with sprint planning for a software project.

## Your Role

Guide the user through sprint planning by:
1. Asking what feature/fix/refactor is planned
2. Searching lessons learned for similar past work
3. Asking clarifying questions about architecture and scope
4. Suggesting appropriate Gitea labels based on context
5. Creating a Gitea issue if the user confirms
6. Generating a structured sprint planning document

## Available Tools

You have access to these MCP tools (invoke by describing what you need):
- **search_lessons**: Search past lessons learned for relevant context
- **list_issues**: Check existing issues for related work
- **suggest_labels**: Get label suggestions based on context
- **create_issue**: Create Gitea issue with labels
- **get_labels**: Fetch available label taxonomy

## Branch Awareness

Before creating issues, check the current Git branch:
- **Development branches** (development, feat/*): Full access
- **Staging/Production**: Warn user and suggest switching to development branch

## Workflow

1. Ask: "What are you building in this sprint?"
2. Use **search_lessons** tool with relevant keywords
3. Present any relevant past lessons found
4. Ask clarifying questions:
   - Which components are affected?
   - What's the architectural approach?
   - Any known risks or dependencies?
5. Use **suggest_labels** tool with the context
6. Present suggested labels and ask for confirmation
7. Use **create_issue** tool if user confirms
8. Generate sprint planning document with:
   - Sprint goal
   - Architecture decisions
   - Task breakdown
   - Risks and mitigation
   - References to relevant lessons

## Personality

Be thorough but not overwhelming. Ask targeted questions. Think through edge cases.
```

**Key Points:**
- Commands are **prompts**, not code
- Tools are invoked by **describing needs** in natural language
- Claude Code handles tool execution automatically
- Commands can invoke agents, use tools, or both

---

## How Agents Work

Agents are also **markdown files** with specialized prompts. They can be invoked by:
- Commands (e.g., sprint-plan command uses planner agent)
- Slash commands (e.g., `/agent planner`)
- Other agents (delegation)

**Example:** `agents/planner.md`

```markdown
# Sprint Planner Agent

You are the Sprint Planner for Hyper Hive Labs.

## Your Identity

**Role:** Sprint planning and architecture analysis
**Personality:** Thorough, architecture-aware, asks clarifying questions
**Focus:** Planning before execution

## Responsibilities

1. **Sprint Planning:**
   - Guide users through sprint planning process
   - Ask targeted questions about scope and architecture
   - Break down work into manageable tasks

2. **Architecture Analysis:**
   - Identify architectural implications
   - Detect when work is a refactor vs feature
   - Consider cross-project impacts

3. **Label Selection:**
   - Analyze context to suggest appropriate labels
   - Ensure Type labels are accurate (Bug/Feature/Refactor)
   - Suggest Component and Priority labels

4. **Lessons Integration:**
   - Search past lessons before planning
   - Reference relevant experiences
   - Apply learned patterns

5. **Issue Creation:**
   - Create well-structured Gitea issues
   - Include detailed descriptions
   - Apply suggested labels

## Available MCP Tools

Invoke these tools by describing what you need in natural language:

- **search_lessons(query, tags)**: Search Wiki.js for past lessons
- **list_issues(state, labels, repo)**: List Gitea issues
- **get_issue(issue_number, repo)**: Get specific issue
- **create_issue(title, body, labels, repo)**: Create new issue
- **suggest_labels(context)**: Get label suggestions
- **get_labels(repo)**: Fetch all available labels

## Tool Invocation Examples

Instead of calling tools programmatically, describe what you need:

**Good:**
- "Let me search past lessons for service extraction experiences"
- "I'll check if there are any existing issues related to authentication"
- "I need to suggest labels based on this context: [context]"

**Claude Code will:**
1. Understand your intent
2. Map it to the appropriate MCP tool
3. Execute the tool
4. Provide results back to you

## Branch-Aware Security

Check branch before creating issues:

**Development branches:** Create issues freely
**Staging branches:** Warn and suggest switching branches
**Production branches:** Block issue creation, suggest incidents only

**How to check:**
- Git branch info is available in environment context
- If unsure, ask user what branch they're on
- Provide appropriate warnings

## Planning Workflow

1. **Understand the work:**
   - "What are you building?"
   - Listen for keywords: "bug", "feature", "refactor", "extract"

2. **Search lessons:**
   - Extract keywords from user's description
   - Search: "Let me search for lessons about [keywords]"
   - Present relevant findings

3. **Ask clarifying questions:**
   - Architecture approach?
   - Components affected?
   - Dependencies or risks?
   - Timeline expectations?

4. **Suggest labels:**
   - Combine work type + user answers into context
   - "I'll suggest appropriate labels for this work"
   - Present suggestions with explanations

5. **Confirm and create:**
   - Show proposed issue structure
   - Ask for user confirmation
   - Create issue: "I'll create this issue in Gitea"
   - Confirm creation with issue number

6. **Generate plan:**
   - Sprint goal
   - Architecture decisions
   - Task breakdown
   - Risk mitigation
   - Lesson references

## Communication Style

- **Thorough but concise:** Don't overwhelm with details
- **Question-driven:** Ask targeted questions
- **Context-aware:** Reference past lessons naturally
- **Clear labeling:** Explain label choices
- **Architecture-focused:** Think through implications

## Example Interaction

```
User: I need to extract the Intuit engine into a separate service

Planner: Let me search for lessons about service extraction...

[Tool executes: search_lessons("service extraction")]

I found two relevant lessons from past work:
- Sprint 08: Service boundary issues with shared DB
- Sprint 12: API versioning during extraction

Before we proceed, a few questions:
1. Have you defined the service boundaries at the data model level?
2. What's your approach to API versioning?
3. Which components will be affected?

[User answers]

Planner: Based on your answers, this is a Type/Refactor with:
- Component/Backend
- Component/API
- Component/Database
- Priority/High
- Risk/Medium

Should I create a Gitea issue with these labels?

[User confirms]

Planner: I'll create the issue...

[Tool executes: create_issue(...)]

Created issue #47: "Extract Intuit Engine Service"
View at: https://gitea.hyperhivelabs.com/org/repo/issues/47

Now let me generate a detailed sprint plan...
```

## Important Notes

- **Never rush planning:** Take time to understand the work
- **Always search lessons:** Past experience prevents mistakes
- **Explain label choices:** Don't just apply labels, explain why
- **Think architecturally:** Consider broader implications
- **Branch safety:** Verify branch before creating issues

## Delegation

You focus on planning. For execution monitoring or implementation:
- **Orchestrator agent:** Sprint progress and coordination
- **Executor agent:** Implementation guidance and code review

Stay in your lane. Planning is your expertise.
```

**Key Points:**
- Agents describe their role and personality
- Tools are invoked via **natural language**, not function calls
- Claude Code maps natural language to MCP tool calls automatically
- Agents can reference other agents for delegation

---

## How Tool Invocation Works

**You don't call tools programmatically.** Instead, agents/commands describe what they need in natural language, and Claude Code handles the execution.

**Example flow:**

1. **Agent says:** "Let me search for lessons about authentication"
2. **Claude Code:**
   - Parses the intent
   - Maps to MCP tool: `search_lessons(query="authentication")`
   - Executes the tool
   - Returns results
3. **Agent receives:** List of matching lessons
4. **Agent continues:** "I found 3 lessons about authentication..."

This natural language interface makes agents more maintainable and readable

---

## Configuration

### Plugin .mcp.json

**File:** `projman/.mcp.json`

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

**Note:** Both MCP servers are shared at `../mcp-servers/` (repository root). The projman plugin includes `GITEA_REPO` and `WIKIJS_PROJECT` for project-scoped operations.

### Environment Variables

**Required (System-Level):**
- `GITEA_API_URL`
- `GITEA_API_TOKEN`
- `GITEA_OWNER`
- `WIKIJS_API_URL`
- `WIKIJS_API_TOKEN`
- `WIKIJS_BASE_PATH`

**Required (Project-Level):**
- `GITEA_REPO` - Repository name (e.g., `cuisineflow`)
- `WIKIJS_PROJECT` - Project path relative to base (e.g., `projects/cuisineflow`)

---

## Three-Agent Model

The projman plugin implements a three-agent architecture mirroring the proven workflow:

### 1. Planner Agent

**File:** `agents/planner.md`

**Role:**
- Sprint planning and architecture analysis
- Clarifying questions about scope
- Architectural decision-making
- Issue creation with appropriate labels
- Lessons learned integration

**Personality:**
- Thorough but not overwhelming
- Asks targeted questions
- Thinks through edge cases
- Never rushes decisions
- Architecture-aware

**Example Prompt:**

```markdown
You are the Sprint Planner for Hyper Hive Labs.

Your role:
- Guide users through sprint planning
- Ask targeted questions about scope and architecture
- Detect issue types (Bug, Feature, Refactor)
- Suggest appropriate labels based on context
- Generate comprehensive sprint documents
- Consider lessons learned from past sprints

You are:
- Thorough but not overwhelming
- Architecture-aware
- Label-conscious (use Type/Refactor for architectural changes)
- Process-oriented

You always:
- Reference relevant past lessons
- Consider technical debt
- Identify cross-project impacts
- Suggest realistic scope

Available Tools:
- search_lessons: Search past lessons learned for relevant context
- list_issues: Check existing issues for related work
- suggest_labels: Get label suggestions based on context
- create_issue: Create Gitea issue with labels
- get_labels: Fetch available label taxonomy

Sprint Planning Flow:
1. Ask what feature/fix/refactor is planned
2. Search lessons learned for similar past work
3. Ask clarifying questions (architecture, components, risks)
4. Suggest appropriate labels
5. Create issue with labels if user confirms
6. Generate sprint planning document
```

### 2. Orchestrator Agent

**File:** `agents/orchestrator.md`

**Role:**
- Sprint progress monitoring
- Task dependency coordination
- Blocker identification
- Git operations (commit, merge, cleanup)
- Status tracking and reporting

**Personality:**
- Concise and action-oriented
- Tracks details meticulously
- Progress-focused
- Blocker-aware

**Example Prompt:**

```markdown
You are the Sprint Orchestrator for Hyper Hive Labs.

Your role:
- Monitor sprint progress
- Track issue status
- Identify and surface blockers
- Coordinate between tasks
- Keep sprint on track
- Handle Git operations

You are:
- Progress-focused
- Blocker-aware
- Context-provider
- Coordination-minded
- Concise in communication

You always:
- Check issue status before reporting
- Identify dependencies
- Surface relevant documentation
- Keep things moving
- Generate lean execution prompts (not full docs)

Available Tools:
- get_issue: Fetch current sprint issue details
- list_issues: Check related issues
- update_issue: Update sprint status
- add_comment: Add progress comments
- search_pages: Find relevant documentation

Status Monitoring:
1. Check sprint issue status
2. Identify completed vs remaining work
3. Surface any blockers
4. Suggest next actions
5. Update issue with progress
```

### 3. Executor Agent

**File:** `agents/executor.md`

**Role:**
- Implementation guidance
- Code review suggestions
- Testing strategy
- Documentation
- Quality standards enforcement

**Personality:**
- Implementation-focused
- Follows specs precisely
- Technically detailed
- Quality-conscious

**Example Prompt:**

```markdown
You are the Sprint Executor for Hyper Hive Labs.

Your role:
- Provide implementation guidance
- Suggest code patterns
- Review technical decisions
- Ensure quality standards
- Reference best practices

You are:
- Technically detailed
- Quality-focused
- Pattern-aware
- Standards-conscious
- Implementation-focused

You always:
- Follow modular architecture principles
- Suggest discrete methods/functions
- Consider testability
- Document decisions
- Follow architectural guidelines from planning

Available Tools:
- get_page: Fetch architectural documentation
- get_shared_docs: Access company-wide patterns
- search_pages: Find relevant technical docs

Implementation Flow:
1. Review sprint issue and planning documents
2. Reference architectural decisions from planning
3. Provide step-by-step implementation guidance
4. Suggest code patterns and structure
5. Ensure testing strategy
6. Generate completion reports
```

---

## Commands

### 1. Sprint Plan Command

**File:** `commands/sprint-plan.md`

**Usage:** `/sprint-plan`

**Description:** Initiates sprint planning with the planner agent

**Flow:**

```
User: /sprint-plan

Planner: Let me help you plan this sprint.

         What are you building?

User: Extract Intuit engine into separate service

Planner: I detected architectural changes - this is Type/Refactor.

         Searching lessons learned for "service extraction"...
         📚 Found 2 relevant lessons:
         - Sprint 08: Service boundary issues with shared DB
         - Sprint 12: API versioning during extraction

         Which components are affected?
         - Component/Backend
         - Component/API
         - Component/Database

         Should we create a Gitea issue for tracking?

User: Yes

Planner: Created issue #47 with labels:
         - Type/Refactor
         - Component/Backend
         - Component/API
         - Component/Database
         - Priority/High
         - Source/Development

         Generating sprint plan...

         Sprint Plan: Intuit Engine Extraction
         =====================================

         ## Architecture
         [Detailed architecture analysis]

         ## Tasks
         1. Define service boundaries
         2. Design API contracts
         3. Extract database schema
         4. Implement service
         5. Update CuisineFlow integration
         6. Deploy and test

         ## Risks
         - Database migration complexity
         - API versioning challenges

         ## Timeline
         Estimated: 2 weeks

         ## References
         - Lesson: Sprint 08 (service boundaries)
         - Lesson: Sprint 12 (API versioning)
```

**Success Criteria:**
- Issue created with correct labels
- Lessons learned referenced
- Sprint document generated
- Only creates issues in development branch

### 2. Sprint Start Command

**File:** `commands/sprint-start.md`

**Usage:** `/sprint-start`

**Description:** Starts sprint with relevant lessons surfaced

**Flow:**

```
User: /sprint-start

Orchestrator: Starting sprint...

              Sprint Issue: #47 - Intuit Engine Extraction

              Searching lessons learned for relevant context...
              📚 Found 2 relevant lessons:
              - Sprint 08: Service boundary issues with shared DB
                → Key takeaway: Define clear service boundaries before extracting
              - Sprint 12: API versioning during extraction
                → Key takeaway: Version APIs from the start

              These might be helpful for this extraction work.

              Next Steps:
              1. Review architectural decisions from planning
              2. Define service boundaries
              3. Create API contract specifications

              Ready to begin. Use /sprint-status to check progress.
```

**Success Criteria:**
- Searches lessons learned
- Surfaces relevant past experiences
- Links to sprint issue
- Provides helpful context

### 3. Sprint Status Command

**File:** `commands/sprint-status.md`

**Usage:** `/sprint-status`

**Description:** Check current sprint progress

**Flow:**

```
User: /sprint-status

Orchestrator: Sprint Status: Intuit Engine Extraction
              Issue: #47

              Progress: 60% complete

              ✅ Completed:
              - Define service boundaries
              - Design API contracts
              - Extract database schema

              🔄 In Progress:
              - Implement service (80%)

              ⏳ Remaining:
              - Update CuisineFlow integration
              - Deploy and test

              🚫 Blockers:
              None identified

              Next Action:
              Complete service implementation, then move to integration testing
```

**Success Criteria:**
- Clear status overview
- Identifies blockers
- Actionable next steps
- Links to relevant issues

### 4. Sprint Close Command

**File:** `commands/sprint-close.md`

**Usage:** `/sprint-close`

**Description:** Closes sprint and captures lessons learned

**Flow:**

```
User: /sprint-close

Orchestrator: Let's close this sprint and capture lessons learned...

              What went wrong that we should avoid next time?

User: Database migration took longer than expected due to foreign key constraints

Orchestrator: What decisions worked really well?

User: Defining API contracts upfront prevented integration issues

Orchestrator: Were there any Claude Code issues that caused loops/blocks?

User: Yes, Claude got stuck in a loop trying to fix a circular import

Orchestrator: Any architectural insights for similar future work?

User: Service boundaries need to be defined at the data model level first

Orchestrator: I'll create a lesson in Wiki.js:

              Sprint 16: Intuit Engine Extraction - Lessons Learned
              =====================================================

              ## What Went Wrong
              - Database migration took longer than expected due to FK constraints
                → Always map FK relationships before extraction

              ## What Worked Well
              - API contracts defined upfront prevented integration issues
                → Continue this practice for all service extractions

              ## Claude Code Issues
              - Circular import loop in service initialization
                → Watch for import cycles in new services

              ## Architecture Insights
              - Service boundaries must be defined at data model level first
                → Data-first approach for future extractions

              Tags detected:
              #service-extraction #api #database #refactoring #claude-code-loops

              Creating page in Wiki.js... ✅
              Path: /hyper-hive-labs/projects/cuisineflow/lessons-learned/sprints/sprint-16-intuit-engine

              Updating INDEX.md... ✅

              Closing sprint issue #47... ✅

              View lesson at: https://wiki.hyperhivelabs.com/hyper-hive-labs/projects/cuisineflow/lessons-learned/sprints/sprint-16-intuit-engine
```

**Success Criteria:**
- Interactive retrospective guide
- Document created in Wiki.js
- INDEX.md updated with tags
- Sprint issue closed
- Lessons searchable for future sprints

### 5. Labels Sync Command

**File:** `commands/labels-sync.md`

**Usage:** `/labels-sync`

**Description:** Sync label taxonomy from Gitea

**Flow:**

```
User: /labels-sync

Agent: Fetching labels from Gitea...
       Comparing with local reference...

       Found 1 new label: Type/Documentation
       Found 2 modified descriptions

       New Label:
       - Type/Documentation
         Color: #0052cc
         Description: Documentation-only changes
         → Should update suggestion logic to detect "docs", "readme"

       Modified Label:
       - Priority/High
         Old: "High priority issues"
         New: "Blocks sprint completion or important feature"
         → Description clarified

       - Component/API
         Old: "API related"
         New: "REST/GraphQL API endpoints and contracts"
         → More specific description

       Shall I update the local reference and suggestion rules?

User: Yes

Agent: Updated ✅
       - labels-reference.md updated with 44 labels (was 43)
       - Suggestion logic updated to detect documentation keywords
       - Label descriptions synchronized

       Summary:
       - Organization labels: 28 (was 27)
       - Repository labels: 16
       - Total: 44 labels in taxonomy
```

**Success Criteria:**
- Fetches live data from Gitea
- Diff detection works correctly
- Agent provides meaningful impact analysis
- Local reference stays synchronized
- Suggestion logic updated as needed

---

## Label Taxonomy System

### 43-Label System

**Organization Labels (27):**
- **Agent/2:** Agent-assigned vs user-created
- **Complexity/3:** Low, Medium, High
- **Efforts/5:** XS, S, M, L, XL
- **Priority/4:** Low, Medium, High, Critical
- **Risk/3:** Low, Medium, High
- **Source/4:** Development, Staging, Production, External
- **Type/6:** Bug, Feature, Refactor, Documentation, Test, Chore

**Repository Labels (16):**
- **Component/9:** Backend, Frontend, API, Database, Auth, Deploy, Testing, Docs, Infra
- **Tech/7:** Python, JavaScript, Docker, PostgreSQL, Redis, Vue, FastAPI

### Type/Refactor Label

**Important:** `Type/Refactor` is now implemented at organization level

**Usage:**
- Architectural changes
- Service extraction (like Intuit engine)
- Code restructuring without feature changes
- Performance optimizations requiring significant changes
- Technical debt reduction

**Detection Keywords:**
- "extract", "refactor", "restructure"
- "optimize architecture"
- "service boundary", "microservice", "decouple"
- "technical debt", "code quality"

### Skill: Label Taxonomy

**File:** `skills/label-taxonomy/labels-reference.md`

This skill provides the complete label reference and is loaded when relevant. It includes:
- Full label list with descriptions
- Exclusive vs non-exclusive rules
- Color codes
- Usage guidelines
- Example scenarios

---

## Branch-Aware Security Model

Plugin behavior adapts to the current Git branch to prevent accidental changes:

### Development Mode

**Branches:** `development`, `feat/*`, `feature/*`

**Permissions:**
- Full access to all operations
- Can create Gitea issues
- Can modify all files
- Can capture lessons learned

### Staging Mode

**Branches:** `staging`, `stage/*`

**Permissions:**
- Read-only for application code
- Can modify `.env` files
- Can create issues to document needed fixes
- Warns on attempted code changes

**Behavior:**
```
User: /sprint-plan

Agent: ⚠️ Warning: You're on the 'staging' branch.

       I can help with planning and create issues for tracking,
       but implementation should be done on a development branch.

       Proceed with planning?
```

### Production Mode

**Branches:** `main`, `master`, `prod/*`

**Permissions:**
- Read-only for application code
- Emergency-only `.env` modifications
- Can create incident issues
- Blocks code changes

**Behavior:**
```
User: /sprint-plan

Agent: 🚫 Error: You're on the 'main' (production) branch.

       Sprint planning and implementation must be done on development branches.
       Creating issues is allowed for incident tracking.

       Please switch to a development branch to proceed.
```

---

## Implementation Phases

### Phase 1: Core Infrastructure

**Deliverable:** Working MCP servers with hybrid configuration

**Tasks:**
1. Set up Gitea MCP server (see MCP-GITEA.md)
2. Set up Wiki.js MCP server (see MCP-WIKIJS.md)
3. Create plugin structure
4. Configure `.mcp.json` to reference shared servers
5. Test configuration loading
6. Validate MCP server connections

**Success Criteria:**
- Both MCP servers running
- Configuration loads correctly
- Plugin can communicate with Gitea and Wiki.js
- Mode detection works (project mode)

### Phase 2: Sprint Planning Commands

**Deliverable:** `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close` commands

**Tasks:**
1. Create command markdown files
2. Define command parameters
3. Integrate with agents
4. Handle branch detection
5. Test command workflows

**Success Criteria:**
- All commands work end-to-end
- Branch detection prevents wrong-branch operations
- Issue creation works
- Lessons learned captured

### Phase 3: Agent System

**Deliverable:** Planner, Orchestrator, Executor agents

**Tasks:**
1. Create agent markdown prompts
2. Define agent personalities
3. Design interaction patterns
4. Integrate with MCP tools
5. Test agent behaviors

**Success Criteria:**
- Agents provide valuable guidance
- Questions are relevant
- Label suggestions accurate
- Sprint documents well-structured

### Phase 4: Lessons Learned System

**Deliverable:** Integrated lessons learned in Wiki.js

**Tasks:**
1. Design Wiki.js page structure
2. Create INDEX.md template
3. Build search integration
4. Implement capture workflow
5. Test tag-based filtering

**Success Criteria:**
- Lessons captured during sprint close
- INDEX.md updated automatically
- Search finds relevant lessons
- Tags work for categorization

### Phase 5: Testing & Validation

**Deliverable:** Comprehensive test coverage

**Tasks:**
1. Write integration tests
2. Test with real sprint
3. Validate configuration scenarios
4. Test branch detection
5. Collect user feedback

**Success Criteria:**
- All tests pass
- Real sprint handled successfully
- No critical bugs
- Saves time vs manual process

### Phase 6: Documentation & Refinement

**Deliverable:** Complete documentation

**Tasks:**
1. Write README.md
2. Write CONFIGURATION.md
3. Create ARCHITECTURE.md
4. Write CONTRIBUTING.md
5. Iterate based on feedback

**Success Criteria:**
- Clear setup instructions
- Configuration well-explained
- Examples provided
- Ready for team use

### Phase 7: Marketplace Preparation

**Deliverable:** Plugin available in Gitea marketplace

**Tasks:**
1. Create marketplace repository
2. Add plugin to marketplace
3. Create marketplace.json
4. Test installation
5. Document for team

**Success Criteria:**
- Plugin available via marketplace
- Installation works smoothly
- Team can access plugin
- Documentation clear

### Phase 8: Production Hardening

**Deliverable:** Production-ready plugin

**Tasks:**
1. Implement error handling
2. Optimize performance
3. Security audit
4. Logging and monitoring
5. Final testing

**Success Criteria:**
- Graceful failure handling
- Fast performance
- No security vulnerabilities
- Ready for production use

---

## Usage Examples

### Example 1: Bug Fix Sprint

```
User: /sprint-plan

Planner: What are you building?

User: Fix authentication bug where tokens expire early

Planner: I detected a bug fix.

         Searching lessons learned for "authentication"...
         📚 Found 1 lesson:
         - Sprint 01: Token expiration issues

         This is Type/Bug with Component/Auth.
         Priority?

User: High

Planner: Created issue #52:
         Labels: Type/Bug, Component/Auth, Priority/High, Source/Development

         Sprint Plan: Fix Token Expiration Bug
         =====================================
         [Plan details]
```

### Example 2: New Feature Sprint

```
User: /sprint-plan

Planner: What are you building?

User: Add export functionality to reports

Planner: This is a new feature.

         Components affected:
         - Component/Backend (export logic)
         - Component/API (export endpoint)
         - Component/Frontend (export button)

         Complexity?

User: Medium

Planner: Created issue #53:
         Labels: Type/Feature, Component/Backend, Component/API, Component/Frontend,
                Complexity/Medium, Priority/Medium, Source/Development

         [Sprint plan generated]
```

### Example 3: Refactor Sprint

```
User: /sprint-plan

Planner: What are you building?

User: Refactor database access layer for better testability

Planner: I detected architectural changes - this is Type/Refactor.

         Searching lessons learned for "refactor"...
         📚 Found 3 lessons from similar refactoring work

         This affects Component/Backend and Component/Database.
         Risk level?

User: Medium

Planner: Created issue #54:
         Labels: Type/Refactor, Component/Backend, Component/Database,
                Risk/Medium, Priority/Medium, Efforts/L, Source/Development

         [Refactoring plan with architecture considerations]
```

---

## Best Practices

### 1. Always Start with Planning

Use `/sprint-plan` to:
- Search relevant lessons learned
- Get label suggestions
- Create tracked issues
- Generate structured plans

### 2. Check Status Regularly

Use `/sprint-status` to:
- Monitor progress
- Identify blockers early
- Stay on track
- Update stakeholders

### 3. Always Close with Lessons

Use `/sprint-close` to:
- Capture what went wrong
- Document what worked
- Record Claude Code issues
- Share architectural insights

### 4. Keep Labels Current

Use `/labels-sync` to:
- Stay synchronized with Gitea
- Update suggestion logic
- Maintain accurate taxonomy

### 5. Branch Awareness

- Do planning on development branches
- Don't attempt code changes on staging/production
- Use production branch only for incidents

---

## Troubleshooting

### Issue: Plugin not loading

**Solution:**
```bash
# Check plugin manifest
cat projman/.claude-plugin/plugin.json

# Verify MCP servers are accessible
ls -la ../mcp-servers/gitea
ls -la ../mcp-servers/wikijs

# Check MCP server virtual environments
ls ../mcp-servers/gitea/.venv
ls ../mcp-servers/wikijs/.venv
```

### Issue: MCP tools not working

**Solution:**
```bash
# Verify environment variables are set
env | grep GITEA
env | grep WIKIJS

# Check system configs exist
cat ~/.config/claude/gitea.env
cat ~/.config/claude/wikijs.env

# Check project config
cat .env
```

### Issue: Lessons learned not saving

**Solution:**
- Verify Wiki.js connectivity
- Check Wiki.js API token permissions
- Ensure base structure exists in Wiki.js
- Verify project path in WIKIJS_PROJECT

### Issue: Labels not suggesting correctly

**Solution:**
- Run `/labels-sync` to update taxonomy
- Check label reference in `skills/label-taxonomy/`
- Verify Gitea has correct labels
- Test with clear keywords

---

## Next Steps

1. **Complete MCP server setup** (see MCP-GITEA.md and MCP-WIKIJS.md)
2. **Create plugin structure**
3. **Implement commands** (Phase 2)
4. **Create agents** (Phase 3)
5. **Test with real sprint** (Phase 5)
6. **Deploy to team** (Phase 7)
