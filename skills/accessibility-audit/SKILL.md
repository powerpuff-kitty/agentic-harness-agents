---
name: accessibility-audit
description: "Audit user-facing journeys for accessibility defects and WCAG-aligned risks using repository evidence plus manual and automated checks. Use when accessibility, keyboard, screen-reader, focus, contrast, forms, motion, or reflow quality is explicitly requested. Do not use for general UX design or design-system conformance alone."
---
# Accessibility Audit

## Objective

Assess the requested user journeys against the project's declared accessibility target and return evidence-backed, prioritized remediation.

## Inputs

Required: target repository or changed UI scope. Optional: target standard/level, browsers/devices, critical journeys, existing automated reports, and known assistive-technology requirements.

## Context

Read `.agentic/DESIGN.md`, accessibility/testing docs, relevant UI code, and only the ADRs/policies that affect accessibility. Follow `references/context-engineering.md`; do not preload unrelated product or backend context.

## Procedure

1. Identify the critical journeys and the project's accessibility target.
2. Inspect semantics, headings/landmarks, accessible names, forms/errors, keyboard navigation, focus order/visibility, live regions, motion, zoom/reflow, and color/contrast.
3. Run available deterministic accessibility tooling and focused UI tests; record tool/version and scope.
4. Perform manual reasoning for issues automation cannot prove, especially keyboard and assistive-technology behavior.
5. Separate confirmed defects from likely risks and avoid claiming screen-reader validation unless it actually ran.
6. Prioritize by user impact, reach, and blocking severity; propose the smallest durable fix.

## Output

Return findings with severity, affected journey/component, evidence, expected behavior, remediation, confidence (`deterministic` or `heuristic`), and checks performed/skipped.

## Completion

Finish only after critical journeys were covered, automated results were interpreted rather than copied blindly, manual gaps are stated, and any changed accessibility truth is reflected in canonical project documentation.
