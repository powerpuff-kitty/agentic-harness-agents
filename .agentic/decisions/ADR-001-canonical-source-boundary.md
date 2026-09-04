# ADR-001: Keep agent procedures downstream of canonical project truth

- Status: accepted
- Date: 2026-09-04
- Deciders: project maintainer
- Supersedes: none
- Superseded by: none

## Decision

This repository defines procedure only. Canonical target structure, policy, packs, profiles, presets, and schemas are resolved from `agentic-harness`; deterministic mechanics belong to `agentic-harness-cli`.

## Consequences

Skills stay portable and prompts cannot silently become architecture. Cross-repository pinning and validation are required.
