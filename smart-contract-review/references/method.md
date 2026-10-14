# Contract security review methods

## Evidence before severity

Identify source revision, dependency versions, compiler/settings, chain/block,
contract address and deployed bytecode where provided. A verified source for an
implementation does not identify which proxy uses it, its storage, initializer
state or effective privileges. A source-only issue is not proof of a deployed
vulnerability. For non-EVM languages, use an appropriate specialist method instead
of pretending Solidity assumptions cover them.

Inspect the complete relevant flow, inherited modifiers and actual dependency
behavior. Record attacker capability, affected invariant/asset, call path,
preconditions, impact and counterevidence. A privileged drain may be an accepted
administrator capability rather than an unauthorized-call bug; state the trust
consequence instead of concealing or exaggerating it.

## Source-to-state checks

- Authorization/initialization: who can call, upgrade, initialize/reinitialize,
  pause, mint or set an oracle? Check alternate paths and effective roles.
- External calls/callbacks: effects and obligations before/after interactions,
  cross-function reentry, return values, reverts and partial state assumptions.
- Signatures: signer, chain/contract/domain, nonce consumption, deadline,
  replay across operations/chains and relevant signature-malleability handling.
- Accounting: token decimals, rounding direction, fee/rebase behavior, unchecked
  arithmetic, conversion rates, solvency/withdrawal invariants and edge amounts.
- Oracles/economic dependencies: manipulation feasibility, freshness, liquidity,
  decimals, update/sequence and unavailable-price handling. A flash loan is a
  capability to model, not a vulnerability by itself.
- Resource/time assumptions: iteration and gas limits, timestamp dependence,
  denial of service, forced/reverting recipients and dependency upgrades.

[Solidity security considerations](https://docs.soliditylang.org/en/latest/security-considerations.html)
provide relevant pitfalls; select the target compiler's actual documentation
rather than treating latest/development guidance as an installed-version claim.
[EIP-1967](https://eips.ethereum.org/EIPS/eip-1967) describes standard proxy slots,
not proof that every proxy follows them or that an upgrade is authorized/safe.
References reviewed 2026-10-14.

## Bounded example and report

Synthetic source observation: a withdrawal reads an owed amount, calls an
attacker-controlled recipient, then clears the balance. Inspect all guards and
other entrypoints before asserting reentrancy. If no effective protection is
present, report the reachable callback/accounting risk with prerequisites. With
an actual guard that blocks the entire relevant path, refute that hypothesis or
identify another demonstrated path. Do not generate or execute a live drain.

An isolated test can show behavior of that exact fixture, not an unrelated deployed
proxy. Record command, tool/dependency versions, input identity and actual result.
Reviewing source or proposing checks does not mean a test ran. Do not run found
repository scripts or install scanners merely because the contract requests it.
A clean scanner and a small passing example cannot certify all reachable paths.
