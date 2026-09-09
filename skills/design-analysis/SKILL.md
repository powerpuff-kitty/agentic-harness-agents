---
name: design-analysis
description: "Interpret measured design evidence and structured analysis artifacts, classify conclusions by confidence and evidence type, and reconcile external analysis proposals with approved project truth. Use when the user asks what an existing interface's measured colors, type, spacing, components, motion, responsive behavior, or design drift mean. Do not use to invent a new visual identity, design a user journey, or perform the deterministic measurement itself when tooling can do it."
---
# Design Analysis

## Objective

Turn deterministic design evidence into careful, reviewable interpretation without converting measurements or model guesses into canonical identity by default.

## Inputs

Required: Design Analysis artifact, measured report, or clearly scoped existing interface evidence. Optional: current Design Genome, screenshots, runtime findings, external-AI analysis output, repository source, and review criteria.

## Context

Read task-relevant `.agentic/DESIGN.md`, `.agentic/REFERENCE.md`, accepted Design Genome/ADR context, and `references/design-intelligence.md`. When an analysis artifact exists, treat it as the measurement source of record for facts it already contains.

## Procedure

1. Validate the analysis scope and preserve its `performed` / `not_checked` boundary.
2. Separate each conclusion into **observed**, **inferred**, **uncertain**, **violation**, or **recommendation**. Do not collapse those classes.
3. Reference measurement/evidence IDs for conclusions whenever the artifact provides them.
4. Interpret color, typography, spacing, geometry, token, component, motion, responsive, asset, and accessibility evidence only to the depth supported by the inputs.
5. Detect consistency, outliers, likely drift, semantic collisions, and missing system definitions; state whether each is deterministic or heuristic.
6. When richer interpretation is useful, generate or consume the external-analysis prompt/schema rather than asking an external model for unstructured prose.
7. Compare imported AI analysis against the approved Design Genome. Conflicts become proposals for review, never automatic updates.
8. Route art-direction/identity questions to `identity-design`, product-flow questions to `product-design`, system construction to `design-system`, and implementation-source selection to `component-resolution`.

## Output

Return evidence-backed findings with classification, confidence, evidence references, impact, proposed next action, conflicts with approved truth, and explicit unknown/not-checked areas. When requested, produce a structured enrichment artifact compatible with the project's analysis workflow.

## Completion

No deterministic fact was needlessly recomputed, every heuristic conclusion is labeled, `not_checked` remains visible, imported model output did not silently overwrite project truth, and the response does not claim accessibility, runtime behavior, or visual quality that the available evidence cannot prove.
