---
name: financial-model-review
description: "Review a financial statement, forecast, valuation or portfolio-risk model for source integrity, accounting reconciliation, formula logic and assumption sensitivity. Use for spreadsheet/model assurance and financial calculations. Do not use for market-data cleanup, trading backtest validation, tax certification or transaction execution."
---
# Financial Model Review

## Objective

Make a financial model's supported conclusions, calculation defects and assumption
risks explicit without presenting a plausible spreadsheet as verified economics.

## Inputs

Required: approved model/artifact and the decision or review scope. Optional:
source statements, reporting basis, entity/period/currency, assumption log,
valuation date, scenario policy, benchmarks and expected reconciliation tolerances.

## Context

Inspect formulas, input lineage and relevant project rules before trusting cached
outputs. Use the [review guide](references/model-review.md) for accounting,
valuation and risk-model checks; use the [report template](assets/report-template.md)
for findings and sensitivity. Never run workbook macros merely to inspect a model.

## Procedure

1. Pin model version, entity/consolidation scope, reporting period, currency/units, accounting basis and intended decision. Distinguish historical statements, management adjustments, forecasts, scenarios and observed results.
2. Trace material inputs to dated filings, approved records or declared assumptions. Preserve original records and distinguish estimates from measurements. Missing inputs permit conditional review, not invented rates, holdings or balances.
3. Inspect formulas and dependencies as well as displayed/cached values. Check signs, percentage scales, units, periods, hardcodes, broken links, circularity, missing values and whether totals reconcile under the stated definitions.
4. Apply relevant accounting, cash-flow, valuation or portfolio checks from the guide. Recompute material results independently with available trusted tools; record tool precision, tolerances and any unavailable recalculation or hidden/external sheets.
5. Stress assumptions and plausible edge cases. Align nominal/real and pre/post-tax quantities, timing and currency. Distinguish contractual facts, model scenarios and probabilistic estimates; avoid false precision or claims unsupported by the available sample.
6. Classify confirmed formula/data defects separately from reasonable modeling choices, assumption risks and unperformed checks. Propose minimal corrections and verification; change a supplied model only when the task authorizes edits.
7. Report decision sensitivity, remaining evidence and review boundaries. Analysis does not place orders, rebalance holdings, move funds or establish accounting/regulatory certification; those are separate workflows with their own authority.

## Output

Return model/source identity, assumptions, reconciliation results, prioritized
findings with formula/cell/path evidence, independent calculations, sensitivity,
actual checks and unresolved limitations. Separate original and corrected results.

## Completion

Material conclusions have traced inputs and reproducible calculations or explicit
unverified status. Accounting identities, cash-flow timing, risk assumptions and
model limits are checked where relevant. A review or scenario is not a forecast guarantee.
