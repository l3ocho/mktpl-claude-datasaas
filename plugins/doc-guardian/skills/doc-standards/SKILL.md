---
name: doc-standards
description: Canonical documentation structure, hierarchy, and enforcement rules for monolithic projects
---

# Documentation Standards

Single source of truth for documentation policy. All commands modifying or evaluating documentation load this skill.

---

## Scope

Applies to: **monolithic projects** (modular or flat).

Out of scope: plugin marketplaces, multi-repo systems, library/SDK projects.

---

## Document Categories

| Category | Examples | Rule |
|---|---|---|
| **Default** | `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `docs/setup.md`, `docs/deployment.md` | Required for any non-trivial project. Content omits sections that do not apply — never write "Database: N/A". |
| **Custom** | `docs/api/*.md`, `docs/data-model.md`, `docs/architecture.md`, any other | Must justify existence by mapping to (a) a code path, (b) a project process, or (c) a historical decision. Orphans get deleted. |

---

## Folder Structure

```
project-root/
├── README.md                          # Top-level project index
├── CLAUDE.md                          # Claude Code behavior shaping
├── CHANGELOG.md
├── CONTRIBUTING.md                    # if applicable
├── src/                               # or equivalent source root
│   ├── README.md                      # describes src/ structure
│   ├── api/
│   │   ├── README.md                  # describes the API layer
│   │   ├── routes/
│   │   │   ├── README.md
│   │   │   └── ...
│   │   └── middlewares/
│   │       ├── README.md
│   │       └── ...
│   └── data/
│       ├── README.md
│       └── ...
└── docs/
    ├── README.md                      # index of docs/
    ├── setup.md
    ├── deployment.md
    ├── api/                           # subfolders allowed for grouping
    │   ├── README.md
    │   └── ...
    └── architecture_decisions/
        ├── README.md                  # ADR index
        ├── 001-initial-stack-choice.md
        └── 002-database-selection.md
```

**Rules:**

- `docs/` may contain subfolders to group related custom docs (e.g., `docs/api/`, `docs/ops/`). Subfolders should be used when 3+ docs share a domain.
- `architecture_decisions/` is **historical reference only**. Not consulted as current truth. Used to understand the evolution of decisions, not the current state.
- Source of truth is the code. Docs describe the code. Code does not describe the docs.

---

## File Naming

- **Kebab-case lowercase:** `data-model.md`, `api-reference.md`
- **Conventional exceptions:** `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`
- **Architecture decisions:** `architecture_decisions/NNN-short-title.md` where `NNN` is zero-padded sequential (`001`, `002`, ...)

---

## Section Hierarchy — Full Documents

Every full doc (not directory README) follows this section structure:

```
1. Title (H1, exactly one per file)
2. Purpose / Summary (always — one paragraph max)
3. Acronyms & Terms (if any project-specific acronyms used)
4. Table of Contents (if file > 200 lines)
5. Body sections (H2 major, H3 sub, H4 only if essential — no H5+)
6. Related Documentation (links to sibling docs)
7. External References (if any external links cited)
```

## Section Hierarchy — Directory READMEs

Directory READMEs follow a smaller, scan-in-30-seconds structure:

```
1. Title (folder name or descriptive)
2. Purpose (one sentence — what this folder contains and why)
3. Contents (table of subdirectories and key files with one-line descriptions)
4. Conventions (if any folder-specific conventions apply)
5. Related (links to parent README and key sibling folders)
```

No acronyms section, no TOC, no external refs unless genuinely needed.

---

## "Needs README" Criteria for Source Folders

Not every folder needs a README. Apply these rules:

| Folder type | README required? |
|---|---|
| Contains 3+ files of meaningful code | **Yes** |
| Contains subdirectories with their own READMEs | **Yes** (acts as index for the subtree) |
| Contains 1-2 files only, no subdirectories | **No** (the files speak for themselves) |
| Pure utility folder (`__pycache__/`, `node_modules/`, `.venv/`, `.git/`) | **Never** |
| `tests/` top-level folder | **Yes** — explains test strategy, fixtures, how to run tests |
| Test subfolders mirroring source structure | **Discouraged by default** — only when subfolder has non-obvious setup, specialized patterns (e2e, load, property-based), or differs significantly from parallel source structure |

---

## README Documentation Index Format (Top-Level)

The top-level `README.md` Documentation Index uses **table format only**:

```markdown
## Documentation Index

| Document | Purpose |
|---|---|
| [Source Code Guide](src/README.md) | Entry point to the codebase structure |
| [Architecture Docs](docs/README.md) | Detailed technical documentation |
| [Setup](docs/setup.md) | Local development environment and dependencies |
| [Deployment](docs/deployment.md) | Production deployment procedures |
```

**Rules:**

- One sentence per `Purpose`. No paragraphs.
- Links use relative paths.
- Includes both `src/README.md` and `docs/README.md` as first-class entries.

---

## Directory README Contents Table Format

Directory READMEs use a structured Contents table that is **machine-parseable** (required for future refactor tooling):

```markdown
## Contents

| Path | Type | Purpose |
|---|---|---|
| [routes/](routes/) | Folder | HTTP route handlers grouped by resource |
| [middlewares/](middlewares/) | Folder | Request middleware (auth, logging, CORS) |
| [server.py](server.py) | File | Application entry point and server config |
| [config.py](config.py) | File | Configuration loading and validation |
```

**Rules:**

- `Type` column values: `Folder` or `File` only.
- `Path` column links are relative to the README's location.
- One sentence per `Purpose`.
- Order: folders first (alphabetical), then files (alphabetical).

---

## CLAUDE.md Required Structure

CLAUDE.md follows the full-document section hierarchy. Its body sections must include (in this order):

```
1. Project Purpose
2. Tech Stack (table format)
3. Where Things Live (table mapping concerns to paths — machine-parseable)
4. Conventions
5. Things Not To Do
6. Available Commands (if marketplace plugins installed)
```

The **Where Things Live** table uses fixed format:

```markdown
## Where Things Live

| Concern | Path |
|---|---|
| HTTP routes | [src/api/routes/](src/api/routes/) |
| Database models | [src/data/models/](src/data/models/) |
| Configuration | [src/config.py](src/config.py) |
| Tests | [tests/](tests/) |
```

This table is **machine-parseable** and used by future refactor tooling to track structural moves.

---

## Linking Rules

- **Internal code references:** Relative links to file paths. `[the auth module](src/auth/__init__.py)`, `[validate_user](src/auth/validators.py)`. Line anchors (`#L42`) discouraged — they break easily.
- **Internal doc references:** Relative links between docs. `[see the data model](docs/data-model.md)`.
- **External references:** Full URLs. Live in a dedicated "External References" section at the bottom, OR inline if cited only once.
- **Bidirectional links:** Where it makes sense — if A links to B as "Related," B should link back to A.
- **No anchor-dependent links:** Avoid linking to headings (`#section-title`) when possible — heading text drift breaks them.

---

## Source-of-Truth Enforcement

- **Citation requirement:** Every factual claim in docs about code behavior, structure, or APIs must link to the relevant code file or function. Claims without citations are flagged by `/doc audit`.
- **Examples must be runnable:** Code blocks in docs must be either (a) verbatim snippets from the repo with a citation link, or (b) demonstrably correct examples that would execute against the current codebase. No invented APIs.

---

## Acronyms & Terms

If a doc uses any project-specific acronym, framework abbreviation, or domain term that is not universally known, it is defined in an "Acronyms & Terms" section near the top.

**Exempt (universal knowledge):** HTTP, JSON, SQL, API (when used generically), URL, REST.

**Requires definition (examples):** DMC (Dash Mantine Components), MCP (Model Context Protocol), project-specific domain terms.

---

## Diagrams

- **Mermaid:** Source goes inline in the markdown using a `mermaid` code block. No exported images.
- **draw.io:** The `.drawio` source file lives next to the `.md` file. The rendered image (PNG/SVG) is generated from it and referenced via relative path. Both files are committed.
- **No mystery images:** Any image in a doc must have a committed source artifact.

---

## Forbidden Patterns

| Pattern | Why |
|---|---|
| `Last updated: YYYY-MM-DD` in doc body | Lies. Git is the source of truth for timestamps. |
| Multiple H1 headings in one file | Markdown convention; breaks tooling. |
| Sections for non-existent features ("Database: N/A") | Pollutes context. Omit instead. |
| Inline jargon without definition | Define in Acronyms & Terms on first use. |
| Code examples for invented APIs | Source of truth is code. Examples reflect reality. |
| Orphan custom docs (no code/process/decision mapping) | Delete. |
| Heading-anchor links (`#some-section`) when avoidable | Brittle to heading text changes. |
| `Last updated:` lines | Git is the timestamp authority. |

---

## Status Indicators

Incomplete docs declare it at the top:

```markdown
> **Status:** Draft — sections marked TODO are incomplete and not yet authoritative.
```

`/doc audit` flags any doc containing `TODO` markers without this status indicator.

---

## Behavioral Rules (For Consuming Commands)

- **No guessing.** When commands encounter ambiguity (missing user input, unclear intent, unresolvable conflicts), they prompt the user with a concrete question. They never fabricate.
- **Consistency is mandatory.** All commands operating on docs apply these rules uniformly.
- **Failures are blocking, not warnings.** A doc violating these rules fails audit. The audit does not soften violations into "consider updating" suggestions.
