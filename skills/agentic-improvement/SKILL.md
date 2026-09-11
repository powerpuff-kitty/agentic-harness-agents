---
name: agentic-improvement
description: "Plan and apply targeted improvements to an existing repository's agentic structure from readiness findings or a model-profile comparison. Use when the user asks to improve context routing, skill design, completion semantics, autonomy, portability, or instruction health. Do not use to produce the initial readiness score or to perform ordinary code-quality refactoring."
---
# Agentic Improvement

## Objective

Convert validated agent-readiness findings into a minimal, previewable improvement plan and safe repository changes.

## Inputs

Required: target repository. Preferred: canonical `ah-agentic`/`ah agentic` audit output. Optional: target model/profile, desired score threshold, scope constraints, and apply authorization.

## Context

Read only findings and files implicated by those findings, plus relevant canonical readiness/model-profile guidance. Keep project truth model-independent and use `references/context-engineering.md`.

## Procedure

1. Establish a baseline from machine-readable readiness findings; if unavailable, label qualitative fallback clearly.
2. Rank findings by severity, expected impact, confidence, and dependency order.
3. Group proposed changes as remove (stale/duplicated), change (routing/trigger/completion/autonomy), or add (missing contract/evidence/validation).
4. For model-specific improvements, trace every recommendation to the canonical model registry and keep changes in thin adapters/profiles where appropriate.
5. Preview affected files and expected score/compatibility movement before writing.
6. Apply only authorized deterministic changes; leave uncertain changes as recommendations.
7. Re-run readiness audit and compare before/after results.

## Output

Return baseline, prioritized change plan, applied changes, before/after scores, evidence/confidence, model-specific deltas, and remaining findings.

## Completion

No canonical project truth was made model-specific, high-impact writes respected approval boundaries, the audit was rerun, and any claimed improvement is supported by measured or explicitly heuristic evidence.
