---
name: database-design
description: "Design or review persistent data models, relational schemas, constraints, indexes, transactions, migrations, retention, and data-access boundaries. Use when the requested artifact is a database/data-model design or schema evolution. Do not use primarily for API contract design, dependency upgrades, or generic backend implementation."
---
# Database Design

## Objective

Create a data model that preserves domain invariants, query needs, migration safety, and operational requirements.

## Inputs

Required: domain entities/use cases and target datastore or constraints. Optional: scale, query patterns, tenancy, consistency requirements, retention/privacy rules, existing schema, and migration constraints.

## Context

Read relevant product/domain truth, architecture, security/privacy, data docs, existing schema/migrations, and ADRs. Do not infer business invariants solely from existing tables.

## Procedure

1. Identify entities, ownership, lifecycle, invariants, and access patterns.
2. Choose modeling boundaries consistent with the accepted datastore/architecture.
3. Define keys, relationships, nullability, uniqueness, constraints, and transactional boundaries.
4. Design indexes from real query patterns and expected cardinality rather than adding them indiscriminately.
5. Address tenancy isolation, sensitive data, retention, deletion, auditability, and concurrency.
6. Plan forward/backward-compatible migrations, backfills, rollback/recovery, and deployment ordering.
7. Validate with schema tooling/tests/explain plans where available.

## Output

Return schema/model changes, rationale, invariants, index/query implications, migration plan, risks, and unresolved decisions.

## Completion

Critical invariants are mechanically enforceable where practical, migrations are operationally safe, privacy/security rules are respected, and performance claims are evidence-based.
