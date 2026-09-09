---
name: accessibility-audit
description: "Audit user-facing journeys for accessibility defects and WCAG-aligned risks using repository evidence plus manual and automated checks. Use when accessibility, keyboard, screen-reader, focus, contrast, forms, motion or reflow is requested. Do not use for general UX design, identity generation, evidence-only inventory or design-system conformance alone."
---
# Accessibility Audit

## Objective

Assess the requested journeys against the project's declared accessibility target and return evidence-backed, prioritized remediation.

## Inputs

Required: target repository or changed UI scope. Optional: standard/level, browsers/devices, critical journeys, automated reports, assistive-technology requirements and Analysis/Genome/Task artifacts.

## Context

Read .agentic/DESIGN.md, relevant testing docs/UI code and accessibility-related ADRs/policies only. Load available Analysis check boundaries and project-designated approved component requirements; no blanket context preload.

## Procedure

1. Identify critical journeys, the declared target and the actual browser/device/theme/state scope.
2. Inspect semantics, headings/landmarks, accessible names, forms/errors, keyboard navigation, focus order/visibility, live regions, motion, zoom/reflow and color/contrast.
3. Run available deterministic tooling and focused UI tests, recording tool/version, environment and scope. Static declarations or a color palette alone do not establish rendered contrast over every background/state.
4. Perform manual examination for issues automation cannot establish. Separate actual keyboard/assistive-technology tests from source-based reasoning.
5. Preserve checks.not_checked unless new evidence really covers a check. Distinguish confirmed defects, plausible risks and unknowns; an unavailable scanner is not a pass.
6. Reconcile provider/component capability claims against actual evidence. Neither a provider claim nor an approved Genome certifies accessibility.
7. Prioritize by user impact and propose the smallest durable fix. Hand conformance/identity decisions to their specialists and require approval for canonical changes.

## Output

Return severity, affected journey/component/state, evidence, expected behavior, remediation, whether the conclusion is deterministic or heuristic, and checks performed/skipped. Use canonical Analysis enums when emitting an artifact; do not invent schema fields.

## Completion

Critical scope is covered or explicit gaps remain. Automated results were interpreted, manual limits recorded, and no screen-reader, accessibility-compliance or runtime claim exceeds the actual tests performed.
