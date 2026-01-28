---
description: Initialize a new CLAUDE.md file for a project
---

# Initialize CLAUDE.md

This command creates a new CLAUDE.md file tailored to your project, gathering context and generating appropriate content.

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  ⚙️ CONFIG-MAINTAINER · CLAUDE.md Initialization                 │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the initialization.

## What This Command Does

1. **Gather Context** - Analyzes project structure and asks clarifying questions
2. **Detect Stack** - Identifies technologies, frameworks, and tools
3. **Generate Content** - Creates tailored CLAUDE.md sections
4. **Review & Refine** - Allows customization before saving
5. **Save File** - Creates the CLAUDE.md in project root

## Usage

```
/config-init
```

Or with options:

```
/config-init --template=api        # Use API project template
/config-init --minimal             # Create minimal version
/config-init --comprehensive       # Create detailed version
```

## Initialization Workflow

```
CLAUDE.md Initialization
========================

Step 1: Project Analysis
------------------------
Scanning project structure...

Detected:
- Language: Python 3.11
- Framework: FastAPI
- Package Manager: pip (requirements.txt found)
- Testing: pytest
- Docker: Yes (Dockerfile found)
- Git: Yes (.git directory)

Step 2: Clarifying Questions
----------------------------

1. Project Description:
   What does this project do? (1-2 sentences)
   > [User provides description]

2. Build/Run Commands:
   Detected commands - are these correct?
   - Install: pip install -r requirements.txt
   - Test: pytest
   - Run: uvicorn main:app --reload
   [Y/n/edit]

3. Critical Rules:
   Any rules Claude MUST follow?
   Examples: "Never modify migrations", "Always use type hints"
   > [User provides rules]

4. Sensitive Areas:
   Any files/directories Claude should be careful with?
   > [User provides or skips]

Step 3: Generate CLAUDE.md
--------------------------

Generating content based on:
- Project type: FastAPI web API
- Detected technologies
- Your provided context

Preview:

---
# CLAUDE.md

## Project Overview
[Generated description]

## Quick Start

```bash
pip install -r requirements.txt  # Install dependencies
pytest                           # Run tests
uvicorn main:app --reload        # Start dev server
```

## Architecture
[Generated based on structure]

## Critical Rules
[Your provided rules]

## File Structure
[Generated from analysis]
---

Save this CLAUDE.md? [Y/n/edit]

Step 4: Complete
----------------

CLAUDE.md created successfully!

Location: /path/to/project/CLAUDE.md
Lines: 87
Score: 85/100 (following best practices)

Recommendations:
- Run /config-analyze periodically to maintain quality
- Update when adding major features
- Add troubleshooting section as issues are discovered
```

## Templates

### Minimal Template
For small projects or when starting fresh:
- Project Overview (required)
- Quick Start (required)
- Critical Rules (required)

### Standard Template (default)
For typical projects:
- Project Overview
- Quick Start
- Architecture
- Critical Rules
- Common Operations
- File Structure

### Comprehensive Template
For large or complex projects:
- All standard sections plus:
- Detailed Architecture
- Troubleshooting
- Integration Points
- Development Workflow
- Deployment Notes

## Auto-Detection

The command automatically detects:

| What | How |
|------|-----|
| Language | File extensions, config files |
| Framework | package.json, requirements.txt, etc. |
| Build system | Makefile, package.json scripts, etc. |
| Testing | pytest.ini, jest.config, etc. |
| Docker | Dockerfile, docker-compose.yml |
| Database | Connection strings, ORM configs |

## Customization

After generation, you can:
- Edit any section before saving
- Add additional sections
- Remove unnecessary sections
- Adjust detail level
- Add project-specific content

## When to Use

Run `/config-init` when:
- Starting a new project
- Project lacks CLAUDE.md
- Existing CLAUDE.md is outdated/poor quality
- Taking over an unfamiliar project

## Tips

1. **Provide accurate description** - This shapes the whole file
2. **Include critical rules** - What must Claude never do?
3. **Review generated content** - Auto-detection isn't perfect
4. **Start minimal, grow as needed** - Add sections when required
5. **Keep it current** - Update when project changes significantly

## Examples

### For a CLI Tool
```
/config-init

> Description: CLI tool for managing cloud infrastructure
> Critical rules: Never delete resources without confirmation, always show dry-run first
```

### For a Web App
```
/config-init

> Description: E-commerce platform with React frontend and Node.js backend
> Critical rules: Never expose API keys, always validate user input, follow the existing component patterns
```

### For a Library
```
/config-init --template=minimal

> Description: Python library for parsing log files
> Critical rules: Maintain backward compatibility, all public functions need docstrings
```
