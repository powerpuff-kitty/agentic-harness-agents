# Backtest review guide

Choose checks by instrument, strategy and engine; this is not a requirement to
rewrite every supplied simulator. All numerical examples below are synthetic.

## Reproducibility and causal timeline

Identify exact source/config/data versions, input hashes where available, engine
version, seeds, universe/listing history, time range, warmup, benchmark, initial
capital, account currency, cash-flow convention and every research trial known to
the reviewer. Store no secrets. Missing code, ledger or data limits what can be
reproduced; a screenshot of a Sharpe ratio is not a run artifact.

For one sample signal, trace each input's event, publication/availability and
revision times through preprocessing, training, feature calculation, signal,
order submission and earliest feasible fill. Close-derived signals generally
cannot fill at that same close unless a realistic executable information/order
mechanism is established. Calendar joins, timezone conversion and delayed inputs
can leak future observations without a literal negative shift in the code.

Synthetic case: a daily close at 100 becomes known after the closing auction;
the strategy uses that close to choose a trade and books its fill at 100 in the
same auction. The entry is unsupported without an established feasible mechanism.
A next-session opening price of 105 changes the fill assumption; moving a column
one row is not sufficient if other features, revisions or preprocessing still leak.

Fit normalization, imputation, universe filters and models on training/available
history only. Check centered rolling windows, full-sample extrema, future labels,
revised fundamentals and present-day constituent lists. Overlapping outcome labels
can contaminate adjacent splits; select an appropriate purged/gapped design when
needed rather than blindly applying a universal split percentage.

[Freqtrade lookahead analysis](https://www.freqtrade.io/en/stable/lookahead-analysis/)
provides an engine-specific bias diagnostic; its scope/caveats still matter. A
clean result does not rule out every data, execution or selection problem.
[Freqtrade backtesting documentation](https://www.freqtrade.io/en/stable/backtesting/)
explains simulator assumptions. Verify the installed version before using its
commands; do not copy provider-specific execution flags into a generic workflow.
References reviewed 2026-10-14.

## Fill, ledger and costs

Inspect the actual cash/position/equity update order. Cover bid/ask and spread,
commissions, slippage/impact, available volume, tick/lot constraints, partial fills,
latency, intrabar order ambiguity and stop/limit priority where applicable. A bar's
high and low alone do not establish which price was reached first. Do not assume
infinite liquidity or a beneficial intrabar path. Reconcile borrow, dividends,
funding, leverage/margin, contract rolls and settlement for applicable positions.

Synthetic one-round-trip cash-equity case: buy 10 shares at 100 and sell them at
110; gross P&L = 100. At a 0.1% fee on each traded notional, fees are 1 + 1.1 = 2.1,
net P&L = 97.9. With initial capital 2000, the entry leaves cash 999 after its
fee; final equity is 2097.9 and return is 4.895% with no other costs/cash flows.
Using capital 1000 for that exact purchase would leave the entry fee unfunded;
do not silently create available capital.

An equity curve must reconcile initial capital, external cash flows, realized and
unrealized P&L and costs. Trade win rate alone cannot validate it. Distinguish cash
flows from returns and use an appropriate money-/time-weighted convention. A
strategy and benchmark need consistent dates, currency, dividend treatment and
capital/cost definitions. Avoid cherry-picking the highest-performing asset, date
range or cost assumption after seeing the results.

## Selection and statistical interpretation

Separate development, validation and untouched test data. Record how many variants,
features, assets and parameter trials influenced selection. A nominal test period
reused for choosing the best variant is no longer untouched. Use walk-forward or
other appropriate time-aware designs, with refitting intervals and input availability
explicit. A single split does not eliminate multiple-testing or regime-selection risk.

Report total/annualized returns, drawdown, turnover, exposure and risk-adjusted
metrics only with clear conventions and enough evidence. For periodic simple
returns r_t with no external cash flows, compounded return is product(1+r_t)-1.
For example, +10% then -10% gives -1%, not zero. Annualization frequency, idle
periods, dependence and risk-free rate matter. A short series or zero volatility
can make a Sharpe statistic undefined or misleading; do not fill it with zero or
infinity to make a scorecard complete. Confidence methods must respect temporal
dependence and the selection process rather than treating every bar as independent.

Sensitivity to fees, spread, slippage, start/end dates, capacity, parameter changes
and regimes should inform the conclusion. A fragile positive historical net return
is a conditional result. No observed evidence means no measured performance claim.

## Paper and live boundaries

[Alpaca paper-trading documentation](https://docs.alpaca.markets/us/docs/paper-trading)
distinguishes simulated execution from live conditions. Paper accounts and live
accounts remain different inputs/environments even when an API shape is similar.
This skill needs no account connection by default. Offline review does not authorize
live/paper bot activation, order submission, transfers or an account configuration
change. If those are separately requested, establish the actual tool/environment,
limits and authority under that task before acting.
