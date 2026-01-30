---
name: review-checklist
description: Code review criteria and severity classification
---

# Review Checklist

## Purpose

Defines code review criteria, severity classification, and output format.

## When to Use

- **Code Reviewer agent**: During pre-sprint-close review
- **Commands**: `/review`

---

## Severity Classification

### Critical (Must Fix Before Close)

Security issues, broken functionality, data loss risks:

- Hardcoded credentials or API keys
- SQL injection vulnerabilities
- Missing authentication/authorization checks
- Unhandled errors that could crash the application
- Data loss or corruption risks
- Broken core functionality

### Warning (Should Fix)

Technical debt that will cause problems soon:

- TODO/FIXME comments left unresolved
- Debug statements (console.log, print) in production code
- Functions over 50 lines (complexity smell)
- Deeply nested conditionals (>3 levels)
- Bare except/catch blocks
- Ignored errors
- Missing error handling

### Recommendation (Future Sprint)

Improvements that can wait:

- Missing docstrings on public functions
- Minor code duplication
- Commented-out code blocks
- Variable naming improvements
- Minor refactoring opportunities

---

## Review Patterns by Language

### Python
| Look For | Severity |
|----------|----------|
| Bare `except:` | Warning |
| `print()` statements | Warning |
| `# TODO` | Warning |
| Missing type hints on public APIs | Recommendation |
| `eval()`, `exec()` | Critical |
| SQL string formatting | Critical |
| `verify=False` in requests | Critical |

### JavaScript/TypeScript
| Look For | Severity |
|----------|----------|
| `console.log` | Warning |
| `// TODO` | Warning |
| `any` type abuse | Warning |
| Missing error boundaries | Warning |
| `eval()` | Critical |
| `innerHTML` with user input | Critical |
| Unescaped user input | Critical |

### Go
| Look For | Severity |
|----------|----------|
| `// TODO` | Warning |
| Ignored errors (`_`) | Warning |
| Missing error returns | Warning |
| SQL concatenation | Critical |
| Missing input validation | Warning |

### Rust
| Look For | Severity |
|----------|----------|
| `// TODO` | Warning |
| `unwrap()` chains | Warning |
| `unsafe` blocks without justification | Warning |
| Unchecked `unwrap()` on user input | Critical |

---

## What NOT to Review

- Style issues (assume formatters handle this)
- Architectural rewrites mid-sprint
- Issues in unchanged code (unless directly impacted)
- Bikeshedding on naming preferences

---

## Output Template

```
## Code Review Summary

**Scope**: [X files from sprint/last N commits]
**Verdict**: [READY FOR CLOSE / NEEDS ATTENTION / BLOCKED]

### Critical (Must Fix)
- `src/auth.py:45` - Hardcoded API key in source code
- `src/db.py:123` - SQL injection vulnerability

### Warnings (Should Fix)
- `src/utils.js:123` - console.log left in production code
- `src/handler.py:67` - Bare except block swallows all errors

### Recommendations (Future Sprint)
- `src/api.ts:89` - Function exceeds 50 lines, consider splitting

### Clean Files
- src/models.py
- src/tests/test_auth.py
```

---

## Verdict Criteria

| Verdict | Criteria |
|---------|----------|
| **READY FOR CLOSE** | No Critical, few/no Warnings |
| **NEEDS ATTENTION** | No Critical, has Warnings that should be addressed |
| **BLOCKED** | Has Critical issues that must be fixed |

---

## Integration with Sprint

When sprint context is available:
- Reference the sprint's issue list
- Create follow-up issues for non-critical findings
- Tag findings with appropriate labels from taxonomy
