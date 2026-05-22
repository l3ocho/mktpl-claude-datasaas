---
name: doc init
description: [doc-guardian] Bootstrap documentation for a new or undocumented project using the doc-standards skill
---

# /doc init

Scaffold the canonical documentation set for a project that lacks one. Produces standard-compliant skeletons with deterministic content where possible, and interactive prompts for content that requires human input.

## Skills to Load

- skills/doc-standards/SKILL.md
- skills/doc-patterns/SKILL.md

## Visual Output

```
+------------------------------------------------------------------+
|  DOC-GUARDIAN - Documentation Bootstrap                          |
+------------------------------------------------------------------+
```

## Options

| Flag | Description | Default |
|---|---|---|
| `--force` | Required to run on already-initialized projects. Does not skip per-file safety prompts. | false |
| `--minimal` | Scaffold only README.md and CLAUDE.md | false |
| `--source-root <path>` | Override source root detection | auto-detect |
| `--no-directory-readmes` | Skip directory README generation | false |

## Process

### 1. Project Introspection

Detect the project's shape from its files:

- **Language:** from file extensions and config files (`pyproject.toml`, `package.json`, `go.mod`, etc.)
- **Framework:** from imports and dependencies (`dash` → Dash, `dash_mantine_components` → DMC, `fastapi` → FastAPI, etc.)
- **Source root:** `src/`, `app/`, or top-level — prefer explicit, fall back to convention
- **Folder tree:** full tree of source code directories
- **Config files:** `.env`, `pyproject.toml`, `requirements.txt`, `package.json`, etc.
- **Database usage:** `psycopg` → PostgreSQL, `sqlalchemy` → ORM present, etc.
- **Deployment artifacts:** `Dockerfile`, `docker-compose.yml`, `fly.toml`, `.github/workflows/`, etc.
- **Test folder:** presence of `tests/`, `test/`, `__tests__/`, etc.

### 2. Pre-Flight Check

**Already-initialized detection:** Check if any of `README.md`, `CLAUDE.md`, or `docs/` exists at the project root.

- **If already initialized AND `--force` not passed:**
  Refuse to run. Output a warning listing which default docs exist and what `/doc init` would potentially modify.
  Instruct the user: "Re-run with `--force` if you want to proceed."
  Stop.

- **If already initialized AND `--force` passed:**
  Proceed to per-file safety prompts. For each existing default doc, ask the user:
  - `[keep]` — leave it as-is
  - `[overwrite]` — replace with a fresh skeleton
  - `[merge]` — insert missing sections while preserving existing content
  `--force` enables the command to start but does **not** skip these per-file prompts.

- **If not already initialized (clean slate):**
  Proceed directly to Doc Set Selection — no warning needed.

If the project has a `docs/` folder with custom docs, list them and confirm they will be preserved. Custom docs are never auto-modified by `/doc init`.

Halt if the user cancels at any stage.

### 3. Doc Set Selection

Present an interactive selection of which docs to scaffold. Show defaults per the table below and ask the user to confirm or adjust:

| Doc | Default Selection |
|---|---|
| `README.md` | Selected |
| `CLAUDE.md` | Selected |
| `CHANGELOG.md` | Selected |
| `CONTRIBUTING.md` | Unselected |
| `docs/setup.md` | Selected |
| `docs/deployment.md` | Selected if deployment artifacts detected |
| `docs/architecture.md` | Selected |
| `docs/data-model.md` | Selected if database detected |
| `docs/architecture_decisions/README.md` | Selected (ADR index) |
| `tests/README.md` | Selected if `tests/` folder detected |
| Source directory READMEs (per "Needs README" criteria) | Selected |
| Test subfolder READMEs | **Not prompted** — create manually if specialized setup warrants it |

If `--minimal` is passed, select only `README.md` and `CLAUDE.md` regardless of the above.

### 4. Interactive Content Gathering

For non-derivable content, ask these questions one at a time using the AskUserQuestion mechanism — never assume answers:

- "In one sentence, what does this project do?"
- "Who is the intended user?"
- "Are there project-specific acronyms or terms? List them (e.g., DMC = Dash Mantine Components)."
- "Are there things Claude should never do in this project? (For CLAUDE.md — Things Not To Do section)"
- For each source folder needing a README: "In one sentence, what does `<folder>/` contain?"

Do not proceed past a question until the user answers it. Never fabricate answers.

### 5. Deterministic Content Generation

For each selected doc, populate what can be derived from the repo without asking:

- **Tech stack table:** from `pyproject.toml` / `package.json` / `go.mod` — list detected framework, language, key dependencies
- **Folder structure tree:** from the detected source layout
- **"Where Things Live" table:** from detected source layout — map concerns to paths
- **Setup commands:** from detected package manager (`pip install -e .`, `npm install`, etc.)
- **Dependency list:** from manifest files

### 6. Skeleton Generation

Generate each selected doc following the `doc-standards` skill exactly:

- Correct section hierarchy (full docs vs. directory READMEs)
- Correct file naming (kebab-case, conventional exceptions)
- Correct linking format (relative paths, no heading anchors)
- Status indicator at top if any sections remain incomplete: `> **Status:** Draft — sections marked TODO are incomplete and not yet authoritative.`
- Acronyms section populated from user input (step 4)
- TODO markers for content that could not be derived and was not provided

### 7. Cross-Linking Pass

After all skeletons are generated:

- Generate the top-level `README.md` Documentation Index table with relative links to every scaffolded doc
- Generate directory README Contents tables for every scaffolded directory README (folders first alphabetically, then files)
- Generate Related Documentation sections with bidirectional links
- Generate ADR index in `architecture_decisions/README.md` (empty table with column headers ready for first entry)

### 8. Generation Order

Process docs in this order to ensure cross-references resolve correctly:

1. Directory READMEs (leaf folders first, then parents)
2. Custom docs in `docs/`
3. ADR index (`docs/architecture_decisions/README.md`)
4. `docs/README.md` (indexes the custom docs)
5. `CLAUDE.md`
6. `CHANGELOG.md` (empty `## [Unreleased]` section only)
7. `CONTRIBUTING.md` (if selected)
8. Top-level `README.md` (last — indexes everything)

### 9. Verification Handoff

On completion, output:

- Summary of files created (list each path)
- List of any remaining TODO markers and which files contain them
- Instruction: "Run `/doc audit` to verify the scaffold meets the standard."

## Interaction with Native `/init`

Claude Code's native `/init` creates a generic CLAUDE.md. `/doc init` supersedes it for projects using doc-guardian — produces a richer CLAUDE.md with the standard's required sections and the "Where Things Live" table. If a CLAUDE.md already exists from native `/init`, the pre-flight check handles it (keep / overwrite / merge).
