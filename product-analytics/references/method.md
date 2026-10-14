# Metric definitions and reconciliation

A funnel contract states unit, eligibility, entry/cohort event, event ordering,
maximum interval, cutoff, timezone, duplicate key, identity and repeated-entry rule.
Use earliest valid entry or the explicitly chosen session/episode definition.
Do not count a conversion that precedes entry or falls outside its window. Report
immature entrants separately instead of calling them failures or dropping them
without a count. A mature-cohort rate describes that cohort, not all current users.

Retention definitions differ: exact period N, bounded interval N, rolling return
at/after N, and calendar versus elapsed intervals. Name the rule and include only
units with the needed follow-up. Acquisition sources and attribution models are
inputs, not facts recovered from aggregate counts. Changing identity, eligibility
or instrumentation can produce a trend without changing product behavior.

Report dataset grain and raw rows -> valid/deduplicated events -> eligible units ->
cohort/mature units -> outcome units. Explain legitimate repeated events and replay
keys. Event-time and ingestion-time answer different questions; pin observation
cutoffs and late-arrival treatment. Never reconstruct private identity by guesswork.

Use actual available local query/analysis tools; retain query/code, versions and
output identity. For small fixtures a transparent list of units/outcomes is useful.
Uncertainty must match the data-generation process; an arbitrary confidence interval
cannot repair selection bias. Nonrandom segment comparisons are descriptive.
Do not infer treatment effect, revenue or market share from a funnel alone.

[Amplitude funnel definitions](https://amplitude.com/docs/analytics/charts/funnel-analysis/funnel-analysis-build)
and [data planning](https://amplitude.com/docs/data/data-planning-playbook) are primary
starting points (reviewed 2026-10-14); verify current vendor behavior before using
its UI/query semantics. The local fixture has synthetic pseudonymous units only.
