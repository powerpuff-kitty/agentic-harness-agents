# Agentic App

Use this skill to initialize, migrate, upgrade, or audit an agent-native repository.

## Source rule

Resolve the current contract and catalog from `agentic-harness`. A target project uses root `AGENTS.md`, canonical `.agentic/` context, and installed `.agents/skills/`. This skill defines procedure only.

## Discovery

Follow `references/repository-discovery.md`. Read permissions and precedence before proposing writes.

## INIT

1. Inspect the target and avoid asking for repository-discoverable facts.
2. Ask only missing high-impact questions: project purpose/type, maturity, stack constraints, deployment/data/security posture, design-system choice, and approval boundaries.
3. Resolve a catalog boilerplate/preset/profile plus packs, policies, and skills.
4. Show consequential assumptions.
5. Use deterministic composition when available.
6. Verify root hygiene, router links, canonical context, lock resolution, and repository-native checks.

## MIGRATE

1. Detect legacy and current layouts.
2. Produce a non-writing move/conflict plan first.
3. Treat identical duplicates separately from divergent canonical files.
4. Require explicit apply authorization and an optional backup path.
5. Never delete a source before the destination is written and verified.
6. Re-run migration to prove idempotence, then validate/audit.

## UPGRADE

Inspect first. Preserve project-authored truth and accepted decisions. Upgrade installed modules and schemas through the lockfile; do not replace canonical content with generic placeholders. Report incompatible changes before applying them.

## AUDIT

Remain read-only unless explicitly asked to repair. Evaluate code quality, maintainability, architecture, testing, security, dependency health, documentation, operations, agent docs, root hygiene, router validity, canonical uniqueness, ADR integrity, placeholder quality, maturity/profile compliance, adapter thinness, module/lock integrity, and design-system compliance when active.

## Completion

Run applicable native checks plus `ah doctor`, `ah validate`, and `ah audit` when available. Report evidence, skipped checks, remaining risks, and unresolved decisions.
