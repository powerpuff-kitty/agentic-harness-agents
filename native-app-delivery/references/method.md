# App lifecycle and evidence

Map accepted journeys to launch/resume, termination/recreation, background policy,
permission state, link/navigation entry and connectivity. OS scheduling and process
lifetime are not application-controlled promises. Define what survives process loss,
what is reconstructed from authoritative data and how an unfinished operation is
identified. Test an ambiguous network response separately from an explicit failure.

For offline writes, define durable intent, operation IDs, ownership, retry bounds,
server/business deduplication where it exists, conflict policy and a visible pending/
failed state. A process-local queue cannot establish durable recovery; a retry may
repeat a business action unless the actual accepting boundary enforces idempotency.
Do not invent a backend guarantee while reviewing a client. If offline writes are
out of scope, preserve safe state and clearly explain unavailable actions instead.

Keep layer evidence separate: source inspection; unit/contract tests; UI tests on a
named simulator/emulator; real hardware checks; archive/signing/packaging; beta/store
processing; production behavior. A tool exit must correspond to the selected target,
configuration and revision. No SDK installed means no claimed build. Cross-platform
framework tests do not establish every native permission/lifecycle integration.

Include text scaling, native screen-reader/focus behavior, keyboard/touch alternatives,
orientation/window changes, themes and locale when applicable. Use actual platform
profiling for startup/jank/memory/network/battery claims. Respect device/user data,
permissions and approved tools. Use synthetic or explicitly approved accounts.
The bundled fixture is a scenario description, not runnable app code or a device test.
