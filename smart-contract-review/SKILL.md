---
name: smart-contract-review
description: "Review a scoped EVM/Solidity contract implementation or change for reachable security weaknesses, privileged controls and upgrade/accounting risks. Use for source-grounded contract assessment; do not infer a deployed exploit from unmatched source or perform live exploitation."
---
# Smart Contract Review

## Objective

Find actionable contract weaknesses with explicit attacker prerequisites, implementation/deployment identity and validation limits.

## Inputs

Required: contract/source/change scope and authorized review activities. Optional: chain/block/address, deployed bytecode, compiler/build settings, proxy/implementation/admin state, threat model and isolated test artifacts.

## Context

Read the actual entrypoints, inherited code/modifiers, external dependencies and accepted invariants. Use the [method guide](references/method.md) for detailed checks and
worked examples, and the [report template](assets/report-template.md) to retain evidence.

## Procedure

1. Pin source/config/dependency/compiler identity and any deployment chain/block/address. Establish whether bytecode/source, proxy implementation and initialization state actually match; unmatched source permits source findings only.
2. Map callers, permissions, balances/obligations, state transitions and external calls. Trace controls through real invocation paths, including callbacks, alternate entrypoints, initialization and upgrades; the presence of a guard or audit badge proves no coverage.
3. Check relevant authorization, reentrancy, signature/replay domains, oracle/time assumptions, rounding/precision, token quirks, external-call failure handling, gas/resource limits and cross-contract accounting. Identify attacker control and realistic preconditions before severity.
4. Review proxy/admin/upgrade/storage-layout authority and dependency changes at the applicable version/block. Distinguish accepted administrator power from a bypass; document its impact and trust assumptions.
5. Use trusted compatible static checks or synthetic local tests only within authorized scope, after inspecting scripts/plugins. No live exploit, transaction submission, wallet connection or secret retrieval follows from a review request. Missing execution leaves a source-based or conditional finding.
6. Challenge findings with reachable guards, accounting invariants, deployment conditions and contrary tests. Report the smallest correction and regression needed; do not certify deployed security or execute fixes without the requested scope.

## Output

Return source/deployment identity, invariants, prioritized findings with paths/functions, prerequisites, impact, counterevidence, actual checks, suggested fixes and unverified deployment or execution claims.

## Completion

Material severity claims identify reachable behavior or missing prerequisites. Source review, isolated proof, deployment match and live exploitability remain separate evidence.
