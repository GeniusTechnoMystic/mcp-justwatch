# Remote HTTP + NixOS Project Plan

**Date:** 2026-04-28
**Scope:** Adapt this fork of `mcp-justwatch` for secure remote MCP deployment suitable for Perplexity custom connectors.

## Goals
- Enable remote HTTP transport for the MCP server.
- Support secure deployment behind Nginx with HTTPS on NixOS 25.11.
- Add deployment guidance for systemd, firewall, and home-router port forwarding.
- Keep the fork understandable to both humans and coding agents.

## Non-goals
- Full OAuth implementation in the first release.
- Broad productization across multiple hosting platforms.
- Unrelated refactors of search logic or MCP tool behavior.

## Deliverables
- Runtime changes for HTTP transport.
- Configurable host and port behavior.
- Cleaner production logging behavior.
- Deployment docs for NixOS 25.11.
- Agent scaffolding and decision records.

## Milestones
1. Documentation and project scaffolding.
2. Runtime design and ADR capture.
3. HTTP transport implementation.
4. Local verification and test updates.
5. NixOS deployment examples.
6. Perplexity connector validation guidance.

## Ownership split
- Agent: research, design, implementation, verification, and documentation drafting.
- User: final hosting environment decisions, DNS, router configuration, and Perplexity connector setup.

## Risks
- FastMCP remote transport behavior may require changes beyond a one-line `run()` edit.
- Home-hosted TLS and router exposure can fail for ISP or NAT reasons.
- Upstream may not want deployment-specific changes merged as-is.

## Exit criteria
- Branch contains docs, ADRs, and agent scaffolding.
- Next implementation tasks are explicit and ordered.
- The fork is ready for transport implementation work.

## Immediate next jobs
1. Add a transport design ADR for remote HTTP mode and loopback-only binding.
2. Patch the FastMCP entrypoint to support HTTP transport with environment-based configuration.
3. Adjust logging so production runs cleanly under systemd and journald.
4. Add or update tests for startup configuration and any changed runtime behavior.
5. Draft NixOS 25.11 deployment instructions covering systemd, Nginx, ACME, firewall, and router forwarding.
6. Smoke-test local HTTP startup and document the Perplexity connector setup path.
