---
description: Quick project setup - configures only project-level settings
---

# Project Initialization (PR Review)

## Visual Output

Display header: `PR-REVIEW - Project Setup`

## Skills to Load

- skills/setup-workflow.md
- skills/output-formats.md

## Purpose

Fast setup when system-level config already exists.

**Use when:** Already ran `/initial-setup`, starting new project

## Workflow

### Pre-Flight Check

Verify `~/.config/claude/gitea.env` exists. If missing: redirect to `/initial-setup`

### Project Setup

Execute `skills/setup-workflow.md`:
1. Verify git repo
2. Check existing .env
3. Auto-detect org/repo from git remote
4. Validate via Gitea API
5. Create/update .env

### Complete

Display project configured format from `skills/output-formats.md`

## Ready Commands

- `/pr-review <number>` - Full review
- `/pr-summary <number>` - Quick summary
- `/pr-findings <number>` - List findings
