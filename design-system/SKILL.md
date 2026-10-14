---
name: design-system
description: "Create or evolve the reusable UI system: tokens, semantic roles, component contracts, variants, states, layouts, patterns, accessibility expectations, and adoption rules. Use when the user asks to define or substantially extend shared interface primitives used across product surfaces. Do not use to discover the brand/art direction, research external UI references, select an external component provider, or merely audit conformance to an existing system."
---
# Design System

## Objective

Define a coherent reusable UI system that implements accepted identity/design intent through accessible tokens, components, states, layouts, and usage rules.

## Inputs

Required: product/UI scope and accepted design intent or desired reusable-system goals. Optional: project-designated approved Design Genome, Design Analysis evidence, current tokens/components, framework, accessibility target, supported themes/platforms, and accepted references.

## Context

Read `.agentic/DESIGN.md`, accepted design ADRs, relevant component/token source, `references/design-intelligence.md`, and a Design Genome only when the target project designates that artifact/version as accepted truth. If accepted sources conflict, surface the conflict and request/record resolution rather than silently choosing the Genome or the newest file. Route unresolved art direction to `identity-design`, research to `design-research`, and provider selection to `component-resolution`.

## Procedure

1. Inventory current tokens, components, patterns, states, and repeated bypasses using deterministic analysis where available.
2. Map accepted identity intent into primitive and semantic tokens: typography, color, spacing, geometry, elevation, density, motion, icons, and theme roles.
3. Define component APIs, anatomy, variants, states, responsive behavior, accessibility expectations, and source ownership.
4. Establish reusable layout/pattern guidance and composition boundaries without creating page-specific components unnecessarily.
5. Preserve design mode: `extend` work should not revise identity/system rules unless a genuine gap is identified and approved; `explore`/`revise` allows proposals, not automatic publication or approval.
6. Prefer existing approved project components. Route missing implementation primitives or external libraries through `component-resolution` rather than silently importing provider defaults.
7. Provide proof through representative examples/stories/fixtures and required states; separate deterministic checks from subjective visual review.
8. Define adoption, migration, deprecation, and exception rules that prevent one-off bypasses.
9. Propose Design Genome/system updates explicitly; do not silently promote inferred rules or external reference styles into accepted truth.

## Output

Return token/component inventories, component/state contracts, layout/pattern rules, source ownership, accessibility/proof requirements, migration/adoption plan, authority conflicts, proposed Design Genome changes, and unresolved system decisions.

## Completion

The reusable system implements accepted identity intent; required component states and accessibility expectations are covered; project primitives are preferred over external defaults; accepted evidence is traceable to rules; source-of-truth conflicts are visible; and any identity/system changes remain explicit, reviewable proposals rather than accidental drift.
