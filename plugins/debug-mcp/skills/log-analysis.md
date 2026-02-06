# Log Analysis Skill

Common MCP server error patterns, their root causes, and fixes.

## Error Pattern: ImportError

```
ImportError: No module named 'pynetbox'
```

**Root Cause:** Missing Python package in the virtual environment.

**Fix:**
```bash
cd <server_cwd> && .venv/bin/pip install -r requirements.txt
```

**Prevention:** Always run `pip install -r requirements.txt` after creating or updating a venv.

## Error Pattern: ConnectionRefused

```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Root Cause:** The external service the MCP server connects to is not running or not reachable.

**Checks:**
1. Is the target service running? (e.g., Gitea, NetBox)
2. Is the URL correct in the env file?
3. Is there a firewall or VPN issue?

**Fix:** Verify the service URL in `~/.config/claude/<server>.env` and confirm the service is accessible.

## Error Pattern: JSONDecodeError

```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1
```

**Root Cause:** The server received non-JSON response from the external API. Usually means:
- API returned HTML error page (wrong URL)
- API returned empty response (auth failed silently)
- Proxy intercepted the request

**Fix:** Check the API URL ends with the correct path (e.g., `/api/v1` for Gitea, `/api` for NetBox).

## Error Pattern: TimeoutError

```
TimeoutError: timed out
httpx.ReadTimeout:
```

**Root Cause:** Server startup took too long or external API is slow.

**Checks:**
1. Network latency to the external service
2. Server doing heavy initialization (loading all tools)
3. Large response from API

**Fix:** Increase timeout in server config or reduce initial tool registration.

## Error Pattern: PermissionError

```
PermissionError: [Errno 13] Permission denied: '/path/to/file'
```

**Root Cause:** Server process cannot read/write required files.

**Fix:** Check file ownership and permissions. Common locations:
- `~/.config/claude/*.env` (should be readable by user)
- Server's `.venv/` directory
- Log files

## Error Pattern: FileNotFoundError (Venv)

```
FileNotFoundError: [Errno 2] No such file or directory: '.venv/bin/python'
```

**Root Cause:** Virtual environment does not exist or was deleted.

**Fix:** Create the venv:
```bash
cd <server_cwd> && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

## Error Pattern: SSL Certificate Error

```
ssl.SSLCertVerificationError: certificate verify failed
```

**Root Cause:** Self-signed certificate on the target service.

**Fix:** Set `VERIFY_SSL=false` in the env file (not recommended for production).

## Log Parsing Tips

1. **Python tracebacks** - Read from bottom up. The last line is the actual error.
2. **JSON-RPC errors** - Look for `"error"` key in JSON responses.
3. **Startup failures** - First few lines after server spawn reveal initialization issues.
4. **Repeated errors** - Same error in a loop means the server is retrying and failing.
