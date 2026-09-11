---
name: api-design
description: "Design or review external or internal API contracts including resources, operations, errors, pagination, versioning, idempotency, authentication boundaries, and compatibility. Use when an API surface or contract is the requested design artifact. Do not use primarily for database schema design, implementation debugging, or broad codebase review."
---
# API Design

## Objective

Create a coherent, evolvable API contract aligned with accepted product, architecture, security, and data boundaries.

## Inputs

Required: target capability/domain and consumers. Optional: protocol/style, existing API, compatibility requirements, auth/tenancy model, performance constraints, and schema tooling.

## Context

Read `.agentic/PRODUCT.md`, `.agentic/ARCHITECTURE.md`, `.agentic/SECURITY.md`, relevant API/data docs and ADRs. Load only domain material needed for the endpoints under design.

## Procedure

1. Identify consumers, use cases, trust boundaries, and compatibility constraints.
2. Model resources/messages around domain concepts rather than storage tables.
3. Define operations, request/response schemas, status/error semantics, pagination/filtering, idempotency, concurrency, and validation.
4. Specify authentication/authorization/tenancy behavior without inventing policy.
5. Define versioning and backward-compatibility expectations.
6. Check observability, rate limits, performance-sensitive payloads, and failure/retry behavior.
7. Validate against existing contracts/tests/schema tooling where available.

## Output

Return the proposed contract, examples, compatibility/security considerations, unresolved decisions, and validation approach; distinguish accepted rules from recommendations.

## Completion

All requested operations have explicit success/failure semantics, security boundaries are consistent with project truth, compatibility risks are stated, and the contract can be verified mechanically where possible.
