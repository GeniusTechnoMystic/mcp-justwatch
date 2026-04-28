# AGENTS.md

## Repository purpose
- This fork adapts `mcp-justwatch` for secure remote MCP deployment, with an initial target of NixOS 25.11 behind Nginx and TLS.
- Preserve upstream compatibility where practical and isolate fork-specific operations in `docs/` and `.agents/`.

## Working agreements
- Prefer minimal, reversible changes over broad refactors.
- Keep upstream-facing code changes focused on transport, runtime configuration, logging, and deployment readiness.
- Place project planning and design material under `docs/plan/`, `docs/design/`, and `docs/adr/`.
- Place agent-oriented operational guidance under `.agents/`.

## Safe change rules
- Do not remove existing MCP tools unless a replacement is documented and tested.
- Do not expose a public network listener without TLS termination and documented auth posture.
- Default to loopback binding for local app processes.
- Prefer environment-variable configuration for host, port, auth, and logging behavior.

## Validation expectations
- Run tests before claiming success.
- For Python changes, run targeted tests first, then the full test suite if feasible.
- When changing runtime behavior, verify expected startup behavior locally.
- Document any command that fails and why.

## Documentation expectations
- Update docs when behavior or deployment instructions change.
- Record architecture-significant decisions in `docs/adr/`.
- Keep docs short, explicit, and dated.

## Git hygiene
- Use focused commits.
- Keep the branch rebased on upstream `main` when practical.
- Do not mix scaffolding-only changes with unrelated implementation changes unless the docs are required for the code review.
