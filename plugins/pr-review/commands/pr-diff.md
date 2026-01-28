# /pr-diff - Annotated PR Diff Viewer

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔍 PR-REVIEW · Diff Viewer                                       │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the diff display.

## Purpose

Display the PR diff with inline annotations from review comments, making it easy to see what feedback has been given alongside the code changes.

## Usage

```
/pr-diff <pr-number> [--repo owner/repo] [--context <lines>]
```

### Options

```
--repo <owner/repo>   Override repository (default: from .env)
--context <n>         Lines of context around changes (default: 3)
--no-comments         Show diff without comment annotations
--file <pattern>      Filter to specific files (glob pattern)
```

## Behavior

### Step 1: Fetch PR Data

Using Gitea MCP tools:
1. `get_pr_diff` - Unified diff of all changes
2. `get_pr_comments` - All review comments on the PR

### Step 2: Parse and Annotate

Parse the diff and overlay comments at their respective file/line positions:

```
═══════════════════════════════════════════════════
PR #123 Diff - Add user authentication
═══════════════════════════════════════════════════

Branch: feat/user-auth → development
Files: 12 changed (+234 / -45)

───────────────────────────────────────────────────
src/api/users.ts (+85 / -12)
───────────────────────────────────────────────────

@@ -42,6 +42,15 @@ export async function getUser(id: string) {
   42 │   const db = getDatabase();
   43 │
   44 │-  const user = db.query("SELECT * FROM users WHERE id = " + id);
      │   ┌─────────────────────────────────────────────────────────────
      │   │ COMMENT by @reviewer (2h ago):
      │   │ This is a SQL injection vulnerability. Use parameterized
      │   │ queries instead: `db.query("SELECT * FROM users WHERE id = ?", [id])`
      │   └─────────────────────────────────────────────────────────────
   45 │+  const query = "SELECT * FROM users WHERE id = ?";
   46 │+  const user = db.query(query, [id]);
   47 │
   48 │   if (!user) {
   49 │     throw new NotFoundError("User not found");
   50 │   }

@@ -78,3 +87,12 @@ export async function updateUser(id: string, data: UserInput) {
   87 │+  // Validate input before update
   88 │+  validateUserInput(data);
   89 │+
   90 │+  const result = db.query(
   91 │+    "UPDATE users SET name = ?, email = ? WHERE id = ?",
   92 │+    [data.name, data.email, id]
   93 │+  );
      │   ┌─────────────────────────────────────────────────────────────
      │   │ COMMENT by @maintainer (1h ago):
      │   │ Good use of parameterized query here!
      │   │
      │   │ REPLY by @author (30m ago):
      │   │ Thanks! Applied the same pattern throughout.
      │   └─────────────────────────────────────────────────────────────

───────────────────────────────────────────────────
src/components/LoginForm.tsx (+65 / -0) [NEW FILE]
───────────────────────────────────────────────────

@@ -0,0 +1,65 @@
    1 │+import React, { useState } from 'react';
    2 │+import { useAuth } from '../context/AuthContext';
    3 │+
    4 │+export function LoginForm() {
    5 │+  const [email, setEmail] = useState('');
    6 │+  const [password, setPassword] = useState('');
    7 │+  const { login } = useAuth();

... (remaining diff content)

═══════════════════════════════════════════════════
Comment Summary: 5 comments, 2 resolved
═══════════════════════════════════════════════════
```

### Step 3: Filter by Confidence (Optional)

If `PR_REVIEW_CONFIDENCE_THRESHOLD` is set, also annotate with high-confidence findings from previous reviews:

```
   44 │-  const user = db.query("SELECT * FROM users WHERE id = " + id);
      │   ┌─── REVIEW FINDING (0.95 HIGH) ─────────────────────────────
      │   │ [SEC-001] SQL Injection Vulnerability
      │   │ Use parameterized queries to prevent injection attacks.
      │   └─────────────────────────────────────────────────────────────
      │   ┌─── COMMENT by @reviewer ────────────────────────────────────
      │   │ This is a SQL injection vulnerability...
      │   └─────────────────────────────────────────────────────────────
```

## Output Formats

### Default (Annotated Diff)

Full diff with inline comments as shown above.

### Plain (--no-comments)

```
/pr-diff 123 --no-comments

# Standard unified diff output without annotations
```

### File Filter (--file)

```
/pr-diff 123 --file "src/api/*"

# Shows diff only for files matching pattern
```

## Use Cases

- **Review preparation**: See the full context of changes with existing feedback
- **Followup work**: Understand what was commented on and where
- **Discussion context**: View threaded conversations alongside the code
- **Progress tracking**: See which comments have been resolved

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PR_REVIEW_CONFIDENCE_THRESHOLD` | `0.7` | Minimum confidence for showing review findings |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/pr-summary` | Quick overview without diff |
| `/pr-review` | Full multi-agent review |
| `/pr-findings` | Filter review findings by category |
