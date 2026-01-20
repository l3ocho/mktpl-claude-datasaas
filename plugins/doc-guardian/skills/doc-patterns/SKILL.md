---
description: Knowledge of documentation patterns and structures for drift detection
---

# Documentation Patterns Skill

## Common Documentation Structures

### README.md Patterns
- Installation section: version requirements, dependencies
- Usage section: function calls, CLI commands
- Configuration section: env vars, config files
- API section: endpoint references

### CLAUDE.md Patterns
- Project context: tech stack versions
- File structure: directory layout
- Commands: available operations
- Workflows: process descriptions

### Code Documentation
- Docstrings: function signatures, parameters, returns
- Type hints: should match docstring types
- Comments: inline references to other code

## Drift Detection Rules

1. **Version Mismatch**: Any hardcoded version in docs must match package.json, pyproject.toml, requirements.txt
2. **Function References**: Function names in docs must exist in codebase with matching signatures
3. **Path References**: File paths in docs must exist in current directory structure
4. **Config Keys**: Environment variables and config keys in docs must be used in code
5. **Command Examples**: CLI examples in docs should be valid commands

## Priority Levels

- **P0 (Critical)**: Broken references that would cause user errors
- **P1 (High)**: Outdated information that misleads users
- **P2 (Medium)**: Missing documentation for public interfaces
- **P3 (Low)**: Style inconsistencies, minor wording issues
