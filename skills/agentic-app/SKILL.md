---
name: agentic-app
description: "Initialize, upgrade, migrate, or broadly audit a repository using the Agentic Harness project contract and selected catalog modules. Use when the requested job spans overall harness setup or lifecycle rather than one specialist procedure. Do not use for a focused readiness score, a standalone legacy migration, or a single domain review when a narrower skill owns the task."
---
# Agentic App

## Objective

Orchestrate the end-to-end Agentic Harness lifecycle while delegating specialist work to narrower skills and deterministic CLI operations.

## Inputs

Required: target repository and requested mode (`init`, `upgrade`, `migrate`, or broad audit). Optional: project type, maturity, stack constraints, profile/preset, packs, policies, skills, design-system posture, and approval boundaries.

## Context

Resolve the current contract/catalog from `agentic-harness`. In a target project, route from root `AGENTS.md` to `.agentic/manifest.yaml` and task-relevant truth. Follow `references/repository-discovery.md` and progressive disclosure.

## Procedure

1. Inspect the target before asking for facts the repository can answer.
2. Resolve only missing high-impact choices and state consequential assumptions.
3. Select the canonical variant/preset/profile plus modules and skills.
4. Prefer `ah` deterministic composition, migration, validation, and audit over hand-copying contract files.
5. Preserve project-authored truth and accepted ADRs during upgrades/migration.
6. Route specialist security, design, model-fit, ADR, or release work to the appropriate narrower skill.
7. Verify root hygiene, router links, manifest/lock integrity, native tests, and relevant quality gates.

## Output

Return resolved composition or audit scope, files/modules affected, assumptions, deterministic command results, conflicts, approvals, and remaining risks.

## Completion

The requested lifecycle operation is complete and repeatable, canonical truth is preserved, installed sources are locked, applicable checks pass, and unresolved decisions or skipped validation are explicit.
