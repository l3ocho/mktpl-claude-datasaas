# Virtual Environment Diagnostics Skill

Patterns for checking virtual environment health in MCP server directories.

## Check 1: Venv Exists

```bash
test -d <server_cwd>/.venv && echo "EXISTS" || echo "MISSING"
```

If missing, the server will fail to start. Fix:
```bash
cd <server_cwd> && python3 -m venv .venv
```

## Check 2: Python Binary Intact

Venvs can break when the system Python is upgraded (symlink becomes dangling).

```bash
<server_cwd>/.venv/bin/python --version 2>&1
```

If error contains "No such file or directory" despite .venv existing, the symlink is broken.

Fix:
```bash
cd <server_cwd> && rm -rf .venv && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

**IMPORTANT:** Never delete .venv without explicit user approval. Show the diagnosis and ask user to confirm the fix.

## Check 3: Requirements Satisfied

Compare requirements.txt with installed packages:

```bash
cd <server_cwd> && .venv/bin/pip freeze > /tmp/installed.txt
```

Then diff against requirements.txt:
- **Missing packages:** In requirements but not installed
- **Version mismatch:** Installed version does not satisfy requirement specifier
- **Extra packages:** Installed but not in requirements (usually OK, may indicate stale venv)

Quick check:
```bash
cd <server_cwd> && .venv/bin/pip check 2>&1
```

This reports broken dependencies (missing or incompatible versions).

## Check 4: Module Import Test

Verify the server's main module can be imported:

```bash
cd <server_cwd> && .venv/bin/python -c "import <module>.server" 2>&1
```

Where `<module>` is the server's Python module:
- gitea: `gitea_mcp` (pip-installed package)
- All others: `mcp_server` (local source)

Common failures:
| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'mcp'` | MCP SDK not installed | `pip install mcp` |
| `ModuleNotFoundError: No module named '<pkg>'` | Missing dependency | `pip install -r requirements.txt` |
| `ImportError: cannot import name 'X'` | Version mismatch | `pip install --upgrade <pkg>` |
| `SyntaxError` | Python version too old | Check `python3 --version` >= 3.10 |

## Check 5: Broken Symlinks

Find broken symlinks in the venv:

```bash
find <server_cwd>/.venv -type l ! -exec test -e {} \; -print 2>/dev/null
```

Any output indicates broken symlinks that may cause import failures.

## Health Summary Format

```
### Venv: <server_name>
- Directory: EXISTS
- Python: 3.11.2 (OK)
- Packages: 12 installed, 10 required, 0 missing
- Import: OK
- Broken symlinks: 0
- Status: HEALTHY
```
