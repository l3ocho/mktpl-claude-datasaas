---
description: Begin sprint execution with relevant lessons learned from previous sprints
---

# Start Sprint Execution

You are initiating sprint execution. The orchestrator agent will coordinate the work, analyze dependencies for parallel execution, search for relevant lessons learned, and guide you through the implementation process.

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

1. **Fetch Sprint Issues**
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

## Getting Started

Simply invoke `/sprint-start` and the orchestrator will:
1. Review your sprint backlog
2. Analyze dependencies and plan parallel execution
3. Search for relevant lessons
4. Dispatch tasks (parallel when possible)
5. Track progress as you work

The orchestrator keeps you focused, maximizes parallelism, and ensures nothing is forgotten.
