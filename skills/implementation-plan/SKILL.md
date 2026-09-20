---
name: implementation-plan
description: "Turn accepted product or architecture scope into an executable, dependency-aware implementation plan with milestones, verification, risks, and rollback points. Use when the user asks how to implement approved work before or alongside coding. Do not use to decide unresolved architecture/product direction or to maintain general documentation after implementation."
---
# Implementation Plan

## Objective

Sequence accepted scope into executable, verifiable work without inventing decisions.

## Inputs

Repository and accepted scope; optional deadlines, team, rollout/migration constraints, tests and target release.

## Context

Follow project routes to applicable rules, affected source/tests and relevant ADRs/tasks. Expand for unresolved dependencies; refresh reused evidence after source, rules or scope change.

## Procedure

1. State outcomes, constraints and unresolved decisions.
2. Map components, API/data boundaries, dependencies and migration/rollout risks.
3. Order prerequisites and reversible steps. Give each major task source references and an observable check, not a blanket reading list.
4. Preserve required checks and approvals for schema, infrastructure, production, policy, secrets and destructive work. Include rollback for user/data risk.
5. Keep tasks implementation-sized. Delegate only necessary independent work; no default extra agents or Jev calls.
6. Reuse existing plans. On continuation, update changed steps, evidence and blockers rather than replay history; keep trivial plans inline.

## Output

Tasks, dependencies, affected files, checks, gates, risks and rollback. Leave unmeasured cost/token benefits unknown.

## Completion

The plan has explicit dependencies, blockers, verification and rollback where needed. Writing it does not execute checks, approve actions or deliver implementation.
