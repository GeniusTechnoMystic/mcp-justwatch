# PROGRESS.md

## Current milestone
Remote HTTPS deployment-ready fork for Perplexity-compatible MCP hosting.

## Session pause snapshot
- Status: paused intentionally for token-budget control
- Pause point: root-level living-state status protocol has been adopted and pushed
- Latest branch commit: `7b9083d`
- Resume priority: open draft PR or begin first live NixOS deployment

## Milestone checklist
- [x] Fork upstream repo and create project branch `project/remote-http-nixos`
- [x] Add project planning, design notes, and ADR scaffolding
- [x] Implement environment-driven FastMCP HTTP runtime support
- [x] Add `/health` endpoint for service-manager and proxy checks
- [x] Update tests for current FastMCP behavior
- [x] Add NixOS deployment notes and Perplexity connector setup notes
- [x] Expand README with HTTP mode and deployment guidance
- [x] Add concrete NixOS and proxy auth examples
- [x] Migrate status tracking to root-level living-state files
- [ ] Deploy to a real HTTPS endpoint
- [ ] Validate end-to-end with a Perplexity custom remote connector
- [ ] Decide what is suitable for upstream contribution

## Active loops
### Loop L1: First live deployment
- Status: pending
- Context: The branch is locally verified and deployment-ready in documentation, but no public HTTPS host has been configured yet.
- Next step: Stand up a NixOS host, apply the documented reverse-proxy shape, and confirm `/health` and `/mcp` over HTTPS.

### Loop L2: Connector validation
- Status: blocked on L1
- Context: Perplexity remote connector validation depends on a working public HTTPS endpoint.
- Next step: Create the connector against the deployed `/mcp` URL and validate auth and transport settings.

### Loop L3: Packaging decision
- Status: pending
- Context: The repo has example NixOS configuration but not a reusable Nix derivation, module, or flake.
- Next step: Decide whether the next reproducibility layer should be a package, a module, or a full flake example.

### Loop L4: Upstreaming strategy
- Status: pending
- Context: Some runtime changes may be upstreamable, while fork-specific docs and deployment opinions likely are not.
- Next step: Separate generic transport improvements from fork-specific deployment materials and assess contribution scope.

## Latest verification snapshot
**Date:** 2026-04-28
**Verified baseline commit:** `9aec3ad`
**Verified current working tree:** root-level status protocol migration changes applied and uncommitted at verification time

### Commands
```bash
pytest -q
ruff check src tests
python -m compileall src
```

### Results
- `pytest -q` → `32 passed`
- `ruff check src tests` → `All checks passed`
- `python -m compileall src` → completed successfully

## Success criteria
- [x] Local stdio mode remains intact
- [x] Local HTTP mode starts on loopback successfully
- [x] `/health` returns `OK` in HTTP mode
- [x] Root-level living-state files exist for progress tracking
- [ ] Public HTTPS endpoint is reachable through reverse proxy only
- [ ] Perplexity custom remote connector validates successfully
- [ ] Deployment runbook is proven against a real host
