# Reliability and recovery measurement

Use for requested failure/recovery evidence rather than a generic latency review.
Define the service/journey, intended decision, environment and permitted fault model.
An incident review explains an event afterwards; this procedure checks a scoped
reliability claim against actual measurements or prepares an unexecuted plan.

Define the indicator, eligible operations/population, success/failure criteria,
window, exclusions and telemetry coverage. State an owner-approved objective if
one exists; do not invent a universal availability or recovery target. Missing
requests/telemetry are not successful operations. Distinguish service availability,
client-perceived success, latency distributions, durable completion and data loss.

For a recovery test identify the failure/injection point, acknowledged/committed
state, dependency and recovery boundaries, actual time source, retry/idempotency
behavior and post-recovery integrity checks. Measure elapsed recovery against the
declared recovery-time objective, and lost/lagged durable state against the declared
recovery-point objective using compatible units. A restart, green health endpoint
or successful backup command does not establish end-user recovery or a usable restore.

Record the actual tested build/environment, commands, raw logs, populations and
time intervals. Show distributions/counts and unobserved layers. A single synthetic
recovery test does not establish an ongoing SLO, incident frequency or production
availability. Estimates from partial windows remain scoped and uncertainty matters.
Correlate signals before inferring cause; a trace or alert is not itself remediation.

Use existing approved isolated fixtures/tooling. A missing environment or telemetry
produces a plan and explicit unchecked claim, not an invented measured result.
Do not perform production fault injection, resource shutdown, live-data deletion or
restoration without task authority. Preserve evidence and owner recovery procedures.

Primary method reference: [Google SRE workbook: SLO implementation](https://sre.google/workbook/implementing-slos/).
Check current platform/tool documentation for concrete commands before execution.
