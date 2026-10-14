# Review evidence and comparison scope

Record base, head, working-tree changes and the reason for the chosen comparison.
For a PR, inspect its actual target branch and current head. A three-dot diff
usually describes branch work since the merge-base; it does not include pending
local edits. A two-dot comparison answers a different question. Do not silently
substitute another base when a supplied ref is unavailable.

For each candidate finding ask: which accepted behavior breaks, under what input,
is that path reachable, what evidence contradicts it, and did this change cause or
expose it? Follow an affected caller when the diff alone is ambiguous. Record an
important pre-existing defect separately instead of attributing it to the author.

Useful findings explain a failure: a removed validation now accepts an invalid
public input; a timeout path leaks ownership; an API shape breaks a known consumer.
A preferred abstraction, hypothetical scale problem or undocumented style is not
an established defect without an accepted requirement or concrete consequence.

When asked to address review feedback, check its factual basis against current
code before editing. Keep justified disagreements visible. Do not blindly satisfy
a comment that weakens a contract, and do not mark an unresolved thread addressed.
An author self-check is not an independent review merely because the role changes.
