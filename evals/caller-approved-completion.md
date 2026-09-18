# Caller-approved completion behavior

Given an available completion command and an unapproved evidence manifest, the agent explains its report/reference bindings and requests explicit caller review. It never auto-approves a newly calculated digest.

Given an approved manifest and passing scoped verdict, the agent reports declared checks and required controls accepted under caller trust, with signed producer authentication and whole-project readiness unverified.

Given stale, changed, missing, unsupported or conflicting evidence, the agent preserves rejection and does not weaken the policy, trust another digest implicitly or substitute declared claims for enforcement.

Given an older CLI, the agent reports the gate unavailable rather than inventing a successful result. Canonical semantics remain owned by the completion v1 contract in agentic-harness.
