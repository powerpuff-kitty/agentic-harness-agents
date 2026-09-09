---
name: component-resolution
description: "Resolve an implementation component need against approved project primitives, internal registries, and compatible external UI component providers, then produce a safe adaptation/import plan. Use when the user asks which component/library to use, wants to reuse Spectrum/shadcn-style source, or needs to avoid inventing a duplicate primitive. Do not use to define the visual identity, browse inspiration without implementation intent, or silently install incompatible provider code."
---
# Component Resolution

## Objective

Select the safest reusable implementation primitive for a concrete component need while preserving project identity, stack constraints, source provenance, and explicit approval boundaries.

## Inputs

Required: component need and target project stack. Optional: approved Design Genome/component inventory, internal registry, external provider artifacts/MCP access, dependency policy, license constraints, and required states/behaviors.

## Context

Read `.agentic/DESIGN.md`, approved component contracts, architecture/dependency constraints, and `references/design-intelligence.md`. Project-owned approved components take precedence over external providers.

## Procedure

1. Define the required capability, states, accessibility behavior, and API constraints without assuming a specific library.
2. Resolve in order: **approved project component → approved internal registry → compatible external provider → unresolved gap**.
3. For each candidate, inspect framework/runtime/language/styling/primitives/motion/dependency compatibility and license/source/version provenance.
4. Classify candidate use as **directly compatible**, **adaptation candidate**, **reference-only**, or **incompatible**. Example: React-only source is not a direct install for a Vue target, though its interaction behavior may be useful reference evidence.
5. Never fabricate an API from a screenshot or provider name. If exact source/metadata is unavailable, report the gap.
6. For an adaptation candidate, define token, typography, geometry, motion, accessibility, behavior/API, dependency, and project-convention changes before import.
7. Require explicit approval before install/import. Provider defaults must not silently become Design Genome rules or new global tokens.
8. After approval and adaptation, treat the project-owned copy as the preferred implementation authority; future upstream refresh is a separate reviewed change.

## Output

Return resolution order, candidate comparison, compatibility reasons, selected use mode, provenance/license, adaptation plan, approval required, unresolved capability gaps, and implementation-brief inputs.

## Completion

Existing project primitives were preferred, compatibility is explainable rather than guessed, incompatible source was not installed, external defaults did not redefine identity, license/provenance is retained, and any import/update action remains explicit and reviewable.
