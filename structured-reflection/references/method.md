# Evidence and stopping

Use completed when evidence supports an observed failure/risk and an actionable
correction; use insufficient_evidence when the cited finding cannot be inspected;
use abstained when no useful correction is justified. Do not fill a template with
invented causes merely to avoid an empty section.

A correction names a reachable target and a check that could disprove success.
Examples include rerunning the original failed boundary test plus neighboring
valid inputs, checking a forbidden dependency edge after refactoring, or obtaining
missing source evidence before a security conclusion. Retry only within the task's
authority and declared attempt/cost bound; the same unexamined failure is a reason
to change the hypothesis or report the blocker, not loop indefinitely.

Retain the failure and later fix as separate snapshots. A follow-up reflection
references its predecessor and new evidence; it does not replace history. Confidence
may remain unknown. Never fabricate a calibrated probability from narrative certainty.

The fixture provides synthetic attempt/evidence identities, not an executed test.
A report can interpret those supplied records; actual implementation/testing needs
an executable target and must remain separately identified.
