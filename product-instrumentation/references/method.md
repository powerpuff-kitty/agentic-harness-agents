# Tracking contract and QA

## Contract fields

Record event/business meaning, schema revision, trigger and non-triggers, owner,
source, unit, identity scope, event ID, occurrence/ingestion timestamps, required
properties/types/enums, allowed extensions, data classification and retention.
State whether schema evolution is additive, dual-emitted or a breaking rename.
Do not combine revisions silently. A transport success is not semantic correctness.

Consent/collection eligibility and project privacy rules are inputs. Minimize data,
keep direct identifiers out unless specifically needed and approved, and test denied
or revoked collection without assuming a particular jurisdiction's legal standard.
Data sent before a denied-state check cannot be fixed by hiding it in a dashboard.

## Identity and retries

Use stable pseudonymous event/unit IDs with explicit scope. An identity map is a
versioned input with allowed joins, effective times and shared-device/reset behavior.
Never stitch unrelated anonymous sessions by guesswork. Apply deduplication to the
specified event/business key, not all repeated user actions. Legitimate repeated
purchases differ from replaying the same purchase event. Preserve raw counts,
duplicate groups, rejected/late events and transformation versions.

Record at-least-once delivery and pending offline operations separately from durable
business success. Prefer a business-confirmed event when the metric is completed
purchase; a click is not completion. Choose bounded retries/queue expiry and report
loss rather than promising exact delivery without an enforced mechanism.

## QA evidence

Make a decision-to-event matrix and expected payload examples before implementation.
Check types, required fields, value bounds, occurrence/ingestion order, schema drift,
collection eligibility and unexpected sensitive fields. Compare event IDs/counts
across client emission, transport acceptance and warehouse ingestion when authorized
access exists; missing layers stay unverified. Do not log raw sensitive values in
findings. Synthetic test markers are data, not permission or a real identity.

Primary reference: [Amplitude data-planning playbook](https://amplitude.com/docs/data/data-planning-playbook)
(reviewed 2026-10-14). Its vendor-specific APIs are optional; this method does not
install or certify an SDK. The bundled input fixture is synthetic and exercises
payload review, not an actual collector.
