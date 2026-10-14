# Financial-model review methods

Choose the sections that fit the model. These examples are synthetic calculation
checks, not a universal accounting policy or a recommendation to buy an asset.

## Identity, lineage and recalculation

Record entity and consolidation scope, period/fiscal calendar, source filing and
publication/as-of date, reporting basis, currency and scale. Do not mix quarterly
flows with year-to-date flows or stock balances with period averages. Preserve
reported and adjusted metrics separately; document the bridge and adjustment basis.
[SEC EDGAR API documentation](https://www.sec.gov/edgar/sec-api-documentation)
helps locate filing/XBRL records, but tags/units/periods still require interpretation.
Use the applicable current accounting/valuation standards when the task calls for
them; this guide makes no jurisdiction-wide compliance claim. Reviewed 2026-10-14.

Inspect formulas, named ranges, hidden sheets, external links, date conventions and
cached-result freshness using available tools. Never enable macros or external
connections merely because a file requests it. If recalculation is unavailable,
report that separately from manual review of selected formulas. Preserve the
original file; use an approved derived copy for requested corrections.

## Statement and cash-flow checks

- Balance sheet: assets = liabilities + equity under the model's sign convention.
- Cash reconciliation: ending cash = beginning cash + operating + investing +
  financing cash flows + separately modeled FX/other reconciliation effects.
- Cross-check profit, debt, retained earnings, working capital, capex and share
  counts against consistent periods/definitions where the model links them.
- Test subtotal formulas and source ranges. A zero total can hide offsetting errors.
  Missing inputs are not zero; tolerances must match currency scale and rounding.
- Define free cash flow explicitly; unlevered/levered cash flow and valuation target
  cannot be interchanged without the corresponding financing/tax treatment.

Synthetic example (all amounts USD thousands): assets 150, liabilities 90, equity
60 reconcile. Beginning cash 20 + operating 15 - investing 5 - financing 2 = ending
cash 28 with no FX/other effect. A displayed ending cash of 30 leaves a residual
of 2 to investigate. It is not evidence that equity should be edited to force fit.

## Forecast and valuation checks

Separate volume/price, fixed/variable costs, working capital, capex, funding and
cash timing where relevant. Assumptions should have owners/sources, dates and
sensitivity ranges; avoid simply extending the best historical period.

For an end-of-year cash flow CF_t and matching annual effective discount rate r,
PV = sum(CF_t / (1+r)^t). Actual dated cash flows may need explicit day-count and
XNPV conventions. Nominal cash flows need nominal rates in the same currency;
pre-/post-tax and levered/unlevered treatment must match the discount rate and
valuation target. Do not treat WACC as a universal rate for any cash flow.

Synthetic two-year case: CF1 = 110, CF2 = 121, r = 10% gives PV = 100 + 100 = 200.
This excludes terminal value and an initial investment. With an initial outflow
of 180 at t=0, project NPV is 20. At r=20%, those same future cash flows have PV
about 175.6944, and NPV about -4.3056. A report must identify which quantity it
calls value/NPV and why the rate changed.

For a perpetual-growth terminal value CF_(n+1)/(r-g), the chosen model requires
r > g and credible steady-state assumptions. A denominator at/near zero, unsupported
horizon or discontinuous terminal margins is a model warning, not a very precise
valuation. Enterprise value, equity value, net debt and per-share quantities need
a consistent bridge, share count and dilution convention. Non-equity instruments
need their own cash-flow/contract models; do not reuse a stock DCF by name alone.

## Portfolio/risk-model checks

Require approved holdings, prices, multipliers, currency/FX and an as-of snapshot.
Net exposure can hide leverage: a 150 long and 50 short portfolio with NAV 100 has
net exposure 100% and gross exposure 200%, ignoring additional liabilities/cash
conventions. Under a common -10% price move and a linear notional approximation,
the long loses 15 and the short gains 5: net loss 10. That is a scenario, not a
maximum possible loss. Options and other nonlinear positions require a suitable
repricing method; delta-only stress misses curvature and changing volatility.

For VaR or expected shortfall, state horizon, confidence/tail definition, return
convention, sample/model, weighting and missingness. A VaR figure is not a worst-case
loss and may be unreliable with short samples or regime shifts. Avoid universal
square-root-time scaling or normality assumptions. For performance ratios, align
risk-free rate, frequency and return type; do not annualize a few dependent
observations as if they were a stable independent sample.

## Finding and handoff example

Confirmed: a forecast references tax in percent units (25) as a decimal rate and
subtracts 25 times pre-tax income. Cite the actual formula and input definition,
show a bounded independent recomputation, propose the minimal correction and test
both normal and loss cases under the accepted tax assumptions.

Conditional: a discount rate looks low but no required-return basis is supplied.
Show sensitivity and ask for the missing policy/source; do not classify preference
as arithmetic error. Independent review belongs to another actual reviewer where
requested, not the author relabeling its own output as independently verified.
