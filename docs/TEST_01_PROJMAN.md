# Projman Plugin Testing Plan

**Status:** Phase 2 & 3 Complete - Ready for Testing
**Date:** 2025-11-18
**Plugin Version:** 0.1.0

## Overview

This document outlines the testing strategy for the Projman plugin, which has completed Phase 2 (Commands) and Phase 3 (Agents).

## What Was Built

### Phase 2: Commands (5 total)
- ✅ `/sprint-plan` - AI-guided planning with planner agent
- ✅ `/sprint-start` - Begin execution with orchestrator agent
- ✅ `/sprint-status` - Quick progress check
- ✅ `/sprint-close` - Capture lessons learned (critical!)
- ✅ `/labels-sync` - Sync label taxonomy from Gitea

### Phase 3: Agents (3 total)
- ✅ **Planner Agent** - Thoughtful, asks clarifying questions, searches lessons learned
- ✅ **Orchestrator Agent** - Concise, action-oriented, tracks progress meticulously
- ✅ **Executor Agent** - Implementation-focused, follows specs precisely

### Supporting Components
- ✅ Plugin manifest (`plugin.json`) with valid schema
- ✅ MCP configuration (`.mcp.json`) for Gitea + Wiki.js
- ✅ Label taxonomy skill with suggestion logic
- ✅ README.md with complete usage guide
- ✅ CONFIGURATION.md with step-by-step setup

**Total:** 13 files, ~3,719 lines of documentation

## Testing Setup

### Prerequisites Completed

✅ **MCP Servers Installed:**
- `mcp-servers/gitea/.venv/` - Gitea MCP Server
- `mcp-servers/wikijs/.venv/` - Wiki.js MCP Server

✅ **System Configuration:**
- `~/.config/claude/gitea.env` - Gitea credentials
- `~/.config/claude/wikijs.env` - Wiki.js credentials

✅ **Project Configuration:**
- `.env` - Project-specific settings (NOT committed)
  ```bash
  GITEA_REPO=claude-code-hhl-toolkit
  WIKIJS_PROJECT=projects/claude-code-hhl-toolkit
  ```

✅ **Local Test Marketplace:**
- `.claude-plugins/projman-test-marketplace/marketplace.json`
- Points to `../../projman` for local testing

### Repository Structure

```
hhl-claude-agents/
├── .env                              ✅ Project config (in .gitignore)
├── .claude-plugins/
│   └── projman-test-marketplace/
│       └── marketplace.json          ✅ Local marketplace
├── projman/                          ✅ Complete plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── .mcp.json
│   ├── commands/
│   │   ├── sprint-plan.md
│   │   ├── sprint-start.md
│   │   ├── sprint-status.md
│   │   ├── sprint-close.md
│   │   └── labels-sync.md
│   ├── agents/
│   │   ├── planner.md
│   │   ├── orchestrator.md
│   │   └── executor.md
│   ├── skills/
│   │   └── label-taxonomy/
│   │       └── labels-reference.md
│   ├── README.md
│   └── CONFIGURATION.md
└── mcp-servers/
    ├── gitea/
    │   └── .venv/
    └── wikijs/
        └── .venv/
```

## Pre-Flight Checks

### 1. Verify MCP Server Connectivity

**Test Gitea Connection:**
```bash
cd mcp-servers/gitea
source .venv/bin/activate
python -c "from mcp_server.config import load_config; config = load_config(); print(f'✅ Gitea: {config.api_url}')"
```

**Expected output:**
```
✅ Gitea: http://gitea.hotport/api/v1
```

**Test Wiki.js Connection:**
```bash
cd mcp-servers/wikijs
source .venv/bin/activate
python -c "from mcp_server.config import load_config; config = load_config(); print(f'✅ Wiki.js: {config.api_url}')"
```

**Expected output:**
```
✅ Wiki.js: http://wikijs.hotport/graphql
```

### 2. Verify Configuration Files

**Check System Config:**
```bash
ls -la ~/.config/claude/*.env
# Should show:
# -rw------- gitea.env
# -rw------- wikijs.env
```

**Check Project Config:**
```bash
cat .env
# Should show:
# GITEA_REPO=claude-code-hhl-toolkit
# WIKIJS_PROJECT=projects/claude-code-hhl-toolkit
```

**Verify .env is ignored:**
```bash
git check-ignore .env
# Should output: .env
```

### 3. Verify Plugin Structure

**Check plugin manifest:**
```bash
cat projman/.claude-plugin/plugin.json | python3 -m json.tool > /dev/null && echo "✅ Valid JSON"
```

**Check MCP config:**
```bash
cat projman/.mcp.json | python3 -m json.tool > /dev/null && echo "✅ Valid JSON"
```

**List all components:**
```bash
tree projman/ -L 2
```

## Testing Phases

### Phase 1: Quick Validation (5-10 minutes)

**Goal:** Verify basic connectivity and command loading

**Test 1.1: Label Sync** (No agent, pure MCP test)
```
/labels-sync
```

**Expected Behavior:**
- ✅ Checks git branch first
- ✅ Connects to Gitea MCP server
- ✅ Fetches organization labels (28)
- ✅ Fetches repository labels (16)
- ✅ Shows total count (44 labels)
- ✅ Updates `projman/skills/label-taxonomy/labels-reference.md`
- ✅ Confirms successful sync

**Success Criteria:**
- No connection errors
- Label counts match Gitea
- File updated with current timestamp
- All label categories present (Agent, Complexity, Efforts, Priority, Risk, Source, Type, Component, Tech)

**Test 1.2: Sprint Status** (Read-only test)
```
/sprint-status
```

**Expected Behavior:**
- ✅ Checks git branch
- ✅ Fetches open issues from Gitea
- ✅ Fetches closed issues from Gitea
- ✅ Categorizes by status (Open, In Progress, Blocked, Completed)
- ✅ Shows completion percentage
- ✅ Identifies priority alerts

**Success Criteria:**
- Issues fetch successfully
- Categorization works
- No write operations attempted
- Progress summary accurate

### Phase 2: Agent Validation (15-20 minutes)

**Goal:** Test agent personalities and MCP tool integration

**Test 2.1: Planner Agent** (via `/sprint-plan`)
```
/sprint-plan
```

**Test Input:**
> "Plan a small sprint to add usage examples to the projman README"

**Expected Planner Behavior:**
1. ✅ Checks git branch (development)
2. ✅ Asks clarifying questions:
   - What kind of examples?
   - How detailed should they be?
   - Any specific use cases?
3. ✅ Searches lessons learned:
   - Uses `search_lessons` MCP tool
   - Searches by tags: "documentation", "readme"
4. ✅ Performs architecture analysis:
   - Thinks through structure
   - Considers edge cases
   - References past lessons
5. ✅ Creates Gitea issues:
   - Uses `suggest_labels` for each issue
   - Creates 2-3 well-structured issues
   - Includes acceptance criteria
   - References architectural decisions
6. ✅ Generates planning document:
   - Summarizes sprint goals
   - Lists created issues
   - Documents assumptions

**Success Criteria:**
- Planner personality evident (thoughtful, asks questions)
- Lessons learned searched proactively
- Labels suggested intelligently
- Issues created in Gitea with proper structure
- Architecture analysis thorough

**Test 2.2: Orchestrator Agent** (via `/sprint-start`)
```
/sprint-start
```

**Expected Orchestrator Behavior:**
1. ✅ Checks git branch
2. ✅ Fetches sprint issues from Gitea
3. ✅ Searches relevant lessons:
   - Uses `search_lessons` with tags
   - Presents relevant past experiences
4. ✅ Identifies next task:
   - Highest priority
   - Unblocked by dependencies
5. ✅ Generates lean execution prompt:
   - Concise (not verbose)
   - Actionable steps
   - References lessons
   - Clear acceptance criteria

**Success Criteria:**
- Orchestrator personality evident (concise, action-oriented)
- Lessons searched by relevant tags
- Next task identified correctly
- Execution prompt is lean (not planning document)
- Dependencies checked

**Test 2.3: Executor Agent** (Manual invocation if needed)

**Note:** Executor typically invoked by orchestrator, but can be tested independently.

**Expected Executor Behavior:**
1. ✅ Checks git branch
2. ✅ Follows specifications precisely
3. ✅ Writes clean, tested code
4. ✅ Handles edge cases
5. ✅ References lessons learned in code comments
6. ✅ Generates completion report

**Success Criteria:**
- Executor personality evident (implementation-focused)
- Code follows specs exactly
- Tests included
- Edge cases covered
- Lessons applied in implementation

### Phase 3: Full Workflow Test (30-45 minutes)

**Goal:** Complete sprint lifecycle end-to-end

**Scenario:** "Add comprehensive testing examples to projman documentation"

**Step 3.1: Planning** (`/sprint-plan`)
```
/sprint-plan

Input: "Add comprehensive testing examples to projman documentation,
including command usage, agent behavior, and troubleshooting scenarios"
```

**Expected Flow:**
1. Planner asks clarifying questions
2. Searches lessons about documentation
3. Creates 3-4 issues in Gitea:
   - Add command usage examples
   - Add agent behavior examples
   - Add troubleshooting guide
   - Add quick start tutorial
4. Suggests appropriate labels for each

**Validation:**
- [ ] Check Gitea - issues created?
- [ ] Check labels - appropriate categories?
- [ ] Check issue bodies - acceptance criteria clear?

**Step 3.2: Execution** (`/sprint-start`)
```
/sprint-start
```

**Expected Flow:**
1. Orchestrator reviews issues
2. Searches lessons about documentation
3. Identifies first task
4. Generates lean execution prompt

**Validation:**
- [ ] Next task correctly identified?
- [ ] Execution prompt concise?
- [ ] Lessons referenced?

**Step 3.3: Work on Task**

Implement the first task (e.g., add command examples to README).

**Step 3.4: Close Sprint** (`/sprint-close`)
```
/sprint-close
```

**Expected Flow:**
1. Orchestrator reviews completion
2. Asks questions about sprint:
   - What challenges faced?
   - What went well?
   - Preventable mistakes?
3. Captures lessons learned:
   - Structures in proper format
   - Suggests appropriate tags
4. Saves to Wiki.js:
   - Uses `create_lesson` MCP tool
   - Creates in `/projects/claude-code-hhl-toolkit/lessons-learned/sprints/`
5. Offers git operations:
   - Commit changes
   - Merge branches
   - Tag sprint

**Validation:**
- [ ] Lessons captured in proper format?
- [ ] Saved to Wiki.js successfully?
- [ ] Tags appropriate for discovery?
- [ ] Check Wiki.js - lesson visible?

### Phase 4: Edge Case Testing (15-20 minutes)

**Goal:** Test branch detection and security

**Test 4.1: Production Branch Detection**

```bash
git checkout main  # Switch to production
/sprint-plan
```

**Expected Behavior:**
- ❌ Command blocks immediately
- ❌ Shows production branch warning
- ❌ Instructs user to switch to development
- ❌ Does NOT proceed with planning

**Test 4.2: Staging Branch Detection**

```bash
git checkout -b staging  # Create staging branch
/sprint-start
```

**Expected Behavior:**
- ⚠️ Command warns about staging
- ⚠️ Limited capabilities (can create issues, cannot modify code)
- ⚠️ Instructs to switch to development for execution

**Test 4.3: Development Branch (Normal)**

```bash
git checkout development  # Back to development
/sprint-plan
```

**Expected Behavior:**
- ✅ Full capabilities enabled
- ✅ No warnings
- ✅ Normal operation

**Validation:**
- [ ] Production branch blocked?
- [ ] Staging branch limited?
- [ ] Development branch full access?

### Phase 5: Error Handling (10-15 minutes)

**Goal:** Test graceful error handling

**Test 5.1: Invalid Configuration**

Temporarily rename `.env`:
```bash
mv .env .env.bak
/sprint-status
```

**Expected Behavior:**
- ❌ Clear error message about missing configuration
- ❌ Instructions to create .env
- ❌ No cryptic errors

**Test 5.2: Network Issues** (Simulate)

Stop Gitea or Wiki.js service temporarily:
```
/labels-sync
```

**Expected Behavior:**
- ❌ Connection error clearly stated
- ❌ Helpful troubleshooting suggestions
- ❌ No crashes or stack traces

**Test 5.3: Invalid Repository**

Edit `.env` with wrong repo name:
```bash
echo "GITEA_REPO=nonexistent-repo" > .env
/sprint-status
```

**Expected Behavior:**
- ❌ Repository not found error
- ❌ Suggestions to check .env configuration
- ❌ No silent failures

**Cleanup:**
```bash
mv .env.bak .env  # Restore configuration
```

## Success Metrics

### Technical Metrics

- [ ] All MCP servers connect successfully
- [ ] All 5 commands execute without errors
- [ ] All 3 agents exhibit correct personalities
- [ ] Branch detection works 100% accurately
- [ ] Labels sync correctly from Gitea
- [ ] Issues created with proper structure and labels
- [ ] Lessons learned saved to Wiki.js successfully
- [ ] No hardcoded secrets or absolute paths
- [ ] Error messages clear and actionable

### User Experience Metrics

- [ ] Commands intuitive to use
- [ ] Agent personalities distinct and helpful
- [ ] Planner asks relevant questions
- [ ] Orchestrator provides concise guidance
- [ ] Executor follows specs precisely
- [ ] Error messages helpful (not cryptic)
- [ ] Documentation clear and accurate

### Quality Metrics

- [ ] No crashes or unhandled exceptions
- [ ] Branch security enforced correctly
- [ ] Configuration validation works
- [ ] MCP tool integration seamless
- [ ] Label suggestions intelligent
- [ ] Lessons learned captured systematically

## Known Limitations (Phase 0.1.0)

1. **No Executor Integration** - Executor agent not yet invoked automatically by orchestrator (Phase 4)
2. **No Milestone Support** - Sprint milestones not implemented (Phase 4)
3. **No Dependencies Tracking** - Issue dependencies not automatically tracked (Phase 4)
4. **No Progress Updates** - Orchestrator doesn't automatically update issue comments (Phase 4)
5. **Manual Git Operations** - Git operations not automated yet (Phase 4)

These are expected at this stage and will be addressed in Phase 4 (Lessons Learned Integration).

## Troubleshooting Guide

### Issue: Commands not found

**Symptoms:** `/sprint-plan` returns "command not found"

**Solutions:**
1. Check marketplace loaded: `ls .claude-plugins/projman-test-marketplace/`
2. Verify plugin path in marketplace.json
3. Restart Claude Code

### Issue: MCP connection errors

**Symptoms:** "Failed to connect to Gitea" or "Failed to connect to Wiki.js"

**Solutions:**
1. Check system config exists: `ls ~/.config/claude/*.env`
2. Verify API URLs correct in config files
3. Test MCP servers manually (see Pre-Flight Checks)
4. Check network connectivity to services

### Issue: Repository not found

**Symptoms:** "Repository 'X' not found in organization"

**Solutions:**
1. Check `.env` file: `cat .env`
2. Verify `GITEA_REPO` matches actual repository name
3. Check Gitea organization matches `GITEA_OWNER` in system config
4. Verify API token has access to repository

### Issue: Lessons not saving to Wiki.js

**Symptoms:** "Failed to create lesson" or permission errors

**Solutions:**
1. Check Wiki.js API token has Pages (create) permission
2. Verify `WIKIJS_BASE_PATH` exists in Wiki.js
3. Check `WIKIJS_PROJECT` path is correct
4. Test Wiki.js connection (see Pre-Flight Checks)

### Issue: Branch detection not working

**Symptoms:** Can create issues on production branch

**Solutions:**
1. Verify git repository initialized: `git status`
2. Check branch name: `git branch --show-current`
3. Review agent prompts - branch check should be first operation
4. This is a critical bug - report immediately

## Next Steps After Testing

### If All Tests Pass ✅

1. **Document Findings**
   - Create test report with results
   - Note any minor issues encountered
   - Capture user experience feedback

2. **Move to Phase 4: Lessons Learned Integration**
   - Implement automatic issue updates
   - Add milestone support
   - Implement dependency tracking
   - Automate git operations

3. **Prepare for Phase 5: Testing & Validation**
   - Write integration tests
   - Test with real sprint on CuisineFlow
   - Collect user feedback from team

### If Tests Fail ❌

1. **Document Failures**
   - Exact error messages
   - Steps to reproduce
   - Expected vs actual behavior

2. **Categorize Issues**
   - Critical: Blocks basic functionality
   - High: Major feature doesn't work
   - Medium: Feature works but has issues
   - Low: Minor UX improvements

3. **Fix and Retest**
   - Fix critical issues first
   - Retest after each fix
   - Update documentation if needed

## Test Execution Log

### Test Session 1: [Date]

**Tester:** [Name]
**Duration:** [Time]
**Environment:**
- Branch: [branch name]
- Claude Code Version: [version]
- Plugin Version: 0.1.0

**Results:**

| Test | Status | Notes |
|------|--------|-------|
| Pre-Flight: MCP Connectivity | [ ] Pass / [ ] Fail | |
| Pre-Flight: Configuration | [ ] Pass / [ ] Fail | |
| 1.1: Label Sync | [ ] Pass / [ ] Fail | |
| 1.2: Sprint Status | [ ] Pass / [ ] Fail | |
| 2.1: Planner Agent | [ ] Pass / [ ] Fail | |
| 2.2: Orchestrator Agent | [ ] Pass / [ ] Fail | |
| 2.3: Executor Agent | [ ] Pass / [ ] Fail | |
| 3: Full Workflow | [ ] Pass / [ ] Fail | |
| 4: Branch Detection | [ ] Pass / [ ] Fail | |
| 5: Error Handling | [ ] Pass / [ ] Fail | |

**Overall Assessment:** [ ] Pass / [ ] Fail

**Critical Issues Found:** [Number]

**Recommendations:** [Next steps]

---

**Testing Status:** Ready to Begin
**Next Step:** Execute Pre-Flight Checks and Phase 1 Quick Validation
