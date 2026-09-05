---
name: incident-review
description: "Conduct a blameless post-incident review from timelines, logs, alerts, deployments, impact, response actions, and recovery evidence. Use after a reliability, security, or operational incident to establish contributing factors and corrective actions. Do not use for a proactive threat model, standalone performance benchmark, or general code review."
---
# Incident Review

## Objective

Create an evidence-based incident record that explains impact, detection, response, contributing conditions, and durable corrective actions without assigning personal blame.

## Inputs

Required: incident scope and available timeline/evidence. Optional: logs, alerts, deploy history, tickets, user impact, metrics, communications, and existing runbooks.

## Context

Read operations/observability/security architecture relevant to the incident and the concrete evidence generated during the event. Treat chat recollections as lower-confidence than timestamped system evidence.

## Procedure

1. Establish start/end, affected services/users, severity, and confirmed impact.
2. Reconstruct a timestamped timeline from evidence and label uncertain entries.
3. Separate trigger, contributing conditions, detection gaps, response friction, and recovery actions.
4. Identify why safeguards, tests, alerts, rollback, or operational procedures did not prevent or shorten the incident.
5. Propose corrective actions with owners/categories, priority, and verification—not vague lessons.
6. Distinguish immediate remediation from systemic prevention.
7. Update durable runbooks/architecture/security truth only when accepted follow-up changes it.

## Output

Return summary, impact, timeline, contributing factors, what worked, what failed, corrective actions, evidence/confidence, and unresolved questions.

## Completion

The timeline is evidence-backed, causality is not overstated, actions are verifiable and prioritized, and sensitive incident data is handled according to project policy.
