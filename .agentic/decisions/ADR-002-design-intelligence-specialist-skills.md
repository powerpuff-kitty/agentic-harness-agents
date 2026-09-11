# ADR-002: Split Design Intelligence into specialist skills

- Status: accepted
- Date: 2026-09-09

## Context

Agentic Harness now has canonical Design Analysis, Design Genome, Design Task, and Design Analysis Diff contracts plus deterministic Analyze/Preserve/Compile/Verify mechanics. The previous agent skill set had strong `design-system`, `product-design`, compliance, and accessibility procedures but no explicit owners for lifecycle orchestration, evidence interpretation, identity/art direction, UI/UX reference research, or external component-provider resolution.

Putting all of those responsibilities into `design-system` would make triggers ambiguous and would conflate project truth, research evidence, creative direction, implementation sources, and verification.

## Decision

Adopt a specialist Design Intelligence hierarchy:

- `design-intelligence` — lifecycle orchestration;
- `design-analysis` — evidence interpretation/import reconciliation;
- `design-research` — visual/UI/flow research;
- `identity-design` — art direction and Design Genome identity intent;
- `product-design` — user journeys and product UX;
- `design-system` — reusable tokens/components/layout patterns;
- `component-resolution` — project/internal/external implementation primitives;
- `design-system-compliance` and `accessibility-audit` — verification specialists.

All design skills share `references/design-intelligence.md`. Approved Design Genome/project truth outranks references, provider defaults, and model inference.

## Consequences

Routing becomes more explicit and skills remain compact. The deterministic CLI/app can evolve independently while the agent layer consumes the same contracts. New design providers or research libraries should extend the relevant specialist rather than creating new sources of project truth.
