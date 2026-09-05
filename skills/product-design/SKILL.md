---
name: product-design
description: "Design a product feature's user flows, information hierarchy, interaction states, requirements, edge cases, and usability behavior from accepted product goals. Use when the requested output is UX/product interaction design for a feature or journey. Do not use to create the shared design system, audit accessibility alone, or write marketing positioning."
---
# Product Design

## Objective

Translate accepted product goals into understandable user journeys and interaction requirements that engineering and design-system work can implement.

## Inputs

Required: target user/problem and feature scope. Optional: research, current UI, constraints, platforms, success criteria, design system, analytics, and accessibility target.

## Context

Read `.agentic/PRODUCT.md`, task-relevant design/research, accepted ADRs, and existing flows/components. Use the design system as a constraint, not as a substitute for product decisions.

## Procedure

1. Define users, jobs, entry/exit conditions, and success/failure outcomes.
2. Map the primary journey before secondary/edge flows.
3. Specify information hierarchy, actions, navigation, state transitions, empty/loading/error/success states, and recovery.
4. Address permissions, destructive actions, validation, accessibility, responsive/platform differences, and interrupted flows.
5. Reuse existing components/patterns when they fit; identify genuine system gaps separately.
6. Define measurable acceptance/usability criteria and unresolved product decisions.
7. Produce wire-level structure or implementation-ready interaction requirements at the requested fidelity.

## Output

Return flow/state model, screen or interaction requirements, edge cases, component/system dependencies, accessibility considerations, acceptance criteria, and open decisions.

## Completion

The primary journey and failure/recovery states are covered, design-system constraints are respected, and unresolved business/product choices are not silently invented.
