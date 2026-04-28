# Remote HTTP + NixOS Design

**Date:** 2026-04-28
**Status:** Proposed

## Current state
The upstream project is a small FastMCP-based Python package intended for MCP host configuration and local execution. Current docs emphasize stdio-style invocation from MCP clients and do not describe remote HTTPS deployment.

## Target state
This fork should support running the MCP server as a local process bound to loopback, exposed externally only through a reverse proxy that terminates TLS and optionally enforces API-key authentication.

## Architecture
- Python application process runs locally via systemd.
- Application binds to `127.0.0.1` on a configurable port.
- Nginx proxies `/mcp` and optional `/health` to the local process.
- NixOS firewall exposes only 80 and 443 publicly.
- Home router forwards 80 and 443 to the NixOS host.
- Perplexity remote connector targets the HTTPS `/mcp` endpoint.

## Design choices
### Transport
Use FastMCP HTTP transport for the fork’s remote deployment mode, while preserving a path for local development and testing.

### Network exposure
Do not expose the Python process directly to the internet. Use loopback binding plus Nginx.

### Authentication
Prefer a simple API-key layer at the reverse proxy for the first secure deployment.

### Logging
Prefer stdout or stderr logging suitable for systemd and journald rather than mandatory file logging.

### Documentation split
Keep human planning material in `docs/` and agent operations material in `AGENTS.md` and `.agents/`.

## Open questions
- Whether HTTP transport should replace default behavior or be enabled by environment variable or CLI flag.
- Whether a health endpoint is provided by FastMCP alone or should be explicitly added/documented.
- Whether proxy-layer auth is sufficient for the first milestone.
