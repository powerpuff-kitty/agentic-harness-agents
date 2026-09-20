---
name: design-system-compliance
description: "Audit product implementation against an accepted design system for token bypasses, duplicate primitives, raw controls, invalid variants, missing required component behavior, and documented exceptions. Use when structural conformance to established project design rules is the goal. Do not use to create or revise the design system, infer brand identity, or conduct a full accessibility audit."
---
# Design System Compliance

## Objective

Review implementation against accepted design rules and component contracts, distinguishing violations, ordinary drift, approved exceptions and untested behaviour.

## Inputs

Required: scope and identifiable accepted authority. Optional: approved Design Genome, token/component contracts, analysis/diffs, mode, exceptions and visual/runtime evidence. Missing or conflicting authority prevents scoring.

## Context

Follow target router/manifest custom routes. Read affected rules, components, tokens and decisions. A Genome is authoritative only at the exact version the project approves; imported candidates are not accepted truth.

Consult the local [review guide](references/review-guide.md), [report template](references/report-template.md) and [design boundaries](references/design-intelligence.md) only as needed. The latter is an exact bundled collection copy. No sibling skill or collection checkout is required.

## Procedure

1. Record revision, dirty-worktree changes, screens/components, authority/version, mode and exclusions. Neither recency, token frequency nor imported design resolves an authority conflict automatically.
2. Map affected rules to evidence for token use, component ownership, variants, states and exceptions. Do not impose a universal library, token scheme or folder layout. Expand to callers/definitions when a finding depends on them, not to every screen by default.
3. Reuse analyses only with matching source, authority, configuration and scope. Refresh changed tokens/components, dependent views and affected checks; a narrow diff does not prove a narrow impact. Preserve exceptions, contrary evidence and required checks rather than trim them for budget.
4. Check installed capabilities before optional trusted static analysis, inventory or diff tools. They may not rewrite context or approve identity during review. Without a compatible tool, inspect mapped source and state coverage; never invent results or require `ah` installation.
5. Trace each hard-coded value, raw control, duplicate or invalid variant to an accepted rule. Check vendor/generated code, fixtures, legitimate platform adapters and exception scope. Similar appearance does not establish duplicate ownership.
6. Classify `observed`, `violation`, `risk`, `exception` or `not_checked`. Frequency/value changes are drift unless forbidden. Static markup cannot verify focus, keyboard, responsive behaviour or visual equivalence. Record actual commands/screens, input identities, exits and relevant failures; use real log references and preserve truncation, not repeated raw logs.
7. Propose scoped repair with approved components/tokens. Delegate system changes, identity and accessibility only to the relevant available specialist, with bounded evidence. Missing specialists remain gaps; no automatic extra agent/provider call. Explore/revise permits proposals, not publication or approval.

## Output

Authority/scope, rule-evidence table, violations, allowed drift, exceptions, untested behaviour and repair priorities. Scores require an accepted rubric and adequate measured coverage; otherwise unknown. Cite reused evidence rather than copy entire artifacts.

## Completion

Every violation cites an accepted rule and inspected implementation. Conflicts, exceptions, stale artifacts and missing checks remain visible. Never claim browser, visual, accessibility or host execution that did not occur; copied components and token files are not verification.
