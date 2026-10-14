---
name: forecast-calibration
description: "Evaluate recorded probabilistic forecasts against defined outcomes using proper scores, calibration diagnostics and out-of-sample checks. Use for event, risk and prediction-model evaluation. Do not use to invent forecasts, treat unresolved outcomes as losses or claim betting profitability from a score."
---
# Forecast Calibration

## Objective

Assess probabilistic predictions with explicit event, timing, sample and scoring conventions while separating accuracy, calibration, sharpness and economic value.

## Inputs

Required: recorded forecast probabilities/timestamps and outcome definitions/statuses or a bounded evaluation plan. Optional: horizon/as-of policy, question IDs, weights, baseline, training/selection history and dependence information.

## Context

Inspect raw predictions and labels, including unresolved/excluded records, before selecting a score or fitting a calibrator. Use the [method guide](references/method.md) for detailed checks and
worked examples, and the [report template](assets/report-template.md) to retain evidence.

## Procedure

1. Define the event/outcome, forecast issue/cutoff and scoring/as-of times, horizon, population, weights and unit of evaluation. Verify that forecasts precede the relevant information and labels have valid resolved status under the specified rules.
2. Validate probability domains and categorical normalization where required. Preserve unresolved/cancelled/missing outcomes as such; record exclusions and selection/censoring risks rather than encoding missing labels as zero.
3. Compute a declared proper score such as binary mean Brier or log loss and a predeclared comparable baseline. State averaging, weighting, multiclass conventions and zero/one probability handling; do not silently clip away impossible-outcome penalties.
4. Assess calibration with bin/reliability counts, predicted versus observed frequencies and uncertainty appropriate to the sample/dependence. Score improvement or a few correct predictions alone does not establish calibration or future reliability.
5. Keep calibrator fitting, method selection and final evaluation separate using appropriate time-aware/out-of-sample data. Account for repeated forecasts of one question, overlapping horizons, regime changes and test reuse; do not tune on the final score and call it untouched.
6. Report actual calculations, baseline sensitivity and coverage limits. A calibration report is not a causal claim, model guarantee, market edge or instruction to submit forecasts/orders/bets; save only requested evaluation artifacts.

## Output

Return dataset/as-of/label identities, exclusions, score and baseline definitions/results, calibration counts/uncertainty, out-of-sample provenance, actual checks and bounded conclusions.

## Completion

Scores reconcile with recorded probabilities/outcomes and explicit denominators. Unresolved events and uncertainty remain visible; fit/evaluation separation and sample limitations qualify the claim.
