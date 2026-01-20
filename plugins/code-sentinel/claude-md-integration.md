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
- `/security-scan` - Full project security audit
- `/refactor <target>` - Apply refactoring pattern
- `/refactor-dry <target>` - Preview refactoring opportunities

### Severity Levels
- 🔴 Critical: Must fix immediately
- 🟠 High: Fix before release
- 🟡 Medium: Improve when possible
