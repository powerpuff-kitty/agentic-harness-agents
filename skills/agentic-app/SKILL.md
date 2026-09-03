# Agentic App Architecture

Use this skill to initialize, upgrade, or audit an agent-native repository.

## Source-of-truth rule

Resolve canonical architecture from `https://github.com/powerpuff-kitty/agentic-harness`. Root boilerplates (`base`, `web-app`, `backend-api`, `saas`, `monorepo`, `library-sdk`) define complete project starting structures. Reusable packs, policies, and profiles live under `modules/`; presets and schemas remain top-level canonical contracts. This skill describes procedure and must not redefine those sources.

## INIT
Inspect the target, infer safe defaults, ask only missing high-impact questions, propose the resolved boilerplate/profile/packs/policies/skills, then use `ah` or equivalent deterministic composition. Preserve project-specific truth.

## UPGRADE
Inspect first. Preserve existing implementation and accepted decisions. Add or repair only missing harness layers. Do not overwrite project-specific truth with generic boilerplate content.

## AUDIT
Read-only unless explicitly asked otherwise. Evaluate architecture/docs/tests/security/operations/agent structure and design-system compliance when active. Ground findings in repository evidence.

## Workflow

1. Discover the repository using `references/repository-discovery.md`.
2. Resolve the selected root boilerplate plus canonical modules/preset/schema information from `agentic-harness`.
3. Separate facts, inference, and unresolved decisions.
4. Select boilerplate/preset/profile/packs/policies and appropriate skills.
5. Show consequential assumptions before high-impact policy/permission changes.
6. Apply with deterministic tooling where available.
7. Validate repository-native checks plus `ah validate` / `ah audit` as appropriate.
8. Persist only durable accepted decisions; keep temporary execution state separate.

Do not depend on deprecated canonical source paths such as `boilerplates/`, `templates/`, `overlay/`, or `template.json`.

For design-heavy projects, use the design-system and design-system-compliance skills and the canonical design-system pack.
