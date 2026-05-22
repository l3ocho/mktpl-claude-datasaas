---
name: doc audit
description: [doc-guardian] Full documentation audit - scans entire project for doc drift without making changes
---

# /doc audit

Perform a comprehensive documentation drift analysis.

## Skills to Load

- skills/doc-standards/SKILL.md
- skills/drift-detection/SKILL.md
- skills/doc-patterns/SKILL.md

## Visual Output

```
+------------------------------------------------------------------+
|  DOC-GUARDIAN - Documentation Audit                              |
+------------------------------------------------------------------+
```

## Process

1. **Inventory Documentation Files**
   Execute `skills/doc-patterns/SKILL.md` - identify all doc files

2. **Cross-Reference Analysis**
   Execute `skills/drift-detection/SKILL.md` - verify all references

3. **Completeness Check**
   - Public functions without docstrings
   - Exported modules without README coverage
   - Environment variables used but not documented
   - CLI commands not in help text

4. **Standards Compliance Check**
   Apply all rules from `skills/doc-standards/SKILL.md`:

   | Check | Description |
   |---|---|
   | **Standard compliance** | Each doc follows the required section hierarchy (full doc vs. directory README) |
   | **Filename convention** | All docs use kebab-case lowercase (with conventional exceptions) |
   | **Forbidden patterns** | Detect `Last updated:` lines, multiple H1s, N/A sections, and other forbidden patterns |
   | **Required default docs** | Verify all default docs exist (`README.md`, `CLAUDE.md`, `CHANGELOG.md`, `docs/setup.md`) |
   | **Orphan custom docs** | Each custom doc maps to a code path, project process, or historical decision |
   | **Directory READMEs** | Every folder meeting "needs README" criteria has one |
   | **Contents table accuracy** | Each directory README's Contents table matches actual folder contents |
   | **Documentation Index accuracy** | Top-level README's index includes every doc that should be listed |
   | **Citation coverage** | Factual claims about code behavior, structure, or APIs link to the relevant code |
   | **Acronyms defined** | All project-specific acronyms used are defined in the Acronyms & Terms section |
   | **Status indicators** | Docs with TODO markers have a `> **Status:** Draft` indicator at the top |
   | **Bidirectional links** | "Related Documentation" links resolve in both directions |

5. **Output**
   Use format from `skills/drift-detection/SKILL.md`

   If required default docs are missing, append: "Run `/doc init` to bootstrap missing documentation."

6. **Failure policy**
   - **Failures block, do not warn.** Exit code 1 if any violation found.
   - Do not soften violations into "consider updating" suggestions.

7. **Do NOT make changes** - audit only, report findings
