---
name: adapter-sync
description: "Synchronize vendor-required agent instruction files as thin adapters to root AGENTS.md and .agentic project truth. Use when creating, updating, checking, or reconciling Codex, Claude, Gemini, Copilot, or Cursor adapter files. Do not use for general documentation migration or for changing canonical project rules."
---
# Agent Adapter Synchronization

## Objective

Keep vendor-specific instruction surfaces minimal, non-authoritative, and consistent with the canonical project router.

## Inputs

Required: target repository. Optional: target vendors, existing adapter files, replacement authorization, and vendor-specific path constraints.

## Context

Read root `AGENTS.md`, `.agentic/manifest.yaml`, and relevant adapter guidance only. Do not copy product, architecture, security, policies, packs, or full skill bodies into adapters.

## Procedure

1. Detect supported vendor locations already present or explicitly requested; do not invent unsupported files.
2. Inspect each existing adapter for unrelated configuration that must be preserved.
3. Compare adapter authority claims and routing with root `AGENTS.md` and `.agentic/`.
4. Generate the smallest vendor-compatible routing statement needed.
5. Treat divergent substantive instructions as conflicts; require explicit replacement authorization rather than silently deleting them.
6. Apply deterministic changes and re-run synchronization to prove idempotence.
7. Check adapter length, canonical references, and contradictory rules.

## Output

Report adapters created/updated/unchanged, preserved vendor configuration, conflicts requiring review, and idempotence/validation results.

## Completion

All requested adapters route to the same canonical truth, contain no duplicated project rules, preserve unrelated settings, and a second synchronization produces no further changes.
