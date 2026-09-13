---
name: design-system-compliance
description: "Audit product implementation against an accepted design system for token bypasses, duplicate primitives, raw controls, invalid variants, missing required component behavior, and documented exceptions. Use when structural conformance to established project design rules is the goal. Do not use to create or revise the design system, infer brand identity, or conduct a full accessibility audit."
---
# Design System Compliance

## Objective

Review implementation against the project's accepted design rules and component contracts. Distinguish a rule violation from ordinary drift, an approved exception and an untested behavior.

## Inputs

Required: target scope and an identifiable accepted design-system authority. Optional: project-approved Design Genome, token/component contracts, analysis/diff artifacts, design mode, exceptions and visual/runtime evidence. Stop scoring when the accepted authority is missing or contradictory.

## Context

Resolve design truth through the target's router and manifest, including custom paths. Read only affected rules, token/component definitions and applicable decisions. `.agentic/DESIGN.md` is a target default. A Design Genome is authority only when the target designates its exact version as approved; candidate/import/reference material is not.

The [review guide](references/review-guide.md) and [report template](references/report-template.md) are bundled locally. The [shared design boundaries](references/design-intelligence.md) are an exact bundled copy of the collection reference. No sibling skill or collection checkout is required at runtime.

## Procedure

1. Record source identity, reviewed screens/components, accepted authority/version, design mode and exclusions. Resolve authority conflicts explicitly; neither recency, token frequency nor an imported design is automatic approval.
2. Build a compact rule-to-evidence map for affected tokens, primitive/component reuse, variants, states and documented exceptions. Do not require a universal token scheme, component library or folder layout.
3. Inspect installed tool versions/help before using deterministic analysis. A compatible trusted CLI may provide static design analysis, component inventory or a diff; it must not rewrite context or approve identity during review. When tooling is unavailable, inspect the mapped source directly and report the reduced coverage.
4. Trace each hard-coded value, raw control, duplicate primitive or invalid variant to a concrete accepted rule. Inspect generated/vendor code, fixtures, legitimate platform adapters and exception scope before filing a violation. Similar appearance alone does not prove duplicate ownership.
5. Classify each result as `observed`, `violation`, `risk`, `exception` or `not_checked`. A new value or frequency change is drift unless an accepted rule forbids it. Static markup cannot by itself establish runtime focus, keyboard interaction, responsive behavior or visual equivalence.
6. Consume previous analysis only with matching inputs/scope and appropriate freshness. Changed source or authority invalidates an earlier conformance conclusion. Record commands/screens actually tested; do not relabel missing visual evidence as a pass.
7. Propose a scoped repair using approved components/tokens. Route creation or revision to design-system work, identity questions to identity design, and accessibility verification to its specialist when available. Explore/revise scope permits proposals, not publication or automatic approval.

## Output

Return accepted authority/scope, a rule-evidence table, confirmed violations, non-violating drift, applicable exceptions, untested behavior and prioritized remediation. Provide a compliance score only when an accepted rubric and adequate measured coverage support it; otherwise leave it unknown.

## Completion

Every violation cites an accepted rule and inspected implementation. Authority conflicts, exceptions and stale artifacts are visible. The report never claims a browser, visual regression, accessibility test or native host ran when it did not. Copying components or finding token files is not verification.
