# Selecting useful verification

Use one clear assertion boundary per behavior claim. Test different failure modes,
not every private implementation step. A cart calculation may need empty, repeated,
rounding and invalid-input cases; an API integration additionally needs serialization,
authorization/error mapping and rollback behavior when those are accepted requirements.

Prefer actual local boundaries for integration tests. A mock that returns the exact
value asserted cannot establish that 2 real components agree. External services
may require recorded/synthetic fixtures or stubs; record which behavior they cannot
verify. Never use a production account or send real messages merely to test a flow.

For browser journeys, start from a known state, use stable semantic selectors, wait
for the required observable condition and assert the final user-visible outcome.
Choose relevant viewport, keyboard and state checks from the change. Inspect console
or network evidence when useful, with sensitive values excluded. Do not assume every
application reaches network-idle or that a fixed delay guarantees rendering.

For flakiness, preserve a failing trace and separate product races from fixture,
ordering, teardown and resource-leak problems. Repeated runs measure uncertainty;
they do not turn an unexplained failure into a pass. Quarantine is an explicit
project decision with a tracked defect and honest gate status.

Mutation thinking can expose weak tests without adding a new tool: would an empty
result, inverted condition or missing side effect still pass? Add a stronger
behavioral assertion when needed. Do not require a mutation framework or a universal
coverage target for ordinary test work.
