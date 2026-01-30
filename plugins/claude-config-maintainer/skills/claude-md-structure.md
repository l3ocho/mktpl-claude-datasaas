# CLAUDE.md Structure Reference

This skill defines the standard structure, required sections, and templates for CLAUDE.md files.

## Required Sections

Every CLAUDE.md MUST have these sections:

| Section | Purpose | Priority |
|---------|---------|----------|
| Project Overview | What the project does | Required |
| Quick Start | Build/test/run commands | Required |
| Critical Rules | Must-follow constraints | Required |
| Pre-Change Protocol | Dependency check before edits | **MANDATORY** |

## Recommended Sections

| Section | When to Include |
|---------|-----------------|
| Architecture | Complex projects with multiple components |
| Common Operations | Projects with repetitive tasks |
| File Structure | Large codebases |
| Troubleshooting | Projects with known gotchas |
| Integration Points | Projects with external dependencies |

## Header Hierarchy

```
# CLAUDE.md (H1 - only one)
## Section (H2 - main sections)
### Subsection (H3 - within sections)
#### Detail (H4 - rarely needed)
```

**Rules:**
- Never skip levels (no H3 before H2)
- Maximum depth: 4 levels
- No orphaned content before first header

## Templates

### Minimal Template
For small projects:
```markdown
# CLAUDE.md

## Project Overview
[Description]

## Quick Start
[Commands]

## Critical Rules
[Constraints]

## Pre-Change Protocol
[Mandatory section - see pre-change-protocol.md]
```

### Standard Template (Default)
```markdown
# CLAUDE.md

## Project Overview
## Quick Start
## Architecture
## Critical Rules
## Pre-Change Protocol
## Common Operations
## File Structure
```

### Comprehensive Template
For large projects - adds:
- Detailed Architecture
- Troubleshooting
- Integration Points
- Development Workflow
- Deployment Notes

## Auto-Detection Signals

| Technology | Detection Method |
|------------|------------------|
| Language | File extensions, config files |
| Framework | package.json, requirements.txt, Cargo.toml |
| Build system | Makefile, scripts in package.json |
| Testing | pytest.ini, jest.config.js, go.mod |
| Docker | Dockerfile, docker-compose.yml |
| Database | ORM configs, connection strings |

## Section Content Guidelines

### Project Overview
- 1-3 sentences describing purpose
- Target audience if relevant
- Key technologies used

### Quick Start
- Install command
- Test command
- Run command
- Each with brief inline comment

### Critical Rules
- Numbered or bulleted list
- Specific, actionable constraints
- Include rationale for non-obvious rules

### Architecture
- High-level component diagram (ASCII or description)
- Data flow explanation
- Key file/directory purposes
