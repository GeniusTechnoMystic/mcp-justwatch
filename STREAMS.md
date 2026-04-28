# STREAMS.md

## Active streams

### Stream S1: Runtime and code path
- Branch: `project/remote-http-nixos`
- Scope: Python runtime settings, transport selection, logging, health endpoint, tests
- Status: complete for the current milestone slice
- Latest relevant commits:
  - `aca3771` — remote HTTP runtime and deployment docs
- Notes:
  - Current runtime supports `stdio` and `http` transport modes.
  - HTTP mode is designed for reverse-proxied deployment rather than direct public exposure.

### Stream S2: Deployment documentation
- Branch: `project/remote-http-nixos`
- Scope: NixOS deployment notes, Perplexity connector setup notes, README updates, example configs
- Status: complete for documentation baseline
- Latest relevant commits:
  - `9aec3ad` — deployment examples and progress journal
- Notes:
  - Example configs exist for NixOS 25.11 and Nginx API-key enforcement.
  - A real host deployment has not been executed yet.

### Stream S3: Status tracking protocol
- Branch: `project/remote-http-nixos`
- Scope: migrate from scattered journal files to root-level living-state files
- Status: complete for current migration slice
- Result:
  - established `ARCHITECT.md`, `PROGRESS.md`, `STREAMS.md`, `ROADMAP.md`, and `actions.jsonl`
  - kept `.agents/` as auxiliary scaffolding rather than the primary status surface

## Blockers
- No public HTTPS host has been provisioned yet.
- Connector validation cannot happen until live deployment exists.

## Handoff
- The branch is locally verified and currently focused on operational readiness rather than new runtime code.
- The next operator should read `ARCHITECT.md`, `PROGRESS.md`, `STREAMS.md`, and `ROADMAP.md`, then decide between:
  - opening a draft PR before deployment work, or
  - proceeding directly to first-host deployment and connector validation
- If deployment work starts next, update `PROGRESS.md` and append deployment actions to `actions.jsonl` in the same commit as any related docs or code changes.
