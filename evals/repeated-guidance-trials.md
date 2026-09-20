# Repeated guidance-trial reporting

This repository evaluator advances P0 #26/#36/#32. It summarizes supplied records;
it does not launch a host, call Jev, read credentials, authenticate traces or prove
that a model followed a skill. Production skill payloads do not load this module.
Use `prepare_guidance_trial.py` for participant preparation and the existing
`guidance-trial-record` v1 for observations. Do not supply reviewer answers to the
participant. Fixture checks and real sessions remain separate evidence kinds.

## Fix the comparison before collecting results

Create a `guidance-series-plan` v1 with exactly these fields:

- `format_version: 1`, `kind: guidance-series-plan`, and `spec` containing the
  existing comparison specification (`case` and `required_checks`).
- `evidence_kind`: `synthetic` or `recorded-session`; `identity` fixes the source,
  policy, checks, host, model and settings using the existing trial identity keys.
- `treatments`: the exact `baseline` and `candidate` name/SHA-256 objects; their
  content fingerprints must differ. Record the actual prepared guidance identities.
- `pair_ids`: all planned repetition IDs, in reporting order, before seeing results.

An identity is not guessed: a plan requires known identity fields. Records with
unknown or different identities remain unassessed and cannot enter aggregate cost
comparison. Use a separate series for another task, model, configuration or version.

Compute the canonical plan fingerprint with `guidance_comparison.fingerprint(plan)`
and retain it independently before execution. This fingerprint normalizes JSON
object-key order, not list order; it is not a raw-file checksum. Supply that reviewed
value to the evaluator rather than regenerating it from a results-adjusted plan.
The evaluator checks equality, not when or by whom the plan was registered. A
producer who rewrites both the plan and the supplied pin can still mislead it.

Collect a JSON list of `{id, baseline, candidate}` pairs. Each role contains the
existing v1 trial record or `null` when unavailable. Entire absent pairs also remain
missing. Retain the actual reason in the separate run record; never manufacture an
observation or zero usage to fill the slot. Unplanned and duplicate pair IDs fail.

For recorded sessions, retain separately scoped trace and usage artifacts per
session. Reusing identical trace/usage digests across records makes the series
not comparable, even under different paths. Shared check-log digests are permitted.
Call IDs stay record-local as in v1; the evaluator cannot infer global provider call
identity, detect unreported attempts or authenticate an edited evidence reference.
Source/evidence references are not followed or executed.

## Run the evaluator

```bash
python3 .github/scripts/guidance_series.py \
  /reviewed/plan.json /reviewed/pairs.json \
  --expected-plan-sha256 "$REVIEWED_PLAN_FINGERPRINT"
```

API: `guidance_series.summarize(plan, pairs, expected_plan_sha256=reviewed_pin)`.
It reuses the existing comparator for acceptance rather than defining a new grader.
The plan and pairs must be reviewed, quiescent JSON inputs in a trusted workspace;
this command is not a hostile-filesystem sandbox. Each input is bounded to 1 MiB,
128 pairs, nesting depth 32 and 100,000 visited values. Each call count is bounded
to 10^12 tokens. All original v1 token-type and unique-call checks still apply.
Invalid inputs produce a fixed error, not partial results or echoed source content.

Exit 0 means the complete matched series has passing supplied acceptance fields
and complete supplied usage, allowing a descriptive comparison. It does not mean
lower cost, better quality, approval or independently verified results. Exit 1
returns a report with missing, mismatched, failed or usage-incomplete runs. Exit 2
means malformed input or a pin mismatch. The command does not modify either file.

## Interpreting results

Every planned pair is retained, including its record fingerprints, acceptance
status, recorded token total when available, and diagnostic reasons. Acceptance
counts use the planned denominator and separate `passed`, `failed` and
`not-assessed`; these describe grader fields, not observed model success rates.
The nested `pair_comparison` is the existing pair comparator result. It cannot
supersede a series-level mismatch or reused-evidence finding.

Aggregate token statistics require the entire planned cohort to match the plan,
with complete usage for every record. There is no automatic passing-only or
known-usage subset. Missing records, unknown usage, mixed evidence or identity
changes leave aggregate statistics null. Per-record known totals stay visible but
are not labeled comparable or complete cohort totals.

When all usage is available, failed-acceptance sessions remain in the cost totals.
A failed baseline is not a quality-preserving optimisation control. A cheaper
candidate with failures receives `acceptance-not-satisfied`, not an optimisation
verdict. Include every recorded model input/output call, retry and auxiliary
provider; tool text already counted in model input is not added a second time.

The report gives n, total, mean, median, min/max and sample standard deviation for
baseline totals, candidate totals and **paired baseline-minus-candidate differences**.
Sample deviation is null for n=1. The reduction fraction uses summed totals, not an
average of per-run percentages, and is null for a zero baseline. Negative values
mean more submitted tokens. These are descriptive numbers, not confidence intervals,
statistical significance, calibration evidence, independence or provider billing.

Trace authentication, preregistration authentication, independence, model quality,
billing savings and verified optimisation remain false for all reports. Independent
review of representative actual sessions is still required by #26.

## Reproducible synthetic counterexample

```bash
python3 .github/scripts/guidance_series.py \
  evals/fixtures/guidance-series/plan.json \
  evals/fixtures/guidance-series/pairs.json \
  --expected-plan-sha256 "$(cat evals/fixtures/guidance-series/plan-fingerprint.txt)"
```

This intentionally exits **1**. Three baseline records declare 100 tokens each.
Candidate records declare 50, 50 and 300; the third fails acceptance. Selecting only
the first two would suggest a saving, but the complete series reports baseline
300 versus candidate 400, paired reduction -100, and candidate acceptance 2 passed /
1 failed / 0 unassessed out of 3 planned. These are invented fixture counts, not
observed model usage. Removing the failed pair instead yields an incomplete series
with no aggregate token comparison. The files contain synthetic data only.

Run `python3 .github/scripts/test_guidance_series.py` for regression tests; the
normal `validate_agents.py` also runs them. All existing comparator behavior,
production skill instructions, host integrations and release versions are unchanged.
