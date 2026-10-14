---
name: defi-risk-analysis
description: "Analyze a specified DeFi protocol or position for collateral, liquidation, oracle, liquidity, governance and dependency risk. Use for lending, AMM and protocol-exposure scenarios with explicit snapshots and assumptions. Do not use to execute swaps, farm yield or certify a protocol as safe."
---
# DeFi Risk Analysis

## Objective

Explain what a defined protocol/position snapshot and scenario support, separating contract controls, economic exposure and uncertain market execution.

## Inputs

Required: protocol/position question and approved records/snapshot. Optional: chain/block/address/version, collateral/debt, units/prices, liquidation parameters, pool configuration, governance and oracle/dependency evidence.

## Context

Establish the actual protocol mechanism and input definitions; do not transplant one lending or AMM formula across every product. Use the [method guide](references/method.md) for detailed checks and
worked examples, and the [report template](assets/report-template.md) to retain evidence.

## Procedure

1. Pin protocol/version/chain/block and supplied position/configuration. Trace token units, prices/oracles, collateral/debt, parameters, upgrade/admin and external dependencies. No snapshot permits a method or synthetic example, not invented holdings.
2. Map collateral, leverage, liquidity, oracle freshness/manipulation, depeg, bridge/custody, governance and contract risks relevant to the requested exposure. Distinguish code findings from economic scenarios and accepted trust assumptions.
3. Apply protocol-specific health/liquidation or AMM/LP calculations with stated units, thresholds, fees, ranges and price paths. Reconcile to the actual parameters and identify unsupported nonlinear or concentrated-liquidity models.
4. Stress material prices, funding/rates, liquidity and dependency failures where inputs allow. A threshold breach indicates a condition, not an observed liquidation, realizable exit price or maximum loss; account for unknown close factors, bonuses and keeper/market availability.
5. Distinguish quoted rates, APR/APY, emissions, fees and realized net returns. Document reinvestment, token-price, gas and horizon assumptions; never convert a current yield or simulation into a guaranteed future return.
6. Report scope, calculations, sensitivities and missing evidence. Use available contract/data specialists only when relevant; do not connect wallets, sign approvals, move collateral, borrow or transact merely to produce a risk report.

## Output

Return identified snapshot/mechanism, exposure/dependency map, protocol-specific calculations and stress results, assumptions, evidence gaps, actual checks and bounded conclusions.

## Completion

Calculations use identified parameters and distinguish observed state from hypothetical outcomes. A healthy sample ratio or prior audit is not a safety or liquidity guarantee.
