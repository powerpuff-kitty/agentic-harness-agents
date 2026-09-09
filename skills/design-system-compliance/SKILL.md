---
name: design-system-compliance
description: "Audit implementation against an existing design system for token bypasses, duplicate primitives, raw controls, invalid variants and scoped exceptions. Use when conformance to accepted design requirements is the goal. Do not use for design-system creation, evidence-only inventory, identity exploration or a full accessibility audit."
---
# Design System Compliance

## Objective

Determine whether product code consumes the accepted design system and identify evidence-backed violations rather than treating every difference as failure.

## Inputs

Required: target scope and accepted design-system source. Optional: approved Genome/Task, component inventory, tokens, exception paths, Design Analysis/Diff, visual-regression results and thresholds.

## Context

Read .agentic/DESIGN.md, project-designated approved Genome, installed guidance, token/component source and only the implementation scope needed. Resolve authority conflicts; an imported approved flag is not enough.

## Procedure

1. Identify canonical tokens/components, applicable rule scope and documented exceptions before evaluating conformance.
2. Check tool availability and run supported deterministic analysis/compliance tools. Read before/after reports where available; do not assume the entire new UI was checked.
3. Inspect raw controls, hard-coded values, duplicate primitives, invalid variants and direct bypasses outside allowed paths.
4. Distinguish confirmed rule violations, deliberate exceptions, unreviewed changes and missing evidence. Measured drift is not automatically a violation or a design-quality/originality score.
5. Infer missing abstractions only when repeated product flows justify a proposal; route system changes to design-system instead of silently redefining requirements.
6. Inspect representative states and actual visual/accessibility evidence. Required component behavior needs evidence; static absence is not proof of runtime failure. Full accessibility work belongs to accessibility-audit.
7. Prioritize fixes by reach and reuse. Preserve checks.not_checked and never replace visual baselines or change accepted constraints merely to pass a check.

## Output

Return scoped status, exact rule/evidence references, exceptions, drift observations, remediation proposals and performed/skipped checks. Report a score only when a real deterministic tool and its documented scope support it.

## Completion

Structural conformance, subjective aesthetics and accessibility are distinct. No unrun check is claimed; reference metadata has not become a mandatory project requirement.
