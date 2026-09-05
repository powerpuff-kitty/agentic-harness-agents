---
name: design-system-compliance
description: "Audit product implementation against an existing design system for token bypasses, duplicate primitives, raw controls, missing shared components, invalid variants, and documented exceptions. Use when conformance to an established system is the goal. Do not use to create the design system itself or to conduct a full accessibility audit."
---
# Design System Compliance

## Objective

Determine whether product code consistently consumes the accepted design system and identify concrete bypasses or missing abstractions.

## Inputs

Required: target repository/scope and existing design-system source. Optional: component inventory, token definitions, allowed exception paths, visual-regression output, and compliance threshold.

## Context

Read `.agentic/DESIGN.md`, installed design-system pack/guidance, component/token source, and only product files in the requested scope.

## Procedure

1. Confirm the design system is active and identify canonical tokens/components.
2. Run deterministic compliance tooling when available.
3. Detect raw controls, hard-coded visual values, duplicate primitives, invalid component variants, and direct style bypasses outside allowed system paths.
4. Infer missing shared components only when repeated product flows justify them.
5. Separate deliberate documented exceptions from accidental divergence.
6. Check representative UI states and visual/accessibility evidence where available.
7. Prioritize fixes by breadth of inconsistency and reuse impact.

## Output

Return compliance score/status when deterministic tooling supports it, violations with evidence, missing/shared-component recommendations, documented exceptions, and remediation.

## Completion

Findings distinguish structural conformance from aesthetics, evidence paths are exact, exceptions are honored, and the audit does not claim visual or accessibility validation that was not performed.
