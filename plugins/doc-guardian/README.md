# doc-guardian

Documentation lifecycle management: bootstrap, drift detection, and sync.

## What it does

Covers the full documentation lifecycle for a project:

- **Bootstrap** (`/doc init`) — scaffold a standard-compliant doc set from scratch using the `doc-standards` skill
- **Audit** (`/doc audit`) — scan for drift between docs and code, enforcing the `doc-standards` rules
- **Sync** (`/doc sync`) — apply pending drift fixes while respecting the standard's structure
- **Changelog** (`/doc changelog-gen`) — generate changelog entries from Conventional Commits

## Commands

| Command | Purpose |
|---|---|
| `/doc init` | Bootstrap documentation for a new or undocumented project |
| `/doc audit` | Scan for drift between docs and code |
| `/doc sync` | Propose or apply drift fixes |
| `/doc changelog-gen` | Generate changelog entries from recent commits |
| `/doc coverage` | Documentation coverage metrics |
| `/doc stale-docs` | Identify stale docs |

## Skills

| Skill | Purpose |
|---|---|
| `skills/doc-standards/SKILL.md` | Canonical documentation structure, hierarchy, and enforcement rules — loaded by `init`, `audit`, and `sync` |
| `skills/drift-detection/SKILL.md` | Cross-reference analysis for detecting doc drift |
| `skills/doc-patterns/SKILL.md` | File inventory patterns for identifying doc files |
| `skills/sync-workflow/SKILL.md` | Batch update workflow for applying fixes |

## Agents (1)

| Agent | Model | Role |
|---|---|---|
| `doc-analyzer` | sonnet | Cross-references code and docs, classifies drift |

## Dependencies

Reads Gitea wiki pages via the `gitea` MCP (for RFC/ADR/lessons cross-refs).
