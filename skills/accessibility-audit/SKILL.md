---
name: accessibility-audit
description: "Audit user-facing journeys for accessibility defects and WCAG-aligned risks using repository, Design Analysis, manual, and automated evidence. Use when accessibility, keyboard, screen-reader, focus, contrast, forms, motion, touch targets, zoom, or reflow is explicitly requested. Do not use for general UX design, visual-style judgment, or design-system conformance alone."
---
# Accessibility Audit

## Objective

Assess the requested journeys against the project's declared accessibility target while separating confirmed defects, evidence-backed risks, and behavior that remains untested.

## Inputs

Required: target repository or changed UI scope. Optional: target standard/level, project-designated approved Design Genome requirements, Design Analysis runtime/static evidence, browsers/devices, critical journeys, automated reports, and known assistive-technology requirements.

## Context

Read `.agentic/DESIGN.md`, accessibility/testing docs, accepted ADRs, task-relevant approved Design Genome rules, relevant UI code, and `references/design-intelligence.md`. Use Design Analysis measurements only for checks they actually performed; preserve `not_checked` exactly.

## Procedure

1. Identify critical journeys, the declared accessibility target, and accepted accessibility requirements.
2. Inspect semantics, landmarks/headings, accessible names, forms/errors, keyboard navigation, focus order/visibility, live regions, contrast, motion, touch targets, zoom/reflow, and responsive behavior relevant to scope.
3. Run available deterministic accessibility tooling and focused UI tests; record tool/version, environment, viewport, and scope. If unavailable, do not simulate a pass.
4. Interpret Design Analysis findings instead of copying them blindly. Static evidence can identify likely risks; runtime/browser evidence may confirm only the checks it actually executed.
5. Classify every result as **confirmed defect**, **risk/heuristic**, or **not checked**. Absence of a state in source analysis is not proof that runtime behavior is inaccessible.
6. Perform manual reasoning for behavior automation cannot prove, especially keyboard flow and assistive-technology semantics. Never claim screen-reader testing unless a screen reader was actually used.
7. Treat before/after design drift as context only. Drift becomes an accessibility defect only when it demonstrably violates an accepted accessibility requirement or measured threshold.
8. Prioritize by user impact, reach, and blocking severity; route general product UX or design-system questions to their specialist skills.

## Output

Return findings with severity, affected journey/component, classification (`confirmed`, `risk`, or `not_checked`), evidence, expected behavior, remediation, tools/environment used, and exact checks performed/skipped.

## Completion

Critical journeys in scope are covered to the extent tools/evidence allow; automated results are interpreted rather than treated as universal truth; manual and assistive-technology gaps are explicit; design drift is not mislabeled as accessibility failure; and changed accepted accessibility truth is reflected in canonical project documentation when approved.
