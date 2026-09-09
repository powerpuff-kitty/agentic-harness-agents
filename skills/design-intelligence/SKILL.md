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

Route from the target AGENTS.md and .agentic/manifest.yaml to task-relevant DESIGN.md, REFERENCE.md, accepted ADRs and artifact locations. Follow bundled `references/design-intelligence.md` when present. Standalone installs retain the essential gates below and use [workflow guidance](references/workflow.md), without requiring the whole collection or network access. Prefer the project's pinned schemas; resolve conflicts between DESIGN.md/ADRs and a Genome before treating either as superseded.

## Procedure

1. Identify the current stage: **Analyze**, **Preserve**, **Compile**, or **Verify**; do not redo completed stages without cause. Record source revision and available tool/skill capabilities first; inspect version/help before invoking commands.
2. For Analyze, prefer deterministic Design Analysis evidence and delegate interpretation to `design-analysis` when installed. An unavailable analyzer or provider remains unavailable; a skill does not install it. Do not invent measurements or tool results.
3. For Preserve, convert evidence into a candidate Design Genome and keep observed, inferred, unknown, and recommended content distinct. Require explicit review of the exact candidate before approval; record actual reviewer provenance, never a fabricated human decision. A project-designated approved artifact is authority, not an arbitrary imported status flag.
4. Route identity/art direction to `identity-design`, reusable UI systems to `design-system`, journeys to `product-design`, research to `design-research`, and implementation primitives to `component-resolution`. Load only the relevant installed specialist; report missing skills rather than claiming delegation.
5. For Compile, prefer the supported deterministic Genome + Task compiler. Do not ask an LLM to rewrite the generated brief. Inspect coverage: omitted required visual values, sources, component behavior or rule exceptions are compiler gaps, not permission to ignore them. Keep approved context as a separate attachment and report blockers.
6. Preserve design mode (`explore`, `extend`, `reproduce`, or `revise`), states, anti-patterns, constraints and unresolved gaps. Explore/revise permits proposals, not automatic approval/publication. Substantive changes after approval require renewed review.
7. For Verify, compare before/after evidence under comparable conditions and route conformance/accessibility to dedicated skills. Measurable drift is evidence, not a subjective quality score. Do not auto-update baselines or drop unverified checks.
8. Record checks performed/not performed, approvals and assumptions. Keep original artifacts recoverable; review paths/snippets/private data before external AI handoff. No source upload or paid provider is required for the local workflow.

## Output

Return lifecycle stage/status, artifact paths/versions, delegated work, tool availability, approval requirements, deterministic command results, compiler coverage gaps and exact verification boundaries. A prose fallback is not a schema-validated artifact or a tested integration.

## Completion

The requested stages have evidence and explicit stopping points. Canonical truth was not replaced by references or guesses, candidate identity was not auto-approved, and unverified claims remain not checked. State actual execution separately from proposals, including missing tools and unresolved contract conflicts.
