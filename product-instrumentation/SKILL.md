---
name: product-instrumentation
description: "Design, implement or review product tracking plans, event contracts, identity semantics and event-payload QA for an authorized measurement question. Use for instrumentation and analytics data quality; use product-analytics for interpreting funnels/cohorts and product-experimentation for causal tests."
---
# Product Instrumentation

## Objective and inputs

Make approved measurement reproducible through versioned event contracts and
observable QA. Establish the product/decision, permitted data, collection scope,
existing event pipeline and intended changes. Do not infer tracking permission
from a request to analyze supplied data or from an unrelated working directory.

## Procedure

1. Map each decision to a metric, unit, denominator and observation window; inventory
   existing events before adding collection. Use the [method](references/method.md)
   for contracts, identity, retries and reconciliation.
2. Specify event name/version, owner, business trigger, required/optional properties,
   types/units/enums, source, timestamps, identity and event IDs. Separate proposed
   schemas from deployed behavior and observational fixtures from actual emissions.
3. Define anonymous/known identity, merge/split/logout and shared-device behavior.
   Record the allowed linking evidence; never join users solely by matching names,
   emails, devices or timestamps. Do not retain direct identifiers by default.
4. Define event-time versus ingestion-time, timezone, retry/idempotency keys,
   ordering/late arrivals, offline buffers, loss and backfill semantics. State where
   deduplication occurs and its window; delivery is not automatically exactly-once.
5. Implement only authorized source changes using existing SDK/configuration and
   project conventions. Keep secrets/server-only fields out of clients and logs.
   Do not provision a vendor, enable production collection or change consent policy
   merely to complete a tracking plan.
6. Exercise synthetic local/staging payloads through actual available tooling:
   success/cancellation/retry, duplicate IDs, missing/extra fields, denied collection,
   identity changes and clock skew. Reconcile emitted versus accepted events and
   downstream metrics; distinguish a validator pass from real transport/collection.
7. Deliver the [tracking/QA report](assets/report-template.md), contracts, actual
   commands/results, excluded data, migration/deprecation plan and remaining gaps.
   Route analysis to product-analytics when available, without requiring that skill.

## Completion

Each proposed metric has a traceable event contract and each implemented claim has
actual QA evidence or an explicit unavailable check. Original payloads remain
recoverable in their authorized location; redact separate reporting copies. No
instrumentation, user linking, account change or production rollout was invented.
