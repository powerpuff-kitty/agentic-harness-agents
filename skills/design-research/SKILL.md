---
name: design-research
description: "Research visual references, UI patterns, interaction patterns, product flows, design critiques, and interface datasets to inform a specific design/product question. Use when the user asks how other interfaces solve a problem, wants examples from UI/UX libraries, or needs evidence before choosing a design direction. Do not use for general competitor/business research, direct component installation, or to turn reference prevalence into project requirements."
---
# Design Research

## Objective

Build a traceable reference set and extract useful design/product principles without copying source identity or mistaking market prevalence for project truth.

## Inputs

Required: research question, target surface/flow/pattern, and relevant product context. Optional: user references, open datasets, current-interface libraries, provider access, platform/category constraints, recency needs, and current Design Genome.

## Context

Read `.agentic/PRODUCT.md`, `.agentic/DESIGN.md`, `.agentic/REFERENCE.md`, accepted research/ADR context, and `references/design-intelligence.md`. Respect provider licensing, retention, redistribution, and benchmarking restrictions.

## Procedure

1. Classify the target as a visual reference, UI pattern, interaction pattern, product flow, implementation reference, or critique/evaluation question.
2. Prefer relevant open/local sources when they answer the question; use current/commercial providers only as permitted and necessary.
3. Build a small, explainable reference set. Preserve source, platform, date/recency, category, and material usage restrictions.
4. For each reference, state **why it is relevant**, which principle is worth studying, and what must not be copied (brand, exact composition, source assets, or unsupported behavior).
5. Compare patterns across references: common steps, differences, state handling, hierarchy, density, permissions, navigation, and interaction choices.
6. Keep market traction, popularity, and frequency as context signals only; they are not evidence of design quality or product necessity.
7. Mark observations separately from recommendations. Feature presence in another product never creates a requirement automatically.
8. Route accepted product-flow implications to `product-design`, identity implications to `identity-design`, reusable UI-system implications to `design-system`, and code-source/provider selection to `component-resolution`.

## Output

Return the reference set with provenance, relevance rationale, observed patterns/differences, project-fit analysis, explicit non-requirements, licensing/retention notes, and recommendations or questions requiring approval.

## Completion

References are traceable and appropriately scoped; `REFERENCE != REQUIREMENT` is preserved; no restricted dataset is mirrored or retained beyond allowed use; no design is recommended solely because it is popular; and downstream decisions remain proposals until accepted by the project.
