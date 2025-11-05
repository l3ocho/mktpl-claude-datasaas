# ProjMan Plugin: Analysis & Design

## Executive Summary

Leo has built a sophisticated, working project management system over 15 sprints using:
- **Skills** for behavioral guidance
- **Python scripts** for Gitea API interaction
- **CLAUDE.md** for branch-aware permission control

**Goal:** Transform this proven system into a reusable, distributable plugin called `projman`.

## Current System Analysis

### What's Working Well

**1. Three-Chat Architecture**
- **Chat 0** (Claude Web): Planning & architecture → generates sprint documents
- **Chat 1** (Claude Code): Orchestration → manages branches, generates prompts, tracks progress
- **Chat 2+** (Claude Code): Execution → implements features according to prompts

**2. Branch-Aware Security**
```
development → Full access
feat/* → Full access  
staging → Read-only code, can modify .env, creates issues
main → Read-only code, emergency .env only, creates issues
```

**3. Gitea Integration**
- Two Python scripts: `create_gitea_issue.py` and `list_gitea_issues.py`
- Proper API authentication via environment variables
- Structured issue creation with labels, priority, affected files

**4. Skills System**
- `sprint-workflow.md` - Planning phase (Chat 0)
- `sprint-orchestrator.md` - Coordination phase (Chat 1)
- `sprint-executor.md` - Implementation phase (Chat 2+)
- `post-task-doc-sync.md` - Documentation updates
- `incident-reporter.md` - Issue creation from staging/prod

### What Feels Messy

Leo identified these friction points:

**1. Skills vs Agents Confusion**
> "I don't think skill would be the best way of handling an Agent"

Current state: Using skills to guide behavior that should be agent personalities

**2. Manual Script Invocation**
Scripts exist but require manual execution:
```bash
python ops/scripts/create_gitea_issue.py --title "..." --problem "..." ...
python ops/scripts/list_gitea_issues.py
```

**3. Mode Detection Redundancy**
Branch detection logic is duplicated across:
- CLAUDE.md
- Each skill file
- Manual checks in workflows

**4. Context Switching Overhead**
User must manually:
- Switch between chats
- Remember which skill to load where
- Copy/paste completion reports between chats

## Plugin Architecture Design

### Core Insight: The 3-Agent Model

Transform the three chats into three distinct agents:

```
projman/
├── agents/
│   ├── planner.md         # Chat 0 → Planning Agent
│   ├── orchestrator.md    # Chat 1 → PM Agent  
│   └── executor.md        # Chat 2+ → Implementation Agent
```

### Component Breakdown

#### 1. MCP Server: `gitea-mcp`

**Purpose:** Provide Gitea API access as tools that agents can use

**Tools to expose:**
```typescript
{
  "list_issues": {
    state: "open" | "closed" | "all",
    labels: string[],
    assignee: string
  },
  "create_issue": {
    title: string,
    body: string,
    labels: string[],
    assignee: string,
    priority: "critical" | "high" | "medium" | "low"
  },
  "update_issue": {
    number: number,
    state: "open" | "closed",
    body: string,
    labels: string[]
  },
  "get_issue": {
    number: number
  },
  "add_comment": {
    number: number,
    body: string
  },
  "get_labels": {
    // Fetches all org + repo labels with metadata
    include_org: boolean,
    include_repo: boolean
  },
  "suggest_labels": {
    // Analyzes context and suggests appropriate labels
    issue_body: string,
    context: {
      branch: string,
      files_changed: string[],
      is_bug: boolean,
      components: string[]
    }
  }
}
```

**Configuration:** `.mcp.json`
```json
{
  "mcpServers": {
    "gitea": {
      "command": "node",
      "args": ["mcp-server/gitea-server.js"],
      "env": {
        "GITEA_URL": "${GITEA_URL}",
        "GITEA_OWNER": "${GITEA_OWNER}",
        "GITEA_REPO": "${GITEA_REPO}",
        "GITEA_API_TOKEN": "${GITEA_API_TOKEN}"
      }
    }
  }
}
```

#### 2. Slash Commands

**Primary commands for user interaction:**

```markdown
commands/
├── sprint-plan.md       # /sprint-plan - Start planning a new sprint
├── sprint-start.md      # /sprint-start - Begin sprint execution
├── sprint-status.md     # /sprint-status - Check current sprint progress
├── sprint-close.md      # /sprint-close - Complete sprint, capture lessons learned
├── issue-create.md      # /issue-create - Quick issue creation
├── issue-list.md        # /issue-list - List issues with filters
├── labels-sync.md       # /labels-sync - Sync label taxonomy from Gitea
└── deploy-check.md      # /deploy-check - Staging/prod environment validation
```

**Example: `/labels-sync`**
```markdown
---
name: labels-sync
description: Sync label taxonomy from Gitea and review changes
agent: planner
---

You are updating the plugin's label reference from Gitea.

**Workflow:**
1. Fetch current labels from Gitea (org + repo)
2. Compare with local reference (skills/label-taxonomy/labels-reference.md)
3. Show user a diff of changes:
   - New labels added
   - Labels removed
   - Description/color changes
4. Discuss impact: "The new Type/Refactor label means we should update suggestion logic for architectural changes"
5. After approval, update local reference
6. Update label suggestion rules if needed

This ensures the plugin stays in sync with your evolving label system.
```

#### 3. Agents

**Agent: `planner.md`**
```markdown
---
name: planner
description: Architecture analysis and sprint planning expert
---

You are the Planning Agent for project management.

**Your Role:** 
- Analyze business requirements
- Make architectural decisions
- Break work into implementation steps
- Generate sprint planning documents
- Create Gitea issues for approved plans

**Your Personality:**
- Ask clarifying questions upfront
- Think through edge cases
- Consider architectural fit
- Document risks explicitly
- Never rush to implementation

**Your Tools:**
- gitea.create_issue - Create issues after approval
- gitea.list_issues - Check for similar existing issues

**Branch Awareness:**
${BRANCH_DETECTION_LOGIC}

**Workflow:**
[... rest of sprint-workflow.md content ...]
```

**Agent: `orchestrator.md`**
```markdown
---
name: orchestrator
description: Sprint execution coordinator and progress tracker
---

You are the Orchestrator Agent for project management.

**Your Role:**
- Manage sprint execution
- Generate lean execution prompts
- Track progress and update documentation
- Handle Git operations (commit, merge, cleanup)
- Coordinate task dependencies

**Your Personality:**
- Concise and action-oriented
- Track details meticulously
- Signal next steps clearly
- Never write application code yourself

**Your Tools:**
- gitea.get_issue - Read issue details
- gitea.update_issue - Update issue status
- gitea.add_comment - Add progress notes

**Branch Awareness:**
${BRANCH_DETECTION_LOGIC}

**Workflow:**
[... rest of sprint-orchestrator.md content ...]
```

**Agent: `executor.md`**
```markdown
---
name: executor
description: Feature implementation and code execution specialist
---

You are the Executor Agent for project management.

**Your Role:**
- Implement features according to execution prompts
- Write clean, tested code
- Follow architectural decisions from planning
- Generate completion reports for orchestrator

**Your Personality:**
- Implementation-focused
- Follow specs precisely
- Test as you build
- Report blockers immediately

**Your Tools:**
- None (uses standard code tools)

**Branch Awareness:**
${BRANCH_DETECTION_LOGIC}

**Workflow:**
[... rest of sprint-executor.md content ...]
```

#### 4. Skills

Skills become **supporting knowledge** rather than primary orchestrators:

```markdown
skills/
├── gitea-api/
│   └── SKILL.md          # How to use Gitea MCP server effectively
├── agile-pm/
│   └── SKILL.md          # Agile/PMP best practices
└── branch-strategy/
    └── SKILL.MD          # Git branching workflow
```

#### 5. Hooks

Automate repetitive actions:

```json
{
  "hooks": [
    {
      "name": "post-task-sync",
      "event": "task_completed",
      "action": "run_command",
      "command": "update-docs",
      "description": "Sync documentation after task completion"
    },
    {
      "name": "staging-incident",
      "event": "file_changed",
      "filter": {
        "branch": "staging",
        "paths": ["src/**/*.py", "src/**/*.js"]
      },
      "action": "warn",
      "message": "⚠️ Code changes on staging branch. Consider creating issue instead."
    }
  ]
}
```

### Environment-Aware Behavior

**Key Design Decision:** Plugin behavior adapts to Git branch

```typescript
// Branch detection in plugin
const CURRENT_BRANCH = getCurrentBranch();
const MODE = detectMode(CURRENT_BRANCH);

// Modify agent permissions based on mode
switch (MODE) {
  case 'DEVELOPMENT':
    // Full access
    agents.planner.allowGiteaAPI = true;
    agents.orchestrator.allowFileWrite = true;
    break;
    
  case 'STAGING':
    // Read-only code, can modify .env, can create issues
    agents.planner.allowGiteaAPI = true;
    agents.orchestrator.allowFileWrite = false;
    agents.orchestrator.allowEnvWrite = true;
    break;
    
  case 'PRODUCTION':
    // Emergency mode only
    agents.planner.allowGiteaAPI = true;  // Create incidents
    agents.orchestrator.allowFileWrite = false;
    agents.orchestrator.allowEnvWrite = true;  // Emergency only
    break;
}
```

## Migration Strategy

### Phase 1: MCP Server (Week 1)

**Goal:** Replace Python scripts with MCP server

**Tasks:**
1. Build `gitea-mcp` server in Node.js/TypeScript
2. Implement 5 core tools (list, create, update, get, comment)
3. Test with environment variables from CuisineFlow
4. Verify equivalent functionality to existing scripts

**Success Criteria:**
- MCP server can create issues identical to `create_gitea_issue.py`
- MCP server can list issues identical to `list_gitea_issues.py`
- No regression in functionality

### Phase 2: Agents (Week 2)

**Goal:** Convert skills to agents

**Tasks:**
1. Create `agents/planner.md` from `sprint-workflow.md`
2. Create `agents/orchestrator.md` from `sprint-orchestrator.md`  
3. Create `agents/executor.md` from `sprint-executor.md`
4. Add agent-specific tool permissions
5. Test agent invocation via commands

**Success Criteria:**
- `/sprint-plan` invokes planner agent correctly
- `/sprint-start` invokes orchestrator agent correctly
- Agents have distinct personalities and tool access

### Phase 3: Commands (Week 2-3)

**Goal:** Create user-facing slash commands

**Tasks:**
1. Build 6 core commands (plan, start, status, issue-create, issue-list, deploy-check)
2. Connect commands to agents
3. Add branch detection to command behavior
4. Test command flow end-to-end

**Success Criteria:**
- Commands invoke correct agents
- Branch restrictions work automatically
- User workflow feels natural

### Phase 4: Hooks (Week 3)

**Goal:** Automate repetitive tasks

**Tasks:**
1. Implement post-task documentation sync
2. Add staging/production code change warnings
3. Auto-update issue status on merge
4. Test hook reliability

**Success Criteria:**
- Hooks trigger at correct moments
- No false positives
- Improve workflow efficiency

### Phase 5: Skills Refactor (Week 4)

**Goal:** Convert orchestration skills to supporting knowledge

**Tasks:**
1. Extract Gitea API patterns → `skills/gitea-api/SKILL.md`
2. Extract PM best practices → `skills/agile-pm/SKILL.md`
3. Extract Git workflows → `skills/branch-strategy/SKILL.md`
4. Remove duplication from agent prompts

**Success Criteria:**
- Skills are referenced by agents, not primary orchestrators
- Less token usage per interaction
- Knowledge is reusable across agents

### Phase 6: Local Testing (Week 4)

**Goal:** Validate entire plugin in CuisineFlow

**Tasks:**
1. Create local marketplace for testing
2. Install plugin in CuisineFlow project
3. Run through complete sprint cycle
4. Compare to current workflow
5. Fix issues and iterate

**Success Criteria:**
- Plugin performs equivalently to current system
- Workflow feels smoother, not worse
- No major regressions

### Phase 7: Distribution (Week 5)

**Goal:** Package for others to use

**Tasks:**
1. Write comprehensive README
2. Add installation instructions
3. Document configuration requirements
4. Create example `.env` template
5. Publish to plugin marketplace

**Success Criteria:**
- Someone else can install and use it
- Clear documentation
- Configuration is straightforward

## Directory Structure

```
projman/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── sprint-plan.md
│   ├── sprint-start.md
│   ├── sprint-status.md
│   ├── issue-create.md
│   ├── issue-list.md
│   └── deploy-check.md
├── agents/
│   ├── planner.md
│   ├── orchestrator.md
│   └── executor.md
├── skills/
│   ├── gitea-api/
│   │   └── SKILL.md
│   ├── agile-pm/
│   │   └── SKILL.md
│   └── branch-strategy/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
├── .mcp.json
├── mcp-server/
│   ├── package.json
│   ├── tsconfig.json
│   ├── gitea-server.ts
│   └── types.ts
├── README.md
├── LICENSE
└── CHANGELOG.md
```

## Key Decisions

### Decision 1: MCP vs Direct API Calls in Commands

**Choice:** Use MCP Server

**Rationale:**
- Agents can use tools naturally in conversation
- Easier to test MCP server independently
- Future-proof for adding more integrations (Asana, Linear)
- Follows Claude Code best practices

### Decision 2: Three Agents vs One Agent with Modes

**Choice:** Three Distinct Agents

**Rationale:**
- Clear separation of concerns matches Leo's three-chat workflow
- Each agent has distinct personality and tool access
- User knows exactly which agent they're talking to
- Prevents mode confusion

### Decision 3: Branch Detection in Plugin vs CLAUDE.md

**Choice:** Both

**Rationale:**
- CLAUDE.md provides base-level permissions (file access)
- Plugin agents adapt behavior based on branch (tool usage)
- Defense in depth - two layers of protection
- Plugin works with or without CLAUDE.md

### Decision 4: Skills as Orchestrators vs Knowledge

**Choice:** Skills as Supporting Knowledge

**Rationale:**
- Agents are the primary interface
- Skills reduce token usage (loaded only when relevant)
- Skills can be shared across agents
- Follows Anthropic's Agent Skills spec

## Validated Requirements from Leo

**Q1: Asana Integration**
- ✅ Build Gitea-only first, add Asana as separate MCP server later

**Q2: Agent Invocation**
- ✅ Via commands only (`/sprint-plan` → planner agent)

**Q3: Multi-Project Support**
- ✅ Two plugins needed:
  - `projman`: Single-repo project management (build first)
  - `projman-pmo`: Multi-project orchestration (build second)
- **Context:** Leo manages interdependent projects:
  - CuisineFlow (main product)
  - CuisineFlow-Site (demo sync + customer gateway)
  - Intuit Engine Service (API aggregator extraction - imminent)
  - HHL-Site (company presence)
- These have real deployment dependencies and require coordination

**Q4: Deployment Environment**
- ✅ Same plugin on laptop + VPS servers, branch-aware behavior handles differences

**Q5: Label System**
- ✅ Leo has sophisticated 43-label taxonomy at org level (enforced consistency)
- ✅ Include label suggestion in v1
- ✅ Plugin maintains local reference, syncs from Gitea with agent review

**Q6: Lessons Learned**
- ✅ Wiki-based implementation in v1 (NOT v2)
- **Critical pain point:** 15 sprints with no lesson capture causing repeated mistakes
- **Real example:** Claude Code infinite loops on same issues 2-3 times
- Must capture at sprint close, reference at sprint start

## Success Metrics

**Technical:**
- ✅ MCP server passes all integration tests
- ✅ Agents invoke correctly via commands
- ✅ Branch detection works 100% reliably
- ✅ No token usage increase vs current system

**User Experience:**
- ✅ Leo completes sprint cycle faster than before
- ✅ Less context switching between chats
- ✅ Fewer manual script invocations
- ✅ Clearer agent personalities

**Distribution:**
- ✅ Another PM can install and use it
- ✅ Documentation is clear enough
- ✅ Configuration takes <10 minutes

## Next Steps

**Immediate (Today):**
1. Leo reviews this analysis
2. Answer open questions (Q1-Q4)
3. Decide: build MCP server first or start with agents?

**Short-term (This Week):**
1. Begin Phase 1 (MCP server) OR Phase 2 (agents)
2. Set up local marketplace for testing
3. Create `plugin.json` manifest

**Medium-term (Next 2 Weeks):**
1. Complete Phases 1-4 (MCP, agents, commands, hooks)
2. Test in real CuisineFlow sprint
3. Iterate based on friction points

## Anti-Over-Engineering Checklist

Before building anything, verify:
- [ ] Have we done this manually 3+ times? ✅ (15 sprints)
- [ ] Is current system actually broken? ✅ (messy, but Leo identified pain points)
- [ ] Will plugin reduce friction? ✅ (fewer manual steps, clearer roles)
- [ ] Can we build incrementally? ✅ (7-phase plan)
- [ ] Is scope contained? ✅ (Gitea only, not all possible features)

**Verdict:** This plugin is justified. Proceed with confidence.
