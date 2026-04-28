# ADR-0001: Use fork-local docs and agent scaffolding

**Date**: 2026-04-28
**Status**: accepted
**Deciders**: user, Perplexity Computer

## Context
This project starts as a fork of `kkrizka/mcp-justwatch` and needs planning, design, and operational guidance that is specific to secure remote deployment on NixOS. The upstream repository is small and does not currently contain a `docs/` tree or agent-scaffolding conventions.

## Decision
We will keep the project as a normal fork without creating a project subdirectory. We will add `docs/plan/`, `docs/design/`, and `docs/adr/` for human-facing project material, plus `AGENTS.md` and `.agents/` subdirectories for agent-facing operational guidance.

## Alternatives Considered
### Alternative 1: Flat files under `docs/`
- **Pros**: Simpler initial layout.
- **Cons**: Harder to scale as planning, design, and decisions accumulate.
- **Why not**: We expect multiple iterations and want cleaner separation.

### Alternative 2: Create a dedicated project subdirectory
- **Pros**: Maximum isolation from upstream material.
- **Cons**: Adds structural overhead and makes the fork feel heavier than needed.
- **Why not**: The repository is already focused on one project.

## Consequences
### Positive
- Human and agent documentation have clear homes.
- Future upstream proposals can keep fork-specific planning material easier to identify.
- The repository is ready for repeated agent-driven work.

### Negative
- The fork gains extra structure beyond upstream.
- Maintainers will need light discipline to keep `docs/` and `.agents/` current.

### Risks
- Some files may never be used if the workflow stays simple.
- Mitigation: keep scaffolding minimal and expand only when it proves useful.
