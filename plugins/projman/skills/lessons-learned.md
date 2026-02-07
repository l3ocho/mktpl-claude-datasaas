---
name: lessons-learned
description: Capture and search workflow for lessons learned system
---

# Lessons Learned System

## Purpose

Defines the workflow for capturing lessons at sprint close and searching them at sprint start/plan.

## When to Use

- **Planner agent**: Search lessons at sprint start
- **Orchestrator agent**: Capture lessons at sprint close
- **Commands**: `/sprint plan`, `/sprint start`, `/sprint close`

---

## Searching Lessons (Sprint Start/Plan)

**ALWAYS search for past lessons before planning or executing.**

```python
search_lessons(
    repo="org/repo",
    query="relevant keywords",
    tags=["technology", "component"],
    limit=10
)
```

**Present findings:**
```
Relevant lessons from previous sprints:

📚 Sprint 12: "JWT Token Expiration Edge Cases"
   Tags: auth, jwt, python
   Key lesson: Handle token refresh explicitly

📚 Sprint 8: "Service Extraction Boundaries"
   Tags: architecture, refactoring
   Key lesson: Define API contracts BEFORE extracting
```

---

## Capturing Lessons (Sprint Close)

### Interview Questions

Ask these probing questions:
1. What challenges did you face this sprint?
2. What worked well and should be repeated?
3. Were there any preventable mistakes?
4. Did any technical decisions need adjustment?
5. What would you do differently?

### Lesson Structure

```markdown
# Sprint N - [Lesson Title]

## Metadata
- **Implementation:** [Change VXX.X.X (Impl N)](wiki-link)
- **Issues:** #XX, #XX
- **Sprint:** Sprint N

## Context
[What were you doing?]

## Problem
[What went wrong / insight / challenge?]

## Solution
[How did you solve it?]

## Prevention
[How to avoid in future?]

## Tags
technology, component, type, pattern
```

### Creating Lesson

```python
create_lesson(
    repo="org/repo",
    title="Sprint N - Lesson Title",
    content="[structured content above]",
    tags=["tag1", "tag2"],
    category="sprints"
)
```

---

## Tagging Strategy

**By Technology:** python, javascript, docker, postgresql, redis, vue, fastapi

**By Component:** backend, frontend, api, database, auth, deploy, testing, docs

**By Type:** bug, feature, refactor, architecture, performance, security

**By Pattern:** infinite-loop, edge-case, integration, boundaries, dependencies

---

## Example Lessons

### Technical Gotcha
```markdown
# Sprint 16 - Claude Code Infinite Loop on Validation Errors

## Metadata
- **Implementation:** [Change V1.2.0 (Impl 1)](wiki-link)
- **Issues:** #45, #46
- **Sprint:** Sprint 16

## Context
Implementing input validation for authentication API.

## Problem
Claude Code entered infinite loop when pytest validation tests failed.
The loop occurred because error messages didn't change between attempts.

## Solution
Added more descriptive error messages specifying what value failed and why.

## Prevention
- Write validation test errors with specific values
- If Claude loops, check if errors provide unique information
- Add loop detection (fail after 3 identical errors)

## Tags
testing, claude-code, validation, python, pytest
```
