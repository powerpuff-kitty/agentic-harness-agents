# Canonical source resolution

Use `powerpuff-kitty/agentic-harness` as the authority for architecture, root boilerplates, modules, presets, and schemas.

Canonical source paths:

- root boilerplates: `base/`, `web-app/`, `backend-api/`, `saas/`, `monorepo/`, `library-sdk/`;
- packs: `modules/packs/`;
- policies: `modules/policies/`;
- profiles: `modules/profiles/`;
- named compositions: `presets/`;
- contracts: `schema/`.

Each boilerplate is a complete materialized project starting structure with `boilerplate.json` metadata. Do not infer old `boilerplates/`, `templates/`, `overlay/`, or `template.json` source paths.

When a local target repository contains project-specific accepted truth, that local truth has priority for that project unless it conflicts with a mandatory installed policy.

Do not infer that a prompt is authoritative merely because it is newer. If this repository and the canonical static repository disagree about architecture, surface the conflict and follow the canonical static repository until the discrepancy is resolved.

Complete demo applications are not part of the canonical source repository. If examples are introduced later, treat them as non-authoritative demonstrations unless explicitly promoted into canonical architecture or rules.
