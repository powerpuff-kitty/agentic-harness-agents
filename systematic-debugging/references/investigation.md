# Choosing the next debugging check

A useful hypothesis predicts an observation that competing explanations do not.
For a wrong total, compare the raw records, transformation and display separately;
changing rounding and filtering together prevents knowing which caused the error.
For a stale result, inspect ownership, cache keys, invalidation and out-of-order
completion before introducing a delay.

For intermittent failures, retain frequency, exact environment and failing inputs.
Use deterministic synchronization or an injected clock when the project supports
it. A passing retry is not a fix. Cancellation, timeout, ordering and resource
ownership can require a multi-layer reproduction; minimize only while preserving
the trigger. Instrument narrowly and remove incidental diagnostics after use.

When a reproduction would require unavailable/private infrastructure, work from
approved logs or a synthetic case, distinguish inference from observation and name
the missing verification. Never change production state to make a local hypothesis
convenient to test.

Examples of useful boundaries:

- A timezone boundary has a failing input, an accepted timezone contract and a
  test spanning that boundary; it does not justify changing all stored dates.
- A configuration-only failure is diagnosed against the actual environment;
  changing application logic without establishing a code defect is premature.
- A recent change is a candidate cause, not proof. A baseline reproduction can
  establish that a defect predates it while keeping the current failure visible.
