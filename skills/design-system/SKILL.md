---
name: design-system
description: "Create or evolve a design system: evidence, tokens, semantic roles, components, states, layouts, patterns, accessibility, and usage guidance. Use when the user asks to define or substantially extend the shared UI system itself. Do not use merely to check whether product code complies with an existing system or to design one isolated product flow."
---
# Design System

## Objective

Define a coherent reusable UI system that translates accepted visual evidence into implementable, accessible foundations and components.

## Inputs

Required: product/UI scope and existing design evidence or desired system goals. Optional: screenshots/reference material, framework, current tokens/components, brand constraints, accessibility target, and supported themes/platforms.

## Context

Read `.agentic/DESIGN.md`, `.agentic/REFERENCE.md`, relevant design docs, current component/token code, and accepted design ADRs. Treat references as evidence and `DESIGN.md` as accepted rule.

## Procedure

1. Inventory existing visual rules, repeated patterns, and inconsistencies.
2. Derive primitive tokens, semantic roles, typography, spacing, elevation, motion, icon, and color behavior.
3. Define component APIs, anatomy, variants, states, responsive behavior, and accessibility expectations.
4. Establish layout/pattern guidance and composition boundaries.
5. Provide proof through examples/stories/fixtures and representative product flows.
6. Define adoption and migration rules that prevent one-off bypasses.
7. Validate visual, interaction, accessibility, and implementation consistency where tooling exists.

## Output

Return system architecture, token/component inventories, usage rules, proof requirements, migration/adoption plan, and unresolved design decisions.

## Completion

The system covers required states and accessibility, accepted evidence is traceable to rules, components are reusable rather than page-specific, and proof/validation exists for subjective and deterministic quality.
