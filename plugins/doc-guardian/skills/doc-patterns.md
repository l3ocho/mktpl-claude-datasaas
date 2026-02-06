---
name: doc-patterns
description: Common documentation structures and patterns
---

# Documentation Patterns

## Purpose

Defines common documentation file structures and their contents.

## When to Use

- **doc audit**: Understanding what to check in each doc type
- **doc coverage**: Identifying documentation locations

---

## README.md Patterns

Typical sections:
- **Installation**: Version requirements, dependencies
- **Usage**: Function calls, CLI commands
- **Configuration**: Environment vars, config files
- **API**: Endpoint references

---

## CLAUDE.md Patterns

Typical sections:
- **Project Context**: Tech stack versions
- **File Structure**: Directory layout
- **Commands**: Available operations
- **Workflows**: Process descriptions

---

## Code Documentation

### Docstrings
- Function signatures
- Parameters and types
- Return values
- Raised exceptions

### Type Hints
- Should match docstring types
- Verify consistency

### Inline Comments
- References to other code
- TODO markers
- Warning notes

---

## File Inventory

Standard documentation files to check:
- `README.md` (root and subdirectories)
- `CLAUDE.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `docs/**/*.md`
- API documentation
- Configuration references
