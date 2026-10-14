---
name: product-experimentation
description: "Design and assess product experiments with explicit randomization/exposure units, metrics, guardrails, stopping rules and trustworthy readouts. Use for A/B and controlled product tests; do not treat observational before/after analytics or a backtest as randomized causal evidence."
---
# Product Experimentation

## Objective and inputs

Make an experiment decision from an explicit design and valid measurement. Establish
hypothesis, target population, practical effect, assignment mechanism/unit, exposure,
metrics, data snapshot and rollout authority. Use the [method](references/method.md)
for validity gates and readout. A design request does not authorize live assignment.

## Procedure

1. Define hypothesis, intervention/control, eligible population, randomization and
   analysis units, interference risks and intended estimand. Distinguish assignment,
   exposure and analysis populations and specify intention-to-treat/exposure rules.
2. Predeclare primary outcome, denominator/window, guardrails, practical threshold,
   exclusions, sample/power or precision assumptions, duration/stopping policy and
   treatment of multiple comparisons. Unknown inputs stay assumptions, not estimates.
3. Verify event/identity contracts, assignment persistence, logging, unit isolation
   and treatment/exposure eligibility with synthetic available checks before launch.
   Use the approved release process for any actual rollout; no implicit spend or
   production experiment is granted by this procedure.
4. Check sample-ratio mismatch against the planned allocation, loss/missingness,
   exposure imbalance, contamination, repeated-unit dependence and metric revisions.
   Investigate validity blockers before interpreting a positive result. SRM is a
   diagnostic signal, not a mechanical proof of a particular root cause.
5. Use the planned method with reproducible code/queries. Report assignment/exposure/
   analysis counts, absolute and relative effects with denominators, uncertainty,
   guardrails and exclusions. Adjust for clustering/sequential looks/multiplicity
   when applicable; do not select a favorable method after seeing the outcome.
6. Separate statistical evidence, practical value, validity and launch authority.
   Retain failed/null/ambiguous outcomes and harm signals. Propose follow-up or a
   bounded decision rather than turning uncertainty into 'no effect' or 'ship'.
7. Deliver the [plan/readout](assets/report-template.md), design/version, actual
   checks, calculations, blockers and next action. Use the assigned experiment/design
   owner (scientist when that role exists); analysis, implementation and independent
   evidence checks remain distinct when available.

## Completion

The readout is reproducible for its assigned/exposed population, validity gaps and
harm remain visible, and no causal or rollout claim outruns the experiment evidence.
