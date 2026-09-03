# Agent instructions

This repository owns agent procedures, not canonical Agentic Harness architecture.

Before changing a skill or prompt that depends on templates, packs, policies, profiles, schemas, or architecture, consult `https://github.com/powerpuff-kitty/agentic-harness` and treat it as the main source of truth.

Keep vendor adapters thin. Put reusable workflow in `skills/`, invocation examples in `prompts/`, and shared agent-only operating guidance in `references/`. Do not duplicate large canonical documents from the static repository.
