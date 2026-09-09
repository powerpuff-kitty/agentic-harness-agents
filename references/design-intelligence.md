# Design Intelligence shared rules

Use this reference for design-related skills that consume Agentic Harness Design Intelligence contracts.

## Authority order

1. Accepted project truth and approved Design Genome.
2. Accepted design ADRs and explicit human/project decisions.
3. Deterministic Design Analysis / Diff evidence for facts in scope.
4. Reviewed imported analysis and research observations.
5. External references, provider metadata, and model inference.

Lower levels may propose changes to higher levels but never silently replace them.

## Evidence classes

Keep these distinct:

- **observed** — directly measured or present in an approved source;
- **inferred** — likely intent/pattern derived from evidence;
- **uncertain** — evidence is insufficient or conflicting;
- **violation** — confirmed mismatch against an approved rule/requirement;
- **recommendation** — proposed change, not current truth.

Frequency, popularity, market success, or repeated visual occurrence is not proof of design intent.

## Core artifacts

- **Design Analysis** — measurement/findings artifact with `performed` and `not_checked` boundaries.
- **Design Genome** — project-owned identity/design contract. Candidate and approved states are materially different.
- **Design Task** — structured task context including design mode and implementation/validation constraints.
- **Design Analysis Diff** — before/after measurable drift evidence; it is not a subjective quality score.

Prefer deterministic CLI/app producers and compilers for these artifacts when available.

## Design modes

- **explore** — create meaningfully different directions; approval required before project truth changes.
- **extend** — add a screen/asset inside the approved identity; do not redesign the system by default.
- **reproduce** — preserve an approved design/behavior with minimal interpretation.
- **revise** — deliberately propose changes to the identity/system and report impact.

## Specialist boundaries

- `design-intelligence` orchestrates lifecycle stages.
- `design-analysis` interprets evidence.
- `identity-design` owns art direction and identity intent.
- `design-research` owns visual/UI/flow reference research.
- `product-design` owns user journeys and product interaction requirements.
- `design-system` owns reusable tokens/components/layout patterns.
- `component-resolution` selects implementation primitives/providers.
- `design-system-compliance` audits structural conformance.
- `accessibility-audit` owns accessibility-specific verification.

## Reference and provider safety

`REFERENCE != REQUIREMENT`.

A screenshot, competitor flow, open dataset, provider component, or MCP result can inform a decision but cannot create product requirements or identity rules by itself. Preserve source/provenance and follow licensing, retention, redistribution, cache, training, and benchmarking restrictions.

External component providers must not dictate project identity. Prefer project-owned approved components; classify external source as direct-compatible, adaptation candidate, reference-only, or incompatible. Require explicit approval before install/import.

## Verification language

Always state what was actually checked. Do not claim runtime behavior, screen-reader behavior, visual quality, originality, or accessibility verification from static evidence alone. Do not accept new visual baselines merely to make tests pass.
