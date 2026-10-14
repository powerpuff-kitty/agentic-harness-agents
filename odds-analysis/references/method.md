# Odds and payoff methods

## Definitions and conversions

For ordinary decimal BACK odds d>1, raw implied probability is 1/d; a winning
unit stake returns d including stake, so net winning profit is d-1. American
+A (A>0) converts to 1+A/100; negative -A to 1+100/A. Fractional a/b converts
to 1+a/b with positive a,b. Confirm actual format rather than guessing from a
number; exchange lay quotes, Asian lines, each-way and prediction-contract prices
require their own liability/payout definitions.

Synthetic conversions: +150 -> 2.5 and raw p .4; -200 -> 1.5 and raw p 2/3;
5/2 -> 3.5 and raw p 2/7. Raw implied probabilities contain margin and are not
validated forecasts. A binary token price .62 is not decimal odds .62; its payout,
collateral, fees and resolution mechanism must be established first.

## Complete-market margin

For mutually exclusive/exhaustive outcomes at the same comparable market/time,
overround = Σ(1/d_i)-1. Decimal quotes 1.80 and 2.20 give raw probabilities
5/9 and 5/11, sum 100/99 and overround 1/99 ≈ 1.010101%.
Proportional normalization yields .55 and .45. This is one assumed margin model,
not a uniquely inferred true distribution or proof the market is calibrated.

Do not sum unrelated or overlapping outcomes. A three-way football market missing
the draw is incomplete, and 90-minute and extra-time-inclusive contracts differ.
Negative overround across stale quotes or inconsistent rules is not executable
arbitrage. Capacity, simultaneous fills, commission, currency and settlement matter.

## Conditional expectation and commissions

With a supported hypothetical win probability p and ordinary decimal back odds d,
unit net expected P&L before costs is p(d-1)-(1-p)=pd-1. At p=.60 and d=1.80,
this is .08 per unit, conditional on those assumptions. It does not establish the
probability, an edge or an appropriate stake.

For one isolated bet with a declared 5% commission on positive net winnings,
winning unit profit is .8×.95=.76. Expected net P&L becomes .6×.76-.4=.056.
For a back stake 100, winning net profit is 76 and loss is 100 under that model.
Do not charge an assumed flat percentage of turnover unless the actual rule says so.
[Betfair's commission documentation](https://support.betfair.com/app/answers/detail/a_id/413/)
uses net market winnings; several offsetting bets may therefore need market-level
netting rather than the isolated-bet simplification. Reference reviewed 2026-10-14;
no fixed commission rate or personal account configuration is inferred.

State the independent probability source, sample/uncertainty, fee assumptions,
matched quote size and timing. Vary assumptions when appropriate. Analysis does
not open accounts, evade limits, choose a personal bankroll or place a bet.
