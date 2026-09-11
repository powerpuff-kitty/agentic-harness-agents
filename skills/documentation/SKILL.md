---
name: documentation
description: "Create or update durable project documentation so current product, architecture, security, design, operational, API, data, or testing truth matches accepted changes. Use when documentation is itself the requested deliverable or must be synchronized after approved work. Do not use to invent decisions, create ADRs, or produce a temporary implementation plan."
---
# Documentation

## Objective

Keep durable project documentation concise, current, correctly routed, and distinct from evidence, decisions, plans, and task state.

## Inputs

Required: target repository and documentation scope/change. Optional: accepted ADR, implemented diff, audience, existing docs, and required format.

## Context

Route through `AGENTS.md` and `.agentic/README.md`. Read only the canonical document being changed plus the evidence/ADR/code needed to verify the new truth.

## Procedure

1. Classify the content: current truth, evidence/reference, accepted decision, temporary plan, active task, or supporting documentation.
2. Update the canonical location instead of duplicating the same rule elsewhere.
3. Derive documentation from accepted decisions and implemented behavior; do not manufacture missing business/architecture choices.
4. Keep root/router files compact and move depth to the relevant `.agentic/` path.
5. Repair links/indexes affected by moves or renames.
6. Remove stale statements only when evidence proves they are obsolete; preserve decision history in ADRs.
7. Run doc/link/schema checks where available.

## Output

Return documents changed, truth/source used, removed contradictions, links/indexes updated, and unresolved documentation gaps.

## Completion

One obvious canonical source exists for each changed fact, ADR history is preserved, temporary content is not promoted to durable truth, and relevant documentation validation passes.
