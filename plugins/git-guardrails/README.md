# git-guardrails

Two `PreToolUse(Bash)` safety hooks, nothing else:

| Hook | Blocks when | Fix |
|---|---|---|
| `branch-check.sh` | Branch-creation commands (`git checkout -b`, `git switch -c`, `git branch <name>`) use an unrecognized prefix or forbidden characters | Use `<type>/<description>` where type is `feat\|fix\|chore\|docs\|refactor\|test\|perf\|debug`, or `claude/...` for Claude Code on the web |
| `commit-msg-check.sh` | `git commit -m "..."` message is not Conventional Commits | Use `<type>(<scope>)?!?: <description>` |

## Why this exists

The retired `git-flow` plugin bundled a large set of commands that reimplemented things Claude Code now does natively through plain Bash. The two hooks were the only parts pulling their weight, so they live here as a hook-only plugin.

## Bypass

Don't. If a hook blocks you, fix the branch name / commit message. Never use `--no-verify`.

## Files

```
git-guardrails/
├── .claude-plugin/
│   ├── plugin.json
│   └── metadata.json
└── hooks/
    ├── hooks.json
    ├── branch-check.sh
    └── commit-msg-check.sh
```
