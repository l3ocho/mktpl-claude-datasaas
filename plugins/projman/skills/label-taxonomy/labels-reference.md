---
name: label-taxonomy
description: Dynamic reference for Gitea label taxonomy (organization + repository labels)
---

# Label Taxonomy Reference

**Status:** ✅ Synced with Gitea
**Last synced:** 2025-11-21 (via automated testing)
**Source:** Gitea (personal-projects/mktpl-claude-datasaas)

## Overview

This skill provides the current label taxonomy used for issue classification in Gitea. Labels are **fetched dynamically** from Gitea and should never be hardcoded.

**Current Taxonomy:** 58 labels (31 organization + 27 repository)

## Organization Labels (31)

Organization-level labels are shared across all repositories in your configured organization.

### Agent (2)
- `Agent/Human` (#0052cc) - Work performed by human developers
- `Agent/Claude` (#6554c0) - Work performed by Claude Code or AI assistants

### Complexity (3)
- `Complexity/Simple` (#c2e0c6) - Straightforward tasks requiring minimal analysis
- `Complexity/Medium` (#fff4ce) - Moderate complexity with some architectural decisions
- `Complexity/Complex` (#ffbdad) - High complexity requiring significant planning and analysis

### Efforts (5)
- `Efforts/XS` (#c2e0c6) - Extra small effort (< 2 hours)
- `Efforts/S` (#d4f1d4) - Small effort (2-4 hours)
- `Efforts/M` (#fff4ce) - Medium effort (4-8 hours / 1 day)
- `Efforts/L` (#ffe0b2) - Large effort (1-3 days)
- `Efforts/XL` (#ffbdad) - Extra large effort (> 3 days)

### Priority (4)
- `Priority/Low` (#d4e157) - Nice to have, can wait
- `Priority/Medium` (#ffeb3b) - Should be done this sprint
- `Priority/High` (#ff9800) - Important, do soon
- `Priority/Critical` (#f44336) - Urgent, blocking other work

### Risk (3)
- `Risk/Low` (#c2e0c6) - Low risk of issues or impact
- `Risk/Medium` (#fff4ce) - Moderate risk, proceed with caution
- `Risk/High` (#ffbdad) - High risk, needs careful planning and testing

### Source (4)
- `Source/Development` (#7cb342) - Issue discovered during development
- `Source/Staging` (#ffb300) - Issue found in staging environment
- `Source/Production` (#e53935) - Issue found in production
- `Source/Customer` (#ab47bc) - Issue reported by customer

### Type (6)
- `Type/Bug` (#d73a4a) - Bug fixes and error corrections
- `Type/Feature` (#0075ca) - New features and enhancements
- `Type/Refactor` (#fbca04) - Code restructuring and architectural changes
- `Type/Documentation` (#0e8a16) - Documentation updates and improvements
- `Type/Test` (#1d76db) - Testing-related work (unit, integration, e2e)
- `Type/Chore` (#fef2c0) - Maintenance, tooling, dependencies, build tasks

### Status (4)
- `Status/In-Progress` (#0052cc) - Work is actively being done on this issue
- `Status/Blocked` (#ff5630) - Blocked by external dependency or issue
- `Status/Failed` (#de350b) - Implementation attempted but failed, needs investigation
- `Status/Deferred` (#6554c0) - Moved to a future sprint or backlog

## Repository Labels (18)

Repository-level labels are specific to each project.

### Component (9)
- `Component/Backend` (#5319e7) - Backend service code and business logic
- `Component/Frontend` (#1d76db) - User interface and client-side code
- `Component/API` (#0366d6) - API endpoints, contracts, and integration
- `Component/Database` (#006b75) - Database schemas, migrations, queries
- `Component/Auth` (#e99695) - Authentication and authorization
- `Component/Deploy` (#bfd4f2) - Deployment, infrastructure, DevOps
- `Component/Testing` (#f9d0c4) - Test infrastructure and frameworks
- `Component/Docs` (#c5def5) - Documentation and guides
- `Component/Infra` (#d4c5f9) - Infrastructure and system configuration

### Tech (7)
- `Tech/Python` (#3572a5) - Python language and libraries
- `Tech/JavaScript` (#f1e05a) - JavaScript/Node.js code
- `Tech/Docker` (#384d54) - Docker containers and compose
- `Tech/PostgreSQL` (#336791) - PostgreSQL database
- `Tech/Redis` (#dc382d) - Redis cache and pub/sub
- `Tech/Vue` (#42b883) - Vue.js frontend framework
- `Tech/FastAPI` (#009688) - FastAPI backend framework

### Sprint Lifecycle (Milestone Metadata)

These are tracked as milestone description metadata, not as Gitea issue labels. They are documented here for completeness.

| Label | Description |
|-------|-------------|
| `Sprint/Planning` | Sprint planning in progress |
| `Sprint/Executing` | Sprint execution in progress |
| `Sprint/Reviewing` | Code review in progress |

**Note:** Lifecycle state is stored in milestone description as `**Sprint State:** Sprint/Executing`. See `skills/sprint-lifecycle.md` for state machine rules.

### Domain (2 labels)

Cross-plugin integration labels for domain-specific validation gates.

| Label | Color | Description |
|-------|-------|-------------|
| `Domain/Viz` | `#7c4dff` | Issue involves visualization/frontend — triggers viz-platform design gates |
| `Domain/Data` | `#00bfa5` | Issue involves data engineering — triggers data-platform data gates |

**Detection Rules:**

**Domain/Viz:**
- Keywords: "dashboard", "chart", "theme", "DMC", "component", "layout", "responsive", "color", "UI", "frontend", "Dash", "Plotly"
- Also applied when: `Component/Frontend` or `Component/UI` label is present
- Example: "Create new neighbourhood comparison dashboard tab"

**Domain/Data:**
- Keywords: "schema", "migration", "pipeline", "dbt", "table", "column", "query", "PostgreSQL", "lineage", "data model"
- Also applied when: `Component/Database` or `Component/Data` label is present
- Example: "Add census demographic data pipeline"

### Epic (5 labels)

Project-level epic labels for multi-sprint work tracking.

| Label | Color | Description |
|-------|-------|-------------|
| `Epic/Database` | `#0E8A16` | Database schema, migrations, seed data |
| `Epic/API` | `#1D76DB` | Backend endpoints, middleware, auth |
| `Epic/Frontend` | `#E99695` | UI components, routing, state management |
| `Epic/Auth` | `#D93F0B` | Authentication and authorization |
| `Epic/Infrastructure` | `#BFD4F2` | CI/CD, deployment, monitoring |

### R&D (4 labels)

Research and development tracking labels for lessons learned.

| Label | Color | Description |
|-------|-------|-------------|
| `RnD/Friction` | `#FBCA04` | Workflow friction points |
| `RnD/Gap` | `#B60205` | Capability gaps discovered |
| `RnD/Pattern` | `#0075CA` | Reusable patterns identified |
| `RnD/Automation` | `#5319E7` | Automation opportunities |

## Label Suggestion Logic

When suggesting labels for issues, consider the following patterns:

### Type Detection

**Type/Bug:**
- Keywords: "bug", "fix", "error", "crash", "broken", "incorrect", "fails"
- Context: Existing functionality not working as expected
- Example: "Fix authentication token expiration bug"

**Type/Feature:**
- Keywords: "add", "implement", "create", "new", "feature", "enhance"
- Context: New functionality being added
- Example: "Add password reset functionality"

**Type/Refactor:**
- Keywords: "refactor", "extract", "restructure", "reorganize", "clean up", "service extraction"
- Context: Improving code structure without changing behavior
- Example: "Extract Intuit Engine service from monolith"

**Type/Documentation:**
- Keywords: "document", "readme", "guide", "docs", "comments"
- Context: Documentation updates
- Example: "Update API documentation for new endpoints"

**Type/Test:**
- Keywords: "test", "testing", "coverage", "unit test", "integration test"
- Context: Testing infrastructure or test writing
- Example: "Add integration tests for authentication flow"

**Type/Chore:**
- Keywords: "update dependencies", "upgrade", "maintenance", "build", "ci/cd", "tooling"
- Context: Maintenance tasks that don't change functionality
- Example: "Update FastAPI to version 0.109"

### Priority Detection

**Priority/Critical:**
- Keywords: "critical", "urgent", "blocking", "production down", "security"
- Context: Immediate action required
- Example: "Fix critical security vulnerability in auth system"

**Priority/High:**
- Keywords: "important", "high priority", "soon", "needed for release"
- Context: Important but not immediately blocking
- Example: "Implement user registration before launch"

**Priority/Medium:**
- Keywords: "should", "moderate", "this sprint"
- Context: Normal priority work
- Example: "Add email verification to registration"

**Priority/Low:**
- Keywords: "nice to have", "future", "low priority", "when time permits"
- Context: Can wait if needed
- Example: "Add dark mode theme option"

### Component Detection

**Component/Backend:**
- Keywords: "backend", "api logic", "business logic", "service", "server"
- Example: "Implement JWT token generation service"

**Component/Frontend:**
- Keywords: "frontend", "ui", "user interface", "form", "page", "component", "vue"
- Example: "Create user registration form"

**Component/API:**
- Keywords: "api", "endpoint", "rest", "graphql", "request", "response"
- Example: "Build user login endpoint"

**Component/Database:**
- Keywords: "database", "schema", "migration", "query", "sql", "postgresql"
- Example: "Add users table migration"

**Component/Auth:**
- Keywords: "auth", "authentication", "authorization", "login", "token", "permission"
- Example: "Implement JWT authentication middleware"

**Component/Deploy:**
- Keywords: "deploy", "deployment", "docker", "infrastructure", "ci/cd", "production"
- Example: "Deploy authentication service to production"

### Status Detection

**Status/In-Progress:**
- Applied when: Agent starts working on an issue
- Remove when: Work completes, fails, or is blocked
- Example: Orchestrator applies when dispatching task to executor

**Status/Blocked:**
- Applied when: Issue cannot proceed due to external dependency
- Context: Waiting for another issue, external service, or decision
- Example: "Blocked by #45 - need JWT service first"

**Status/Failed:**
- Applied when: Implementation was attempted but failed
- Context: Errors, permission issues, technical blockers
- Example: Agent hit permission errors and couldn't complete

**Status/Deferred:**
- Applied when: Work is moved to a future sprint
- Context: Scope reduction, reprioritization
- Example: "Moving to Sprint 5 due to scope constraints"

### Tech Detection

**Tech/Python:**
- Keywords: "python", "fastapi", "pydantic"
- Example: "Implement Python JWT utility"

**Tech/JavaScript:**
- Keywords: "javascript", "js", "node", "npm"
- Example: "Add JavaScript form validation"

**Tech/Vue:**
- Keywords: "vue", "vuex", "vue router", "component"
- Example: "Create Vue login component"

**Tech/Docker:**
- Keywords: "docker", "dockerfile", "compose", "container"
- Example: "Update Docker compose configuration"

**Tech/PostgreSQL:**
- Keywords: "postgresql", "postgres", "pg", "database schema"
- Example: "Optimize PostgreSQL query performance"

**Tech/Redis:**
- Keywords: "redis", "cache", "session", "pubsub"
- Example: "Implement Redis session storage"

## Multi-Label Suggestions

Most issues should have multiple labels from different categories:

**Example 1:** "Fix critical authentication bug in production API"
- Type/Bug (it's a bug fix)
- Priority/Critical (it's critical and in production)
- Component/Auth (authentication system)
- Component/API (API endpoint affected)
- Source/Production (found in production)
- Tech/Python (likely Python code)
- Tech/FastAPI (if using FastAPI)

**Example 2:** "Implement user registration with email verification"
- Type/Feature (new functionality)
- Priority/High (important for launch)
- Complexity/Medium (moderate complexity)
- Efforts/L (1-3 days work)
- Component/Backend (backend logic needed)
- Component/Frontend (registration form needed)
- Component/Auth (authentication related)
- Tech/Python (backend)
- Tech/Vue (frontend)

**Example 3:** "Extract Intuit Engine service from monolith"
- Type/Refactor (architectural change)
- Priority/High (important architectural work)
- Complexity/Complex (significant planning needed)
- Efforts/XL (more than 3 days)
- Risk/High (significant change)
- Component/Backend (backend restructuring)
- Component/API (new API boundaries)
- Tech/Python (Python service)
- Tech/Docker (new container needed)

## Usage in Commands

This skill is loaded when agents need to suggest labels:

**In /sprint plan:**
The planner agent uses this reference along with `suggest_labels` MCP tool to recommend appropriate labels for newly created issues.

**In /labels sync:**
The command updates this file with the latest taxonomy from Gitea.

## Keeping This Updated

**IMPORTANT:** Run `/labels sync` to:
1. Fetch actual labels from Gitea
2. Update this reference file
3. Ensure suggestion logic matches current taxonomy

**Update frequency:**
- First time setup: Run `/labels sync` immediately
- Regular updates: Monthly or when taxonomy changes
- Team notification: When new labels are added to Gitea

## Dynamic Approach

**Never hardcode labels** in commands or agents. Always:
1. Fetch labels dynamically using `get_labels` MCP tool
2. Use `suggest_labels` for intelligent suggestions
3. Reference this skill for context and patterns
4. Update this file via `/labels sync` when taxonomy changes

This ensures the plugin adapts to taxonomy evolution without code changes.
