---
name: agentic-app
description: "Initialize, upgrade, migrate or broadly audit a repository using the Agentic Harness contract and selected modules. Use when the job spans overall harness setup or lifecycle. Do not use for focused readiness scoring, standalone legacy migration, design-only lifecycle orchestration or a single specialist review."
---
# Agentic App

## Objective

Orchestrate the Agentic Harness lifecycle while delegating specialist work and deterministic operations.

## Inputs

Required: target repository and requested init, upgrade, migrate or broad-audit mode. Optional: project type, maturity, stack, profile/preset, packs, policies, skills, design posture and approval boundaries.

## Context

Resolve current contract/catalog from agentic-harness using project pins. Route from AGENTS.md to .agentic/manifest.yaml and task-relevant truth. Follow bundled repository-discovery/context guidance when present; standalone installs inspect the local router without requiring unrelated files.

## Procedure

1. Inspect the target before asking for facts the repository can answer.
2. Resolve missing high-impact choices and state consequential assumptions.
3. Select canonical variant/preset/profile plus installed modules/skills. Check actual tool and skill availability; never claim delegation to a missing specialist.
4. Prefer supported ah composition, migration, validation and audit over hand-copying contracts. Verify version/help before invoking commands.
5. Preserve project-authored truth and accepted ADRs during upgrades/migration.
6. Route multi-stage design work to design-intelligence; route focused identity, analysis, research, component resolution, UX, design-system, compliance and accessibility requests directly to their owning skills. Installing a skill does not install a provider, dataset, MCP server or runtime analyzer.
7. Route security, model-fit, ADR and release tasks to their existing specialists.
8. Verify root hygiene, links, manifest/lock integrity, native tests and relevant gates. Do not silently change approvals or release/update installed skill snapshots.

## Output

Return composition/audit scope, files/modules affected, assumptions, actual command results, conflicts, approvals, handoffs and remaining risks.

## Completion

The requested operation is repeatable, canonical truth preserved, sources pinned, and actual validation recorded. Missing tools/skills/providers and skipped checks remain explicit rather than being replaced with claimed success.
