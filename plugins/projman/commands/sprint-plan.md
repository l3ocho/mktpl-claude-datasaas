---
description: Start sprint planning with AI-guided architecture analysis and issue creation
---

# Sprint Planning

You are initiating sprint planning. The planner agent will guide you through architecture analysis, ask clarifying questions, and help create well-structured Gitea issues with appropriate labels.

## CRITICAL: Pre-Planning Validations

**BEFORE PLANNING**, the planner agent performs mandatory checks:

### 1. Branch Detection

```bash
git branch --show-current
```

**Branch Requirements:**
- **Development branches** (`development`, `develop`, `feat/*`, `dev/*`): Full planning capabilities
- **Staging branches** (`staging`, `stage/*`): Can create issues to document needed changes, but cannot modify code
- **Production branches** (`main`, `master`, `prod/*`): READ-ONLY - no planning allowed

If you are on a production or staging branch, you MUST stop and ask the user to switch to a development branch.

### 2. Repository Organization Check

Use `validate_repo_org` MCP tool to verify the repository belongs to an organization.

**If NOT an organization repository:**
```
REPOSITORY VALIDATION FAILED

This plugin requires the repository to belong to an organization, not a user.
Please transfer or create the repository under that organization.
```

### 3. Label Taxonomy Validation

Verify all required labels exist using `get_labels`:

**Required label categories:**
- Type/* (Bug, Feature, Refactor, Documentation, Test, Chore)
- Priority/* (Low, Medium, High, Critical)
- Complexity/* (Simple, Medium, Complex)
- Efforts/* (XS, S, M, L, XL)

**If labels are missing:** Use `create_label` to create them.

### 4. Input Source Detection

The planner supports flexible input sources for sprint planning:

| Source | Detection | Action |
|--------|-----------|--------|
| **Local file** | `docs/changes/*.md` exists | Parse frontmatter, migrate to wiki, delete local |
| **Existing wiki** | `Change VXX.X.X: Proposal` exists | Use as-is, create new implementation page |
| **Conversation** | Neither file nor wiki exists | Create wiki from discussion context |

**Input File Format** (if using local file):
```yaml
---
version: "4.1.0"        # or "sprint-17" for internal work
title: "Feature Name"
plugin: plugin-name     # optional
type: feature           # feature | bugfix | refactor | infra
---

# Feature Description
[Free-form content...]
```

**Detection Logic:**
1. Check for `docs/changes/*.md` files
2. Check for existing wiki proposal matching version
3. If neither found, use conversation context
4. If ambiguous, ask user which input to use

## Planning Workflow

The planner agent will:

1. **Understand Sprint Goals**
   - Ask clarifying questions about the sprint objectives
   - Understand scope, priorities, and constraints
   - Never rush - take time to understand requirements fully

2. **Detect Input Source**
   - Check for `docs/changes/*.md` files
   - Check for existing wiki proposal by version
   - If neither: use conversation context
   - Ask user if multiple sources found

3. **Search Relevant Lessons Learned**
   - Use the `search_lessons` MCP tool to find past experiences
   - Search by keywords and tags relevant to the sprint work
   - Review patterns and preventable mistakes from previous sprints

4. **Create/Update Wiki Proposal**
   - If local file: migrate content to wiki, create proposal page
   - If conversation: create proposal from discussion
   - If existing wiki: skip creation, use as-is
   - **Page naming:** `Change VXX.X.X: Proposal` or `Change Sprint-NN: Proposal`

5. **Create Wiki Implementation Page**
   - Create `Change VXX.X.X: Proposal (Implementation N)`
   - Include tags: Type, Version, Status=In Progress, Date, Origin
   - Update proposal page with link to this implementation
   - This page tracks THIS sprint's work on the proposal

6. **Architecture Analysis**
   - Think through technical approach and edge cases
   - Identify architectural decisions needed
   - Consider dependencies and integration points
   - Review existing codebase architecture

7. **Create Gitea Issues**
   - Use the `create_issue` MCP tool for each planned task
   - Apply appropriate labels using `suggest_labels` tool
   - **Issue Title Format (MANDATORY):** `[Sprint XX] <type>: <description>`
   - **Include wiki reference:** `Implementation: [Change VXX.X.X (Impl N)](wiki-link)`
   - Include acceptance criteria and technical notes

8. **Set Up Dependencies**
   - Use `create_issue_dependency` to establish task dependencies
   - This enables parallel execution planning

9. **Create or Select Milestone**
   - Use `create_milestone` to group sprint issues
   - Assign issues to the milestone

10. **Cleanup & Summary**
    - Delete local input file (wiki is now source of truth)
    - Summarize architectural decisions
    - List created issues with labels
    - Document dependency graph
    - Provide sprint overview with wiki links

11. **Request Sprint Approval**
    - Present approval request with scope summary
    - Capture explicit user approval
    - Record approval in milestone description
    - Approval scopes what sprint-start can execute

## Sprint Approval (MANDATORY)

**Planning DOES NOT equal execution permission.**

After creating issues, the planner MUST request explicit approval:

```
Sprint 17 Planning Complete
===========================

Created Issues:
- #45: [Sprint 17] feat: JWT token generation
- #46: [Sprint 17] feat: Login endpoint
- #47: [Sprint 17] test: Auth tests

Execution Scope:
- Branches: feat/45-*, feat/46-*, feat/47-*
- Files: auth/*, api/routes/auth.py, tests/test_auth*
- Dependencies: PyJWT, python-jose

⚠️ APPROVAL REQUIRED

Do you approve this sprint for execution?
This grants permission for agents to:
- Create and modify files in the listed scope
- Create branches with the listed prefixes
- Install listed dependencies

Type "approve sprint 17" to authorize execution.
```

**On Approval:**
1. Record approval in milestone description
2. Note timestamp and scope
3. Sprint-start will verify approval exists

**Approval Record Format:**
```markdown
## Sprint Approval
**Approved:** 2026-01-28 14:30
**Approver:** User
**Scope:**
- Branches: feat/45-*, feat/46-*, feat/47-*
- Files: auth/*, api/routes/auth.py, tests/test_auth*
```

## Issue Title Format (MANDATORY)

```
[Sprint XX] <type>: <description>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring
- `docs` - Documentation
- `test` - Test additions/changes
- `chore` - Maintenance tasks

**Examples:**
- `[Sprint 17] feat: Add user email validation`
- `[Sprint 17] fix: Resolve login timeout issue`
- `[Sprint 18] refactor: Extract authentication module`

## Task Sizing Rules (MANDATORY)

**CRITICAL: Tasks sized L or XL MUST be broken down into smaller tasks.**

| Effort | Files | Checklist Items | Max Tool Calls | Agent Scope |
|--------|-------|-----------------|----------------|-------------|
| **XS** | 1 file | 0-2 items | ~30 | Single function/fix |
| **S** | 1 file | 2-4 items | ~50 | Single file feature |
| **M** | 2-3 files | 4-6 items | ~80 | Multi-file feature |
| **L** | MUST BREAK DOWN | - | - | Too large for one agent |
| **XL** | MUST BREAK DOWN | - | - | Way too large |

**Why This Matters:**
- Agents running 400+ tool calls take 1+ hour, with no visibility
- Large tasks lack clear completion criteria
- Debugging failures is extremely difficult
- Small tasks enable parallel execution

**Scoping Checklist:**
1. Can this be completed in one file? → XS or S
2. Does it touch 2-3 files? → M (maximum for single task)
3. Does it touch 4+ files? → MUST break down
4. Would you estimate 50+ tool calls? → MUST break down
5. Does it require complex decision-making mid-task? → MUST break down

**Example Breakdown:**

**BAD (L - too broad):**
```
[Sprint 3] feat: Implement schema diff detection hook
Labels: Efforts/L
- Hook skeleton
- Pattern detection for DROP/ALTER/RENAME
- Warning output formatting
- Integration with hooks.json
```

**GOOD (broken into S tasks):**
```
[Sprint 3] feat: Create schema-diff-check.sh hook skeleton
Labels: Efforts/S
- [ ] Create hook file with standard header
- [ ] Add file type detection for SQL/migrations
- [ ] Exit 0 (non-blocking)

[Sprint 3] feat: Add DROP/ALTER pattern detection
Labels: Efforts/S
- [ ] Detect DROP COLUMN/TABLE/INDEX
- [ ] Detect ALTER TYPE changes
- [ ] Detect RENAME operations

[Sprint 3] feat: Add warning output formatting
Labels: Efforts/S
- [ ] Format breaking change warnings
- [ ] Add hook prefix to output
- [ ] Test output visibility

[Sprint 3] chore: Register hook in hooks.json
Labels: Efforts/XS
- [ ] Add PostToolUse:Edit hook entry
- [ ] Test hook triggers on SQL edits
```

**The planner MUST refuse to create L/XL tasks without breakdown.**

## MCP Tools Available

**Gitea Tools:**
- `list_issues` - Review existing issues
- `get_issue` - Get detailed issue information
- `create_issue` - Create new issue with labels
- `update_issue` - Update issue
- `get_labels` - Fetch current label taxonomy
- `suggest_labels` - Get intelligent label suggestions based on context
- `create_label` - Create missing labels
- `validate_repo_org` - Check if repo is under organization

**Milestone Tools:**
- `list_milestones` - List milestones
- `create_milestone` - Create milestone
- `update_milestone` - Update milestone

**Dependency Tools:**
- `create_issue_dependency` - Create dependency between issues
- `list_issue_dependencies` - List dependencies for an issue
- `get_execution_order` - Get parallel execution batches

**Lessons Learned Tools (Gitea Wiki):**
- `search_lessons` - Search lessons learned from previous sprints
- `list_wiki_pages` - List wiki pages
- `get_wiki_page` - Fetch specific documentation page
- `create_wiki_page` - Create new wiki page (proposals, implementations)
- `update_wiki_page` - Update wiki page content

## Label Taxonomy

The system uses a dynamic 44-label taxonomy (28 org + 16 repo). Always use the `suggest_labels` tool to get appropriate labels based on the issue context.

**Key Label Categories:**
- **Type/***: Bug, Feature, Refactor, Documentation, Test, Chore
- **Priority/***: Low, Medium, High, Critical
- **Complexity/***: Simple, Medium, Complex
- **Efforts/***: XS, S, M, L, XL
- **Component/***: Backend, Frontend, API, Database, Auth, Deploy, Testing, Docs, Infra
- **Tech/***: Python, JavaScript, Docker, PostgreSQL, Redis, Vue, FastAPI

## Planner Personality

The planner agent is thoughtful and methodical:
- Asks clarifying questions before making assumptions
- Thinks through edge cases and architectural implications
- Never rushes planning - quality over speed
- References lessons learned proactively
- Suggests appropriate labels based on context
- Creates well-structured, detailed issues

## Example Planning Session

```
User: I want to plan a sprint for user authentication
Planner: Great! Let me first run pre-planning validations...

[Checks branch, repo org, labels]
All validations passed.

[Checks for input sources]
Found: docs/changes/v1.2.0-user-authentication.md

I'll use this file as the planning input. Let me ask a few questions:

1. What authentication method are you planning? (JWT, OAuth, session-based?)
2. Are there any specific security requirements or compliance needs?
3. Should this integrate with existing user management?

[Uses search_lessons to find past authentication work]

Based on previous experience, I found these relevant lessons:
- Sprint 12: JWT token expiration handling edge cases
- Sprint 8: OAuth integration pitfalls with third-party providers

[Creates wiki proposal and implementation pages]
✓ Created: "Change V1.2.0: Proposal" (wiki)
✓ Created: "Change V1.2.0: Proposal (Implementation 1)" (wiki)
✓ Deleted: docs/changes/v1.2.0-user-authentication.md (migrated to wiki)

Now, let me analyze the architecture and create issues...

[Creates issues with wiki references]

Created 5 issues for the authentication sprint:
- Issue #45: [Sprint 17] feat: Implement JWT token generation
  Labels: Type/Feature, Priority/High, Component/Auth, Tech/Python
  Implementation: [Change V1.2.0 (Impl 1)](wiki-link)

- Issue #46: [Sprint 17] feat: Build user login endpoint
  Labels: Type/Feature, Priority/High, Component/API, Tech/FastAPI
  Implementation: [Change V1.2.0 (Impl 1)](wiki-link)

Dependency Graph:
#45 -> #46 -> #47
       |
       v
      #48

Milestone: Sprint 17 - User Authentication (Due: 2025-02-01)
Wiki: https://gitea.example.com/org/repo/wiki/Change-V1.2.0%3A-Proposal
```

## Getting Started

Invoke the planner agent by providing your sprint goals. The agent will guide you through the planning process.

**Input Options:**
1. Create `docs/changes/vX.Y.Z-feature-name.md` with frontmatter before running
2. Create wiki proposal page manually, then run `/sprint-plan`
3. Just start a conversation - the planner will capture context and create wiki pages

**Example:**
> "I want to plan a sprint for extracting the Intuit Engine service from the monolith"

The planner will then:
1. Run pre-planning validations
2. Detect input source (file, wiki, or conversation)
3. Ask clarifying questions
4. Search lessons learned
5. Create wiki proposal and implementation pages
6. Create issues with wiki references
7. Set up dependencies
8. Create milestone
9. Cleanup and generate planning summary
