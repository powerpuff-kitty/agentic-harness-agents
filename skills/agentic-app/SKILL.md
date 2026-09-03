# Agentic App Architecture

Use this skill to initialize, upgrade, or audit an agent-native repository.

## Source-of-truth rule

Resolve canonical architecture, templates, packs, policies, profiles, presets, schemas, and examples from `https://github.com/powerpuff-kitty/agentic-harness`. This skill describes procedure; it must not redefine that source.

## INIT
Inspect the target, infer safe defaults, ask only missing high-impact questions, propose the resolved template/profile/packs/policies/skills, then use `ah` or equivalent deterministic composition. Preserve project-specific truth.

## UPGRADE
Inspect first. Preserve existing implementation and accepted decisions. Add or repair only missing harness layers. Do not overwrite project-specific truth with generic templates.

## AUDIT
Read-only unless explicitly asked otherwise. Evaluate architecture/docs/tests/security/operations/agent structure and design-system compliance when active. Ground findings in repository evidence.

## Workflow

1. Discover the repository using `references/repository-discovery.md`.
2. Resolve canonical source material from `agentic-harness`.
3. Separate facts, inference, and unresolved decisions.
4. Select template/preset/profile/packs/policies and appropriate skills.
5. Show consequential assumptions before high-impact policy/permission changes.
6. Apply with deterministic tooling where available.
7. Validate repository-native checks plus `ah validate` / `ah audit` as appropriate.
8. Persist only durable accepted decisions; keep temporary execution state separate.

For design-heavy projects, use the design-system and design-system-compliance skills and the canonical design-system pack.
