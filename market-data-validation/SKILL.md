---
name: market-data-validation
description: "Validate financial market datasets for point-in-time research, backtests and portfolio analysis. Use for timestamp/availability checks, corporate actions, instrument identity, missing sessions and price/return provenance. Do not use for price predictions, trade execution or general non-market data cleaning."
---
# Market Data Validation

## Objective

Establish what a market dataset can support without hiding missing history,
revisions, timing ambiguity or unsupported instruments behind a clean CSV.

## Inputs

Required: approved dataset or access scope and its intended use/as-of time.
Optional: provider contract, instrument master, venue/session calendar, publication
and revision timestamps, adjustment policy, currency and comparison source.

## Context

Inspect the actual schema, source metadata and transformations first. Use the
[validation guide](references/validation-guide.md) for temporal, instrument and
corporate-action checks, and the [report template](assets/report-template.md) for
a reusable evidence contract. Missing data access permits a validation plan only.

## Procedure

1. Pin dataset/source identity, retrieval time, covered instruments and permitted reads. Keep raw inputs; do not acquire paid data, credentials or live account access merely to validate a file.
2. Define each field's unit and semantics: quote/trade/bar, event/start/end time, timezone, publication/available-at time, revision, venue, price currency, volume unit and adjustment. Identify symbols by durable instrument/venue identifiers where available.
3. Establish chronological availability for the intended decision: observations and revisions must have been known then. Separate event time, source publication, ingestion and strategy latency. A current snapshot is not automatically point-in-time history.
4. Check duplicates, ordering, finite values, OHLC relationships and volume conventions against the instrument contract. Compare missing intervals with the correct venue calendar, listing/halt history and sampling policy; do not invent zero returns or universal weekday sessions.
5. Trace split/dividend/roll adjustments, delisted instruments, historical universe membership, FX timestamps and benchmark alignment. Reject mixing adjusted and raw prices or applying a return transformation without its assumptions. Negative prices can be valid for some instruments.
6. Corroborate consequential discrepancies using approved independent records when available. Separate deterministic defects, suspected provider differences and unavailable checks; repair only requested derived copies with a recorded transformation.
7. State suitability for the specific use, required corrections and unresolved temporal/coverage limits. Route financial model or backtest questions to their methods only when relevant and available; this skill does not select investments or execute transactions.

## Output

Return dataset/as-of identity, field/time/adjustment contract, coverage and evidence,
confirmed defects, conditional risks, actual checks, permitted transformations and
use-specific suitability. Preserve unknowns and reproducible input references.

## Completion

Material claims trace to identified records and checks. Availability, actions and
universe biases are addressed or explicitly unverified. Clean sampled records do
not establish complete history, current prices or viable trading performance.
