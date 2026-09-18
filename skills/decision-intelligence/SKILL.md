---
name: decision-intelligence
description: "Use when a workflow needs bounded semantic classification, scoring, probability judgment, or task/tool/skill routing that deterministic code cannot reliably express. Do not use for open-ended generation, ordinary reasoning, deterministic parsing, authorization, or direct destructive, production, or release decisions."
---
# Decision Intelligence

## Objective

Use small typed semantic decisions only where deterministic project logic is insufficient, while keeping policy, authorization, thresholds, fallbacks, and side effects in ordinary reviewed code.

## Inputs

Required: the target repository, the state to evaluate, the bounded decision to make, and the accepted project policy governing that decision. Depending on the primitive, also require a finite choice set, boolean criteria, or an ordered score rubric. Optional inputs include an approved provider, model/version pin, labeled calibration cases, cost/latency budget, and a stronger-model or human fallback.

## Context

Read the smallest relevant project context: root `AGENTS.md`, `.agentic/manifest.yaml`, and any project-owned decision policy/configuration. When the installed canonical Harness exposes the Semantic Decision Intelligence v1 contract, use that versioned contract rather than inventing a provider-specific project format.

For TypeSafe Jev API fields and current provider behavior, use TypeSafe's official `typesafe-ai` Agent Skill or current TypeSafe documentation. Do not copy vendor API documentation into project truth. The project configuration owns the question intent, criteria, thresholds, fallback behavior, and allowed decision classes.

## Procedure

1. **Test the deterministic path first.** If parsing, schema validation, static analysis, a policy rule, a lookup, or a normal program condition can answer the question reliably, use that instead of a semantic model.
2. **Make the question atomic and typed.** Use a boolean-probability judgment for a bounded yes/no uncertainty, a finite choice for unordered alternatives, or an ordered score rubric for a continuum. Split unrelated judgments rather than hiding them inside one vague prompt.
3. **Bound the taxonomy.** Define explicit criteria for every choice or score level. Add an `other`, `unknown`, or fallback route when the taxonomy is not exhaustive rather than forcing an incorrect category.
4. **Centralize reviewable definitions.** Keep questions, criteria, thresholds, provider/model selection, cost/latency limits, and fallback rules in a small project-owned configuration. Do not scatter decision prompts across application code.
5. **Batch compatible questions.** When several independent judgments inspect the same state and the provider supports batching, evaluate them together while keeping each answer independently typed.
6. **Keep interpretation in code.** Treat returned probabilities, choices, scores, and confidence as advisory evidence. Apply thresholds, escalation, retry behavior, and workflow branching in ordinary code that can be tested without the provider.
7. **Fail explicitly.** Missing credentials, provider unavailability, timeout, invalid output, low confidence, or an uncovered category must select the project's declared fallback. Never silently convert provider failure into approval or success.
8. **Preserve consequential boundaries.** A semantic decision may suggest review or routing, but it must not directly authorize destructive actions, releases, production changes, secret access, security exceptions, payments, or other approval-required operations.
9. **Record reproducibility evidence.** Retain the provider, requested/resolved model when available, question-set revision or digest, state/input digest, timestamp, usage/latency, result status, and what was not verified. Never persist API keys or raw secrets.
10. **Evaluate before broad routing.** Use representative labeled cases and record false positives/negatives, ambiguous cases, model/version, sample size, and fallback behavior. Static fixtures prove contract shape, not model quality.
11. **Keep the provider skill current.** For TypeSafe with skills.sh, project-local installation is `npx skills add typesafe-ai/skills --skill typesafe-ai`; add `-g` for a device/global install. Update skills.sh-managed skills with `npx skills update`. For Claude Code, use TypeSafe's documented marketplace/plugin install and update flow. Prefer project-local installation when a team needs repository-specific reproducibility; use global installation as a personal default, not as project provenance.
12. **Do not assume installation proves loading.** Record skill source/version separately from evidence that the active host discovered and followed it.

## Output

Return the selected decision primitive, centralized question/criteria configuration or proposed change, provider/model requirement, fallback and escalation policy, evidence fields to retain, and any project/global skill lifecycle command actually required. Clearly separate deterministic checks, provider-returned semantic evidence, and unverified interpretation.

## Completion

The decision is bounded and justified as non-deterministic; questions and thresholds are reviewable; secrets are not persisted; provider failure cannot grant approval; consequential actions still require their existing authorization path; reproducibility metadata is defined; relevant routing/calibration cases exist; and any installed external provider skill has an explicit project or global scope and update path.
