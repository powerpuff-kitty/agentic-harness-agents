---
name: design-system
description: "Create or evolve the reusable UI system: tokens, semantic roles, component contracts, variants, states, layouts, patterns, accessibility expectations, and adoption rules. Use when the user asks to define or substantially extend shared interface primitives used across product surfaces. Do not use to discover the brand/art direction, research external UI references, select an external component provider, or merely audit conformance to an existing system."
---
# Design System

## Objective

Define a coherent reusable UI system that implements approved identity/design intent through accessible tokens, components, states, layouts, and usage rules.

## Inputs

Required: product/UI scope and approved design intent or desired reusable-system goals. Optional: approved Design Genome, Design Analysis evidence, current tokens/components, framework, accessibility target, supported themes/platforms, and accepted references.

## Context

Read `.agentic/DESIGN.md`, the approved Design Genome when present, relevant component/token source, accepted design ADRs, and `references/design-intelligence.md`. Treat the approved Genome as identity/design authority. Route unresolved art direction to `identity-design`, research to `design-research`, and provider selection to `component-resolution`.

## Procedure

1. Inventory current tokens, components, patterns, states, and repeated bypasses using deterministic analysis where available.
2. Map approved identity intent into primitive and semantic tokens: typography, color, spacing, geometry, elevation, density, motion, icons, and theme roles.
3. Define component APIs, anatomy, variants, states, responsive behavior, accessibility expectations, and source ownership.
4. Establish reusable layout/pattern guidance and composition boundaries without creating page-specific components unnecessarily.
5. Preserve design mode: `extend` work should not revise identity/system rules unless a genuine gap is identified and approved.
6. Prefer existing approved project components. Route missing implementation primitives or external libraries through `component-resolution` rather than silently importing provider defaults.
7. Provide proof through representative examples/stories/fixtures and required states; separate deterministic checks from subjective visual review.
8. Define adoption, migration, deprecation, and exception rules that prevent one-off bypasses.
9. Propose Design Genome/system updates explicitly; do not silently promote inferred rules or external reference styles into approved truth.

## Output

Return token/component inventories, component/state contracts, layout/pattern rules, source ownership, accessibility/proof requirements, migration/adoption plan, proposed Design Genome changes, and unresolved system decisions.

## Completion

The reusable system implements approved identity intent; required component states and accessibility expectations are covered; project primitives are preferred over external defaults; accepted evidence is traceable to rules; and any identity/system changes remain explicit, reviewable proposals rather than accidental drift.
