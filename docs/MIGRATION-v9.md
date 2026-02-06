# Migration Guide: v8.x → v9.0.0

## Overview

v9.0.0 standardizes all commands to the `/<noun> <action>` sub-command pattern. Every command in the marketplace now follows this convention.

**Breaking change:** All old command names are removed. Update your workflows, scripts, and CLAUDE.md references.

---

## Complete Command Mapping

### projman

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/sprint-plan` | `/sprint plan` | |
| `/sprint-start` | `/sprint start` | |
| `/sprint-status` | `/sprint status` | |
| `/sprint-close` | `/sprint close` | |
| `/pm-review` | `/sprint review` | Moved under `/sprint` |
| `/pm-test` | `/sprint test` | Moved under `/sprint` |
| `/pm-setup` | `/projman setup` | Moved under `/projman` |
| `/pm-debug` | `/projman debug` | Moved under `/projman` |
| `/labels-sync` | `/labels sync` | |
| `/suggest-version` | `/projman suggest-version` | Moved under `/projman` |
| `/proposal-status` | `/projman proposal-status` | Moved under `/projman` |
| `/rfc <sub>` | `/rfc <sub>` | Unchanged |
| `/project <sub>` | `/project <sub>` | Unchanged |
| `/adr <sub>` | `/adr <sub>` | Unchanged |

### git-flow

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/git-commit` | `/gitflow commit` | |
| `/git-commit-push` | `/gitflow commit --push` | **Consolidated** into flag |
| `/git-commit-merge` | `/gitflow commit --merge` | **Consolidated** into flag |
| `/git-commit-sync` | `/gitflow commit --sync` | **Consolidated** into flag |
| `/branch-start` | `/gitflow branch-start` | |
| `/branch-cleanup` | `/gitflow branch-cleanup` | |
| `/git-status` | `/gitflow status` | |
| `/git-config` | `/gitflow config` | |

**Note:** The three commit variants (`-push`, `-merge`, `-sync`) are now flags on `/gitflow commit`. This reduces 8 commands to 5.

### pr-review

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/pr-review` | `/pr review` | |
| `/pr-summary` | `/pr summary` | |
| `/pr-findings` | `/pr findings` | |
| `/pr-diff` | `/pr diff` | |
| `/pr-setup` | `/pr setup` | |
| `/project-init` | `/pr init` | Renamed |
| `/project-sync` | `/pr sync` | Renamed |

### clarity-assist

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/clarify` | `/clarity clarify` | |
| `/quick-clarify` | `/clarity quick-clarify` | |

### doc-guardian

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/doc-audit` | `/doc audit` | |
| `/doc-sync` | `/doc sync` | |
| `/changelog-gen` | `/doc changelog-gen` | Moved under `/doc` |
| `/doc-coverage` | `/doc coverage` | |
| `/stale-docs` | `/doc stale-docs` | Moved under `/doc` |

### code-sentinel

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/security-scan` | `/sentinel scan` | |
| `/refactor` | `/sentinel refactor` | |
| `/refactor-dry` | `/sentinel refactor-dry` | |

### claude-config-maintainer

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/config-analyze` (or `/analyze`) | `/claude-config analyze` | |
| `/config-optimize` (or `/optimize`) | `/claude-config optimize` | |
| `/config-init` (or `/init`) | `/claude-config init` | |
| `/config-diff` | `/claude-config diff` | |
| `/config-lint` | `/claude-config lint` | |
| `/config-audit-settings` | `/claude-config audit-settings` | |
| `/config-optimize-settings` | `/claude-config optimize-settings` | |
| `/config-permissions-map` | `/claude-config permissions-map` | |

### contract-validator

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/validate-contracts` | `/cv validate` | |
| `/check-agent` | `/cv check-agent` | |
| `/list-interfaces` | `/cv list-interfaces` | |
| `/dependency-graph` | `/cv dependency-graph` | |
| `/cv-setup` | `/cv setup` | |
| `/cv status` | `/cv status` | Unchanged |

### cmdb-assistant

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/cmdb-setup` | `/cmdb setup` | |
| `/cmdb-search` | `/cmdb search` | |
| `/cmdb-device` | `/cmdb device` | |
| `/cmdb-ip` | `/cmdb ip` | |
| `/cmdb-site` | `/cmdb site` | |
| `/cmdb-audit` | `/cmdb audit` | |
| `/cmdb-register` | `/cmdb register` | |
| `/cmdb-sync` | `/cmdb sync` | |
| `/cmdb-topology` | `/cmdb topology` | |
| `/change-audit` | `/cmdb change-audit` | Moved under `/cmdb` |
| `/ip-conflicts` | `/cmdb ip-conflicts` | Moved under `/cmdb` |

### data-platform

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/data-ingest` | `/data ingest` | |
| `/data-profile` | `/data profile` | |
| `/data-schema` | `/data schema` | |
| `/data-explain` | `/data explain` | |
| `/data-lineage` | `/data lineage` | |
| `/data-run` | `/data run` | |
| `/lineage-viz` | `/data lineage-viz` | Moved under `/data` |
| `/dbt-test` | `/data dbt-test` | Moved under `/data` |
| `/data-quality` | `/data quality` | |
| `/data-review` | `/data review` | |
| `/data-gate` | `/data gate` | |
| `/data-setup` | `/data setup` | |

### viz-platform

| Old (v8.x) | New (v9.0.0) | Notes |
|-------------|--------------|-------|
| `/viz-setup` | `/viz setup` | |
| `/viz-chart` | `/viz chart` | |
| `/viz-chart-export` | `/viz chart-export` | |
| `/viz-dashboard` | `/viz dashboard` | |
| `/viz-theme` | `/viz theme` | |
| `/viz-theme-new` | `/viz theme-new` | |
| `/viz-theme-css` | `/viz theme-css` | |
| `/viz-component` | `/viz component` | |
| `/accessibility-check` | `/viz accessibility-check` | Moved under `/viz` |
| `/viz-breakpoints` | `/viz breakpoints` | |
| `/design-review` | `/viz design-review` | Moved under `/viz` |
| `/design-gate` | `/viz design-gate` | Moved under `/viz` |

### project-hygiene

No changes — already used `/<noun> <action>` pattern.

| Command | Status |
|---------|--------|
| `/hygiene check` | Unchanged |

---

## Verifying Plugin Installation (v9.0.0)

Test commands use the new format:

| Plugin | Test Command |
|--------|--------------|
| git-flow | `/git-flow:gitflow-status` |
| projman | `/projman:sprint-status` |
| pr-review | `/pr-review:pr-summary` |
| clarity-assist | `/clarity-assist:clarity-clarify` |
| doc-guardian | `/doc-guardian:doc-audit` |
| code-sentinel | `/code-sentinel:sentinel-scan` |
| claude-config-maintainer | `/claude-config-maintainer:claude-config-analyze` |
| cmdb-assistant | `/cmdb-assistant:cmdb-search` |
| data-platform | `/data-platform:data-ingest` |
| viz-platform | `/viz-platform:viz-chart` |
| contract-validator | `/contract-validator:cv-validate` |

---

## CLAUDE.md Updates

If your project's CLAUDE.md references old command names, update them:

**Find old references:**
```bash
grep -rn '/sprint-plan\|/pm-setup\|/git-commit\|/pr-review\|/security-scan\|/config-analyze\|/validate-contracts\|/cmdb-search\|/data-ingest\|/viz-chart\b\|/clarify\b\|/doc-audit' CLAUDE.md
```

**Key patterns to search and replace:**
- `/sprint-plan` → `/sprint plan`
- `/pm-setup` → `/projman setup`
- `/pm-review` → `/sprint review`
- `/git-commit` → `/gitflow commit`
- `/pr-review` → `/pr review`
- `/security-scan` → `/sentinel scan`
- `/refactor` → `/sentinel refactor`
- `/config-analyze` → `/claude-config analyze`
- `/validate-contracts` → `/cv validate`
- `/clarify` → `/clarity clarify`
- `/doc-audit` → `/doc audit`
- `/cmdb-search` → `/cmdb search`
- `/data-ingest` → `/data ingest`
- `/viz-chart` → `/viz chart`

---

*Last Updated: 2026-02-06*
