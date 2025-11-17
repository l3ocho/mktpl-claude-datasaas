# PMO Plugin Reference (projman-pmo)

## Overview

The `projman-pmo` plugin provides multi-project PMO coordination with cross-project dependency tracking, resource allocation, and company-wide visibility. It builds on projman but operates at the organization level.

**Build Order:** Build AFTER projman is working and validated
**Target Users:** PMO coordinators, engineering managers, CTOs
**Scope:** Multi-project coordination across entire organization

**Key Features:**
- Cross-project status aggregation
- Dependency tracking and visualization
- Resource conflict detection
- Release coordination
- Company-wide lessons learned search
- Multi-project prioritization

---

## Plugin Structure

```
projman-pmo/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest
├── .mcp.json                      # Points to ../mcp-servers/ (company mode)
├── commands/
│   ├── pmo-status.md             # Multi-project status overview
│   ├── pmo-priorities.md         # Cross-project prioritization
│   ├── pmo-dependencies.md       # Dependency visualization
│   ├── pmo-conflicts.md          # Resource conflict detection
│   └── pmo-schedule.md           # Deployment schedule coordination
├── agents/
│   └── pmo-coordinator.md        # Multi-project coordination agent
└── README.md                      # Installation and usage guide
```

---

## Plugin Manifest

**File:** `projman-pmo/.claude-plugin/plugin.json`

```json
{
  "name": "projman-pmo",
  "version": "0.1.0",
  "displayName": "Projman PMO - Multi-Project Coordination",
  "description": "PMO coordination with cross-project visibility, dependency tracking, and resource management",
  "author": "Hyper Hive Labs",
  "homepage": "https://gitea.hotserv.cloud/hhl-infra/claude-code-hhl-toolkit/projman-pmo",
  "repository": {
    "type": "git",
    "url": "https://gitea.hotserv.cloud/hhl-infra/claude-code-hhl-toolkit.git"
  },
  "license": "MIT",
  "keywords": [
    "pmo",
    "multi-project",
    "coordination",
    "dependencies",
    "resource-management"
  ],
  "minimumClaudeVersion": "1.0.0",
  "main": "commands/",
  "dependencies": {
    "projman": ">=0.1.0"
  },
  "contributes": {
    "commands": [
      {
        "name": "pmo-status",
        "title": "PMO Status",
        "description": "Multi-project status overview",
        "file": "commands/pmo-status.md"
      },
      {
        "name": "pmo-priorities",
        "title": "PMO Priorities",
        "description": "Cross-project priority analysis",
        "file": "commands/pmo-priorities.md"
      },
      {
        "name": "pmo-dependencies",
        "title": "PMO Dependencies",
        "description": "Project dependency visualization",
        "file": "commands/pmo-dependencies.md"
      },
      {
        "name": "pmo-conflicts",
        "title": "PMO Resource Conflicts",
        "description": "Resource conflict detection and resolution",
        "file": "commands/pmo-conflicts.md"
      },
      {
        "name": "pmo-schedule",
        "title": "PMO Schedule",
        "description": "Multi-project deployment scheduling",
        "file": "commands/pmo-schedule.md"
      }
    ],
    "agents": [
      {
        "name": "pmo-coordinator",
        "title": "PMO Coordinator",
        "description": "Strategic multi-project coordination and dependency management",
        "file": "agents/pmo-coordinator.md"
      }
    ]
  },
  "configuration": {
    "required": [
      "GITEA_API_URL",
      "GITEA_API_TOKEN",
      "GITEA_OWNER",
      "WIKIJS_API_URL",
      "WIKIJS_API_TOKEN",
      "WIKIJS_BASE_PATH"
    ],
    "properties": {
      "GITEA_API_URL": {
        "type": "string",
        "description": "Gitea API base URL (e.g., https://gitea.example.com/api/v1)"
      },
      "GITEA_API_TOKEN": {
        "type": "string",
        "description": "Gitea API token with organization-level access",
        "secret": true
      },
      "GITEA_OWNER": {
        "type": "string",
        "description": "Gitea organization name"
      },
      "WIKIJS_API_URL": {
        "type": "string",
        "description": "Wiki.js GraphQL API URL (e.g., https://wiki.example.com/graphql)"
      },
      "WIKIJS_API_TOKEN": {
        "type": "string",
        "description": "Wiki.js API token with company-wide read access",
        "secret": true
      },
      "WIKIJS_BASE_PATH": {
        "type": "string",
        "description": "Base path in Wiki.js (e.g., /company-name)"
      }
    },
    "notes": {
      "company_mode": "PMO plugin operates in company-wide mode. Do NOT set GITEA_REPO or WIKIJS_PROJECT environment variables."
    }
  }
}
```

**Key Differences from projman:**
- `dependencies`: Declares dependency on projman plugin
- No `GITEA_REPO` or `WIKIJS_PROJECT` in configuration (company-wide mode)
- Focused on coordination, not individual project management

---

## Configuration

### Plugin .mcp.json

**File:** `projman-pmo/.mcp.json`

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

**Critical Differences from projman:**
- **NO** `GITEA_REPO` → operates on all repositories
- **NO** `WIKIJS_PROJECT` → operates on entire `/hyper-hive-labs` namespace
- Same shared MCP servers at `../mcp-servers/`

### Environment Variables

**Required (System-Level Only):**
- `GITEA_API_URL`
- `GITEA_API_TOKEN`
- `GITEA_OWNER`
- `WIKIJS_API_URL`
- `WIKIJS_API_TOKEN`
- `WIKIJS_BASE_PATH`

**NOT Required:**
- `GITEA_REPO` - PMO operates across all repos
- `WIKIJS_PROJECT` - PMO operates across entire namespace

---

## PMO Coordinator Agent

**File:** `agents/pmo-coordinator.md`

### Agent Personality

```markdown
You are the PMO Coordinator for Hyper Hive Labs.

Your role:
- Maintain strategic view across all projects
- Identify cross-project dependencies
- Detect resource conflicts
- Balance competing priorities
- Coordinate release timing
- Track customer deployment schedules
- Surface company-wide lessons learned

You are:
- Strategic thinker
- Dependency-aware
- Conflict detector
- Priority balancer
- Team coordinator
- NOT a micromanager

You delegate to project-level agents:
- Don't micromanage single projects
- Focus on cross-project issues
- Surface conflicts early
- Facilitate coordination
- Provide strategic guidance

Available Tools:
- aggregate_issues: Fetch issues across all repositories
- search_all_projects: Search lessons across all projects
- list_repos: Get all organization repositories
- get_shared_docs: Access company-wide patterns and best practices

Key Principles:
1. Strategic overview, not tactical details
2. Cross-project coordination, not single-project management
3. Identify conflicts before they become problems
4. Balance competing priorities across teams
5. Learn from patterns across all projects
```

### Delegation Model

```
PMO Agent (projman-pmo)
    ├─ Identifies cross-project issues
    ├─ Detects resource conflicts
    ├─ Coordinates release timing
    └─ Delegates to...
        ├─ Planner Agent (projman) → for project planning
        ├─ Orchestrator Agent (projman) → for project execution
        └─ Executor Agent (projman) → for implementation
```

**Example:**
```
User: /pmo-status

PMO: Projects Overview:

     CuisineFlow: Sprint in progress, 60% complete
     └─ Blocking: CuisineFlow-Site deployment

     I notice CuisineFlow-Site is waiting on API changes.
     Use projman in the cuisineflow-site repo to plan the sync work.
```

---

## Commands

### 1. PMO Status Command

**File:** `commands/pmo-status.md`

**Usage:** `/pmo-status`

**Description:** Consolidated view of all active projects

**Flow:**

```
User: /pmo-status

PMO: Projects Overview
     ================

     CuisineFlow (main product)
     ├── Sprint: Intuit Engine Extraction
     ├── Status: In Progress (60%)
     ├── Issue: #47
     ├── Blockers: None
     ├── Next: API testing
     └── Timeline: On track (1 week remaining)

     CuisineFlow-Site (demo)
     ├── Sprint: Dashboard Updates
     ├── Status: Waiting on dependencies
     ├── Issue: #12
     ├── Blockers: Depends on CuisineFlow #47 (API changes)
     ├── Next: Deploy when API ready
     └── Timeline: Blocked (waiting on CuisineFlow)

     Intuit-Engine (service)
     ├── Sprint: Initial Setup
     ├── Status: Planning
     ├── Issue: #3
     ├── Blockers: Architecture decisions needed
     ├── Next: Service boundary definition
     └── Timeline: Not started

     HHL-Site (marketing)
     ├── Sprint: Content Updates
     ├── Status: Complete
     ├── Issue: #8 (closed)
     ├── Blockers: None
     ├── Next: Deploy to production
     └── Timeline: Ready for deployment

     Cross-Project Insights:
     - CuisineFlow-Site blocked by CuisineFlow #47
     - Intuit-Engine needs architectural guidance
     - HHL-Site ready for deployment

     Suggested Actions:
     1. Prioritize CuisineFlow #47 completion (unblocks Site)
     2. Schedule architecture review for Intuit-Engine
     3. Deploy HHL-Site content updates
```

**Success Criteria:**
- Shows all active projects
- Identifies blockers
- Surfaces dependencies
- Provides actionable insights

### 2. PMO Priorities Command

**File:** `commands/pmo-priorities.md`

**Usage:** `/pmo-priorities`

**Description:** Review and adjust priorities across projects

**Flow:**

```
User: /pmo-priorities

PMO: Priority Analysis Across Projects
     =================================

     Critical (Blocks launches):
     1. CuisineFlow #47 - Intuit Engine Extraction
        → Blocks: CuisineFlow v2.0 launch (Nov 15)
        → Blocks: CuisineFlow-Site deployment
        → Status: 60% complete, 1 week remaining
        → Recommendation: Maintain focus

     High (Important features):
     2. CuisineFlow-Site #12 - Dashboard Updates
        → Depends on: CuisineFlow #47
        → Status: Waiting
        → Recommendation: Begin planning, wait for #47

     3. Intuit-Engine #3 - Initial Setup
        → Enables: Service architecture
        → Status: Planning phase
        → Recommendation: Schedule architecture review

     Medium (Enhancements):
     4. HHL-Site #8 - Content Updates
        → Status: Complete, ready to deploy
        → Recommendation: Deploy this week

     Resource Analysis:
     Leo (primary developer):
     - Working on: CuisineFlow #47 (Critical)
     - Next: CuisineFlow-Site #12 (High)
     - Later: Intuit-Engine #3 (High)

     ⚠️ Potential Conflict:
     Leo is assigned to 3 high-priority items. Consider:
     - Maintaining focus on #47 (blocks launch)
     - Queueing #12 for after #47 completion
     - Scheduling #3 architecture review with team

     Recommend any priority changes?
```

**Success Criteria:**
- Clear priority ranking
- Resource allocation visibility
- Conflict identification
- Actionable recommendations

### 3. PMO Dependencies Command

**File:** `commands/pmo-dependencies.md`

**Usage:** `/pmo-dependencies`

**Description:** Visualize and manage project dependencies

**Flow:**

```
User: /pmo-dependencies

PMO: Project Dependencies
     ====================

     Dependency Graph:

     Intuit-Engine (service)
         ↓ (must complete before)
     CuisineFlow (main)
         ↓ (API changes required by)
     CuisineFlow-Site (demo)
         ↓ (deploy together)
     Customer VPS (deployments)

     Detailed Dependencies:

     1. CuisineFlow → Intuit-Engine
        Type: Service extraction
        Status: In progress
        Blocker: Must complete #47 before v2.0 launch
        Impact: High (blocks launch)

     2. CuisineFlow → CuisineFlow-Site
        Type: Feature sync
        Status: Waiting
        Blocker: Dashboard updates need API changes from #47
        Impact: Medium (demo consistency)

     3. CuisineFlow → Customer VPS
        Type: Deployment
        Status: Pending
        Blocker: v2.0 launch must complete before customer updates
        Impact: High (customer commitments)

     Deployment Order:
     1. Complete Intuit-Engine service extraction
     2. Deploy CuisineFlow v2.0 to production
     3. Sync CuisineFlow-Site demo
     4. Update customer VPS instances

     Critical Path:
     Intuit-Engine (#3) → CuisineFlow (#47) → Site (#12) → Customer VPS
     Estimated timeline: 3 weeks total

     Risks:
     - CuisineFlow #47 delay would cascade to all downstream
     - Customer VPS updates have Nov 20 deadline
```

**Success Criteria:**
- Dependencies clearly visualized
- Critical path identified
- Deployment order defined
- Risks highlighted

### 4. PMO Conflicts Command

**File:** `commands/pmo-conflicts.md`

**Usage:** `/pmo-conflicts`

**Description:** Detect and resolve resource conflicts

**Flow:**

```
User: /pmo-conflicts

PMO: Resource Conflict Analysis
     ==========================

     ⚠️ Resource Conflict Detected

     Leo (Developer):
     Assigned to:
     - CuisineFlow #47: Intuit Engine extraction (Priority: Critical)
     - CuisineFlow-Site #12: Dashboard redesign (Priority: High)
     - HHL-Site #8: Content update (Priority: Medium)
     - Intuit-Engine #3: Service setup (Priority: High)

     Conflict Analysis:
     - 4 active assignments across 3 projects
     - 2 are high priority or above
     - Estimated total effort: 4 weeks
     - Timeline: 2 weeks available

     Recommendations:
     1. FOCUS: CuisineFlow #47 (Critical, blocks launch)
        → Keep as primary focus
        → Estimated completion: 1 week

     2. QUEUE: CuisineFlow-Site #12 (High, depends on #47)
        → Start after #47 completes
        → Natural sequencing

     3. DELEGATE: HHL-Site #8 (Medium, content work)
        → Can be handled by marketing team
        → Low technical complexity

     4. SCHEDULE: Intuit-Engine #3 (High, planning phase)
        → Schedule architecture review session
        → Team collaboration, not solo work

     Timeline Conflict:

     Without changes:
     Week 1-2: CuisineFlow #47
     Week 3-4: Site #12 + Engine #3 (CONFLICT)

     With recommendations:
     Week 1-2: CuisineFlow #47 (FOCUS)
     Week 3: CuisineFlow-Site #12 (QUEUE)
     Week 4: Intuit-Engine #3 (SCHEDULE)
     HHL-Site #8: Marketing (DELEGATE)

     Apply recommendations?
```

**Success Criteria:**
- Conflicts identified automatically
- Clear impact analysis
- Actionable recommendations
- Timeline visualization

### 5. PMO Schedule Command

**File:** `commands/pmo-schedule.md`

**Usage:** `/pmo-schedule`

**Description:** Coordinate deployment schedules

**Flow:**

```
User: /pmo-schedule

PMO: Deployment Schedule
     ===================

     Week of Nov 6:
     - CuisineFlow: Continue Sprint #47 (Intuit Engine)
     - HHL-Site: Deploy content updates (#8) ✅

     Week of Nov 13:
     - CuisineFlow: Complete Sprint #47 ⚠️
       → Critical: Must complete by Nov 15 for launch
     - CuisineFlow-Site: Begin Dashboard updates (#12)

     Week of Nov 20:
     - CuisineFlow: Deploy v2.0 to production 🚀
       → Deployment window: Nov 20-22
     - CuisineFlow-Site: Sync demo with v2.0
     - Customer VPS: Begin rollout (Deadline: Nov 20)

     Week of Nov 27:
     - Customer VPS: Continue rollout
     - Intuit-Engine: Begin service implementation (#3)

     Critical Dates:
     - Nov 15: CuisineFlow v2.0 feature freeze
     - Nov 20: Production deployment
     - Nov 20: Customer VPS deadline
     - Nov 22: Demo site sync

     Dependencies:
     ✅ Intuit-Engine service boundaries defined
     🔄 CuisineFlow #47 in progress (60%)
     ⏳ CuisineFlow-Site #12 waiting
     ⏳ Customer VPS rollout pending

     Risks:
     ⚠️ CuisineFlow #47 delay would impact:
        - v2.0 launch date (Nov 20)
        - Customer VPS deadline (Nov 20)
        - Demo site sync (Nov 22)

     Mitigation:
     - Monitor #47 progress daily
     - Prepare rollback plan for customer VPS
     - Communicate delays early if detected
```

**Success Criteria:**
- Clear timeline visibility
- Dependencies tracked
- Critical dates highlighted
- Risk mitigation planned

---

## Multi-Project Coordination Workflows

### Cross-Project Lessons Learned

```
User: Search for lessons about service extraction across all projects

PMO: Searching lessons across all projects...

     Found 5 relevant lessons:

     CuisineFlow:
     - Sprint 08: Service boundary issues with shared DB
       Tags: #service-extraction #database #refactoring
       Key: Define boundaries at data model level first

     - Sprint 12: API versioning during extraction
       Tags: #api #versioning #refactoring
       Key: Version APIs from the start

     Intuit-Engine:
     - Sprint 02: Circular dependencies in service init
       Tags: #service-extraction #dependencies
       Key: Watch for import cycles

     CuisineFlow-Site:
     - Sprint 05: Sync issues during backend refactor
       Tags: #sync #refactoring
       Key: Coordinate deployments during major changes

     Shared Patterns:
     - /hyper-hive-labs/shared/architecture-patterns/service-extraction
       Key: Service Extraction Playbook

     Common Themes:
     1. Data model boundaries are critical
     2. API versioning prevents integration issues
     3. Watch for circular dependencies
     4. Coordinate deployments during refactors

     Apply these insights to current Intuit Engine extraction?
```

### Resource Allocation

```
User: /pmo-status

PMO: [Shows status]

     Resource Analysis:
     - Leo: 3 active projects (CuisineFlow, Site, Engine)
     - Marketing: 1 project (HHL-Site)

     Bottleneck detected: Leo is on critical path for all technical work

     Recommendations:
     1. Prioritize work that unblocks others
     2. Consider hiring/contracting for parallel work
     3. Delegate non-critical work (HHL-Site content)

     Would you like a detailed resource allocation report?
```

### Release Coordination

```
User: Plan the v2.0 release across all affected projects

PMO: Release Coordination: CuisineFlow v2.0
     ======================================

     Affected Projects:
     1. CuisineFlow (main product)
     2. Intuit-Engine (new service)
     3. CuisineFlow-Site (demo)
     4. Customer VPS instances

     Pre-Release Checklist:
     ✅ Intuit-Engine service deployed
     🔄 CuisineFlow #47 complete (60%)
     ⏳ Integration tests pending
     ⏳ Demo site updates pending
     ⏳ Customer migration scripts ready

     Deployment Sequence:
     1. Deploy Intuit-Engine service (backend)
        → Date: Nov 18
        → Duration: 2 hours
        → Rollback plan: Ready

     2. Deploy CuisineFlow v2.0 (main app)
        → Date: Nov 20
        → Duration: 4 hours
        → Rollback plan: Ready

     3. Sync CuisineFlow-Site (demo)
        → Date: Nov 22
        → Duration: 1 hour
        → Dependencies: Step 2 complete

     4. Update Customer VPS (production instances)
        → Date: Nov 23-25
        → Duration: Phased rollout
        → Dependencies: Steps 2 and 3 complete

     Communication Plan:
     - Nov 15: Feature freeze announcement
     - Nov 19: Deployment notification
     - Nov 20: v2.0 launch announcement
     - Nov 25: Completion report

     Risks & Mitigation:
     - Risk: #47 completion delayed
       Mitigation: Daily progress checks, adjust timeline early

     - Risk: Integration issues during deployment
       Mitigation: Comprehensive testing, rollback plan ready

     - Risk: Customer VPS migration issues
       Mitigation: Phased rollout, support on standby
```

---

## Company-Wide Patterns

### Accessing Shared Documentation

```python
# PMO agent can access company-wide patterns
shared_patterns = await wikijs.get_shared_docs("architecture-patterns")

# Returns:
# - microservices.md
# - api-gateway.md
# - database-per-service.md
# - service-extraction.md (created from lessons learned)
```

### Creating Shared Patterns

```
User: Create a shared pattern document for service extraction

PMO: I'll create a pattern document based on lessons from:
     - CuisineFlow Sprint 08
     - CuisineFlow Sprint 12
     - Intuit-Engine Sprint 02

     Creating: /hyper-hive-labs/shared/architecture-patterns/service-extraction

     Service Extraction Pattern
     =========================

     ## When to Use
     - Extracting microservice from monolith
     - Creating separate deployable service
     - Isolating domain boundaries

     ## Prerequisites
     - Clear service boundaries defined
     - Data model dependencies mapped
     - API contracts specified

     ## Steps
     1. Define service boundaries at data model level
     2. Design and version APIs first
     3. Extract data layer with foreign key awareness
     4. Implement service logic
     5. Update integration points
     6. Deploy and test

     ## Common Pitfalls
     - Not defining boundaries at data level first
     - Missing API versioning
     - Circular dependencies in initialization
     - Uncoordinated deployments

     ## Lessons Learned
     [Links to specific sprint lessons]

     Created ✅
     Tags: #service-extraction #microservices #refactoring #architecture

     This pattern is now available to all projects.
```

---

## Implementation Phases

### Phase 9: PMO Plugin Foundation

**Deliverable:** PMO plugin requirements and design

**Tasks:**
1. Analyze multi-project workflows
2. Identify coordination pain points
3. Design PMO agent scope
4. Extend MCP server for multi-repo operations
5. Define delegation model

**Success Criteria:**
- Clear PMO plugin scope
- Multi-repo queries working
- Delegation model defined
- Doesn't duplicate projman functionality

### Phase 10: PMO Commands & Workflows

**Deliverable:** PMO-specific commands working

**Tasks:**
1. Implement `/pmo-status` command
2. Implement `/pmo-priorities` command
3. Implement `/pmo-dependencies` command
4. Implement `/pmo-conflicts` command
5. Implement `/pmo-schedule` command
6. Build conflict detection logic
7. Create dependency visualization
8. Design release coordination workflow

**Success Criteria:**
- All commands provide valuable insights
- Dependencies clearly visualized
- Conflicts easily identified
- Coordination reduces manual overhead

### Phase 11: PMO Testing & Integration

**Deliverable:** Validated PMO plugin integrated with projman

**Tasks:**
1. Test with multiple projects (CuisineFlow, Site, Engine, HHL-Site)
2. Simulate deployment coordination scenarios
3. Test priority conflict resolution
4. Validate dependency tracking
5. Test cross-project lessons search
6. Ensure PMO delegates to projman agents

**Success Criteria:**
- Handles multiple projects correctly
- Dependencies respected
- Conflicts detected and surfaced
- Seamless integration with projman
- Cross-project lessons accessible

### Phase 12: Production Deployment

**Deliverable:** PMO plugin deployed and operational

**Tasks:**
1. Deploy across all environments (laptop, staging, production)
2. Configure for company-wide access
3. Set up backup and recovery
4. Establish monitoring and maintenance
5. Train team on PMO capabilities

**Success Criteria:**
- Works in all environments
- Configuration portable
- Backup procedures documented
- Team trained and comfortable

---

## PMO vs Projman: Key Differences

| Aspect | projman | projman-pmo |
|--------|---------|-------------|
| **Scope** | Single repository | All repositories |
| **Configuration** | `GITEA_REPO` + `WIKIJS_PROJECT` | Neither (company-wide) |
| **Agents** | Planner, Orchestrator, Executor | PMO Coordinator |
| **Commands** | Sprint-focused | Cross-project coordination |
| **Gitea Access** | Single repo issues | All repos issues |
| **Wiki.js Access** | Project path | Entire namespace |
| **Primary User** | Developer, Team Lead | PMO, Manager, CTO |
| **Focus** | Tactical execution | Strategic coordination |
| **Delegation** | N/A | Delegates to projman |

---

## Usage Examples

### Example 1: Detecting Blocked Work

```
User: /pmo-status

PMO: CuisineFlow-Site: Waiting on dependencies
     Blocked by: CuisineFlow #47 (API changes)

     Recommendation: Focus resources on CuisineFlow #47 to unblock Site work
```

### Example 2: Resource Conflict Resolution

```
User: /pmo-conflicts

PMO: Leo assigned to 4 tasks across 3 projects
     Estimated: 4 weeks work in 2 weeks timeline

     Recommendations:
     - Maintain focus on Critical priority (CuisineFlow #47)
     - Delegate content work (HHL-Site #8) to marketing
     - Schedule architectural review (Intuit-Engine #3) as team session
```

### Example 3: Release Planning

```
User: /pmo-schedule

PMO: Critical Path: Engine → CuisineFlow → Site → Customer VPS
     Deadline: Nov 20 (Customer VPS commitment)

     Current: Week 1 of 3
     Status: On track

     Risk: If CuisineFlow #47 delayed, entire timeline at risk
     Mitigation: Daily progress monitoring
```

---

## Best Practices

### 1. Use PMO for Strategic View

- Don't micromanage individual projects
- Focus on cross-project issues
- Identify blockers and dependencies
- Balance competing priorities

### 2. Delegate to Projman

- Use projman for project-specific planning
- Let project teams handle tactical execution
- PMO provides coordination, not implementation

### 3. Monitor Critical Path

- Identify which work blocks others
- Focus resources on critical path items
- Communicate delays early

### 4. Learn Across Projects

- Search lessons across all projects
- Create shared patterns from common themes
- Build company-wide knowledge base

### 5. Coordinate Releases

- Plan deployments across dependent projects
- Communicate timelines clearly
- Have rollback plans ready

---

## Troubleshooting

### Issue: PMO showing wrong mode

**Solution:**
```bash
# Ensure GITEA_REPO and WIKIJS_PROJECT are NOT set
env | grep GITEA
env | grep WIKIJS

# Should only show:
# GITEA_API_URL, GITEA_API_TOKEN, GITEA_OWNER
# WIKIJS_API_URL, WIKIJS_API_TOKEN, WIKIJS_BASE_PATH
```

### Issue: Can't access all repositories

**Solution:**
- Verify API token has organization-level access
- Check token permissions in Gitea
- Ensure GITEA_OWNER is correct

### Issue: Cross-project search not working

**Solution:**
- Verify Wiki.js structure exists
- Check base path is correct
- Ensure projects have lessons-learned directories

---

## Next Steps

1. **Complete projman plugin** (Phases 1-8)
2. **Validate projman works** with real sprints
3. **Begin PMO foundation** (Phase 9)
4. **Implement PMO commands** (Phase 10)
5. **Test with multiple projects** (Phase 11)
6. **Deploy to production** (Phase 12)
