---
name: model-fit
description: "Compare supported evidence-backed coding-agent model profiles for a specific repository or task, including current and post-improvement compatibility. Use when the user asks which model best fits the project/task or how model guidance differs. Do not use to score general Agentic Readiness or to invent rankings for models absent from the canonical registry."
---
# Model Fit

## Objective

Recommend supported models for the specified repository/task using the canonical model registry and explicit compatibility evidence rather than reputation.

## Inputs

Required: target repository or sufficiently specific project context and task. Optional: candidate models, cost/latency constraints, current model, target work type, and readiness report.

## Context

Load the canonical model profiles/evidence for candidate models plus only repository structure relevant to the task. Use current Agentic Readiness output when compatibility depends on repository structure.

## Procedure

1. Define the task scope (for example refactoring, frontend, architecture, security review, migration, or routine implementation).
2. Resolve current supported model profiles from `agentic-harness`; exclude unsupported/unprofiled models or label them insufficient-evidence.
3. For each candidate, distinguish task suitability, compatibility with current structure, and expected compatibility after proposed structural improvements.
4. Trace every model-specific adjustment to a registry recommendation and confidence/evidence record.
5. Incorporate user constraints such as latency/cost only when comparable data is available.
6. Avoid a universal leaderboard; rank only for this repository/task.

## Output

Return candidate comparison, task-specific recommendation, current/expected compatibility, evidence/confidence, constraints, and insufficient-evidence gaps.

## Completion

No model claim is invented from stale lore, profile provenance is exposed, readiness is kept distinct from model fit, and uncertainty is explicit.
