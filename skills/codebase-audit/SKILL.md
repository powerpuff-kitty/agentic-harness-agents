---
name: codebase-audit
description: "Perform a broad evidence-backed technical audit of code quality, maintainability, architecture, tests, dependencies, documentation, operations, performance posture, and security signals. Use when the user asks for an overall repository/codebase audit. Do not use when the requested score is specifically Agentic Readiness or when a single specialist review is sufficient."
---
# Codebase Audit

## Objective

Assess repository engineering health across the requested dimensions and prioritize actionable risks without overstating unexecuted checks.

## Inputs

Required: target repository. Optional: maturity target, scope, known incidents, quality thresholds, baseline audit, and excluded areas.

## Context

Read the repository router, relevant `.agentic/` truth, manifests/lockfiles, tests, CI, operational docs, and source files indicated by evidence. Use progressive disclosure; do not scan every file merely because it exists.

## Procedure

1. Profile languages, frameworks, manifests, tests, CI, docs, and operational surfaces.
2. Run available deterministic repository/audit commands first.
3. Inspect high-risk evidence for maintainability, architecture, testing, dependency health, security, operations, and performance.
4. Separate structural/file-presence signals from executed build/test/security results.
5. Rank findings by severity, confidence, blast radius, and remediation leverage.
6. Avoid duplicating specialist audits unless the broad review surfaces a reason to invoke them.

## Output

Return scoped scores/findings, exact evidence, confidence, remediation, checks performed, checks not performed, and maturity/readiness caveats.

## Completion

Findings are evidence-backed, high-severity claims were verified where feasible, specialist gaps are clearly routed, and the report never implies builds/tests/scanners ran when they did not.
