# code-sentinel

Security scanning and code refactoring tools for Claude Code projects.

## Features

### Security Scanning
- **PreToolUse Hook**: Catches vulnerabilities BEFORE code is written
- **Full Audit**: `/security-scan` for comprehensive project review
- **Pattern Detection**: SQL injection, XSS, command injection, secrets, and more

### Refactoring
- **Pattern Library**: Extract method, simplify conditionals, modernize syntax
- **Safe Transforms**: Preview changes before applying
- **Reference Updates**: Automatically updates all call sites

## Commands

| Command | Description |
|---------|-------------|
| `/security-scan` | Full project security audit |
| `/refactor <target>` | Apply refactoring with pattern |
| `/refactor-dry <target>` | Preview opportunities without changes |

## Hooks

- **PreToolUse (Write\|Edit)**: Scans code for security patterns before writing

## Security Patterns Detected

| Category | Examples |
|----------|----------|
| Injection | SQL, Command, Code (eval), XSS |
| Secrets | Hardcoded API keys, passwords |
| Deserialization | Pickle, unsafe YAML |
| Path Traversal | Unsanitized file paths |

## Installation

```bash
/plugin marketplace add https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace.git
/plugin install code-sentinel
```

## Integration

See claude-md-integration.md for CLAUDE.md additions.
