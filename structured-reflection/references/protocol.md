# Optional Harness serialization

For requested `work-reflection` v1, use the exact canonical schema at
[registry/agent-work/reflection.v1.schema.json](https://github.com/powerpuff-kitty/agentic-harness/blob/864e5fde38557217e7e3564b3bf47532fc8b922d/registry/agent-work/reflection.v1.schema.json).
Record supplied work/run/attempt IDs; trigger and evidence/finding refs; status;
observation and unsupported assumptions; causes with evidence and nullable confidence;
corrections with scope and nullable action/next-attempt refs; provider identity with
unknown fields null; resulting action, next attempt, candidate memory and prior
reflection refs; actual created_at. Unknown identity is not a fabricated identifier.
If required input identities are unavailable, return a prose report and serialization
blocker rather than invent a valid-looking protocol object.

Completed requires observed evidence and a proposed correction. Insufficient evidence
or abstention carries no corrections, resulting action or candidate memory. Check
both JSON schema and canonical semantic rules when available. A schema pass does
not prove that evidence exists, an action executed or a correction succeeded.
