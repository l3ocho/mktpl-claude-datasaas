---
description: Sync project configuration with current git remote
---

# Project Sync (PR Review)

## Visual Output

Display header: `PR-REVIEW - Project Sync`

## Skills to Load

- skills/setup-workflow.md
- skills/output-formats.md

## Purpose

Updates config when git remote URL changed.

**Use when:** Repo moved/renamed, SessionStart detected mismatch

## Workflow

Execute `skills/setup-workflow.md` Sync Workflow:

1. Verify system config exists
2. Read current .env values
3. Detect org/repo from git remote
4. Compare - if match, exit; if mismatch, continue
5. Validate new values via API
6. Update .env with sed
7. Display confirmation from `skills/output-formats.md`
