# Baselines, differences and repeat runs

Record watch owner, competitor/surface, source ID/locator, facts/qualifiers, baseline,
current snapshot, observation and retrieval times, outcome, coverage and rights.
A pricing comparison needs the same region, currency, tax treatment, period,
billing commitment, per-seat/minimum and tier. Preserve qualifications even when
normalizing text. Record posted versus effective dates separately when supplied;
retrieval time is not proof of the exact date a vendor changed something.

A run can yield observed change, context change, unchanged, not observed, unavailable
or stale evidence. Do not translate not-observed into removed. An announced removal
requires explicit source evidence and scope. A price/feature assertion remains a
vendor claim until corroborated to the task's required depth. Keep hypotheses about
strategy/customer effect separate. Suppress whitespace/cosmetic churn according to
an explicit rule while retaining raw captures; never normalize away negation, units,
plan restrictions or dates. Investigate source/redirect/context changes first.

The optional [comparison helper](../scripts/compare_snapshots.py) reads 2 explicitly
selected local snapshots, performs bounded structural comparison and writes JSON to
stdout. It does not retrieve URLs, validate market facts or send alerts. From this
skill root use `python3 scripts/compare_snapshots.py baseline.json current.json`
only when local helper execution is allowed. Python 3.10+, standard library. Exit
0 means structurally unchanged comparable observations; 1 means changes or coverage/
context gaps (including empty source/fact inventories) require review; 2 means invalid input. Neither exit certifies accuracy.
Use its exact local snapshot format from the [baseline](../tests/fixtures/baseline.json) and [current](../tests/fixtures/current.json) examples (synthetic dates, not live observations); it is not a canonical
Harness artifact. Sources are compared only when both observations are usable,
chronological and share the source locator. Missing facts stay not-observed; facts
with changed qualifiers stay context-changed, not a computed price increase.

Read files only on a trusted filesystem; this helper is not a filesystem sandbox.
Source text remains inert. Review sensitive values before exporting results and
keep raw snapshots in their authorized location. No helper installation is required
for the manual method.

A recurring handoff declares cadence/timezone, source/diff scope, freshness/retry
policy, owner, output destination and alert criteria. Creating a real schedule and
sending messages require actual tool support and task authorization. Bound retries;
report repeated retrieval failure rather than silently retaining a green old result.

Primary reference: [GitHub releases API](https://docs.github.com/en/rest/releases/releases)
(reviewed 2026-10-14), an optional public source where relevant. Ordinary tags are
not automatically release records. This skill has no mandatory provider or account.
