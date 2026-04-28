# Test Results

**Date:** 2026-04-28
**Branch:** `project/remote-http-nixos`
**Verified commit:** `aca3771`

## Commands run
```bash
pytest -q
ruff check src tests
python -m compileall src
```

## Results
- `pytest -q` → `32 passed`
- `ruff check src tests` → `All checks passed`
- `python -m compileall src` → completed successfully

## HTTP smoke test
### Startup command
```bash
env MCP_JUSTWATCH_TRANSPORT=http MCP_JUSTWATCH_HOST=127.0.0.1 MCP_JUSTWATCH_PORT=8123 python -m mcp_justwatch.server
```

### Observed behavior
- FastMCP started on `http://127.0.0.1:8123/mcp`
- `GET /health` returned `200 OK` with body `OK`
- Plain `GET /mcp` returned `406 Not Acceptable`, which is expected for a protocol endpoint rather than a generic browser route
