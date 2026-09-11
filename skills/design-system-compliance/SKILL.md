---
name: design-system-compliance
description: "Audit product implementation against an accepted design system for token bypasses, duplicate primitives, raw controls, invalid variants, missing required component behavior, and documented exceptions. Use when structural conformance to established project design rules is the goal. Do not use to create or revise the design system, infer brand identity, or conduct a full accessibility audit."
---
# Design System Compliance

## Objective

Determine whether product code conforms to the project's accepted design-system rules and component contracts without treating ordinary design drift or unreviewed analysis as an automatic violation.

## Inputs

Required: target repository/scope and accepted design-system source. Optional: project-designated approved Design Genome, Design Analysis/Diff artifacts, component inventory/contracts, token definitions, allowed exception paths, visual-regression evidence, and compliance threshold.

## Context

Read `.agentic/DESIGN.md`, accepted design ADRs, canonical token/component source, and `references/design-intelligence.md`. Use a Design Genome as authority only when the target project designates that artifact/version as accepted truth. If DESIGN.md, ADRs, and Genome conflict, report the conflict instead of choosing silently.

## Procedure

1. Identify the accepted design-system authority and exact scope; distinguish canonical rules from candidate/import/reference material.
2. Run deterministic compliance tooling when it is available and version-compatible; otherwise use focused source inspection and report the fallback.
3. Detect raw controls, hard-coded visual values, duplicate primitives, invalid variants, direct style bypasses, and confirmed missing behavior against approved component requirements.
4. Consume Design Analysis/Diff as evidence. A new color, spacing value, component, or changed frequency is **drift**, not a violation unless it conflicts with an accepted rule or contract.
5. Distinguish `observed`, `violation`, `risk`, and `not_checked`. Static absence of evidence must not become a claim that runtime behavior is broken.
6. Infer a missing shared abstraction only when repeated product usage justifies it; route creation/evolution of that system to `design-system` and external primitive resolution to `component-resolution`.
7. Honor documented exceptions and design-mode scope. Explore/revise work can intentionally diverge while still requiring explicit approval before new rules become canonical.
8. Route accessibility-specific findings to `accessibility-audit`; do not convert generic visual differences into accessibility claims.

## Output

Return authority/scope, evidence-backed violations, measurable drift that is not yet a violation, missing-evidence/not-checked areas, documented exceptions, remediation, and a compliance score/status only when deterministic tooling and an accepted rule set support it.

## Completion

Every violation maps to an accepted project rule or verified component requirement; drift alone is not scored as failure; evidence paths are exact; authority conflicts and exceptions are visible; and the audit does not claim visual, runtime, or accessibility verification that was not performed.
