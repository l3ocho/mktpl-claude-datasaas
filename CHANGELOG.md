# Changelog

All notable changes to the Leo Claude Marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Fixed

- Confirmed projman `metadata.json` exists with gitea MCP mapping
- Synced `marketplace-full.json` and `marketplace-lean.json` to current version (were stale)
- Added `metadata.json` validation to `validate-marketplace.sh` — rejects `mcp_servers` in `plugin.json`, verifies MCP server references
- Updated `CANONICAL-PATHS.md` to current version

### Changed

- Deprecated `switch-profile.sh` in favor of `claude-launch.sh`

---

## [7.1.0] - 2026-02-04

### Added

- **marketplace:** Task-specific launcher script for token optimization
  - New script: `scripts/claude-launch.sh` loads only needed plugins via `--plugin-dir`
  - Profiles: sprint (default), review, data, infra, full
  - Reduces token overhead from ~22K to ~4-6K tokens
  - Enables `ENABLE_TOOL_SEARCH=true` for MCP lazy loading
- **marketplace:** Lean/full profile config files for manual switching (superseded by `claude-launch.sh`)
  - Files: `.mcp-lean.json`, `.mcp-full.json`, `marketplace-lean.json`, `marketplace-full.json`
  - Script `scripts/switch-profile.sh` available but `claude-launch.sh` is the recommended approach
  - Full profile remains the default baseline; launcher handles selective loading
- **projman:** Token usage estimation reporting at sprint workflow boundaries
  - New skill: `token-budget-report.md` with MCP overhead and skill loading estimation model
  - Token report displayed at end of `/sprint-plan` and `/sprint-close`
  - On-demand via `/sprint-status --tokens`
  - Helps identify which phases and components consume the most context budget

### Changed

- **projman:** `/sprint-status` now uses conditional skill loading for reduced token overhead
  - Only loads `mcp-tools-reference.md` by default (~1.5k tokens vs ~5k)
  - `--diagram` flag loads `dependency-management.md` and `progress-tracking.md`
  - `--tokens` flag loads `token-budget-report.md`
  - Estimated savings: ~3.5k tokens per status check

### Fixed

- **docs:** Stale command references in data-platform visual-header.md and viz-platform claude-md-integration.md updated to v7.0.0 namespaced names
- **docs:** git-flow visual-header.md and git-status.md quick actions updated to namespaced commands
- **docs:** projman/CONFIGURATION.md and docs/DEBUGGING-CHECKLIST.md updated with correct command names

---

## [7.0.0] - 2026-02-03

### BREAKING CHANGES

#### Command Namespace Rename

All generic command names are now prefixed with their plugin's namespace to eliminate collisions across the marketplace. This is a **breaking change** for consuming projects — update your CLAUDE.md integration snippets.

**Full Rename Map:**

| Plugin | Old | New |
|--------|-----|-----|
| projman | `/setup` | `/pm-setup` |
| projman | `/review` | `/pm-review` |
| projman | `/test` | `/pm-test` |
| projman | `/debug` | `/pm-debug` |
| git-flow | `/commit` | `/git-commit` |
| git-flow | `/commit-push` | `/git-commit-push` |
| git-flow | `/commit-merge` | `/git-commit-merge` |
| git-flow | `/commit-sync` | `/git-commit-sync` |
| pr-review | `/initial-setup` | `/pr-setup` |
| cmdb-assistant | `/initial-setup` | `/cmdb-setup` |
| data-platform | `/initial-setup` | `/data-setup` |
| data-platform | `/run` | `/data-run` |
| data-platform | `/ingest` | `/data-ingest` |
| data-platform | `/profile` | `/data-profile` |
| data-platform | `/schema` | `/data-schema` |
| data-platform | `/explain` | `/data-explain` |
| data-platform | `/lineage` | `/data-lineage` |
| viz-platform | `/initial-setup` | `/viz-setup` |
| viz-platform | `/theme` | `/viz-theme` |
| viz-platform | `/theme-new` | `/viz-theme-new` |
| viz-platform | `/theme-css` | `/viz-theme-css` |
| viz-platform | `/chart` | `/viz-chart` |
| viz-platform | `/chart-export` | `/viz-chart-export` |
| viz-platform | `/dashboard` | `/viz-dashboard` |
| viz-platform | `/component` | `/viz-component` |
| viz-platform | `/breakpoints` | `/viz-breakpoints` |
| contract-validator | `/initial-setup` | `/cv-setup` |

**Migration:** Update your project's CLAUDE.md integration snippets to use the new command names. Run `/plugin list` to verify installed plugins are using v7.0.0+.

**Unchanged:** Commands already using plugin-namespaced prefixes (`/sprint-*`, `/cmdb-*`, `/labels-sync`, `/branch-*`, `/git-status`, `/git-config`, `/pr-review`, `/pr-summary`, `/pr-findings`, `/pr-diff`, `/project-init`, `/project-sync`, `/config-*`, `/design-*`, `/data-quality`, `/data-review`, `/data-gate`, `/lineage-viz`, `/dbt-test`, `/accessibility-check`, `/validate-contracts`, `/check-agent`, `/list-interfaces`, `/dependency-graph`, `/doc-audit`, `/doc-sync`, `/security-scan`, `/refactor`, `/refactor-dry`, `/clarify`, `/suggest-version`, `/proposal-status`, `/rfc`, `/change-audit`, `/ip-conflicts`) are **not affected**.

### Added

#### Plan-Then-Batch Skill Optimization (projman)

New execution pattern that separates cognitive work from mechanical API operations, reducing skill-related token consumption by ~76-83% during sprint workflows.

- **`skills/batch-execution.md`** — New skill defining the plan-then-batch protocol:
  - Phase 1: Cognitive work with all skills loaded
  - Phase 2: Execution manifest (structured plan of all API operations)
  - Phase 3: Batch execute API calls using only frontmatter skills
  - Phase 4: Batch report with success/failure summary
  - Error handling: continue on individual failures, report at end

- **Frontmatter skill promotion:**
  - Planner agent: `mcp-tools-reference` and `batch-execution` promoted to frontmatter (auto-injected, zero re-read cost)
  - Orchestrator agent: same promotion
  - Eliminates per-operation skill file re-reads during API execution loops

- **Phase-based skill loading:**
  - Planner: 3 phases (validation → analysis → approval) with explicit "read once" instructions
  - Orchestrator: 2 phases (startup → dispatch) with same pattern
  - New `## Skill Loading Protocol` section replaces flat `## Skills to Load` in agent files

### Changed

- **`planning-workflow.md`** — Steps 8-10 restructured:
  - Step 8: "Draft Issue Specifications" (no API calls — resolve all parameters first)
  - Step 8a: "Batch Execute Issue Creation" (tight API loop, frontmatter skills only)
  - Step 9: Merged into Step 8a (dependencies created in batch)
  - Step 10: Milestone creation moved before batch (must exist for assignment)

- **Agent matrix updated:**
  - Planner: `body text (14)` → `frontmatter (2) + body text (12)`
  - Orchestrator: `body text (12)` → `frontmatter (2) + body text (10)`

- **`docs/CONFIGURATION.md`** — New "Phase-Based Skill Loading" subsection documenting the pattern

### Token Impact

| Scenario | Before | After | Savings |
|----------|--------|-------|---------|
| 6-issue sprint (planning) | ~23,800 lines | ~5,600 lines | ~76% |
| 10-issue sprint (planning) | ~35,000 lines | ~7,000 lines | ~80% |
| 8-issue status updates (orchestrator) | ~9,600 lines | ~1,600 lines | ~83% |

---

## [5.10.0] - 2026-02-03

### Added

#### NetBox MCP Server: Module-Based Tool Filtering

Environment-variable-driven module filtering to reduce token consumption:

- **New config option**: `NETBOX_ENABLED_MODULES` in `~/.config/claude/netbox.env`
- **Token savings**: ~15,000 tokens (from ~19,810 to ~4,500) with recommended config
- **Default behavior**: All modules enabled if env var unset (backward compatible)
- **Startup logging**: Shows enabled modules and tool count on initialization
- **Routing guard**: Clear error message when calling disabled module's tools

**Recommended configuration for cmdb-assistant users:**
```bash
NETBOX_ENABLED_MODULES=dcim,ipam,virtualization,extras
```

This enables ~43 tools covering all cmdb-assistant commands while staying well below the 25K token warning threshold.

### Fixed

#### cmdb-assistant Documentation: Incorrect Tool Names

Fixed documentation referencing non-existent `virtualization_*` tool names:

| File | Wrong | Correct |
|------|-------|---------|
| `claude-md-integration.md` | `virtualization_list_virtual_machines` | `virt_list_vms` |
| `claude-md-integration.md` | `virtualization_create_virtual_machine` | `virt_create_vm` |
| `cmdb-search.md` | `virtualization_list_virtual_machines` | `virt_list_vms` |

Also fixed NetBox README.md tool name references for virtualization, wireless, and circuits modules.

#### Gitea MCP Server: Standardized Build Backend

Changed `mcp-servers/gitea/pyproject.toml` from hatchling to setuptools:
- Matches all other MCP servers (contract-validator, viz-platform, data-platform)
- Updated license format to PEP 639 compliance
- Added pytest configuration for consistency

---

## [5.9.0] - 2026-02-03

### Added

#### Plugin Installation Scripts
New scripts for installing marketplace plugins into consumer projects:

- **`scripts/install-plugin.sh`** — Install a plugin to a consumer project
  - Adds MCP server entry to target's `.mcp.json` (if plugin has MCP server)
  - Appends integration snippet to target's `CLAUDE.md`
  - Idempotent: safe to run multiple times
  - Validates plugin exists and target path is valid

- **`scripts/uninstall-plugin.sh`** — Remove a plugin from a consumer project
  - Removes MCP server entry from `.mcp.json`
  - Removes integration section from `CLAUDE.md`

- **`scripts/list-installed.sh`** — Show installed plugins in a project
  - Lists fully installed, partially installed, and available plugins
  - Shows plugin versions and descriptions

**Usage:**
```bash
./scripts/install-plugin.sh data-platform ~/projects/personal-portfolio
./scripts/list-installed.sh ~/projects/personal-portfolio
./scripts/uninstall-plugin.sh data-platform ~/projects/personal-portfolio
```

**Documentation:** `docs/CONFIGURATION.md` updated with "Installing Plugins to Consumer Projects" section.

### Fixed

#### Plugin Installation Scripts — MCP Mapping & Section Markers

**MCP Server Mapping:**
- Added `mcp_servers` field to plugin.json for plugins that use shared MCP servers
- `projman` and `pr-review` now correctly install `gitea` MCP server
- `cmdb-assistant` now correctly installs `netbox` MCP server
- Scripts read MCP server names from plugin.json instead of assuming plugin name = server name

**CLAUDE.md Section Markers:**
- Install script now wraps integration content with HTML comment markers:
  `<!-- BEGIN marketplace-plugin: {name} -->` and `<!-- END marketplace-plugin: {name} -->`
- Uninstall script uses markers for precise section removal (no more code block false positives)
- Backward compatible: falls back to legacy header detection for pre-marker installations

**Plugins updated with `mcp_servers` field:**
- `projman` → `["gitea"]`
- `pr-review` → `["gitea"]`
- `cmdb-assistant` → `["netbox"]`
- `data-platform` → `["data-platform"]`
- `viz-platform` → `["viz-platform"]`
- `contract-validator` → `["contract-validator"]`

#### Agent Model Selection

Per-agent model selection using Claude Code's now-supported `model` frontmatter field.

- All 25 marketplace agents assigned appropriate model (`sonnet`, `haiku`, or `inherit`)
- Model assignment based on reasoning depth, tool complexity, and latency requirements
- Documentation added to `CLAUDE.md` and `docs/CONFIGURATION.md`

**Supported values:** `sonnet` (default), `opus`, `haiku`, `inherit`

**Model assignments:**
| Model | Agent Types |
|-------|-------------|
| sonnet | Planner, Orchestrator, Executor, Code Reviewer, Coordinator, Security Reviewers, Data Advisor, Design Reviewer, etc. |
| haiku | Maintainability Auditor, Test Validator, Component Check, Theme Setup, Git Assistant, Data Ingestion, Agent Check |

### Fixed

#### Agent Frontmatter Standardization

- Fixed viz-platform and data-platform agents using non-standard `agent:` field (now `name:`)
- Removed non-standard `triggers:` field from domain agents (trigger info already in agent body)
- Added missing frontmatter to 13 agents across pr-review, viz-platform, contract-validator, clarity-assist, git-flow, doc-guardian, code-sentinel, cmdb-assistant, and data-platform
- All 25 agents now have consistent `name`, `description`, and `model` fields

### Changed

#### Agent Frontmatter Hardening v3

Comprehensive agent-level configuration using Claude Code's supported frontmatter fields.

**permissionMode added to all 25 agents:**
- `bypassPermissions` (1): Executor — full autonomy with code-sentinel + Code Reviewer safety nets
- `acceptEdits` (7): Orchestrator, Data Ingestion, Theme Setup, Refactor Advisor, Doc Analyzer, Git Assistant, Maintainer
- `default` (7): Planner, Code Reviewer, Data Advisor, Layout Builder, Full Validation, Clarity Coach, CMDB Assistant
- `plan` (10): All pr-review agents (5), Data Analysis, Design Reviewer, Component Check, Agent Check, Security Reviewer (code-sentinel)

**disallowedTools added to 12 agents:**
- All `plan`-mode agents (10) + Code Reviewer + Clarity Coach receive `disallowedTools: Write, Edit, MultiEdit`
- Enforces read-only contracts at platform level (defense-in-depth with `permissionMode`)

**Model promotions:**
- Planner: `sonnet` → `opus` (architectural reasoning benefits from deeper analysis)
- Code Reviewer: `sonnet` → `opus` (quality gate benefits from thorough review)

**skills frontmatter on 3 agents:**
- Executor: 7 safety-critical skills auto-injected (branch-security, runaway-detection, etc.)
- Code Reviewer: 4 review skills auto-injected
- Maintainer: 2 config skills auto-injected
- Body text `## Skills to Load` removed for these agents to avoid duplication

**Documentation:**
- `CLAUDE.md` and `docs/CONFIGURATION.md` updated with complete agent configuration matrix
- New subsections: permissionMode Guide, disallowedTools Guide, skills Frontmatter Guide

---

## [5.8.0] - 2026-02-02

### Added

#### claude-config-maintainer v1.2.0 - Settings Audit Feature

New commands for auditing and optimizing `settings.local.json` permission configurations:

- **`/config-audit-settings`** — Audit `settings.local.json` permissions with 100-point scoring across redundancy, coverage, safety alignment, and profile fit
- **`/config-optimize-settings`** — Apply permission optimizations with dry-run, named profiles (`conservative`, `reviewed`, `autonomous`), and consolidation modes
- **`/config-permissions-map`** — Generate Mermaid diagram of review layer coverage and permission gaps
- **`skills/settings-optimization.md`** — Comprehensive skill for permission pattern analysis, consolidation rules, review-layer-aware recommendations, and named profiles

**Key Features:**
- Settings Efficiency Score (100 points) alongside existing CLAUDE.md score
- Review layer verification — agent reads `hooks/hooks.json` from installed plugins before recommending auto-allow patterns
- Three named profiles: `conservative` (prompts for most writes), `reviewed` (for projects with ≥2 review layers), `autonomous` (sandboxed environments)
- Pattern consolidation detection: duplicates, subsets, merge candidates, stale entries, conflicts

#### Projman Hardening Sprint
Targeted improvements to safety gates, command structure, lifecycle tracking, and cross-plugin contracts.

**Sprint Lifecycle State Machine:**
- New `skills/sprint-lifecycle.md` - defines valid states and transitions via milestone metadata
- States: idle -> Sprint/Planning -> Sprint/Executing -> Sprint/Reviewing -> idle
- All sprint commands check and set lifecycle state on entry/exit
- Out-of-order calls produce warnings with guidance, `--force` override available

**Sprint Dispatch Log:**
- Orchestrator now maintains a structured dispatch log during execution
- Records task dispatch, completion, failure, gate checks, and resume events
- Enables timeline reconstruction after interrupted sessions

**Gate Contract Versioning:**
- Gate commands (`/design-gate`, `/data-gate`) declare `gate_contract: v1` in frontmatter
- `domain-consultation.md` Gate Command Reference includes expected contract version
- `validate_workflow_integration` now checks contract version compatibility
- Mismatch produces WARNING, missing contract produces INFO suggestion

**Shared Visual Output Skill:**
- New `skills/visual-output.md` - single source of truth for projman visual headers
- All 4 agent files reference the skill instead of inline templates
- Phase Registry maps agents to emoji and phase names

### Changed

**Sprint Approval Gate Hardened:**
- Approval is now a hard block, not a warning (was "recommended", now required)
- `--force` flag added to bypass in emergencies (logged to milestone)
- Consistent language across sprint-approval.md, sprint-start.md, and orchestrator.md

**RFC Commands Normalized:**
- 5 individual commands (`/rfc-create`, `/rfc-list`, `/rfc-review`, `/rfc-approve`, `/rfc-reject`) consolidated into `/rfc create|list|review|approve|reject`
- `/clear-cache` absorbed into `/setup --clear-cache`
- Command count reduced from 17 to 12

**`/test` Command Documentation Expanded:**
- Sprint integration section (pre-close verification workflow)
- Concrete usage examples for all modes
- Edge cases table
- DO NOT rules for both modes

### Removed

- `plugins/projman/commands/rfc-create.md` (replaced by `/rfc create`)
- `plugins/projman/commands/rfc-list.md` (replaced by `/rfc list`)
- `plugins/projman/commands/rfc-review.md` (replaced by `/rfc review`)
- `plugins/projman/commands/rfc-approve.md` (replaced by `/rfc approve`)
- `plugins/projman/commands/rfc-reject.md` (replaced by `/rfc reject`)
- `plugins/projman/commands/clear-cache.md` (replaced by `/setup --clear-cache`)

---

## [5.7.1] - 2026-02-02

### Added
- **contract-validator**: New `validate_workflow_integration` MCP tool — validates domain plugins expose required advisory interfaces (gate command, review command, advisory agent)
- **contract-validator**: New `MISSING_INTEGRATION` issue type for workflow integration validation

### Fixed
- `scripts/setup.sh` banner version updated from v5.1.0 to v5.7.1

### Reverted
- **marketplace.json**: Removed `integrates_with` field — Claude Code schema does not support custom plugin fields (causes marketplace load failure)

---

## [5.7.0] - 2026-02-02

### Added
- **data-platform**: New `data-advisor` agent for data integrity, schema, and dbt compliance validation
- **data-platform**: New `data-integrity-audit.md` skill defining audit rules, severity levels, and scanning strategies
- **data-platform**: New `/data-gate` command for binary pass/fail data integrity gates (projman integration)
- **data-platform**: New `/data-review` command for comprehensive data integrity audits

### Changed
- Domain Advisory Pattern now fully operational for both Viz and Data domains
- projman orchestrator `Domain/Data` gates now resolve to live `/data-gate` command (previously fell through to "gate unavailable" warning)

---

## [5.6.0] - 2026-02-01

### Added
- **Domain Advisory Pattern**: Cross-plugin integration enabling projman to consult domain-specific plugins during sprint lifecycle
- **projman**: New `domain-consultation.md` skill for domain detection and gate protocols
- **viz-platform**: New `design-reviewer` agent for design system compliance auditing
- **viz-platform**: New `design-system-audit.md` skill defining audit rules and severity levels
- **viz-platform**: New `/design-review` command for detailed design system audits
- **viz-platform**: New `/design-gate` command for binary pass/fail validation gates
- **Labels**: New `Domain/Viz` and `Domain/Data` labels for domain routing

### Changed
- **projman planner**: Now loads domain-consultation skill and performs domain detection during planning
- **projman orchestrator**: Now runs domain gates before marking Domain/* labeled issues as complete

---

## [5.5.0] - 2026-02-01

### Added

#### RFC System for Feature Tracking
Wiki-based Request for Comments (RFC) system for capturing, reviewing, and tracking feature ideas through their lifecycle.

**New Commands (projman):**
- `/rfc-create` - Create new RFC from conversation or clarified specification
- `/rfc-list` - List all RFCs grouped by status (Draft, Review, Approved, Implementing, Implemented, Rejected, Stale)
- `/rfc-review` - Submit Draft RFC for maintainer review
- `/rfc-approve` - Approve RFC, making it available for sprint planning
- `/rfc-reject` - Reject RFC with documented reason

**RFC Lifecycle:**
- Draft → Review → Approved → Implementing → Implemented
- Terminal states: Rejected, Superseded
- Stale: Drafts with no activity >90 days

**Sprint Integration:**
- `/sprint-plan` now detects approved RFCs and offers selection
- `/sprint-close` updates RFC status to Implemented on completion
- RFC-Index wiki page auto-maintained with status sections

**Clarity-Assist Integration:**
- Vagueness hook now detects feature request patterns
- Suggests `/rfc-create` for feature ideas
- `/clarify` offers RFC creation after delivering clarified spec

**New MCP Tool:**
- `allocate_rfc_number` - Allocates next sequential RFC number

**New Skills:**
- `skills/rfc-workflow.md` - RFC lifecycle and state transitions
- `skills/rfc-templates.md` - RFC page template specifications

### Changed

#### Sprint 8: Hook Efficiency Quick Wins
Performance optimizations for plugin hooks to reduce overhead on every command.

**Changes:**
- **viz-platform:** Remove SessionStart hook that only echoed "loaded" (zero value)
- **git-flow:** Add early exit to `branch-check.sh` for non-git commands (skip JSON parsing)
- **git-flow:** Add early exit to `commit-msg-check.sh` for non-git commands (skip Python spawn)
- **project-hygiene:** Add 60-second cooldown to `cleanup.sh` (reduce find operations)

**Impact:** Hooks now exit immediately for 90%+ of Bash commands that don't need processing.

**Issues:** #321, #322, #323, #324
**PR:** #334

---

## [5.4.1] - 2026-01-30

### Removed

#### Multi-Model Agent Support (REVERTED)

**Reason:** Claude Code does not support `defaultModel` in plugin.json or `model` in agent frontmatter. The schema validation rejects these as "Unrecognized key".

**Removed:**
- `defaultModel` field from all plugin.json files (6 plugins)
- `model` field references from agent frontmatter
- `docs/MODEL-RECOMMENDATIONS.md` - Deleted entirely
- Model configuration sections from `docs/CONFIGURATION.md` and `CLAUDE.md`

**Lesson:** Do not implement features without verifying they are supported by Claude Code's plugin schema.

---

## [5.4.0] - 2026-01-28 [REVERTED]

### Added (NOW REMOVED - See 5.4.1)

#### Sprint 7: Multi-Model Agent Support
~~Configurable model selection for agents with inheritance chain.~~

**This feature was reverted in 5.4.1 - Claude Code does not support these fields.**

Original sprint work:
- Issues: #302, #303, #304, #305, #306
- PRs: #307, #308

---

## [5.3.0] - 2026-01-28

### Added

#### Sprint 6: Visual Branding Overhaul
Consistent visual headers and progress tracking across all plugins.

**Visual Output Headers (109 files):**
- **Projman**: Double-line headers (╔═╗) with phase indicators (🎯 PLANNING, ⚡ EXECUTION, 🏁 CLOSING)
- **Other Plugins**: Single-line headers (┌─┐) with plugin icons
- **All 23 agents** updated with Visual Output Requirements section
- **All 86 commands** updated with Visual Output section and header templates

**Plugin Icon Registry:**
| Plugin | Icon |
|--------|------|
| projman | 📋 |
| code-sentinel | 🔒 |
| doc-guardian | 📝 |
| pr-review | 🔍 |
| clarity-assist | 💬 |
| git-flow | 🔀 |
| cmdb-assistant | 🖥️ |
| data-platform | 📊 |
| viz-platform | 🎨 |
| contract-validator | ✅ |
| claude-config-maintainer | ⚙️ |

**Wiki Branding Specification (4 pages):**
- [branding/visual-spec](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/branding%2Fvisual-spec) - Central specification
- [branding/plugin-registry](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/branding%2Fplugin-registry) - Icons and styles
- [branding/header-templates](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/branding%2Fheader-templates) - Copy-paste templates
- [branding/progress-templates](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/branding%2Fprogress-templates) - Sprint progress blocks

### Fixed
- **Docs:** Version sync - CLAUDE.md, marketplace.json, README.md now consistent
- **Docs:** Added 18 missing commands from Sprint 4 & 5 to README.md and COMMANDS-CHEATSHEET.md
- **MCP:** Registered `/sprint-diagram` as invokable skill

**Sprint Completed:**
- Milestone: Sprint 6 - Visual Branding Overhaul (closed 2026-01-28)
- Issues: #272, #273, #274, #275, #276, #277, #278
- PRs: #284, #285
- Wiki: [Sprint 6 Lessons](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/lessons/sprints/sprint-6---visual-branding-and-documentation-maintenance)

---

## [5.2.0] - 2026-01-28

### Added

#### Sprint 5: Documentation (V5.2.0 Plugin Enhancements)
Documentation and guides for the plugin enhancements initiative.

**git-flow v1.2.0:**
- **Branching Strategy Guide** (`docs/BRANCHING-STRATEGY.md`) - Complete documentation of `development -> staging -> main` promotion flow with Mermaid diagrams

**clarity-assist v1.2.0:**
- **ND Support Guide** (`docs/ND-SUPPORT.md`) - Documentation of neurodivergent accommodations, features, and usage examples

**Gitea MCP Server:**
- **`update_issue` milestone parameter** - Can now assign/change milestones programmatically

**Sprint Completed:**
- Milestone: Sprint 5 - Documentation (closed 2026-01-28)
- Issues: #266, #267, #268, #269
- Wiki: [Change V5.2.0: Plugin Enhancements (Sprint 5 Documentation)](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/Change-V5.2.0%3A-Plugin-Enhancements-%28Sprint-5-Documentation%29)

---

#### Sprint 4: Commands (V5.2.0 Plugin Enhancements)
Implementation of 18 new user-facing commands across 8 plugins.

**projman v3.3.0:**
- **`/sprint-diagram`** - Generate Mermaid diagram of sprint issues with dependencies and status

**pr-review v1.1.0:**
- **`/pr-diff`** - Formatted diff with inline review comments and annotations
- **Confidence threshold config** - `PR_REVIEW_CONFIDENCE_THRESHOLD` env var (default: 0.7)

**data-platform v1.2.0:**
- **`/data-quality`** - DataFrame quality checks (nulls, duplicates, types, outliers) with pass/warn/fail scoring
- **`/lineage-viz`** - dbt lineage visualization as Mermaid diagrams
- **`/dbt-test`** - Formatted dbt test runner with summary and failure details

**viz-platform v1.1.0:**
- **`/chart-export`** - Export charts to PNG, SVG, PDF via kaleido
- **`/accessibility-check`** - Color blind validation (WCAG contrast ratios)
- **`/breakpoints`** - Responsive layout breakpoint configuration
- **New MCP tools**: `chart_export`, `accessibility_validate_colors`, `accessibility_validate_theme`, `accessibility_suggest_alternative`, `layout_set_breakpoints`
- **New dependency**: kaleido>=0.2.1 for chart rendering

**contract-validator v1.2.0:**
- **`/dependency-graph`** - Mermaid visualization of plugin dependencies with data flow

**doc-guardian v1.1.0:**
- **`/changelog-gen`** - Generate changelog from conventional commits
- **`/doc-coverage`** - Documentation coverage metrics by function/class
- **`/stale-docs`** - Flag documentation behind code changes

**claude-config-maintainer v1.1.0:**
- **`/config-diff`** - Track CLAUDE.md changes over time with behavioral impact analysis
- **`/config-lint`** - 31 lint rules for CLAUDE.md (security, structure, content, format, best practices)

**cmdb-assistant v1.2.0:**
- **`/cmdb-topology`** - Infrastructure topology diagrams (rack, network, site views)
- **`/change-audit`** - NetBox audit trail queries with filtering
- **`/ip-conflicts`** - Detect IP conflicts and overlapping prefixes

**Sprint Completed:**
- Milestone: Sprint 4 - Commands (closed 2026-01-28)
- Issues: #241-#258 (18/18 closed)
- Wiki: [Change V5.2.0: Plugin Enhancements (Sprint 4 Commands)](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/Change-V5.2.0%3A-Plugin-Enhancements-%28Sprint-4-Commands%29)
- Lessons: [Sprint 4 - Plugin Commands Implementation](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/lessons/sprints/sprint-4---plugin-commands-implementation)

### Fixed
- **MCP:** Project directory detection - all run.sh scripts now capture `CLAUDE_PROJECT_DIR` from PWD before changing directories
- **Docs:** Added Gitea auto-close behavior and MCP session restart notes to DEBUGGING-CHECKLIST.md

---

#### Sprint 3: Hooks (V5.2.0 Plugin Enhancements)
Implementation of 6 foundational hooks across 4 plugins.

**git-flow v1.1.0:**
- **Commit message enforcement hook** - PreToolUse hook validates conventional commit format on all `git commit` commands (not just `/commit`). Blocks invalid commits with format guidance.
- **Branch name validation hook** - PreToolUse hook validates branch naming on `git checkout -b` and `git switch -c`. Enforces `type/description` format, lowercase, max 50 chars.

**clarity-assist v1.1.0:**
- **Vagueness detection hook** - UserPromptSubmit hook detects vague prompts and suggests `/clarify` when ambiguity, missing context, or unclear scope detected.

**data-platform v1.1.0:**
- **Schema diff detection hook** - PostToolUse hook monitors edits to schema files (dbt models, SQL migrations). Warns on breaking changes (column removal, type narrowing, constraint addition).

**contract-validator v1.1.0:**
- **SessionStart auto-validate hook** - Smart validation that only runs when plugin files changed since last check. Detects interface compatibility issues at session start.
- **Breaking change detection hook** - PostToolUse hook monitors plugin interface files (README.md, plugin.json). Warns when changes would break consumers.

**Sprint Completed:**
- Milestone: Sprint 3 - Hooks (closed 2026-01-28)
- Issues: #225, #226, #227, #228, #229, #230
- Wiki: [Change V5.2.0: Plugin Enhancements Proposal](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/Change-V5.2.0:-Plugin-Enhancements-Proposal)
- Lessons: Background agent permissions, agent runaway detection, MCP branch detection bug

### Known Issues
- **MCP Bug #231:** Branch detection in Gitea MCP runs from installed plugin directory, not user's project directory. Workaround: close issues via Gitea web UI.

---

#### Gitea MCP Server - create_pull_request Tool
- **`create_pull_request`**: Create new pull requests via MCP
  - Parameters: title, body, head (source branch), base (target branch), labels
  - Branch-aware security: only allowed on development/feature branches
  - Completes the PR lifecycle (was previously missing - only had list/get/review/comment)

#### cmdb-assistant v1.1.0 - Data Quality Validation
- **SessionStart Hook**: Tests NetBox API connectivity at session start
  - Warns if VMs exist without site assignment
  - Warns if devices exist without platform
  - Non-blocking: displays warning, doesn't prevent work
- **PreToolUse Hook**: Validates input parameters before VM/device operations
  - Warns about missing site, tenant, platform
  - Non-blocking: suggests best practices without blocking
- **`/cmdb-audit` Command**: Comprehensive data quality analysis
  - Scopes: all, vms, devices, naming, roles
  - Identifies Critical/High/Medium/Low issues
  - Provides prioritized remediation recommendations
- **`/cmdb-register` Command**: Register current machine into NetBox
  - Discovers system info: hostname, platform, hardware, network interfaces
  - Discovers running apps: Docker containers, systemd services
  - Creates device with interfaces, IPs, and sets primary IP
  - Creates cluster and VMs for Docker containers
- **`/cmdb-sync` Command**: Sync machine state with NetBox
  - Compares current state with NetBox record
  - Shows diff of changes (interfaces, IPs, containers)
  - Updates with user confirmation
  - Supports --full and --dry-run flags
- **NetBox Best Practices Skill**: Reference documentation
  - Dependency order for object creation
  - Naming conventions (`{role}-{site}-{number}`, `{env}-{app}-{number}`)
  - Role consolidation guidance
  - Site/tenant/platform assignment requirements
- **Agent Enhancement**: Updated cmdb-assistant agent with validation requirements
  - Proactive suggestions for missing fields
  - Naming convention checks
  - Dependency order enforcement
  - Duplicate prevention

---

## [5.0.0] - 2026-01-26

### Added

#### Sprint 1: viz-platform Plugin ✅ Completed
- **viz-platform** v1.0.0 - Visualization tools with Dash Mantine Components validation and theming
  - **DMC Tools** (3 tools): `list_components`, `get_component_props`, `validate_component`
    - Version-locked component registry prevents Claude from hallucinating invalid props
    - Static JSON registry approach for fast, deterministic validation
  - **Chart Tools** (2 tools): `chart_create`, `chart_configure_interaction`
    - Plotly-based visualization with theme token support
  - **Layout Tools** (5 tools): `layout_create`, `layout_add_filter`, `layout_set_grid`, `layout_get`, `layout_add_section`
    - Dashboard composition with responsive grid system
  - **Theme Tools** (6 tools): `theme_create`, `theme_extend`, `theme_validate`, `theme_export_css`, `theme_list`, `theme_activate`
    - Design token-based theming system
    - Dual storage: user-level (`~/.config/claude/themes/`) and project-level
  - **Page Tools** (5 tools): `page_create`, `page_add_navbar`, `page_set_auth`, `page_list`, `page_get_app_config`
    - Multi-page Dash app structure generation
  - **Commands**: `/chart`, `/dashboard`, `/theme`, `/theme-new`, `/theme-css`, `/component`, `/initial-setup`
  - **Agents**: `theme-setup`, `layout-builder`, `component-check`
  - **SessionStart Hook**: DMC version check (non-blocking)
  - **Tests**: 94 tests passing
    - config.py: 82% coverage
    - component_registry.py: 92% coverage
    - dmc_tools.py: 88% coverage
    - chart_tools.py: 68% coverage
    - theme_tools.py: 99% coverage

**Sprint Completed:**
- Milestone: Sprint 1 - viz-platform Plugin (closed 2026-01-26)
- Issues: #170-#182 (13/13 closed)
- Wiki: [Sprint-1-viz-platform-Implementation-Plan](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/Sprint-1-viz-platform-Implementation-Plan)
- Lessons: [sprint-1---viz-platform-plugin-implementation](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/lessons/sprints/sprint-1---viz-platform-plugin-implementation)
- Reference: `docs/changes/CHANGE_V04_0_0_PROPOSAL_ORIGINAL.md` (Phases 4-5)

---

## [4.1.0] - 2026-01-26

### Added
- **projman:** Wiki-based planning workflow enhancement (V04.1.0)
  - Flexible input source detection in `/sprint-plan` (file, wiki, or conversation)
  - Wiki proposal and implementation page creation during sprint planning
  - Wiki reference linking in created issues
  - Wiki status updates in `/sprint-close` (Implemented/Partial/Failed)
  - Metadata section in lessons learned with implementation link for traceability
  - New `/proposal-status` command for viewing proposal/implementation tree
- **projman:** `/suggest-version` command - Analyzes CHANGELOG and recommends semantic version bump
- **projman:** SessionStart hook now suggests sprint planning when open issues exist without milestone
- **projman:** SessionStart hook now warns about unreleased CHANGELOG entries

### Changed
- **doc-guardian:** Hook now tracks documentation dependencies and queues specific files needing updates
  - Outputs which specific docs need updating (e.g., "commands changed → update needed: docs/COMMANDS-CHEATSHEET.md README.md")
  - Maintains queue file (`.doc-guardian-queue`) for batch processing
- **docs:** COMMANDS-CHEATSHEET.md updated with data-platform plugin (7 commands + hook)

### Fixed
- Documentation drift: COMMANDS-CHEATSHEET.md was missing data-platform plugin added in v4.0.0
- Proactive sprint planning: projman now suggests `/sprint-plan` at session start when unplanned issues exist

### Known Issues
- **MCP Bug #160:** `update_wiki_page` tool renames pages to "unnamed" when page_name contains URL-encoded characters (`:` → `%3A`). Workaround: use `create_wiki_page` to overwrite instead.

---

## [4.0.0] - 2026-01-25

### Added

#### New Plugin: data-platform v1.0.0
- **pandas MCP Tools** (14 tools): DataFrame operations with Arrow IPC data_ref persistence
  - `read_csv`, `read_parquet`, `read_json` - Load data with chunking support
  - `to_csv`, `to_parquet` - Export to various formats
  - `describe`, `head`, `tail` - Data exploration
  - `filter`, `select`, `groupby`, `join` - Data transformation
  - `list_data`, `drop_data` - Memory management

- **PostgreSQL MCP Tools** (10 tools): Database operations with asyncpg connection pooling
  - `pg_connect`, `pg_query`, `pg_execute` - Core database operations
  - `pg_tables`, `pg_columns`, `pg_schemas` - Schema exploration
  - `st_tables`, `st_geometry_type`, `st_srid`, `st_extent` - PostGIS spatial support

- **dbt MCP Tools** (8 tools): Build tool wrapper with pre-execution validation
  - `dbt_parse` - Pre-flight validation (catches dbt 1.9+ deprecations)
  - `dbt_run`, `dbt_test`, `dbt_build` - Execution with auto-validation
  - `dbt_compile`, `dbt_ls`, `dbt_docs_generate`, `dbt_lineage` - Analysis tools

- **Commands**: `/ingest`, `/profile`, `/schema`, `/explain`, `/lineage`, `/run`
- **Agents**: `data-ingestion` (loading/transformation), `data-analysis` (exploration/profiling)
- **SessionStart Hook**: Graceful PostgreSQL connection check (non-blocking warning)

- **Key Features**:
  - data_ref system for DataFrame persistence across tool calls
  - 100k row limit with chunking support for large datasets
  - Hybrid configuration (system: `~/.config/claude/postgres.env`, project: `.env`)
  - Auto-detection of dbt projects
  - Arrow IPC format for efficient memory management

---

## [3.2.0] - 2026-01-24

### Added
- **git-flow:** `/commit` now detects protected branches before committing
  - Warns when on protected branch (main, master, development, staging, production)
  - Offers to create feature branch automatically instead of committing directly
  - Configurable via `GIT_PROTECTED_BRANCHES` environment variable
- **netbox:** Platform and primary_ip parameters added to device update tools
- **claude-config-maintainer:** Auto-enforce mandatory behavior rules via SessionStart hook
- **scripts:** `release.sh` - Versioning workflow script for consistent releases
- **scripts:** `verify-hooks.sh` - Verify all hooks are command type

### Changed
- **doc-guardian:** Hook switched from `prompt` type to `command` type
  - Prompt hooks unreliable - Claude ignores explicit instructions
  - New `notify.sh` bash script guarantees exact output behavior
  - Only notifies for config file changes (commands/, agents/, skills/, hooks/)
  - Silent exit for all other files - no blocking possible
- **All hooks:** Converted to command type with stricter plugin prefix enforcement
  - All hooks now mandate `[plugin-name]` prefix with "NO EXCEPTIONS" rule
  - Simplified output formats with word limits
  - Consistent structure across projman, pr-review, code-sentinel, doc-guardian
- **CLAUDE.md:** Replaced destructive "ALWAYS CLEAR CACHE" rule with "VERIFY AND RESTART"
  - Cache clearing mid-session breaks MCP tools
  - Added guidance for proper plugin development workflow

### Fixed
- **cmdb-assistant:** Complete MCP tool schemas for update operations (#138)
- **netbox:** Shorten tool names to meet 64-char API limit (#134)
- **cmdb-assistant:** Correct NetBox API URL format in setup wizard (#132)
- **gitea/projman:** Type safety for `create_label_smart`, curl-based debug-report (#124)
- **netbox:** Add diagnostic logging for JSON parse errors (#121)
- **labels:** Add duplicate check before creating labels (#116)
- **hooks:** Convert ALL hooks to command type with proper prefixes (#114)
- Protected branch workflow: Claude no longer commits directly to protected branches (fixes #109)
- doc-guardian hook no longer blocks workflow (fixes #110)

---

## [3.1.1] - 2026-01-22

### Added
- **git-flow:** `/commit-sync` now prunes stale remote-tracking branches with `git fetch --prune`
- **git-flow:** `/commit-sync` detects and reports local branches with deleted upstreams
- **git-flow:** `/branch-cleanup` now handles stale branches (upstream gone) separately from merged branches
- **git-flow:** New `GIT_CLEANUP_STALE` environment variable for stale branch cleanup control

### Changed
- **All hooks:** Added `[plugin-name]` prefix to all hook messages for better identification
  - `[projman]`, `[pr-review]`, `[code-sentinel]`, `[doc-guardian]` prefixes
- **doc-guardian:** Hook now notification-only (no file reads or blocking operations)
  - Suggests running `/doc-sync` instead of performing inline checks
  - Significantly reduces workflow interruption

### Fixed
- doc-guardian hook no longer stalls workflow with deep file analysis

---

## [3.1.0] - 2026-01-21

### Added

#### Debug Workflow Commands (projman)
- **`/debug-report`** - Run diagnostics in test projects, create structured issues in marketplace
  - Runs 5 diagnostic MCP tool tests with explicit repo parameter
  - Captures full project context (git remote, cwd, branch)
  - Generates structured issue with hypothesis and investigation steps
  - Creates issue in configured marketplace repository automatically

- **`/debug-review`** - Investigate diagnostic issues with human approval gates
  - Lists open diagnostic issues for triage
  - Maps errors to relevant code files using error-to-file mapping
  - MANDATORY: Reads relevant files before proposing any fix
  - Three approval gates: investigation summary, fix approach, PR creation
  - Creates feature branch, commits, and PR with proper linking

#### MCP Server Improvements
- Dynamic label format detection in `suggest_labels`
  - Supports slash format (`Type/Bug`) and colon-space format (`Type: Bug`)
  - Fetches actual labels from repo and matches suggestions to real format
  - Handles Effort/Efforts singular/plural normalization

### Changed
- **`/labels-sync`** completely rewritten with explicit execution steps
  - Step 1 now explicitly requires running `git remote get-url origin` via Bash
  - All MCP tool calls show required `repo` parameter
  - Added "DO NOT" section preventing common mistakes
  - Removed confusing "Label Reference" section that caused file creation prompts

### Fixed
- MCP tools no longer fail with "Use 'owner/repo' format" error
  - Root cause: MCP server is sandboxed and cannot auto-detect project directory
  - Solution: Command documentation now instructs Claude to detect repo via Bash first

---

## [3.0.1] - 2026-01-21

### Added
- `/project-init` command for quick project setup when system is already configured
- `/project-sync` command to sync .env with git remote after repository move/rename
- SessionStart hooks for automatic mismatch detection between git remote and .env
- Interactive setup wizard (`/initial-setup`) redesigned to use Claude tools instead of bash script

### Changed
- `GITEA_ORG` moved from system-level to project-level configuration (different projects may belong to different organizations)
- Environment variables renamed to match MCP server expectations:
  - `GITEA_URL` → `GITEA_API_URL` (must include `/api/v1`)
  - `GITEA_TOKEN` → `GITEA_API_TOKEN`
  - `NETBOX_URL` → `NETBOX_API_URL` (must include `/api`)
  - `NETBOX_TOKEN` → `NETBOX_API_TOKEN`
- Setup commands now validate repository via Gitea API before saving configuration
- README.md simplified to show only wizard setup path (manual setup moved to CONFIGURATION.md)

### Fixed
- API URL paths in curl commands (removed redundant `/api/v1` since it's now in the URL variable)
- Documentation now correctly references environment variable names

---

## [3.0.0] - 2026-01-20

### Added

#### New Plugins
- **clarity-assist** v1.0.0 - Prompt optimization with ND accommodations
  - `/clarify` command for full 4-D methodology optimization
  - `/quick-clarify` command for rapid single-pass clarification
  - clarity-coach agent with ND-friendly questioning patterns
  - prompt-patterns skill with optimization rules

- **git-flow** v1.0.0 - Git workflow automation
  - `/commit` command with smart conventional commit messages
  - `/commit-push`, `/commit-merge`, `/commit-sync` workflow commands
  - `/branch-start`, `/branch-cleanup` branch management commands
  - `/git-status` enhanced status with recommendations
  - `/git-config` interactive configuration
  - git-assistant agent for complex operations
  - workflow-patterns skill with branching strategies

- **pr-review** v1.0.0 - Multi-agent pull request review
  - `/pr-review` command for comprehensive multi-agent review
  - `/pr-summary` command for quick PR overview
  - `/pr-findings` command for filtering review findings
  - coordinator agent for orchestrating reviews
  - security-reviewer, performance-analyst, maintainability-auditor, test-validator agents
  - review-patterns skill with confidence scoring rules

#### Gitea MCP Server Enhancements
- 6 new Pull Request tools:
  - `list_pull_requests` - List PRs with filters
  - `get_pull_request` - Get PR details
  - `get_pr_diff` - Get PR diff
  - `get_pr_comments` - Get PR comments
  - `create_pr_review` - Create review (approve, request changes, comment)
  - `add_pr_comment` - Add comment to PR

#### Documentation
- `docs/CONFIGURATION.md` - Centralized configuration guide for all plugins

### Changed
- **BREAKING:** Marketplace renamed from `claude-code-marketplace` to `leo-claude-mktplace`
- **BREAKING:** MCP servers moved from plugin directories to shared `mcp-servers/` at repository root
- All plugins now have `category`, `tags`, and `license` fields in marketplace.json
- Plugin MCP dependencies now use symlinks to shared servers
- projman version bumped to 3.0.0 (includes PR tools integration)
- projman CONFIGURATION.md slimmed down, links to central docs

### Removed
- Standalone MCP server directories inside plugins (replaced with symlinks)

---

## [2.3.0] - 2026-01-20

### Added

#### New Plugins
- **doc-guardian** v1.0.0 - Documentation lifecycle management
  - `/doc-audit` command for full project documentation drift analysis
  - `/doc-sync` command to batch apply pending documentation updates
  - PostToolUse hook for automatic drift detection
  - Stop hook reminder for pending updates
  - doc-analyzer agent for cross-reference analysis
  - doc-patterns skill for documentation structure knowledge

- **code-sentinel** v1.0.0 - Security scanning and refactoring
  - `/security-scan` command for comprehensive security audit
  - `/refactor` command to apply refactoring patterns
  - `/refactor-dry` command to preview refactoring opportunities
  - PreToolUse hook for real-time security scanning
  - security-reviewer agent for vulnerability analysis
  - refactor-advisor agent for code structure improvements
  - security-patterns skill for vulnerability detection rules

#### projman Enhancements
- `/test-gen` command - Generate unit, integration, and e2e tests for specified code

### Changed
- Marketplace version bumped to 2.3.0
- projman version bumped to 2.3.0

## [2.2.0] - 2026-01-20

### Added
- `/review` command for pre-sprint-close code quality checks (projman)
- `/test-check` command for test verification before sprint close (projman)
- `code-reviewer` agent for structured code review workflow (projman)
- Validation script (`scripts/validate-marketplace.sh`) for marketplace compliance
- `homepage` and `repository` fields to all plugin entries in marketplace.json
- `metadata` wrapper for description/version in marketplace.json
- Keywords to all plugin manifests for better discoverability
- `commands` and `agents` directory references to plugin manifests
- Versioning rule: version displayed only in main README.md title

### Changed
- Updated marketplace.json with required fields per Claude Code spec
- Fixed installation documentation to use official Claude Code methods
- Prioritized public HTTPS URL over Tailscale SSH URL in documentation
- Updated all plugin manifests with author, homepage, repository, license fields
- Consolidated version display to main README.md title only
- Removed version numbers from plugin documentation titles

### Fixed
- Plugin manifests now include all required fields per Claude Code spec
- Installation section uses `extraKnownMarketplaces` instead of undocumented `pluginMarketplace`

### Removed
- `docs/references/` directory (obsolete planning documents)
- Version numbers from individual plugin README titles
- Version section from plugins/projman/README.md

## [2.1.0] - 2026-01-15

### Added
- `docs/CANONICAL-PATHS.md` - Single source of truth for all file paths
- Path verification rules in CLAUDE.md (mandatory pre-flight check)
- Recovery protocol for path issues
- Installation script (`scripts/setup.sh`) for new users
- Post-update script (`scripts/post-update.sh`) for updates
- Update documentation (`docs/UPDATING.md`)
- `/initial-setup` slash command
- File creation governance rules in CLAUDE.md
- `.scratch/` directory for transient work
- `scripts/` directory for setup automation

### Changed
- Replaced `docs/CORRECT-ARCHITECTURE.md` reference with `docs/CANONICAL-PATHS.md`
- Added mandatory path verification section to CLAUDE.md
- Updated CLAUDE.md with file creation governance

### Fixed
- Removed dead reference to non-existent `docs/CORRECT-ARCHITECTURE.md`

### Removed
- Organization/workspace GID variable (no longer needed)
- Development output files (test scripts, status reports)
- IDE-specific workspace files
- Stray files from project root

## [2.0.0] - 2026-01-06

### Added
- Full Gitea integration with wiki, milestones, dependencies
- Parallel execution batching via dependency graph
- Wiki tools for lessons learned (`create_lesson`, `search_lessons`)
- Milestone tools (`list_milestones`, `create_milestone`, `update_milestone`)
- Dependency tools (`list_issue_dependencies`, `create_issue_dependency`, `get_execution_order`)
- Validation tools (`validate_repo_org`, `get_branch_protection`)
- MCP servers bundled inside plugins (not shared at root)

### Changed
- MCP server architecture: bundled in plugins instead of shared at root
- Configuration uses `${CLAUDE_PLUGIN_ROOT}/mcp-servers/` paths

## [1.0.0] - 2025-12-15

### Added
- projman plugin with basic sprint commands
- `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close` commands
- `/labels-sync` command for label taxonomy synchronization
- Three-agent model (planner, orchestrator, executor)
- Gitea MCP server with issue and label tools
- 43-label taxonomy system
- Hybrid configuration system (system + project level)
- Branch-aware security model

## [0.1.0] - 2025-12-01

### Added
- Initial repository structure
- projman plugin structure (planned)
- projman-pmo plugin structure (planned)
- project-hygiene plugin for cleanup automation
- claude-config-maintainer plugin structure
- cmdb-assistant plugin structure
- Basic marketplace manifest
