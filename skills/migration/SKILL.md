# Migration

Inventory current and target states, compatibility constraints, data/code dependencies, rollback path, and observability. Prefer staged, reversible migrations. Define backfill strategy and idempotency where relevant. Test representative data and failure paths. Do not delete legacy state until the new path is verified and rollback risk is accepted.
