---
name: release-review
description: "Review a release candidate against documented quality, security, migration, compatibility, documentation, artifact, and operational gates and return a go/no-go assessment. Use before publication when release readiness is the requested decision. Do not use to publish the release itself or for a general repository audit unrelated to a candidate."
---
# Release Review

## Objective

Determine whether a specific release candidate meets its declared release criteria and identify blockers before publication.

## Inputs

Required: target repository/candidate commit or artifact set. Optional: target version, release checklist, baseline, deployment environment, migration plan, and required score thresholds.

## Context

Read release policy/checklist, candidate diff, CI/test/security results, migration/rollback docs, changelog, version metadata, and affected architecture/API compatibility evidence.

## Procedure

1. Confirm the exact candidate commit/version/artifacts under review.
2. Enumerate required gates from project policy instead of inventing arbitrary ones.
3. Verify CI, tests, security checks, migrations, compatibility, docs/changelog, artifact provenance, and operational readiness.
4. Distinguish blocking failures from warnings and unavailable checks.
5. Reproduce critical checks or inspect primary evidence rather than relying on status summaries alone where feasible.
6. Assess rollback and monitoring for risky changes.
7. Return go/no-go/conditional with explicit rationale; do not publish.

## Output

Return candidate identity, gate table, blockers, warnings, skipped/unavailable checks, compatibility/migration risks, and final readiness recommendation.

## Completion

Every required gate has evidence or an explicit unknown, blockers are unambiguous, and the review remains separate from publication authorization/execution.
