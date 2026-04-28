# ARCHITECT.md

## Purpose
- This fork adapts `kkrizka/mcp-justwatch` for secure remote MCP deployment.
- The initial target runtime is a NixOS 25.11 host with Nginx TLS termination and a loopback-bound FastMCP HTTP process.
- Preserve upstream compatibility where practical while keeping fork-specific delivery and operational guidance easy to find.

## System shape
- The application remains a Python MCP server implemented in `src/mcp_justwatch/server.py`.
- Default runtime mode is local `stdio` for MCP host integrations.
- Optional runtime mode is FastMCP `http` transport for reverse-proxied remote deployment.
- In HTTP mode, the app exposes `/mcp` as the protocol endpoint and `/health` as a simple health endpoint.

## Runtime modes
### Stdio mode
- Default mode.
- Intended for local MCP clients.
- No public network listener.

### HTTP mode
- Enabled with `MCP_JUSTWATCH_TRANSPORT=http`.
- Intended for reverse-proxied HTTPS deployment.
- Expected bind target is loopback only unless a different deployment model is deliberately documented.

## Deployment invariants
- Do not expose the raw Python process directly to the public internet.
- Bind the application to `127.0.0.1` in the baseline deployment shape.
- Publish only the reverse proxy on ports 80 and 443.
- Terminate TLS at Nginx.
- Prefer API-key enforcement at the reverse proxy for the first remote deployment milestone.
- Keep configuration environment-driven.

## Environment variables
- `MCP_JUSTWATCH_TRANSPORT` → `stdio` or `http`
- `MCP_JUSTWATCH_HOST` → bind host for HTTP mode
- `MCP_JUSTWATCH_PORT` → bind port for HTTP mode
- `MCP_JUSTWATCH_LOG_LEVEL` → logging level
- `MCP_JUSTWATCH_LOG_FILE` → optional file log path

## Repo layout
- `src/` → Python package code
- `tests/` → unit and runtime tests
- `docs/plan/` → project plans
- `docs/design/` → design notes, deployment notes, connector setup notes, example configs
- `docs/adr/` → architecture decision records
- `.agents/` → agent-oriented scaffolding and optional helper material
- `ARCHITECT.md` → stable architecture and repo rules
- `PROGRESS.md` → active progress, milestones, loops, verification snapshot
- `STREAMS.md` → workstream status and handoff context
- `ROADMAP.md` → dependency-aware execution path
- `actions.jsonl` → append-only action log

## Status tracking rules
- Read `ARCHITECT.md`, `PROGRESS.md`, and `STREAMS.md` before substantive work.
- Update `PROGRESS.md` or `STREAMS.md` in the same commit as status-changing work.
- Append major actions and verification events to `actions.jsonl`.
- Keep root status files short enough to fit comfortably alongside active code context.
- Treat long-form reasoning and durable decisions as docs or ADR material, not as transient status notes.

## Safe change rules
- Do not remove or rename MCP tools without replacement coverage and tests.
- Do not broaden network exposure without documenting the new security posture.
- Prefer focused changes over broad refactors.
- Keep fork-specific delivery materials isolated from upstream-facing code where possible.

## Verification baseline
Run these before claiming implementation success for Python or runtime changes:

```bash
pytest -q
ruff check src tests
python -m compileall src
```

For runtime changes, also verify local HTTP startup and `/health` behavior.
