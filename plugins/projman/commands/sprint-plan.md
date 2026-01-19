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

### 4. docs/changes/ Folder Check

Verify the project has a `docs/changes/` folder for sprint input files.

**If folder does NOT exist:** Prompt user to create it.

**If sprint starts with discussion but no input file:**
- Capture the discussion outputs
- Create a change file: `docs/changes/sprint-XX-description.md`

## Planning Workflow

The planner agent will:

1. **Understand Sprint Goals**
   - Ask clarifying questions about the sprint objectives
   - Understand scope, priorities, and constraints
   - Never rush - take time to understand requirements fully

2. **Search Relevant Lessons Learned**
   - Use the `search_lessons` MCP tool to find past experiences
   - Search by keywords and tags relevant to the sprint work
   - Review patterns and preventable mistakes from previous sprints

3. **Architecture Analysis**
   - Think through technical approach and edge cases
   - Identify architectural decisions needed
   - Consider dependencies and integration points
   - Review existing codebase architecture

4. **Create Gitea Issues**
   - Use the `create_issue` MCP tool for each planned task
   - Apply appropriate labels using `suggest_labels` tool
   - **Issue Title Format (MANDATORY):** `[Sprint XX] <type>: <description>`
   - Include acceptance criteria and technical notes

5. **Set Up Dependencies**
   - Use `create_issue_dependency` to establish task dependencies
   - This enables parallel execution planning

6. **Create or Select Milestone**
   - Use `create_milestone` to group sprint issues
   - Assign issues to the milestone

7. **Generate Planning Document**
   - Summarize architectural decisions
   - List created issues with labels
   - Document dependency graph
   - Provide sprint overview

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

## Task Granularity Guidelines

| Size | Scope | Example |
|------|-------|---------|
| **Small** | 1-2 hours, single file/component | Add validation to one field |
| **Medium** | Half day, multiple files, one feature | Implement new API endpoint |
| **Large** | Should be broken down | Full authentication system |

**If a task is too large, break it down into smaller tasks.**

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

[Checks branch, repo org, labels, docs/changes folder]

All validations passed. Now let me ask a few questions:

1. What authentication method are you planning? (JWT, OAuth, session-based?)
2. Are there any specific security requirements or compliance needs?
3. Should this integrate with existing user management?
4. What's the priority level for this sprint?

Let me also search for relevant lessons learned about authentication...

[Uses search_lessons to find past authentication work]

Based on previous experience, I found these relevant lessons:
- Sprint 12: JWT token expiration handling edge cases
- Sprint 8: OAuth integration pitfalls with third-party providers

Now, let me analyze the architecture...

[Creates issues with appropriate labels and dependencies]

Created 5 issues for the authentication sprint:
- Issue #45: [Sprint 17] feat: Implement JWT token generation
  Labels: Type/Feature, Priority/High, Component/Auth, Tech/Python
  Dependencies: None

- Issue #46: [Sprint 17] feat: Build user login endpoint
  Labels: Type/Feature, Priority/High, Component/API, Tech/FastAPI
  Dependencies: #45

- Issue #47: [Sprint 17] feat: Create user registration form
  Labels: Type/Feature, Priority/Medium, Component/Frontend, Tech/Vue
  Dependencies: #46

Dependency Graph:
#45 -> #46 -> #47
       |
       v
      #48

Milestone: Sprint 17 - User Authentication (Due: 2025-02-01)
```

## Getting Started

Invoke the planner agent by providing your sprint goals. The agent will guide you through the planning process.

**Example:**
> "I want to plan a sprint for extracting the Intuit Engine service from the monolith"

The planner will then:
1. Run pre-planning validations
2. Ask clarifying questions
3. Search lessons learned
4. Create issues with proper naming and labels
5. Set up dependencies
6. Create milestone
7. Generate planning summary
