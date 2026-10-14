# DeFi risk methods

## Mechanism and provenance

Record protocol/version, chain, contract/pool/position, block hash/finality,
collateral/debt units, oracle source/time/decimals, parameters, market data and
requested question. Identify proxies/admins, governance/timelocks, dependencies,
bridges and custodial/wrapped-token assumptions. No address, snapshot or source
access means no factual current-position claim.

Contract correctness, economics, liquidity and operator authority are distinct.
A formally checked function does not establish oracle truth, redeemability or
market capacity. Token symbols and an advertised stable price do not prove a peg.
Use approved read-only evidence; no wallet/signature is needed by default.

## Lending example

For a declared single-collateral model, health factor may be collateral value ×
liquidation threshold / debt value. A synthetic position with collateral 120,
threshold .75 and debt 60 has HF 1.5. If only collateral price falls 40%, collateral
becomes 72 and HF .9, with unchanged debt/threshold. This is a modeled threshold
breach. It does not establish an executed liquidation, its amount or a maximum loss.

[Aave health-factor documentation](https://aave.com/help/borrowing/liquidations)
describes its mechanism; obtain the actual deployment/version/parameters before
applying it. Multiple collateral assets, efficiency/isolation modes, price rules,
interest, close factors, bonuses and liquidity may change the result. Missing
parameters must not be filled with defaults from an unrelated market/version.

## AMM/LP example

For a fee-free full-range constant-product two-asset pool, LP value relative to
holding the initial assets after relative price ratio r can be 2√r/(1+r). At r=4,
this equals .8, or -20% relative to that holding benchmark. This is a relative
model result, not a -20% USD loss or a maximum loss. Fees, external cash flows,
rebalancing and concentrated ranges are excluded.

[Uniswap v2 mechanism documentation](https://docs.uniswap.org/contracts/v2/concepts/protocol-overview/how-uniswap-works)
is a reference for that model, not a formula for every AMM or Uniswap version.
Concentrated liquidity needs range, active inventory, fee accrual and price-path
handling. A pool price is not automatically the realizable price of a large exit.
Both protocol references were reviewed 2026-10-14.

## Risk report boundaries

Stress collateral AND debt/oracle prices, rates, depegs, withdrawal/bridge delay,
liquidity and governance/dependency changes when relevant. Explain uncertain
correlations and nonlinear paths. APY requires a compounding/reinvestment model;
APR, emissions and realized net return are different quantities. Gas, financing,
slippage and token-price changes can dominate a quoted yield.

Separate confirmed configuration facts, source-based contract risks, hypothetical
stress results and not-checked dependencies. Identify the next bounded verification
rather than recommending a wallet action or calling a protocol safe.
