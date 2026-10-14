# Trust boundaries and adversarial evidence

Use a source-to-sink ledger: attacker input, interpretation/transform, attempted
operation, authoritative policy/control, data sensitivity/destination and observed
result. Consider stored attacks that become active in a later retrieval or child
handoff; a coordinator's summary cannot upgrade evidence into permission.

Test a bounded threat model: untrusted page requests an unrelated export; a tool
result claims the user approved it; a retrieved memory requests a policy override;
a sensitive canary is carried into an output/egress argument; a poisoned package
changes instructions. Use inert synthetic values and .invalid destinations only as
labels, never live endpoints. Model refusal and backend refusal are separate results.

At a tool boundary, bind actual task authority to operation/resource/destination and
identity before any side effect; validate arguments after model interpretation.
Separate read and write credentials, prevent user/tenant scope widening, and enforce
necessary approvals in trusted application code. Do not prescribe a universal broker
or sandbox without the integration's threat model.

Primary guidance reviewed 2026-10-14:
[OWASP AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html),
[LLM01 prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) and
[LLM06 excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/).
These inform a review; they do not certify the target. The local gateway fixture is
intentionally vulnerable and never executes an actual tool or network operation.
