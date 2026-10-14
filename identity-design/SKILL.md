---
name: identity-design
description: "Define or deliberately evolve a product's brand-facing visual identity and art direction: personality, differentiation, typography character, palette direction, imagery, geometry, density, composition, motion, voice, and intentional anti-patterns. Use when the user asks what the product should look or feel like, wants distinct visual directions, or needs identity continuity across surfaces. Do not use to engineer the reusable component/token system, design a product flow, or audit implementation compliance."
---
# Identity Design

## Objective

Create and preserve a distinctive, product-specific visual identity whose rationale can be carried across agents, sessions, surfaces, and future implementation without imposing one generic Harness aesthetic.

## Inputs

Required: product purpose/audience or an existing approved identity. Optional: competitive/design research, references, current Design Genome, brand constraints, supported media, accessibility target, approved/rejected examples, and desired design mode.

## Context

Read `.agentic/PRODUCT.md`, `.agentic/DESIGN.md`, `.agentic/REFERENCE.md`, accepted design ADRs, and task-relevant research. Follow `references/design-intelligence.md`. Treat references as evidence, not authority.

## Procedure

1. Resolve design mode: **explore**, **extend**, **reproduce**, or **revise**. Ordinary feature work should not become an unsolicited identity revision.
2. Establish purpose, audience, personality, differentiation, and the visual/emotional role the identity should play.
3. Define art-direction dimensions: typography character, color strategy, geometry, density, image/photography/illustration treatment, icon language, composition, and motion personality.
4. Produce meaningfully distinct directions when exploring. Do not return the same composition with cosmetic palette changes.
5. Explain why each important choice fits this product and what would make it feel generic or off-brand. Avoid universal anti-slop blacklists; scope anti-patterns to the identity and context.
6. Preserve approved and rejected examples with rationale so future agents understand intent, not only visible attributes.
7. Separate identity choices from reusable token/component engineering; route that implementation system to `design-system`.
8. Propose accepted identity decisions for the Design Genome, keeping proposal/candidate status explicit until human/project approval.

## Output

Return identity principles, personality/differentiation, visual direction, media/motion guidance, composition principles, scoped anti-patterns, approved/rejected evidence rationale, proposed Design Genome updates, and unresolved creative decisions.

## Completion

The result is product-specific rather than a reusable house style; important choices have reasons; references were adapted rather than copied; explore/extend/reproduce/revise authority is clear; and no candidate identity is presented as approved project truth without explicit acceptance.
