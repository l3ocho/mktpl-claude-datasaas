# ProjMan Plugin Suite - Implementation Plan

**Plugins:** `projman` (single-repo) + `projman-pmo` (multi-project)
**Build Order:** projman first, then projman-pmo
**Label System:** Type/Refactor now implemented at organization level

---

## Phase 1: Core Infrastructure (projman)

### 1.1 MCP Server Foundation

**Deliverable:** Working Gitea MCP server with all required tools

**Tasks:**
- Set up Node.js/TypeScript project structure
- Implement authentication with Gitea API
- Create 7 core tools:
  - `list_issues` - Query issues with filters
  - `get_issue` - Fetch single issue details
  - `create_issue` - Create new issue with labels
  - `update_issue` - Modify existing issue
  - `add_comment` - Add comments to issues
  - `get_labels` - Fetch org + repo label taxonomy
  - `suggest_labels` - Analyze context and suggest appropriate labels
- Write integration tests against actual Gitea instance
- Create `.mcp.json` configuration template

**Success Criteria:**
- All tools pass integration tests
- Label suggestion correctly identifies Type/Refactor for architectural changes
- Error handling for network failures and API rate limits
- Environment variable configuration works

### 1.2 Label Taxonomy System

**Deliverable:** Label reference with sync capability

**Tasks:**
- Create `skills/label-taxonomy/` directory structure
- Port `gitea-labels-reference.md` to plugin
- Document exclusive vs non-exclusive label rules
- Build label suggestion logic:
  - Type detection (Bug, Feature, Refactor, etc.)
  - Component inference from file paths
  - Tech stack detection from extensions
  - Source/Priority/Risk heuristics
- Implement `/labels-sync` command
- Create agent workflow for reviewing label changes

**Success Criteria:**
- Local reference matches current Gitea state
- Suggestion engine correctly identifies Type/Refactor for architecture work
- Sync command shows clear diffs
- Agent discusses impact of label changes before applying

**Label Categories (43 total):**
- Organization (27): Agent/2, Complexity/3, Efforts/5, Priority/4, Risk/3, Source/4, Type/6 (includes Refactor)
- Repository (16): Component/9, Tech/7 (includes Tech/AI)

### 1.3 Plugin Structure

**Deliverable:** Complete plugin directory with manifest

**Tasks:**
- Create `.claude-plugin/plugin.json` with metadata
- Set up all required directories
- Configure plugin dependencies
- Write README with installation instructions
- Create example `.env` template
- Add LICENSE and CHANGELOG

**Directory Structure:**
```
projman/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── sprint-plan.md
│   ├── sprint-start.md
│   ├── sprint-status.md
│   ├── sprint-close.md
│   ├── issue-create.md
│   ├── issue-list.md
│   ├── labels-sync.md
│   └── deploy-check.md
├── agents/
│   ├── planner.md
│   ├── orchestrator.md
│   └── executor.md
├── skills/
│   ├── gitea-api/
│   │   └── SKILL.md
│   ├── label-taxonomy/
│   │   ├── SKILL.md
│   │   └── labels-reference.md
│   ├── lessons-learned/
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
│   ├── src/
│   │   ├── gitea-server.ts
│   │   ├── label-suggester.ts
│   │   ├── types.ts
│   │   └── utils.ts
│   └── tests/
│       └── integration.test.ts
├── README.md
├── LICENSE
└── CHANGELOG.md
```

**Success Criteria:**
- Plugin manifest valid
- All directories in place
- Documentation complete
- Installable via local marketplace

---

## Phase 2: Agent Development (projman)

### 2.1 Planner Agent

**Deliverable:** Planning agent for architecture and sprint setup

**Tasks:**
- Port `sprint-workflow.md` logic to agent prompt
- Integrate branch detection (Development vs Development-Claude modes)
- Add label suggestion workflow
- Implement sprint document generation
- Connect to `gitea.create_issue` tool
- Add Gitea issue export for Development-Claude mode
- Implement lessons learned search at planning start

**Agent Personality:**
- Asks clarifying questions upfront
- Thinks through edge cases and risks
- Documents architectural decisions
- Never rushes to implementation
- References past lessons learned

**Tools Used:**
- `gitea.create_issue` (Development mode only)
- `gitea.get_labels` (for validation)
- `gitea.suggest_labels` (for new issues)
- `gitea.list_issues` (to check for duplicates)

**Success Criteria:**
- Generates complete sprint planning documents
- Creates properly labeled Gitea issues
- Exports issue data in Development-Claude mode
- Finds and references relevant past lessons
- Suggests appropriate labels (including Type/Refactor when applicable)

### 2.2 Orchestrator Agent

**Deliverable:** Sprint execution coordinator

**Tasks:**
- Port `sprint-orchestrator.md` logic to agent prompt
- Implement progress tracking
- Create execution prompt generation
- Add Git operation handling (commit, merge, cleanup)
- Build dependency coordination logic
- Integrate with lessons learned capture

**Agent Personality:**
- Concise and action-oriented
- Tracks details meticulously
- Signals next steps clearly
- Never writes application code
- Coordinates between tasks

**Tools Used:**
- `gitea.get_issue` (read sprint details)
- `gitea.update_issue` (update progress)
- `gitea.add_comment` (log milestones)

**Success Criteria:**
- Generates lean execution prompts (not full docs)
- Tracks sprint progress accurately
- Manages branch operations safely
- Coordinates task dependencies
- Signals clear next steps

### 2.3 Executor Agent

**Deliverable:** Implementation specialist

**Tasks:**
- Port `sprint-executor.md` logic to agent prompt
- Implement feature development workflow
- Add completion report generation
- Integrate with orchestrator handoff

**Agent Personality:**
- Implementation-focused
- Follows specifications precisely
- Tests as builds
- Reports blockers immediately
- Generates detailed completion reports

**Tools Used:**
- Standard Claude Code tools (no Gitea access)

**Success Criteria:**
- Implements features according to prompts
- Writes clean, tested code
- Follows architectural decisions from planning
- Generates useful completion reports
- Surfaces blockers early

---

## Phase 3: Commands (projman)

### 3.1 Sprint Lifecycle Commands

**Deliverable:** Core sprint management commands

**Tasks:**
- `/sprint-plan` - Invokes planner agent
- `/sprint-start` - Invokes orchestrator agent
- `/sprint-status` - Shows current progress
- `/sprint-close` - Captures lessons learned

**Command Behaviors:**
- Detect current branch and adjust permissions
- Pass context to appropriate agents
- Handle mode restrictions (Development vs Development-Claude)
- Provide clear user feedback

**Success Criteria:**
- Commands invoke correct agents
- Branch detection works reliably
- User workflow feels natural
- Mode restrictions enforced

### 3.2 Issue Management Commands

**Deliverable:** Gitea issue interaction commands

**Tasks:**
- `/issue-create` - Quick issue creation with label suggestions
- `/issue-list` - Filter and display issues
- `/labels-sync` - Sync label taxonomy from Gitea

**Success Criteria:**
- Quick issue creation with smart defaults
- Filtering works for sprint planning
- Label sync includes impact discussion
- Type/Refactor appears in suggestions for architecture work

### 3.3 Deployment Commands

**Deliverable:** Environment validation commands

**Tasks:**
- `/deploy-check` - Validate staging/production environment
- Branch-aware behavior for deployment contexts

**Success Criteria:**
- Detects configuration issues
- Creates issues on code problems (staging/prod modes)
- Handles .env modifications appropriately

---

## Phase 4: Lessons Learned System (projman)

### 4.1 Wiki Structure

**Deliverable:** Markdown-based lessons learned repository

**Tasks:**
- Create `docs/lessons-learned/` directory structure
- Build sprint lesson template
- Create pattern-based categorization
- Implement searchable index

**Directory Structure:**
```
docs/lessons-learned/
├── INDEX.md                           # Master index with tags
├── sprints/
│   ├── sprint-01-auth-refactor.md
│   ├── sprint-02-deployment.md
│   └── sprint-N-[name].md
├── patterns/
│   ├── claude-infinite-loops.md       # Recurring Claude Code issues
│   ├── deployment-gotchas.md          # Deployment problems
│   ├── architecture-mistakes.md       # Architecture decisions
│   └── integration-issues.md          # Third-party API problems
└── templates/
    └── lesson-template.md
```

**Lesson Template:**
```markdown
# Lesson: [Short Title]

**Sprint:** [Sprint number/name]
**Date:** [YYYY-MM-DD]
**Category:** [Architecture/Deployment/Claude/Integration/etc.]
**Impact:** [High/Medium/Low]

## What Happened
[Describe the issue/situation]

## Root Cause
[Why it happened]

## What We Did
[How it was resolved]

## Prevention
[How to avoid this in the future]

## Keywords
[Tags for searchability: deployment, auth, infinite-loop, etc.]
```

**Success Criteria:**
- Easy to create new lessons
- Searchable by keyword/category
- Git tracked and versioned
- Referenced by planner agent

### 4.2 Agent Integration

**Deliverable:** Automated lesson capture and retrieval

**Tasks:**
- Orchestrator prompts for lessons at sprint close
- Planner searches lessons at sprint start
- INDEX.md maintained automatically
- Pattern categorization suggests categories

**Sprint Close Flow:**
```
Orchestrator: "Sprint completed ✅

Let's capture lessons learned:

1. What went wrong that we should avoid next time?
2. What decisions worked really well?
3. Were there any Claude Code issues that caused loops/blocks?
4. Any architectural insights for similar future work?

[User provides answers]

I'll create:
- docs/lessons-learned/sprints/sprint-16-intuit-refactor.md
- Update INDEX.md with searchable tags
- File under patterns/architecture-mistakes.md if applicable
"
```

**Sprint Start Flow:**
```
Planner: "Let me search past lessons learned..."

[Searches INDEX.md for keywords: 'intuit', 'api', 'service', 'refactor']

📚 Found 3 relevant lessons:
- sprint-08: Service boundary decisions (Type/Refactor)
- sprint-12: Claude Code loop on validation logic
- sprint-14: API rate limiting with third-party services

I'll reference these in the planning document.
```

**Success Criteria:**
- Lessons captured at every sprint close
- Relevant lessons surfaced at sprint start
- INDEX stays current
- Patterns emerge and get documented

### 4.3 Retroactive Lesson Capture

**Deliverable:** Document past 15 sprints' lessons

**Tasks:**
- Create command `/lessons-backfill` for guided retrospective
- Agent interviews user about past sprints
- Focuses on repeated issues (Claude infinite loops, etc.)
- Prioritizes high-impact lessons

**Interview Process:**
```
Orchestrator: "Let's capture lessons from past sprints.

I'll focus on patterns that repeated across sprints.

You mentioned Claude Code infinite loops on similar issues 2-3 times.
Can you describe:
1. What type of code triggered the loops?
2. What was Claude trying to do?
3. How did you eventually resolve it?
4. Which sprints did this happen in?

[Captures pattern lesson, not individual sprint lessons]
"
```

**Success Criteria:**
- Most impactful past lessons documented
- Patterns identified and categorized
- No need to document every sprint detail
- Focus on preventable repetitions

---

## Phase 5: Hooks and Automation (projman)

### 5.1 Documentation Sync Hook

**Deliverable:** Automatic doc updates after task completion

**Tasks:**
- Port `post-task-doc-sync.md` logic to hook
- Trigger on task completion
- Update sprint documentation
- Maintain change logs

**Hook Configuration:**
```json
{
  "name": "post-task-sync",
  "event": "task_completed",
  "action": "run_command",
  "command": "update-sprint-docs",
  "description": "Sync sprint documentation after task completion"
}
```

**Success Criteria:**
- Docs stay current automatically
- No manual sync needed
- Change history preserved

### 5.2 Staging/Production Guards

**Deliverable:** Prevent accidental code changes on protected branches

**Tasks:**
- Detect file changes on staging/main branches
- Warn if attempting code modifications
- Suggest creating issue instead

**Hook Configuration:**
```json
{
  "name": "staging-code-guard",
  "event": "file_changed",
  "filter": {
    "branch": "staging",
    "paths": ["src/**/*.py", "src/**/*.js", "backend/**/*", "frontend/**/*"]
  },
  "action": "warn",
  "message": "⚠️ Code changes on staging branch. Use /issue-create to document needed fixes."
},
{
  "name": "production-code-guard",
  "event": "file_changed",
  "filter": {
    "branch": "main",
    "paths": ["src/**/*.py", "src/**/*.js", "backend/**/*", "frontend/**/*"]
  },
  "action": "block",
  "message": "🚫 Code changes blocked on production. Use /issue-create for incidents."
}
```

**Success Criteria:**
- Prevents accidental code changes
- Guides user to correct workflow
- Allows .env modifications as needed

### 5.3 Issue Status Automation

**Deliverable:** Auto-update issues on branch merge

**Tasks:**
- Detect sprint branch merges
- Update corresponding Gitea issue status
- Add completion comment with branch info

**Success Criteria:**
- Issues auto-close on merge
- Audit trail maintained
- Manual override available

---

## Phase 6: Local Testing (projman)

### 6.1 Local Marketplace Setup

**Deliverable:** Test marketplace for plugin development

**Tasks:**
- Create local marketplace directory structure
- Write marketplace.json manifest
- Configure plugin source path
- Add marketplace to Claude Code

**Structure:**
```
~/projman-dev-marketplace/
├── .claude-plugin/
│   └── marketplace.json
└── projman/                    # Symlink to plugin directory
    └── [plugin contents]
```

**Success Criteria:**
- Plugin installs locally
- Can iterate and reinstall
- Changes reflect immediately

### 6.2 Integration Testing

**Deliverable:** Validated plugin in CuisineFlow repo

**Tasks:**
- Install plugin in CuisineFlow project
- Test all commands with real Gitea instance
- Run through complete sprint cycle
- Validate branch detection on all branch types
- Test label suggestions with Type/Refactor
- Capture and review lessons learned

**Test Scenarios:**
- Plan sprint with `/sprint-plan` on development branch
- Create issue with Type/Refactor label
- Start sprint with `/sprint-start`
- Execute tasks in separate chat
- Close sprint with `/sprint-close` and capture lessons
- Sync labels with `/labels-sync`
- Test staging mode restrictions
- Test production incident reporting

**Success Criteria:**
- All commands work as expected
- Branch detection reliable
- Label suggestions accurate (including Refactor)
- Lessons learned capture works
- No major regressions vs current system

### 6.3 Real-World Validation

**Deliverable:** Plugin used in actual sprint (Intuit refactor)

**Tasks:**
- Use plugin for Intuit engine extraction sprint
- Document friction points
- Collect improvement ideas
- Measure workflow efficiency vs current system

**Metrics to Track:**
- Time to create sprint (planning to issue creation)
- Number of manual steps eliminated
- Lessons learned capture rate
- Label accuracy on created issues

**Success Criteria:**
- Plugin performs equal or better than current workflow
- User finds it helpful, not hindering
- Captures lessons that would have been missed
- Identifies areas for improvement

---

## Phase 7: Skills Refinement (projman)

### 7.1 Extract Supporting Knowledge

**Deliverable:** Clean, reusable skills

**Tasks:**
- Extract Gitea API patterns → `skills/gitea-api/SKILL.md`
- Extract PM best practices → `skills/agile-pm/SKILL.md`
- Extract Git workflows → `skills/branch-strategy/SKILL.md`
- Extract label taxonomy usage → `skills/label-taxonomy/SKILL.md`
- Extract lessons learned patterns → `skills/lessons-learned/SKILL.md`

**Each Skill Contains:**
- When to use this knowledge
- Common patterns and anti-patterns
- Examples from past sprints
- Tool usage guidelines
- Reference to full documentation

**Success Criteria:**
- Skills are concise (< 200 lines)
- Agents reference skills appropriately
- Knowledge is reusable across agents
- Reduced token usage per interaction

### 7.2 Agent Prompt Optimization

**Deliverable:** Lean agent prompts that reference skills

**Tasks:**
- Remove duplicated knowledge from agent prompts
- Add skill references where appropriate
- Optimize for token efficiency
- Maintain agent personality clarity

**Example Before:**
```markdown
# Planner Agent
[500 lines including all label rules, Git workflow, PM practices]
```

**Example After:**
```markdown
# Planner Agent

**Skills:** label-taxonomy, agile-pm, branch-strategy, gitea-api

**Core Personality:**
- Ask clarifying questions upfront
- Think through edge cases
- Document risks explicitly
[150 lines focused on agent-specific behavior]
```

**Success Criteria:**
- Agent prompts < 300 lines each
- Skills invoked automatically when relevant
- Token usage reduced 30-40%
- No loss in agent effectiveness

---

## Phase 8: Documentation and Distribution (projman)

### 8.1 User Documentation

**Deliverable:** Complete usage guide

**Tasks:**
- Write README with:
  - Installation instructions
  - Configuration guide (Gitea credentials, .env setup)
  - Command reference with examples
  - Agent personality descriptions
  - Branch-aware behavior explanation
  - Label taxonomy overview
  - Lessons learned workflow
- Create CONTRIBUTING.md for future enhancements
- Write troubleshooting guide
- Add FAQ section

**Success Criteria:**
- New user can install and configure in < 15 minutes
- All commands documented with examples
- Common issues covered
- Clear explanation of Type/Refactor and other labels

### 8.2 Plugin Marketplace Publication

**Deliverable:** Public plugin in marketplace

**Tasks:**
- Clean up code and documentation
- Add comprehensive testing
- Create example configurations
- Write clear changelog
- Publish to plugin marketplace
- Announce in community

**Success Criteria:**
- Plugin discoverable in marketplace
- Installation is one command
- Example .env template provided
- Positive feedback from early adopters

---

## Phase 9: PMO Plugin Foundation (projman-pmo)

### 9.1 Multi-Project Requirements Analysis

**Deliverable:** Specification for PMO plugin

**Tasks:**
- Document current cross-project coordination workflow
- Map project dependencies:
  - CuisineFlow → CuisineFlow-Site (demo sync)
  - CuisineFlow → Intuit Engine Service (API aggregation)
  - Customer VPS deployments (IP restrictions)
- Identify coordination pain points
- Define success metrics for PMO plugin

**Research Questions:**
- How do you currently track CuisineFlow-Site demo sync?
- What triggers Intuit engine updates?
- How do you coordinate customer VPS deployments?
- Where do multi-project conflicts happen?
- What decisions require cross-project visibility?

**Success Criteria:**
- Clear understanding of multi-project workflows
- Pain points documented
- PMO plugin scope defined
- Not duplicating single-repo functionality

### 9.2 MCP Server Extension

**Deliverable:** Multi-repo query capabilities

**Tasks:**
- Extend Gitea MCP server for multi-repo operations
- Add tools:
  - `list_repos` - Get all organization repos
  - `aggregate_issues` - Fetch issues across repos
  - `check_dependencies` - Analyze cross-repo dependencies
  - `get_deployment_status` - Check deployment states
- Build dependency graph visualization data

**Success Criteria:**
- Can query multiple repos efficiently
- Dependency analysis works
- Aggregated views make sense
- Performance acceptable for 3-5 repos

### 9.3 PMO Agent Design

**Deliverable:** Multi-project coordinator agent

**Tasks:**
- Define PMO agent personality
- Design cross-project prioritization logic
- Create resource allocation algorithms
- Build conflict detection rules
- Design dependency tracking system

**PMO Agent Personality:**
- Strategic thinker across projects
- Identifies bottlenecks and conflicts
- Balances competing priorities
- Maintains company-wide view
- Delegates to project-level agents

**Success Criteria:**
- Clear separation from projman agents
- Valuable for multi-project scenarios
- Doesn't micromanage single projects
- Integrates with projman seamlessly

---

## Phase 10: PMO Plugin Development (projman-pmo)

### 10.1 Cross-Project Commands

**Deliverable:** PMO-specific commands

**Tasks:**
- `/pmo-status` - View all projects status
- `/pmo-priorities` - Review and adjust priorities
- `/pmo-dependencies` - Visualize cross-project dependencies
- `/pmo-resources` - Track resource allocation
- `/pmo-sync` - Coordinate dependent deployments

**Success Criteria:**
- Commands provide multi-project insight
- Integration with projman plugins
- Don't duplicate single-project functionality
- Actually useful for coordination

### 10.2 Dependency Management

**Deliverable:** Track and visualize project dependencies

**Tasks:**
- Build dependency declaration format
- Create dependency graph visualization
- Implement impact analysis (what breaks if X changes)
- Add deployment coordination logic
- Handle version pinning across projects

**Example Dependencies:**
```yaml
# In CuisineFlow-Site
dependencies:
  - repo: cuisineflow
    type: demo-sync
    constraint: "same-version"
    trigger: "on-release"
  
  - repo: intuit-engine
    type: api-provider
    constraint: "stable-api"
    trigger: "on-breaking-change"
```

**Success Criteria:**
- Dependencies clearly documented
- Impact analysis accurate
- Deployment coordination works
- Version conflicts detected early

### 10.3 Resource Tracking

**Deliverable:** Cross-project resource visibility

**Tasks:**
- Track which projects are active
- Identify resource conflicts
- Suggest priority adjustments
- Maintain project roadmaps
- Coordinate customer deployment schedules

**Success Criteria:**
- Clear view of where effort is going
- Conflicts surfaced early
- Priorities aligned with company strategy
- Customer deployment schedule respected

---

## Phase 11: PMO Plugin Testing (projman-pmo)

### 11.1 Multi-Project Scenario Testing

**Deliverable:** Validated PMO plugin

**Tasks:**
- Test with CuisineFlow + CuisineFlow-Site + Intuit Engine
- Simulate deployment coordination scenarios
- Test priority conflict resolution
- Validate dependency tracking
- Test customer deployment scheduling

**Test Scenarios:**
- CuisineFlow release triggers Site demo update
- Intuit engine breaking change impacts CuisineFlow
- Competing priorities across projects
- Customer VPS deployment window coordination
- Resource constraint identification

**Success Criteria:**
- All scenarios handled correctly
- Dependencies respected
- Conflicts detected and surfaced
- Coordination reduces manual overhead

### 11.2 Integration with projman

**Deliverable:** Seamless plugin interoperability

**Tasks:**
- Ensure PMO agent delegates to projman agents
- Test command interoperability
- Validate shared MCP server usage
- Check lessons learned sharing across projects

**Success Criteria:**
- PMO doesn't interfere with single-project work
- Delegation works smoothly
- Shared infrastructure stable
- Cross-project lessons accessible

---

## Phase 12: Production Deployment

### 12.1 Multi-Environment Rollout

**Deliverable:** Plugins deployed across all environments

**Tasks:**
- Deploy to laptop (development)
- Deploy to staging VPS
- Deploy to production VPS
- Configure branch-aware permissions per environment
- Test network connectivity and API access

**Environment Matrix:**
```
| Environment | Branch | projman | projman-pmo | Permissions |
|-------------|--------|---------|-------------|-------------|
| Laptop      | dev/*  | ✅      | ✅          | Full access |
| Laptop      | staging| ✅      | ✅          | Read + issues |
| Laptop      | main   | ✅      | ✅          | Read + incidents |
| VPS Staging | staging| ✅      | ✅          | Read + config |
| VPS Prod    | main   | ✅      | ✅          | Read + emergency config |
```

**Success Criteria:**
- All environments configured correctly
- Branch detection works everywhere
- API credentials secured properly
- Network access validated

### 12.2 Team Onboarding

**Deliverable:** Plugin adoption by team/future collaborators

**Tasks:**
- Create onboarding documentation
- Record walkthrough videos
- Provide example workflows
- Document common pitfalls
- Set up support channel

**Success Criteria:**
- New team member can use plugin in < 30 minutes
- Common questions documented
- Positive user feedback
- Adoption rate high

---

## Success Metrics

### Technical Metrics
- ✅ All integration tests passing
- ✅ Branch detection 100% reliable
- ✅ Label suggestions 85%+ accurate
- ✅ Zero data loss in Gitea operations
- ✅ Performance: Commands respond < 2 seconds

### User Experience Metrics
- ✅ Sprint planning time reduced 40%
- ✅ Manual steps eliminated: 10+ per sprint
- ✅ Lessons learned capture rate: 100% (vs 0% before)
- ✅ Label accuracy on issues: 90%+
- ✅ User satisfaction: "Definitely better than current system"

### Workflow Metrics
- ✅ Complete sprint cycle uses plugin end-to-end
- ✅ No fallback to manual scripts
- ✅ Agent personalities clear and helpful
- ✅ Cross-project coordination improved (PMO plugin)

---

## Critical Path Items

These must be completed in order:

1. **MCP Server** - Nothing works without Gitea integration
2. **Label System** - Required for issue creation
3. **Planner Agent** - Entry point for sprint workflow
4. **Lessons Learned** - Addresses immediate pain
5. **Testing in Real Sprint** - Validates everything
6. **PMO Foundation** - Can't build multi-project without single-project working

---

## Rollback Plan

If plugin causes more problems than it solves:

**Immediate Fallback:**
- Keep existing skills and scripts functional
- Plugin is opt-in, not replacement
- Document issues and iterate

**Criteria for Rollback:**
- Plugin slower than current workflow
- Frequent errors or data loss
- User frustration increases
- Blocks urgent work (like Intuit refactor)

**Progressive Enhancement:**
- Build plugin alongside current system
- Migrate piece by piece
- Keep escape hatches
- Only deprecate scripts when plugin proven

---

## Notes on Type/Refactor Label

**Label Details:**
- **Name:** `Type/Refactor`
- **Level:** Organization (available to all repos)
- **Category:** Type/ (Exclusive - only one Type per issue)
- **Color:** #0052cc (matches other Type labels)
- **Description:** Architectural changes and code restructuring

**Usage in Plugin:**
- Planner agent suggests Type/Refactor for:
  - Service extraction (like Intuit engine)
  - Architecture modifications
  - Code restructuring without feature changes
  - Performance optimizations requiring significant changes
- Label suggestion engine detects refactor keywords:
  - "extract", "refactor", "restructure", "optimize architecture"
  - "service boundary", "microservice", "decouple"
  - "technical debt", "code quality"
- Shows in label sync diffs when fetching from Gitea
- Documented in label taxonomy skill

**Integration Points:**
- MCP server includes Type/Refactor in label enumeration
- Suggestion engine trained on architectural patterns
- Sprint planning templates include refactor considerations
- Lessons learned can tag architectural mistakes for future refactors

---

## End of Implementation Plan

This plan builds two plugins systematically, starting with single-repo project management and expanding to multi-project coordination. Each phase builds on previous phases, with testing and validation throughout.

The plan is execution-ready but flexible - adjust based on real-world feedback and discovered requirements.
