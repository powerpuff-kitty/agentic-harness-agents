---
name: threat-model
description: "Create or update a threat model for a proposed system, feature, integration, data flow, or architecture by mapping assets, actors, trust boundaries, attack paths, abuse cases, controls, and residual risk. Use before or during design when security threats must shape architecture. Do not use primarily to audit already-implemented code for vulnerabilities."
---
# Threat Model

## Objective

Make security assumptions and attack surfaces explicit early enough to influence architecture and requirements.

## Inputs

Required: system/feature scope and architecture/data flow. Optional: assets/data classification, actors, deployment model, auth/tenancy, external integrations, regulatory constraints, and existing threat model.

## Context

Read product scope, architecture diagrams/boundaries, security policy, data/API docs, and accepted ADRs relevant to the modeled flow. Avoid implementation detail unless it changes a boundary or control.

## Procedure

1. Define scope, assumptions, assets, security objectives, and out-of-scope areas.
2. Map actors, components, data flows, trust boundaries, external dependencies, and privileged operations.
3. Enumerate plausible threats/abuse cases across identity, authorization, spoofing, tampering, disclosure, availability, supply chain, and business-logic abuse as relevant.
4. Rate risk using the project's accepted method or clearly stated qualitative likelihood/impact.
5. Map existing controls and identify missing/preventive/detective/recovery mitigations.
6. Record residual risk, assumptions, validation requirements, and ownership.
7. Feed accepted architecture/security decisions into ADRs/current truth rather than leaving them only in the threat model.

## Output

Return scope, assets/actors, trust-boundary/data-flow model, threats with risk/evidence, controls, proposed mitigations, residual risks, assumptions, and validation tasks.

## Completion

Critical assets/boundaries are covered, risk rationale is explicit, mitigations are testable, unresolved architecture/security decisions are surfaced, and implementation vulnerability scanning is not falsely claimed.
