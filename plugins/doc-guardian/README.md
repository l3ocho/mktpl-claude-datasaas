# doc-guardian

Documentation drift detection and sync.

## What it does

Scans your codebase for places where docs have fallen out of step with the code and proposes fixes. Also generates changelog entries from Conventional Commits.

## Commands

| Command | Purpose |
|---|---|
| `/doc audit` | Scan for drift between docs and code |
| `/doc sync` | Propose or apply drift fixes |
| `/doc changelog-gen` | Generate changelog entries from recent commits |
| `/doc coverage` | Documentation coverage metrics |
| `/doc stale-docs` | Identify stale docs |

## Agents (1)

| Agent | Model | Role |
|---|---|---|
| `doc-analyzer` | sonnet | Cross-references code and docs, classifies drift |

## Dependencies

Reads Gitea wiki pages via the `gitea` MCP (for RFC/ADR/lessons cross-refs).
