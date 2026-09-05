---
name: implementation-plan
description: "Turn accepted product or architecture scope into an executable, dependency-aware implementation plan with milestones, verification, risks, and rollback points. Use when the user asks how to implement approved work before or alongside coding. Do not use to decide unresolved architecture/product direction or to maintain general documentation after implementation."
---
# Implementation Plan

## Objective

Translate accepted scope into a concrete sequence that another agent or engineer can execute and verify without inventing missing decisions.

## Inputs

Required: target repository and accepted outcome/scope. Optional: deadline, team boundaries, rollout constraints, migration requirements, test expectations, and target branch/release.

## Context

Read relevant product/architecture/security/design truth, accepted ADRs, affected source/tests, and current plans/tasks. Load only areas touched by the requested change.

## Procedure

1. Restate accepted outcome, constraints, and unresolved blockers.
2. Map affected components, data/API boundaries, dependencies, and migration/rollout concerns.
3. Sequence work so prerequisites and reversible steps come first.
4. Define a verification checkpoint and observable completion condition for every major step.
5. Identify approval gates for schema, infrastructure, production, policy, secret, or destructive changes.
6. Include rollback/backout strategy where failure could affect users/data.
7. Keep tasks implementation-sized and avoid prescribing unnecessary reasoning detail.

## Output

Return phases/tasks with dependencies, files/systems likely affected, validation per step, approval gates, risks, rollout/rollback, and definition of done.

## Completion

The plan is executable from repository truth, blocks on unresolved decisions instead of inventing them, covers verification and rollback where needed, and has no hidden dependency between steps.
