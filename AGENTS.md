# Agent instructions

This repository owns agent procedures, not canonical Agentic Harness architecture.

Before changing a skill or prompt that depends on project structure, packs, policies, profiles, presets, schemas, or architecture, consult `https://github.com/powerpuff-kitty/agentic-harness` and treat it as the main source of truth.

Canonical project starting points are complete root directories (`base/`, `web-app/`, `backend-api/`, `saas/`, `monorepo/`, `library-sdk/`). Shared modules live under `modules/packs/`, `modules/policies/`, and `modules/profiles/`. Do not rely on deprecated `boilerplates/`, `templates/`, or `template.json` paths.

Keep vendor adapters thin. Put reusable workflow in `skills/`, invocation examples in `prompts/`, and shared agent-only operating guidance in `references/`. Do not duplicate large canonical documents from the static repository.
