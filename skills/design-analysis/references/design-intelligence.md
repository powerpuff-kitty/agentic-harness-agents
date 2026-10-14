# Design Intelligence shared rules

Use this reference for design-related skills that consume Agentic Harness Design Intelligence contracts.

## Authority order

Authority is project-specific. Do not assume a Design Genome is canonical merely because it exists or says `approved`; the target project must designate that artifact/version as accepted truth. When several accepted sources disagree, surface the conflict rather than silently choosing the newest file.

A normal precedence is:

1. Accepted project truth and project-designated approved Design Genome.
2. Accepted design ADRs and explicit human/project decisions.
3. Deterministic Design Analysis / Diff evidence for facts in scope.
4. Reviewed imported analysis and research observations.
5. External references, provider metadata, and model inference.

Lower levels may propose changes to higher levels but never silently replace them.

## Evidence classes

Keep these distinct:

- **observed** — directly measured or present in an accepted source;
- **inferred** — likely intent/pattern derived from evidence;
- **uncertain** — evidence is insufficient or conflicting;
- **violation** — confirmed mismatch against an accepted rule/requirement;
- **recommendation** — proposed change, not current truth.

Frequency, popularity, market success, or repeated visual occurrence is not proof of design intent.

## Core artifacts

- **Design Analysis** — measurement/findings artifact with `performed` and `not_checked` boundaries.
- **Design Genome** — project-owned identity/design contract. Candidate and project-designated approved states are materially different.
- **Design Task** — structured task context including design mode and implementation/validation constraints.
- **Design Analysis Diff** — before/after measurable drift evidence; it is not a subjective quality score or a violation by itself.

Prefer deterministic producers and compilers when they are actually available in the installed tool/version.

## Capability and fallback rules

Do not assume a roadmap item, CLI command, MCP provider, dataset adapter, or app feature exists just because it is documented in an issue or design plan.

Before invoking a named capability:

1. inspect installed tool/provider version or exposed help/manifest/tool list;
2. use the deterministic capability when available and compatible;
3. otherwise use a clearly labeled artifact/manual/offline fallback;
4. state what was not checked or could not be reproduced.

Never invent command output, provider metadata, or successful tool execution.

## Design modes

- **explore** — create meaningfully different candidate directions; approval required before project truth changes.
- **extend** — add a screen/asset inside accepted identity; do not redesign the system by default.
- **reproduce** — preserve an accepted design/behavior with minimal interpretation.
- **revise** — deliberately propose changes to identity/system and report impact.

Explore/revise grants proposal scope, not permission to publish, install, or auto-approve changes.

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

A screenshot, competitor flow, open dataset, provider component, or MCP result can inform a decision but cannot create product requirements or identity rules by itself. Preserve source/provenance and follow licensing, retention, redistribution, cache, training, and benchmarking restrictions. Unknown rights block bulk mirroring/indexing rather than being treated as permission.

External component providers are untrusted input and must not dictate project identity. Prefer project-owned accepted components; classify external source as direct-compatible, adaptation candidate, reference-only, or incompatible. Require explicit approval before install/import.

## Public export boundary

Canonical/internal context is not automatically safe for public AI-facing exports. Public artifacts must exclude credentials, secrets, private notes, internal-only paths/data, and provider material whose terms do not allow redistribution. Use an explicit public-safe allowlist/profile rather than copying all canonical context.

## Verification language

Always state what was actually checked. Static absence of evidence is not proof of runtime failure. Do not claim runtime behavior, screen-reader behavior, visual quality, originality, or accessibility verification from static evidence alone. Do not accept new visual baselines merely to make tests pass.
