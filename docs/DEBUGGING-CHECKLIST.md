# Debugging checklist — v12.0.0

Systematic approach when something's wrong with the marketplace.

## 1. MCP server isn't loading

Symptom: `gitea` / `data-platform` / `dmc-design` tools aren't available in Claude Code.

```bash
# Check venv exists and is healthy
./scripts/setup-venvs.sh --check

# If anything's missing or broken
./scripts/setup-venvs.sh
```

Then verify `.mcp.json` at repo root lists the server:

```bash
jq . .mcp.json
```

Then **restart Claude Code**. MCP servers are loaded at session start.

## 2. Plugin changes aren't taking effect

Remember: the marketplace has two copies.

| Copy | Path |
|---|---|
| Source | `~/Projects/personal/mktpl-claude-datasaas/` |
| Installed | `~/.claude/plugins/marketplaces/mktpl-claude-datasaas/` |

Claude Code runs the **installed** copy. Edits to source don't take effect until reinstall.

```bash
# From inside the source repo
./scripts/post-update.sh   # clears plugin cache
# Then restart Claude Code
```

If you edited the installed copy directly, your changes will be overwritten on next update. Move them back to source.

## 3. A command doesn't exist

Symptom: `/sprint plan` or `/data ingest` says "unknown command".

- Is it one of the commands removed in v12? Check `docs/COMMANDS-CHEATSHEET.md` → "Removed in v12.0.0" table.
- Did you install the short skill aliases? Run `./scripts/install-skill-aliases.sh` — without them, you have to use the fully-qualified form like `/projman:sprint`.
- Did you restart Claude Code after the install?

## 4. A hook is blocking you

`git-guardrails` has two `PreToolUse(Bash)` hooks:

- `branch-check.sh` — blocks invalid branch names.
- `commit-msg-check.sh` — blocks non-Conventional-Commits messages.

**Don't bypass.** Fix the name / message. See `plugins/git-guardrails/README.md` for the valid formats.

## 5. Gitea MCP tools return errors

Check credentials:

```bash
cat ~/.config/claude/gitea.env   # must have real token, not template
cat .env                          # must have GITEA_ORG and GITEA_REPO
```

Verify the token works:

```bash
source ~/.config/claude/gitea.env
curl -H "Authorization: token $GITEA_API_TOKEN" "$GITEA_API_URL/user" | jq .
```

If `401`, regenerate the token in Gitea. If `404`, check `GITEA_API_URL` (trailing `/api/v1` required).

## 6. Validation fails

```bash
./scripts/validate-marketplace.sh
./scripts/verify-hooks.sh
```

Both should exit `0`. If `validate-marketplace.sh` fails, it names the exact file and field. If `verify-hooks.sh` fails, the hook inventory drifted from the expected 2-hooks-in-git-guardrails state.

## 7. Sessions are getting compressed too often

Expected symptoms after v12.0.0:
- Much less compression.
- If you're still seeing frequent compression, the common causes are:
  1. Running projman workflows with a very long `CLAUDE.md` at project level (v12 target: <200 lines).
  2. Loading many projman skills upfront — v12 converted them to the Skills system so they load lazily; confirm your installed copy is v12.
  3. A consumer project has its own large CLAUDE.md. Trim it using the same guidance.

## 8. Investigating "what did Claude actually do"

Projman's orchestrator posts progress updates to Gitea issues via `add_comment`. Check the issue thread.

For code changes, use standard git tooling:

```bash
git log --oneline -20
git diff HEAD~5 HEAD
```

## 9. Fresh-install verification

On a new machine:

```bash
git clone <repo>
cd mktpl-claude-datasaas
./scripts/setup.sh                       # creates venvs, templates, skill aliases
# Fill in ~/.config/claude/gitea.env
# Create .env in project with GITEA_ORG and GITEA_REPO
./scripts/validate-marketplace.sh        # should print "All validations passed"
./scripts/verify-hooks.sh                # should print "All hooks verified"
# Start Claude Code — /sprint status should return your current sprint
```

## 10. When all else fails

1. Re-read the output of the failing command. It usually names the file.
2. Check `docs/CANONICAL-PATHS.md` — if a path isn't listed, it shouldn't exist.
3. Run `./scripts/validate-marketplace.sh` — broken file references are the most common failure.
4. Ask for help with the exact error message and the output of `./scripts/validate-marketplace.sh`.
