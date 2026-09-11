---
name: agentic-structure-audit
description: "Evaluate Agentic Readiness: context architecture, AGENTS.md quality, skill routing, completion/autonomy, verification, portability, instruction health, decision history, and agent security. Use when the user asks how agent-ready a repository is or requests a model compatibility score. Do not use for broad code-quality auditing or for applying fixes."
---
# Agentic Structure Audit

## Objective

Produce a model-independent Universal Agentic Structure Score and, when requested, an evidence-backed model compatibility score.

## Inputs

Required: target repository. Optional: target model/profile, task type, baseline report, and requested output format.

## Context

Prefer machine-readable output from current `agentic-harness-cli` (`ah-agentic audit --json` or integrated equivalent). Inspect only files tied to findings. Resolve scoring rules and model profiles from canonical `agentic-harness`.

## Procedure

1. Run the canonical readiness audit when available; do not reimplement its score from prompt intuition.
2. Verify evidence for the highest-impact findings and classify confidence as deterministic, heuristic, or profile-backed.
3. Keep ordinary code quality separate from Agentic Readiness.
4. Evaluate context routing, `AGENTS.md`, skill overlap, completion semantics, decision boundaries, verification/tooling, architecture discoverability, decision history, portability, instruction health, and agent security.
5. If a target model is supplied, apply only profile-backed compatibility adjustments and cite the profile recommendation/evidence.
6. Rank remediation by severity and likely readiness impact without modifying the repository.

## Output

Return Universal Agentic Structure Score, dimension scores, optional model compatibility score, ordered findings with exact repository evidence, confidence, and concrete remediation.

## Completion

The audit remains read-only, scoring provenance is clear, model-specific claims come from the registry, and any unavailable deterministic check is labeled rather than guessed.
