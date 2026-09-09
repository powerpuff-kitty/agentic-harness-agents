---
name: design-intelligence
description: "Orchestrate the repository-native Analyze → Preserve → Compile → Verify design lifecycle across canonical Design Analysis, Design Genome, Design Task, and drift artifacts. Use when a request spans multiple design-intelligence stages or asks to make an existing product reproducible for AI implementation. Do not use for one isolated UX flow, a standalone design-system definition, or a narrow compliance/accessibility audit."
---
# Design Intelligence

## Objective

Coordinate the end-to-end design-intelligence lifecycle while keeping deterministic evidence, agent interpretation, human approval, and canonical project truth separate.

## Inputs

Required: target project or existing design artifacts and the requested lifecycle stage(s). Optional: Design Analysis, Design Genome, Design Task, before/after analysis, references, provider artifacts, product goals, and approval boundaries.

## Context

Read `.agentic/DESIGN.md`, `.agentic/REFERENCE.md`, accepted design ADRs, and only task-relevant Design Intelligence artifacts. Follow `references/design-intelligence.md`. Prefer canonical schemas and deterministic `ah design` operations when available.

## Procedure

1. Identify the current stage: **Analyze**, **Preserve**, **Compile**, or **Verify**; do not redo completed stages without cause.
2. For Analyze, prefer deterministic Design Analysis evidence and delegate interpretation to `design-analysis` rather than inventing measurements.
3. For Preserve, convert evidence into a candidate Design Genome and keep observed, inferred, unknown, and recommended content distinct. Candidate truth requires explicit review before approval.
4. Route identity/art-direction decisions to `identity-design`, reusable UI-system work to `design-system`, user journeys to `product-design`, research to `design-research`, and external implementation primitives to `component-resolution`.
5. For Compile, prefer the deterministic Design Genome + Design Task compiler. Do not ask an LLM to rewrite canonical context merely to produce a prompt.
6. For implementation handoff, preserve design mode (`explore`, `extend`, `reproduce`, or `revise`), required states, anti-patterns, implementation constraints, and unresolved gaps.
7. For Verify, compare before/after evidence and route conformance/accessibility findings to the dedicated compliance and accessibility skills. Treat measurable drift as evidence, not a subjective quality score.
8. Record checks performed, checks not performed, approvals, assumptions, and unresolved decisions.

## Output

Return lifecycle stage/status, artifacts consumed or produced, delegated specialist work, approval requirements, deterministic command/contract usage, unresolved gaps, and exact verification boundaries.

## Completion

The requested lifecycle stages are reproducible; canonical truth was not silently replaced by references or model guesses; candidate identity was not auto-approved; deterministic outputs were preferred where available; and every unverified visual/runtime claim is explicitly marked as not checked.
