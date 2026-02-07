---
name: claude-config init
description: Initialize a new CLAUDE.md file for a project
---

# /claude-config init

Create a new CLAUDE.md file tailored to your project.

## Skills to Load

- skills/visual-header.md
- skills/claude-md-structure.md
- skills/pre-change-protocol.md

## Visual Output

Display: `CONFIG-MAINTAINER - CLAUDE.md Initialization`

## Usage

```
/claude-config init                    # Interactive
/claude-config init --minimal          # Minimal version
/claude-config init --comprehensive    # Detailed version
```

## Workflow

1. Analyze project structure, ask clarifying questions
2. Detect technologies, frameworks, tools
3. Generate tailored CLAUDE.md sections
4. Allow review and customization
5. Save file in project root

## Templates

| Template | Sections |
|----------|----------|
| Minimal | Overview, Quick Start, Critical Rules, Pre-Change Protocol |
| Standard | + Architecture, Common Operations, File Structure |
| Comprehensive | + Troubleshooting, Integration Points, Workflow |

**Note:** Pre-Change Protocol is MANDATORY in all templates.

## When to Use

- Starting a new project
- Project lacks CLAUDE.md
- Taking over unfamiliar project
