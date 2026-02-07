# Output Formats

## Visual Header

All commands display this header:

```
+----------------------------------------------------------------------+
|  PR-REVIEW [Command Name]                                            |
+----------------------------------------------------------------------+
```

## Review Report Format

```
===================================================
PR Review Report: #<number>
===================================================

Summary:
  Files changed: <n>
  Lines: +<added> / -<removed>
  Agents consulted: <list>

Findings: <total>
  Critical: <n>
  Major: <n>
  Minor: <n>
  Suggestions: <n>

---------------------------------------------------
CRITICAL FINDINGS
---------------------------------------------------

[<ID>] <Title> (Confidence: <score>)
File: <path>:<line>
Category: <category>

<Description>

Suggested fix:
<code block>

---------------------------------------------------
VERDICT: <APPROVE|COMMENT|REQUEST_CHANGES>
---------------------------------------------------

<Justification>
```

## Summary Format

```
===================================================
PR Summary: #<number> - <title>
===================================================

Author: @<username>
Branch: <head> -> <base>
Status: <status>

---------------------------------------------------
CHANGES OVERVIEW
---------------------------------------------------

Files: <n> changed
  + <n> new files
  ~ <n> modified files
  - <n> deleted files

Lines: +<added> / -<removed> (net +<diff>)

---------------------------------------------------
WHAT THIS PR DOES
---------------------------------------------------

<Plain-language description>

---------------------------------------------------
KEY FILES
---------------------------------------------------

* <path> (+<lines>) - <description>

---------------------------------------------------
QUICK ASSESSMENT
---------------------------------------------------

Scope: <Small|Medium|Large>
Risk: <Low|Medium|High>
Recommendation: <action>
===================================================
```

## Findings List Format

### Detailed (default)

```
===================================================
PR #<number> Findings (filtered: <filter>)
===================================================

Showing <n> of <total> findings

---------------------------------------------------

[<ID>] <Title>
Confidence: <score> (<label>) | Severity: <level>
File: <path>:<line>

<Description>

Fix: <suggestion>

---------------------------------------------------
```

### Compact (--compact)

```
<ID> | <Severity> | <Confidence> | <File>:<Line> | <Title>
```

### JSON (--json)

```json
{
  "pr": <number>,
  "findings": [
    {
      "id": "<ID>",
      "category": "<category>",
      "severity": "<severity>",
      "confidence": <score>,
      "file": "<path>",
      "line": <number>,
      "title": "<title>",
      "description": "<description>",
      "fix": "<suggestion>"
    }
  ]
}
```

## Setup Complete Format

```
+============================================================+
|                  PR-REVIEW SETUP COMPLETE                  |
+============================================================+
| MCP Server (Gitea):    Ready                               |
| System Config:         ~/.config/claude/gitea.env          |
| Project Config:        ./.env                              |
+============================================================+
```

## Project Configured Format

```
+============================================================+
|                   PROJECT CONFIGURED                       |
+============================================================+
| Organization:  <org>                                       |
| Repository:    <repo>                                      |
| Config file:   ./.env                                      |
+============================================================+

Ready to review PRs:
- /pr review <number>   Full multi-agent review
- /pr summary <number>  Quick summary
- /pr findings <number> List findings
```

## Annotated Diff Format

```
===================================================
PR #<number> Diff - <title>
===================================================

Branch: <head> -> <base>
Files: <n> changed (+<added> / -<removed>)

---------------------------------------------------
<file> (+<added> / -<removed>)
---------------------------------------------------

@@ -<old>,<ctx> +<new>,<ctx> @@ <context>
  <line> |   existing code
  <line> |-  removed code
         |   +--- COMMENT by @<user> (<time>) ---
         |   | <comment text>
         |   +-----------------------------------
  <line> |+  added code

===================================================
Comment Summary: <n> comments, <n> resolved
===================================================
```
