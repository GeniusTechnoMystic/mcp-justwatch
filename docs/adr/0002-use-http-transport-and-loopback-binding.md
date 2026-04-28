# ADR-0002: Use HTTP transport and loopback-first runtime configuration

**Date**: 2026-04-28
**Status**: accepted
**Deciders**: user, Perplexity Computer

## Context
The upstream project is oriented around local MCP host execution and currently starts with `mcp.run()` and file-based logging. This fork needs a runtime mode suitable for secure remote deployment behind Nginx and compatible with Perplexity remote connectors, which require an HTTPS-accessible remote MCP endpoint using Streamable HTTP or SSE.

## Decision
We will add environment-configurable runtime settings and support FastMCP HTTP transport for remote deployment. The application process will default to loopback binding and rely on a reverse proxy for public exposure, TLS termination, and optional API-key enforcement.

## Alternatives Considered
### Alternative 1: Keep stdio-only behavior
- **Pros**: Minimal change and maximum upstream similarity.
- **Cons**: Does not support remote HTTPS deployment for the target use case.
- **Why not**: It does not satisfy the deployment goal.

### Alternative 2: Expose the Python app directly on a public interface
- **Pros**: Fewer moving parts than using a reverse proxy.
- **Cons**: Weaker operational posture for TLS, auth, and deployment hardening.
- **Why not**: Reverse proxying is safer and better aligned with the NixOS target deployment.

### Alternative 3: Add OAuth in the first milestone
- **Pros**: Stronger auth story.
- **Cons**: Significantly more complexity than needed for the first deployment.
- **Why not**: API-key protection at the proxy layer is sufficient for the first milestone.

## Consequences
### Positive
- The fork can support local development and remote deployment.
- Runtime behavior becomes explicit and configurable.
- Logging can align with systemd and journald instead of mandatory file output.

### Negative
- The server entrypoint becomes more complex than upstream.
- Deployment instructions must clearly distinguish local and remote modes.

### Risks
- FastMCP runtime API changes could require follow-up adjustments.
- Mitigation: keep the wrapper thin and covered by tests.
