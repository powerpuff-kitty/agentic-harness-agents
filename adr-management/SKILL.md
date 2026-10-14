---
name: adr-management
description: "Create, update, supersede, reject, or index Architecture Decision Records while preserving decision history. Use when a consequential technical or product decision has been proposed or accepted and needs durable rationale. Do not use merely to edit current architecture documentation or to design a solution that has not yet been decided."
---
# ADR Management

## Objective

Maintain durable, traceable decision history without confusing past rationale with current architecture truth.

## Inputs

Required: target project and decision statement. Optional: status, context/evidence, alternatives, consequences, superseded ADR, decision owner/date, and implementation follow-up.

## Context

Read `.agentic/decisions/README.md`, `index.yaml`, relevant existing ADRs, current architecture/product/security truth, and only evidence needed for this decision.

## Procedure

1. Determine whether the request is a new decision, status change, correction, or supersession.
2. Check for an existing ADR that already owns the decision; do not duplicate it.
3. Capture context, considered alternatives, decision, consequences, and explicit status without manufacturing rationale.
4. Allocate/validate the ADR identifier and canonical filename.
5. For supersession, update both old and new records consistently while retaining history.
6. Update `index.yaml` deterministically.
7. If accepted truth changed, identify the canonical document that must be updated separately (for example `ARCHITECTURE.md`).

## Output

Return the ADR path, identifier/status, index change, supersession relationships, canonical-truth follow-up, and unresolved evidence or approval gaps.

## Completion

The ADR is indexed, internally consistent, preserves prior history, does not contradict current truth silently, and any required architecture/product/security update is completed or explicitly queued.
