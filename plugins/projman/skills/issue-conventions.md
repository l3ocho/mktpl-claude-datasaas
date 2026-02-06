---
name: issue-conventions
description: Issue title format, wiki references, and creation standards
---

# Issue Conventions

## Purpose

Defines standard formats for issue titles, bodies, and wiki references.

## When to Use

- **Planner agent**: When creating issues during sprint planning
- **Commands**: `/sprint plan`

---

## Title Format (MANDATORY)

```
[Sprint XX] <type>: <description>
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code refactoring |
| `docs` | Documentation |
| `test` | Test additions/changes |
| `chore` | Maintenance tasks |

### Examples

- `[Sprint 17] feat: Add user email validation`
- `[Sprint 17] fix: Resolve login timeout issue`
- `[Sprint 18] refactor: Extract authentication module`
- `[Sprint 18] test: Add JWT token edge case tests`
- `[Sprint 19] docs: Update API documentation`

---

## Issue Body Structure

Every issue body MUST include:

```markdown
## Description
[Clear description of the task]

## Implementation
**Wiki:** [Change VXX.X.X (Impl N)](wiki-link)

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

## Technical Notes
[Optional: Architecture decisions, constraints, considerations]
```

---

## Wiki Reference (MANDATORY)

Every issue MUST reference its implementation wiki page:

```markdown
## Implementation
**Wiki:** [Change V4.1.0 (Impl 1)](https://gitea.example.com/org/repo/wiki/Change-V4.1.0%3A-Proposal-(Implementation-1))
```

This enables:
- Traceability between issues and proposals
- Context for the broader feature being implemented
- Connection to lessons learned

---

## Issue Creation Example

```python
create_issue(
    repo="org/repo",
    title="[Sprint 17] feat: Implement JWT generation",
    body="""## Description
Create a JWT token generation service for user authentication.

## Implementation
**Wiki:** [Change V1.2.0 (Impl 1)](wiki-link)

## Acceptance Criteria
- [ ] Generate tokens with user_id, email, expiration
- [ ] Use HS256 algorithm
- [ ] Include token refresh logic
- [ ] Unit tests cover all paths

## Technical Notes
- Token expiration: 24 hours
- Refresh window: last 4 hours of validity
- See Sprint 12 lesson on token refresh edge cases
""",
    labels=["Type/Feature", "Priority/High", "Component/Auth", "Tech/Python", "Efforts/M"],
    milestone=17
)
```

---

## Auto-Close Keywords

Use in commit messages to auto-close issues:
- `Closes #XX`
- `Fixes #XX`
- `Resolves #XX`

Example commit:
```
feat: implement JWT token generation

- Add generate_token(user_id, email) function
- Add verify_token(token) function
- Include refresh logic per Sprint 12 lesson

Closes #45
```
