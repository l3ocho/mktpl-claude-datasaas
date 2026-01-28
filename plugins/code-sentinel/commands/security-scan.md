---
description: Full security audit of codebase - scans all files for vulnerability patterns
---

# Security Scan

Comprehensive security audit of the project.

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔒 CODE-SENTINEL · Security Scan                                │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the scan workflow.

## Process

1. **File Discovery**
   Scan all code files: .py, .js, .ts, .jsx, .tsx, .go, .rs, .java, .rb, .php, .sh

2. **Pattern Detection**

   ### Critical Vulnerabilities
   | Pattern | Risk | Detection |
   |---------|------|-----------|
   | SQL Injection | High | String concat in SQL queries |
   | Command Injection | High | shell=True, os.system with vars |
   | XSS | High | innerHTML with user input |
   | Code Injection | Critical | eval/exec with external input |
   | Deserialization | Critical | pickle.loads, yaml.load unsafe |
   | Path Traversal | High | File ops without sanitization |
   | Hardcoded Secrets | High | API keys, passwords in code |
   | SSRF | Medium | URL from user input in requests |

   ### Code Quality Issues
   | Pattern | Risk | Detection |
   |---------|------|-----------|
   | Broad Exceptions | Low | `except:` or `except Exception:` |
   | Debug Statements | Low | print/console.log with data |
   | TODO/FIXME Security | Medium | Comments mentioning security |
   | Deprecated Functions | Medium | Known insecure functions |

3. **Output Format**
```
## Security Scan Report

### Critical (Immediate Action Required)
🔴 src/db.py:45 - SQL Injection
   Code: `f"SELECT * FROM users WHERE id = {user_id}"`
   Fix: Use parameterized query: `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`

### High
🟠 config.py:12 - Hardcoded Secret
   Code: `API_KEY = "sk-1234..."`
   Fix: Use environment variable: `API_KEY = os.environ.get("API_KEY")`

### Medium
🟡 utils.py:78 - Broad Exception
   Code: `except:`
   Fix: Catch specific exceptions

### Summary
- Critical: X (must fix before deploy)
- High: X (fix soon)
- Medium: X (improve when possible)
```

4. **Exit Code Guidance**
   - Critical findings: Recommend blocking merge/deploy
   - High findings: Recommend fixing before release
   - Medium/Low: Informational
