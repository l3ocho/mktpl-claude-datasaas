---
name: label-taxonomy
description: Dynamic reference for Gitea label taxonomy (organization + repository labels)
---

# Label Taxonomy Reference

**Status:** Initial template - Run `/labels-sync` to populate with actual labels from Gitea

**Last synced:** Never (please run `/labels-sync`)
**Source:** Gitea (hhl-infra repository)

## Overview

This skill provides the current label taxonomy used for issue classification in Gitea. Labels are **fetched dynamically** from Gitea and should never be hardcoded.

**Current Taxonomy:** ~44 labels (28 organization + 16 repository)

## Organization Labels (~28)

Organization-level labels are shared across all repositories in the `hhl-infra` organization.

### Agent (2)
- `Agent/Human` - Work performed by human developers
- `Agent/Claude` - Work performed by Claude Code or AI assistants

### Complexity (3)
- `Complexity/Simple` - Straightforward tasks requiring minimal analysis
- `Complexity/Medium` - Moderate complexity with some architectural decisions
- `Complexity/Complex` - High complexity requiring significant planning and analysis

### Efforts (5)
- `Efforts/XS` - Extra small effort (< 2 hours)
- `Efforts/S` - Small effort (2-4 hours)
- `Efforts/M` - Medium effort (4-8 hours / 1 day)
- `Efforts/L` - Large effort (1-3 days)
- `Efforts/XL` - Extra large effort (> 3 days)

### Priority (4)
- `Priority/Low` - Nice to have, can wait
- `Priority/Medium` - Should be done this sprint
- `Priority/High` - Important, do soon
- `Priority/Critical` - Urgent, blocking other work

### Risk (3)
- `Risk/Low` - Low risk of issues or impact
- `Risk/Medium` - Moderate risk, proceed with caution
- `Risk/High` - High risk, needs careful planning and testing

### Source (4)
- `Source/Development` - Issue discovered during development
- `Source/Staging` - Issue found in staging environment
- `Source/Production` - Issue found in production
- `Source/Customer` - Issue reported by customer

### Type (6)
- `Type/Bug` - Bug fixes and error corrections
- `Type/Feature` - New features and enhancements
- `Type/Refactor` - Code restructuring and architectural changes
- `Type/Documentation` - Documentation updates and improvements
- `Type/Test` - Testing-related work (unit, integration, e2e)
- `Type/Chore` - Maintenance, tooling, dependencies, build tasks

## Repository Labels (~16)

Repository-level labels are specific to each project.

### Component (9)
- `Component/Backend` - Backend service code and business logic
- `Component/Frontend` - User interface and client-side code
- `Component/API` - API endpoints, contracts, and integration
- `Component/Database` - Database schemas, migrations, queries
- `Component/Auth` - Authentication and authorization
- `Component/Deploy` - Deployment, infrastructure, DevOps
- `Component/Testing` - Test infrastructure and frameworks
- `Component/Docs` - Documentation and guides
- `Component/Infra` - Infrastructure and system configuration

### Tech (7)
- `Tech/Python` - Python language and libraries
- `Tech/JavaScript` - JavaScript/Node.js code
- `Tech/Docker` - Docker containers and compose
- `Tech/PostgreSQL` - PostgreSQL database
- `Tech/Redis` - Redis cache and pub/sub
- `Tech/Vue` - Vue.js frontend framework
- `Tech/FastAPI` - FastAPI backend framework

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

**In /sprint-plan:**
The planner agent uses this reference along with `suggest_labels` MCP tool to recommend appropriate labels for newly created issues.

**In /labels-sync:**
The command updates this file with the latest taxonomy from Gitea.

## Keeping This Updated

**IMPORTANT:** This file is a template. Run `/labels-sync` to:
1. Fetch actual labels from Gitea
2. Update this reference file
3. Ensure suggestion logic matches current taxonomy

**Update frequency:**
- First time setup: Run `/labels-sync` immediately
- Regular updates: Monthly or when taxonomy changes
- Team notification: When new labels are added to Gitea

## Dynamic Approach

**Never hardcode labels** in commands or agents. Always:
1. Fetch labels dynamically using `get_labels` MCP tool
2. Use `suggest_labels` for intelligent suggestions
3. Reference this skill for context and patterns
4. Update this file via `/labels-sync` when taxonomy changes

This ensures the plugin adapts to taxonomy evolution without code changes.
