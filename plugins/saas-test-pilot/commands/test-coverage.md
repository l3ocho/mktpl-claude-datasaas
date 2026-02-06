---
name: test coverage
description: Analyze test coverage, identify untested paths, and prioritize gaps by risk
---

# /test coverage

Analyze test coverage and identify gaps prioritized by risk.

## Visual Output

```
+----------------------------------------------------------------------+
|  TEST-PILOT - Coverage Analysis                                       |
+----------------------------------------------------------------------+
```

## Usage

```
/test coverage [<target>] [--threshold=80] [--format=summary|detailed]
```

**Target:** File, directory, or module to analyze (defaults to entire project)
**Threshold:** Minimum acceptable coverage percentage
**Format:** Output detail level

## Skills to Load

- skills/coverage-analysis.md

## Process

1. **Discover Coverage Data**
   - Look for existing coverage reports: `.coverage`, `coverage.xml`, `lcov.info`, `coverage/`
   - If no report exists, attempt to run coverage: `pytest --cov`, `npx vitest --coverage`
   - Parse coverage data into structured format

2. **Analyze Gaps**
   - Identify uncovered lines, branches, and functions
   - Classify gaps by type:
     - Error handling paths (catch/except blocks)
     - Conditional branches (if/else, switch/case)
     - Edge case logic (boundary checks, null guards)
     - Integration points (API calls, database queries)

3. **Risk Assessment**
   - Score each gap by:
     - Complexity of uncovered code (cyclomatic complexity)
     - Criticality of the module (auth, payments, data persistence)
     - Frequency of changes (git log analysis)
     - Proximity to user input (trust boundary distance)

4. **Generate Report**
   - Overall coverage metrics
   - Per-file breakdown
   - Prioritized gap list with risk scores
   - Suggested test cases for top gaps

## Output Format

```
## Coverage Report

### Overall: 74% lines | 61% branches

### Files Below Threshold (80%)
| File | Lines | Branches | Risk |
|------|-------|----------|------|
| src/auth/login.py | 52% | 38% | HIGH |
| src/api/handlers.py | 67% | 55% | MEDIUM |

### Top 5 Coverage Gaps (by risk)
1. **src/auth/login.py:45-62** — OAuth error handling
   Risk: HIGH | Uncovered: 18 lines | Suggestion: test invalid token flow
2. **src/api/handlers.py:89-104** — Rate limit branch
   Risk: MEDIUM | Uncovered: 16 lines | Suggestion: test 429 response

### Recommendations
- Focus on auth module — highest risk, lowest coverage
- Add branch coverage to CI threshold
- 12 new test cases would bring coverage to 85%
```
