---
name: dependency-upgrade
description: "Plan and execute safe package, framework, runtime, or toolchain dependency upgrades with changelog review and compatibility verification. Use when the main task is changing dependency versions or adapting to their breaking changes. Do not use for Agentic Harness filesystem migration, ordinary release packaging, or unrelated refactoring."
---
# Dependency Upgrade

## Objective

Upgrade dependencies with minimal scope, explicit compatibility evidence, and reproducible verification.

## Inputs

Required: target repository and dependency/runtime/toolchain to upgrade. Optional: target version, security advisory, compatibility window, lockfile policy, and rollout constraints.

## Context

Read dependency manifests/lockfiles, relevant architecture/security policies, CI, and code directly coupled to the dependency. Consult authoritative release notes/advisories for the exact source and target versions.

## Procedure

1. Establish current resolved versions and why the upgrade is needed.
2. Read release notes, migration guides, advisories, and supported runtime ranges.
3. Identify breaking API/config/build changes and transitive dependency impacts.
4. Update manifests and lockfiles using the repository's native package manager.
5. Make only required compatibility edits; avoid unrelated modernization churn.
6. Run focused tests first, then applicable broader checks/builds.
7. Report unresolved deprecations, behavior changes, and rollback considerations.

## Output

Return version changes, authoritative compatibility evidence, code/config adaptations, test/build results, remaining warnings, and rollback notes.

## Completion

Resolved versions are locked, required migrations are complete, applicable checks pass, and no unsupported compatibility claim is left implicit.
