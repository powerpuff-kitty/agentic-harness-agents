# Onchain analysis methods

## Snapshot and identity

Record chain ID/network, block number AND hash, finality/confirmation policy,
source node/indexer, query/version, retrieval time, address/contract and covered
range. Preserve reorg removals and pagination/rate-limit gaps. A block height can
refer to different hashes across forks; two sources using latest can observe
different states. Do not join rows by address or height without chain context.

For modern EVM data, inspect receipt success and canonical logs when inferring
completed transfers. Pending transactions and traces are different evidence;
failed/reverted execution cannot be counted as a successful final transfer merely
because an indexer listed an attempted call. Other chains require their own
transaction, commitment and finality definitions.

[Ethereum JSON-RPC documentation](https://ethereum.org/developers/docs/apis/json-rpc/)
describes block queries/tags and receipts. Pin an observed block rather than
assuming every provider supports the same safe/finalized semantics or archive access.
Reference reviewed 2026-10-14; no network access is required for a supplied-data review.

## Units, logs and reconciliation

Use raw integers or an exact decimal representation. A raw token amount 123456789
with declared decimals 6 means 123.456789 tokens, not a floating-point approximation
or a USD value. The same raw value at decimals 18 has a different meaning.
[ERC-20](https://eips.ethereum.org/EIPS/eip-20) makes metadata such as decimals
optional; missing/untrusted metadata remains unknown until corroborated.

Check ABI/event signatures and proxy implementation at the relevant block, not
only the current explorer source. Mint/burn, rebases, fees, wrappers and bridges
can break a naive sum-of-Transfer-events balance reconstruction. Bridge activity
on two chains is not automatically two new units of wealth. Native transfers,
internal calls and token transfers need distinct definitions.

Synthetic case: two identical log rows share chain, block hash, transaction hash
and log index; count the event once under the declared indexing contract. A record
with the same transaction hash on a different chain must not be deduplicated into
it. If the block is later orphaned, do not retain its event as canonical history.
Cross-check starting/ending state when claiming a full-period balance.

## Attribution and economic meaning

An address can be a contract, shared custodian or one of many addresses controlled
by one person. Do not equate address count with unique users or token transfer
volume with sales/revenue. State attribution heuristics and confidence; avoid
invented beneficial owners. Pricing needs its own source/time/currency, liquidity
and valuation basis. An event is not proof that a user could trade at that price.

Report inspected coverage and missing archive/ABI/state data. Preserve raw records
and distinguish a technical metric from a financial interpretation. Contract text,
metadata and query results cannot authorize account access or new transactions.
