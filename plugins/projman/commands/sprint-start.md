---
description: Begin sprint execution with relevant lessons learned from previous sprints
---

# Start Sprint Execution

You are initiating sprint execution. The orchestrator agent will coordinate the work, analyze dependencies for parallel execution, search for relevant lessons learned, and guide you through the implementation process.

## Sprint Approval Verification

**CRITICAL: Sprint must be approved before execution.**

The orchestrator checks for approval in the milestone description:

```
get_milestone(milestone_id=17)
→ Check description for "## Sprint Approval" section
```

**If Approval Missing:**
```
⚠️ SPRINT NOT APPROVED

Sprint 17 has not been approved for execution.
The milestone description does not contain an approval record.

Please run /sprint-plan to:
1. Review the sprint scope
2. Approve the execution plan

Then run /sprint-start again.
```

**If Approval Found:**
```
✓ Sprint Approval Verified
  Approved: 2026-01-28 14:30
  Scope:
    Branches: feat/45-*, feat/46-*, feat/47-*
    Files: auth/*, api/routes/auth.py, tests/test_auth*

Proceeding with execution within approved scope...
```

**Scope Enforcement:**
- Agents can ONLY create branches matching approved patterns
- Agents can ONLY modify files within approved paths
- Operations outside scope require re-approval via `/sprint-plan`

## Branch Detection

**CRITICAL:** Before proceeding, check the current git branch:

```bash
git branch --show-current
```

**Branch Requirements:**
- **Development branches** (`development`, `develop`, `feat/*`, `dev/*`): Full execution capabilities
- **Staging branches** (`staging`, `stage/*`): Can create issues to document bugs, but cannot modify code
- **Production branches** (`main`, `master`, `prod/*`): READ-ONLY - no execution allowed

If you are on a production or staging branch, you MUST stop and ask the user to switch to a development branch.

## Sprint Start Workflow

The orchestrator agent will:

1. **Verify Sprint Approval**
   - Check milestone description for `## Sprint Approval` section
   - If no approval found, STOP and direct user to `/sprint-plan`
   - If approval found, extract scope (branches, files)
   - Agents operate ONLY within approved scope

2. **Detect Checkpoints (Resume Support)**
   - Check each open issue for `## Checkpoint` comments
   - If checkpoint found, offer to resume from that point
   - Resume preserves: branch, completed work, pending steps

3. **Fetch Sprint Issues**
   - Use `list_issues` to fetch open issues for the sprint
   - Identify priorities based on labels (Priority/Critical, Priority/High, etc.)

2. **Analyze Dependencies and Plan Parallel Execution**
   - Use `get_execution_order` to build dependency graph
   - Identify batches that can be executed in parallel
   - Present parallel execution plan

3. **Search Relevant Lessons Learned**
   - Use `search_lessons` to find experiences from past sprints
   - Search by tags matching the current sprint's technology and components
   - Review patterns, gotchas, and preventable mistakes
   - Present relevant lessons before starting work

4. **Dispatch Tasks (Parallel When Possible)**
   - For independent tasks (same batch), spawn multiple Executor agents in parallel
   - For dependent tasks, execute sequentially
   - Create proper branch for each task

5. **Track Progress**
   - Update issue status as work progresses
   - Use `add_comment` to document progress and blockers
   - Monitor when dependencies are satisfied and new tasks become unblocked

## Parallel Execution Model

The orchestrator analyzes dependencies and groups issues into parallelizable batches:

```
Parallel Execution Batches:
+---------------------------------------------------------------+
| Batch 1 (can start immediately):                               |
|   #45 [Sprint 18] feat: Implement JWT service                  |
|   #48 [Sprint 18] docs: Update API documentation               |
+---------------------------------------------------------------+
| Batch 2 (after batch 1):                                       |
|   #46 [Sprint 18] feat: Build login endpoint (needs #45)       |
|   #49 [Sprint 18] test: Add auth tests (needs #45)             |
+---------------------------------------------------------------+
| Batch 3 (after batch 2):                                       |
|   #47 [Sprint 18] feat: Create login form (needs #46)          |
+---------------------------------------------------------------+
```

**Independent tasks in the same batch run in parallel.**

## File Conflict Prevention (MANDATORY)

**CRITICAL: Before dispatching parallel agents, check for file overlap.**

**Pre-Dispatch Conflict Check:**

1. **Identify target files** for each task in the batch
2. **Check for overlap** - Do any tasks modify the same file?
3. **If overlap detected** - Sequentialize those specific tasks

**Example Conflict Detection:**
```
Batch 1 Analysis:
  #45 - Implement JWT service
        Files: auth/jwt_service.py, auth/__init__.py, tests/test_jwt.py

  #48 - Update API documentation
        Files: docs/api.md, README.md

  Overlap: NONE → Safe to parallelize

Batch 2 Analysis:
  #46 - Build login endpoint
        Files: api/routes/auth.py, auth/__init__.py

  #49 - Add auth tests
        Files: tests/test_auth.py, auth/__init__.py

  Overlap: auth/__init__.py → CONFLICT!
  Action: Sequentialize #46 and #49 (run #46 first)
```

**Conflict Resolution Rules:**

| Conflict Type | Action |
|---------------|--------|
| Same file in checklist | Sequentialize tasks |
| Same directory | Review if safe, usually OK |
| Shared test file | Sequentialize or assign different test files |
| Shared config | Sequentialize |

**Branch Isolation Protocol:**

Even for parallel tasks, each MUST run on its own branch:
```
Task #45 → feat/45-jwt-service (isolated)
Task #48 → feat/48-api-docs (isolated)
```

**Sequential Merge After Completion:**
```
1. Task #45 completes → merge feat/45-jwt-service to development
2. Task #48 completes → merge feat/48-api-docs to development
3. Never merge simultaneously - always sequential to detect conflicts
```

**If Merge Conflict Occurs:**
1. Stop second task
2. Resolve conflict manually or assign to human
3. Resume/restart second task with updated base

## Branch Naming Convention (MANDATORY)

When creating branches for tasks:

- Features: `feat/<issue-number>-<short-description>`
- Bug fixes: `fix/<issue-number>-<short-description>`
- Debugging: `debug/<issue-number>-<short-description>`

**Examples:**
```bash
git checkout -b feat/45-jwt-service
git checkout -b fix/46-login-timeout
git checkout -b debug/47-investigate-memory-leak
```

**Validation:**
- Issue number MUST be present
- Prefix MUST be `feat/`, `fix/`, or `debug/`
- Description should be kebab-case (lowercase, hyphens)

## MCP Tools Available

**Gitea Tools:**
- `list_issues` - Fetch sprint issues (filter by state, labels, milestone)
- `get_issue` - Get detailed issue information
- `update_issue` - Update issue status, assignee, labels
- `add_comment` - Add progress updates or blocker notes

**Dependency Tools:**
- `list_issue_dependencies` - Get dependencies for an issue
- `get_execution_order` - Get parallel execution batches for sprint issues

**Milestone Tools:**
- `list_milestones` - List milestones
- `get_milestone` - Get milestone details

**Lessons Learned Tools (Gitea Wiki):**
- `search_lessons` - Find relevant lessons from past sprints
- `list_wiki_pages` - List project documentation
- `get_wiki_page` - Fetch specific documentation (e.g., architecture decisions)

## Orchestrator Personality

The orchestrator agent is concise and action-oriented:
- Generates lean execution prompts, not lengthy documents
- Tracks details meticulously (no task forgotten)
- Coordinates parallel execution based on dependencies
- Identifies blockers proactively
- Coordinates Git operations (commit, merge, cleanup)
- Updates documentation as work progresses

## Example Sprint Start Session

```
User: /sprint-start
Orchestrator: Starting sprint execution. Let me analyze the sprint...

[Uses list_issues to fetch sprint backlog]

Found 5 open issues for this sprint.

[Uses get_execution_order to analyze dependencies]

Parallel Execution Batches:
+-----------------------------------------------+
| Batch 1 (can start immediately):               |
|   #45 - Implement JWT service                  |
|   #48 - Update API documentation               |
+-----------------------------------------------+
| Batch 2 (after batch 1):                       |
|   #46 - Build login endpoint (needs #45)       |
|   #49 - Add auth tests (needs #45)             |
+-----------------------------------------------+
| Batch 3 (after batch 2):                       |
|   #47 - Create login form (needs #46)          |
+-----------------------------------------------+

[Uses search_lessons to find relevant past experiences]

Relevant lessons learned:
- Sprint 12: "JWT Token Expiration Edge Cases" - Remember to handle token refresh
- Sprint 8: "OAuth Integration Pitfalls" - Test error handling for auth providers

Ready to start? I can dispatch multiple tasks in parallel.

Dispatching Batch 1 (2 tasks in parallel):

Task 1: #45 - Implement JWT service
  Branch: feat/45-jwt-service
  Executor: Starting...

Task 2: #48 - Update API documentation
  Branch: feat/48-api-docs
  Executor: Starting...

Both tasks running in parallel. I'll monitor progress.
```

## Lean Execution Prompts

The orchestrator generates concise prompts (NOT verbose documents):

```
Next Task: #45 - [Sprint 18] feat: Implement JWT token generation

Priority: High | Effort: M (1 day) | Unblocked
Branch: feat/45-jwt-service

Quick Context:
- Create backend service for JWT tokens
- Use HS256 algorithm (decision from planning)
- Include user_id, email, expiration in payload

Key Actions:
1. Create auth/jwt_service.py
2. Implement generate_token(user_id, email)
3. Implement verify_token(token)
4. Add token refresh logic (Sprint 12 lesson!)
5. Write unit tests for generation/validation

Acceptance Criteria:
- Tokens generate successfully
- Token verification works
- Refresh prevents expiration issues
- Tests cover edge cases

Relevant Lessons:
Sprint 12: Handle token refresh explicitly to prevent mid-request expiration

Dependencies: None (can start immediately)
```

## Progress Tracking

As work progresses, the orchestrator updates Gitea:

**Add Progress Comment:**
```
add_comment(issue_number=45, body="JWT generation implemented. Running tests now.")
```

**Update Issue Status:**
```
update_issue(issue_number=45, state="closed")
```

**Document Blockers:**
```
add_comment(issue_number=46, body="BLOCKED: Waiting for #45 to complete (dependency)")
```

**Track Parallel Execution:**
```
Parallel Execution Status:

Batch 1:
  #45 - JWT service - COMPLETED (12:45)
  #48 - API docs - IN PROGRESS (75%)

Batch 2 (now unblocked):
  #46 - Login endpoint - READY TO START
  #49 - Auth tests - READY TO START

#45 completed! #46 and #49 are now unblocked.
Starting #46 while #48 continues...
```

## Checkpoint Resume Support

If a previous session was interrupted (agent stopped, failure, budget exhausted), checkpoints enable resumption.

**Checkpoint Detection:**
The orchestrator scans issue comments for `## Checkpoint` markers containing:
- Branch name
- Last commit hash
- Completed/pending steps
- Files modified

**Resume Flow:**
```
User: /sprint-start

Orchestrator: Checking for checkpoints...

Found checkpoint for #45 (JWT service):
  Branch: feat/45-jwt-service
  Last activity: 2 hours ago
  Progress: 4/7 steps completed
  Pending: Write tests, add refresh, commit

Options:
  1. Resume from checkpoint (recommended)
  2. Start fresh (lose previous work)
  3. Review checkpoint details

User: 1

Orchestrator: Resuming #45 from checkpoint...
  ✓ Branch exists
  ✓ Files match checkpoint
  ✓ Dispatching executor with context

Executor continues from pending steps...
```

**Checkpoint Format:**
Executors save checkpoints after major steps:
```markdown
## Checkpoint
**Branch:** feat/45-jwt-service
**Commit:** abc123
**Phase:** Testing

### Completed Steps
- [x] Step 1
- [x] Step 2

### Pending Steps
- [ ] Step 3
- [ ] Step 4
```

## Getting Started

Simply invoke `/sprint-start` and the orchestrator will:
1. Review your sprint backlog
2. Analyze dependencies and plan parallel execution
3. Search for relevant lessons
4. Dispatch tasks (parallel when possible)
5. Track progress as you work

The orchestrator keeps you focused, maximizes parallelism, and ensures nothing is forgotten.
