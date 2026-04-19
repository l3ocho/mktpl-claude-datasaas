# Code Sentinel Integration

Add to your project's CLAUDE.md:

## Security & Code Quality

This project uses code-sentinel for security scanning and refactoring.

### Automatic Security Checks
PreToolUse hooks scan all code changes for:
- SQL/Command/Code injection
- XSS vulnerabilities
- Hardcoded secrets
- Unsafe deserialization

Critical issues are blocked. Warnings are noted but allowed.

### Commands
- `/security-review` - Full project security audit (built-in Claude Code command: SQL injection, XSS, secrets, auth flaws, dependency vulnerabilities)
- `/sentinel refactor <target>` - Apply refactoring pattern
- `/sentinel refactor-dry <target>` - Preview refactoring opportunities

### Severity Levels
- Critical: Must fix immediately
- High: Fix before release
- Medium: Improve when possible
