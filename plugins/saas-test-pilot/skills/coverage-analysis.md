---
description: Coverage gap detection, risk scoring, and prioritization
---

# Coverage Analysis Skill

## Overview

Systematic approach to identifying, scoring, and prioritizing test coverage gaps. Coverage data is a tool for finding untested behavior, not a target to maximize blindly.

## Coverage Types

| Type | Measures | Tool Support |
|------|----------|-------------|
| **Line** | Which lines executed | All tools |
| **Branch** | Which conditional paths taken | pytest-cov, istanbul, c8 |
| **Function** | Which functions called | istanbul, c8 |
| **Statement** | Which statements executed | istanbul |

Branch coverage is the minimum useful metric. Line coverage alone hides untested else-branches and short-circuit evaluations.

## Gap Classification

### By Code Pattern

| Pattern | Risk Level | Priority |
|---------|------------|----------|
| Exception handlers (catch/except) | HIGH | Test both the trigger and the handling |
| Auth/permission checks | CRITICAL | Must test both allowed and denied |
| Input validation branches | HIGH | Test valid, invalid, and boundary |
| Default/fallback cases | MEDIUM | Often untested but triggered in production |
| Configuration variations | MEDIUM | Test with different config values |
| Logging/metrics code | LOW | Usually not worth dedicated tests |

### By Module Criticality

Score modules 1-5 based on:
- **Data integrity** — Does it write to database/files? (+2)
- **Security boundary** — Does it handle auth/authz? (+2)
- **User-facing** — Does failure affect users directly? (+1)
- **Frequency of change** — Changed often in git log? (+1)
- **Dependency count** — Many callers depend on it? (+1)

## Prioritization Formula

```
Priority = (Module Criticality * 2) + (Gap Risk Level) - (Test Complexity)
```

Where Test Complexity:
- 1: Simple unit test, no mocks needed
- 2: Requires basic mocking
- 3: Requires complex setup (database, fixtures)
- 4: Requires infrastructure (message queue, external service)
- 5: Requires E2E or manual testing

## Reporting Guidelines

- Always show current coverage alongside target
- Group gaps by module, sorted by priority
- For each gap: file, line range, description, suggested test
- Estimate coverage improvement if top-N gaps are addressed
- Never recommend deleting code to improve coverage
