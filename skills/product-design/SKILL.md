---
name: product-design
description: "Design a feature's user journey, information hierarchy, interaction states, requirements, edge cases, recovery, and usability behavior from accepted product goals. Use when the requested output is UX/product interaction design for a screen, workflow, or end-to-end journey. Do not use to define brand/art direction, construct the shared token/component system, research reference libraries as the primary task, or turn competitor features into requirements."
---
# Product Design

## Objective

Translate accepted product goals into understandable user journeys and interaction requirements that respect the approved Design Genome and can be implemented by the design system and engineering stack.

## Inputs

Required: target user/problem and feature scope. Optional: approved Design Genome, Design Task, design research, current UI, analytics, constraints, platforms, success criteria, component inventory, and accessibility target.

## Context

Read `.agentic/PRODUCT.md`, the approved Design Genome/design rules relevant to the task, accepted ADRs, current flows/components, and `references/design-intelligence.md`. Research is evidence, not a substitute for product decisions. Route primary reference research to `design-research` and identity questions to `identity-design`.

## Procedure

1. Define users/jobs, entry conditions, desired outcome, failure conditions, and scope boundaries from accepted product truth.
2. Map the primary journey before secondary and edge flows; preserve the Design Task mode so routine `extend` work does not become an identity/system redesign.
3. Specify information hierarchy, actions, navigation, state transitions, empty/loading/error/success/selected states, interrupted flows, and recovery.
4. Address permissions, destructive actions, validation, accessibility, responsive/platform differences, persistence, and latency/offline behavior where relevant.
5. Use research to compare approaches and expose tradeoffs, but keep observed market patterns separate from project requirements. A paywall, onboarding step, dashboard, or other competitor feature is not required merely because references contain it.
6. Reuse approved project components/patterns when they fit. Route genuine reusable-system gaps to `design-system` and implementation-provider gaps to `component-resolution`.
7. Define measurable acceptance/usability criteria, required states/viewports, and unresolved product decisions suitable for a structured Design Task.
8. Avoid feature slop: every significant screen/action must trace back to an accepted user problem, product capability, or explicit decision.

## Output

Return flow/state model, screen/interaction requirements, edge cases, component/system dependencies, research-derived observations vs project decisions, accessibility considerations, Design Task inputs, acceptance criteria, and open decisions.

## Completion

The primary journey and recovery states are covered; approved identity/system constraints are respected; research did not silently create product requirements; component/system gaps are routed to the correct specialist; and unresolved business/product choices are explicit rather than invented.
