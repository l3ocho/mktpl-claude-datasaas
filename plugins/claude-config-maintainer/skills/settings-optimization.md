# Settings Optimization Skill

This skill provides comprehensive knowledge for auditing and optimizing Claude Code `settings.local.json` permission configurations.

---

## Section 1: Settings File Locations & Format

Claude Code uses two configuration formats for permissions:

### Newer Format (Recommended)

**Primary target:** `.claude/settings.local.json` (project-local, gitignored)

**Secondary locations:**
- `.claude/settings.json` (shared, committed)
- `~/.claude.json` (legacy global config)

```json
{
  "permissions": {
    "allow": ["Edit", "Write(plugins/**)", "Bash(git *)"],
    "deny": ["Read(.env*)", "Bash(rm *)"],
    "ask": ["Bash(pip install *)"]
  }
}
```

**Field meanings:**
- `allow`: Operations auto-approved without prompting
- `deny`: Operations blocked entirely
- `ask`: Operations that always prompt (overrides allow)

### Legacy Format

Found in `~/.claude.json` with per-project entries:

```json
{
  "projects": {
    "/path/to/project": {
      "allowedTools": ["Read", "Write", "Bash(git *)"]
    }
  }
}
```

**Detection strategy:**
1. Check `.claude/settings.local.json` first (primary)
2. Check `.claude/settings.json` (shared)
3. Check `~/.claude.json` for project entry (legacy)
4. Report which format is in use

---

## Section 2: Permission Rule Syntax Reference

| Pattern | Meaning |
|---------|---------|
| `Tool` or `Tool(*)` | Allow all uses of that tool |
| `Bash(npm run build)` | Exact command match |
| `Bash(npm run test *)` | Prefix match (space+asterisk = word boundary) |
| `Bash(npm*)` | Prefix match without word boundary |
| `Write(plugins/**)` | Glob — all files recursively under `plugins/` |
| `Write(plugins/projman/*)` | Glob — direct children only |
| `Read(.env*)` | Pattern matching `.env`, `.env.local`, etc. |
| `mcp__gitea__*` | All tools from the gitea MCP server |
| `mcp__netbox__list_*` | Specific MCP tool pattern |
| `WebFetch(domain:github.com)` | Domain-restricted web fetch |

### Important Nuances

**Word boundary matching:**
- `Bash(ls *)` (with space) matches `ls -la` but NOT `lsof`
- `Bash(ls*)` (no space) matches both `ls -la` AND `lsof`

**Precedence rules:**
- `deny` rules take precedence over `allow` rules
- `ask` rules override both (always prompts even if allowed)
- More specific patterns do NOT override broader patterns

**Command operators:**
- Piped commands (`cmd1 | cmd2`) may not match individual command rules (known Claude Code limitation)
- Shell operators (`&&`, `||`) — Claude Code is aware of these and won't let prefix rules bypass them
- Commands with redirects (`>`, `>>`, `<`) are evaluated as complete strings

---

## Section 3: Pattern Consolidation Rules

The audit detects these optimization opportunities:

| Issue | Example | Recommendation |
|-------|---------|----------------|
| **Exact duplicates** | `Write(plugins/**)` listed twice | Remove duplicate |
| **Subset redundancy** | `Write(plugins/projman/*)` when `Write(plugins/**)` exists | Remove the narrower pattern — already covered |
| **Merge candidates** | `Write(plugins/projman/*)`, `Write(plugins/git-flow/*)`, `Write(plugins/pr-review/*)` ... (4+ similar patterns) | Merge to `Write(plugins/**)` |
| **Overly broad** | `Bash` (no specifier = allows ALL bash) | Flag as security concern, suggest scoped patterns |
| **Stale patterns** | `Write(plugins/old-plugin/**)` for a plugin that no longer exists | Remove stale entry |
| **Missing MCP permissions** | MCP servers in `.mcp.json` but no `mcp__servername__*` in allow | Suggest adding if server is trusted |
| **Conflicting rules** | Same pattern in both `allow` and `deny` | Flag conflict — deny wins, but allow is dead weight |

### Consolidation Algorithm

1. **Deduplicate:** Remove exact duplicates from each array
2. **Subset elimination:** For each pattern, check if a broader pattern exists
   - `Write(plugins/projman/*)` is subset of `Write(plugins/**)`
   - `Bash(git status)` is subset of `Bash(git *)`
3. **Merge detection:** If 4+ patterns share a common prefix, suggest merge
   - Threshold: 4 patterns minimum before suggesting consolidation
4. **Stale detection:** Cross-reference file patterns against actual filesystem
5. **Conflict detection:** Check for patterns appearing in multiple arrays

---

## Section 4: Review-Layer-Aware Recommendations

This is the key section. Map upstream review processes to directory scopes:

| Directory Scope | Active Review Layers | Auto-Allow Recommendation |
|----------------|---------------------|---------------------------|
| `plugins/*/commands/*.md` | Sprint approval, PR review | `Write(plugins/*/commands/**)` — 2 layers cover this |
| `plugins/*/skills/*.md` | Sprint approval, PR review | `Write(plugins/*/skills/**)` — 2 layers |
| `plugins/*/agents/*.md` | Sprint approval, PR review | `Write(plugins/*/agents/**)` — 2 layers |
| `mcp-servers/*/mcp_server/*.py` | Code-sentinel PreToolUse, sprint approval, PR review | `Write(mcp-servers/**)` + `Edit(mcp-servers/**)` — sentinel catches secrets |
| `docs/*.md` | PR review | `Write(docs/**)` + `Edit(docs/**)` — with caution flag |
| `.claude-plugin/*.json` | validate-marketplace.sh, PR review | `Write(.claude-plugin/**)` |
| `scripts/*.sh` | Code-sentinel, PR review | `Write(scripts/**)` — with caution flag |
| `CLAUDE.md`, `CHANGELOG.md`, `README.md` | PR review | `Write(CLAUDE.md)`, `Write(CHANGELOG.md)`, `Write(README.md)` |

### Critical Rule: Hook Verification

**Before recommending auto-allow for a scope, the agent MUST verify the hook is actually configured.**

Read the relevant `plugins/*/hooks/hooks.json` file:
- If code-sentinel's hook is missing or disabled, do NOT recommend auto-allowing `mcp-servers/**` writes
- If git-flow's hook is missing, do NOT recommend auto-allowing `Bash(git *)` operations
- If cmdb-assistant's hook is missing, do NOT recommend auto-allowing MCP netbox create/update operations
- Count the number of verified review layers before making recommendations

**Minimum threshold:** Only recommend auto-allow for scopes with ≥2 verified review layers.

---

## Section 5: Permission Profiles

Three named profiles for different project contexts:

### `conservative` (Default for New Users)

Minimal permissions, prompts for most write operations:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "LS",
      "Write(docs/**)",
      "Edit(docs/**)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(cat *)",
      "Bash(ls *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(wc *)",
      "Bash(grep *)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(./secrets/**)",
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  }
}
```

### `reviewed` (Projects with ≥2 Upstream Review Layers)

This is the target profile for projects using the marketplace's multi-layer review architecture:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "LS",
      "Edit",
      "Write",
      "MultiEdit",
      "Bash(git *)",
      "Bash(python *)",
      "Bash(pip install *)",
      "Bash(cd *)",
      "Bash(cat *)",
      "Bash(ls *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(wc *)",
      "Bash(grep *)",
      "Bash(find *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(mv *)",
      "Bash(touch *)",
      "Bash(chmod *)",
      "Bash(source *)",
      "Bash(echo *)",
      "Bash(sed *)",
      "Bash(awk *)",
      "Bash(sort *)",
      "Bash(uniq *)",
      "Bash(diff *)",
      "Bash(jq *)",
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(node *)",
      "Bash(pytest *)",
      "Bash(python -m *)",
      "Bash(./scripts/*)",
      "WebFetch",
      "WebSearch"
    ],
    "deny": [
      "Read(.env*)",
      "Read(./secrets/**)",
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(curl * | bash*)",
      "Bash(wget * | bash*)"
    ]
  }
}
```

### `autonomous` (Trusted CI/Sandboxed Environments Only)

Maximum permissions for automated environments:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "LS",
      "Edit",
      "Write",
      "MultiEdit",
      "Bash",
      "WebFetch",
      "WebSearch"
    ],
    "deny": [
      "Read(.env*)",
      "Read(./secrets/**)",
      "Bash(rm -rf /)",
      "Bash(sudo *)"
    ]
  }
}
```

**Warning:** The `autonomous` profile allows unscoped `Bash` — only use in fully sandboxed environments.

---

## Section 6: Scoring Criteria (Settings Efficiency Score — 100 points)

| Category | Points | What It Measures |
|----------|--------|------------------|
| **Redundancy** | 25 | No duplicates, no subset patterns, merged where possible |
| **Coverage** | 25 | Common tools allowed, MCP servers covered, no unnecessary gaps |
| **Safety Alignment** | 25 | Deny rules cover secrets, destructive commands; review layers verified |
| **Profile Fit** | 25 | How close to recommended profile for the project's review layer count |

### Scoring Breakdown

**Redundancy (25 points):**
- 25: No duplicates, no subsets, patterns are consolidated
- 20: 1-2 minor redundancies
- 15: 3-5 redundancies or 1 merge candidate group
- 10: 6+ redundancies or 2+ merge candidate groups
- 5: Significant redundancy (10+ issues)
- 0: Severe redundancy (20+ issues)

**Coverage (25 points):**
- 25: All common tools allowed, MCP servers covered
- 20: Missing 1-2 common tool patterns
- 15: Missing 3-5 patterns or 1 MCP server
- 10: Missing 6+ patterns or 2+ MCP servers
- 5: Significant gaps causing frequent prompts
- 0: Minimal coverage (prompts on most operations)

**Safety Alignment (25 points):**
- 25: Deny rules cover secrets + destructive ops, review layers verified
- 20: Minor gaps (e.g., missing one secret pattern)
- 15: Overly broad allow without review layer coverage
- 10: Missing deny rules for secrets or destructive commands
- 5: Unsafe patterns without review layer justification
- 0: Security concerns (e.g., unscoped `Bash` without review layers)

**Profile Fit (25 points):**
- 25: Matches recommended profile exactly
- 20: Within 90% of recommended profile
- 15: Within 80% of recommended profile
- 10: Within 70% of recommended profile
- 5: Significant deviation from recommended profile
- 0: No alignment with any named profile

### Score Interpretation

| Score Range | Status | Meaning |
|-------------|--------|---------|
| 90-100 | Optimized | Minimal prompt interruptions, safety maintained |
| 70-89 | Good | Minor consolidation opportunities |
| 50-69 | Needs Work | Significant redundancy or missing permissions |
| Below 50 | Poor | Likely getting constant approval prompts unnecessarily |

---

## Section 7: Hook Detection Method

To verify which review layers are active, read these files:

| File | Hook Type | Tool Matcher | Purpose |
|------|-----------|--------------|---------|
| `plugins/code-sentinel/hooks/hooks.json` | PreToolUse | Write\|Edit\|MultiEdit | Blocks hardcoded secrets |
| `plugins/git-flow/hooks/hooks.json` | PreToolUse | Bash | Branch naming + commit format |
| `plugins/cmdb-assistant/hooks/hooks.json` | PreToolUse | MCP create/update | NetBox input validation |
| `plugins/clarity-assist/hooks/hooks.json` | UserPromptSubmit | (all prompts) | Vagueness detection |

### Verification Process

1. **Read each hooks.json file**
2. **Parse the JSON to find hook configurations**
3. **Check the `type` field** — must be `"command"` (not `"prompt"`)
4. **Check the `event` field** — maps to when hook runs
5. **Check the `tools` array** — which operations are intercepted
6. **Verify plugin is in marketplace** — check `.claude-plugin/marketplace.json`

### Example Hook Structure

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "type": "command",
      "command": "./hooks/security-check.sh",
      "tools": ["Write", "Edit", "MultiEdit"]
    }
  ]
}
```

### Review Layer Count

Count verified review layers for each scope:

| Layer | Verification |
|-------|-------------|
| Sprint approval | Check if projman plugin is installed (milestone workflow) |
| PR review | Check if pr-review plugin is installed |
| code-sentinel PreToolUse | hooks.json exists with PreToolUse on Write/Edit/MultiEdit |
| git-flow PreToolUse | hooks.json exists with PreToolUse on Bash |
| cmdb-assistant PreToolUse | hooks.json exists with PreToolUse on MCP create/update |

**Recommendation threshold:** Only recommend auto-allow for scopes with ≥2 verified layers.
