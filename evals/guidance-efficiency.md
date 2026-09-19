# Guidance efficiency evaluations

`guidance-efficiency.json` contains synthetic prompts and source evidence, not completed model runs. It covers bounded decisions, absent/contradictory evidence, native checks, provider absence, untrusted instructions, mandatory context, changed working trees, truncated logs, explicit provider permission, unknown usage and independent authorisation.

`guidance_eval.py` checks explicitly supplied observation fields against a case. It validates referenced fixture-source digests and checks recorded route/outcome, provider budget, unsupported confidence, policy promotion and unobserved verification. It cannot authenticate a trace, prove that content was really read, interpret arbitrary prose, establish factual/model correctness or enforce a host policy. Case IDs and digests are evaluator-local, not Decision Kernel receipts.

The test suite constructs synthetic observations to test the grader, then mutates them to ensure that missing fields, required-evidence removal, source drift and unsafe claims fail. These tests do not execute a coding agent or Jev and must not be reported as a model pass rate. Entry-point size checks are byte-budget regressions, not token savings.

For a real trial, preserve the exact task/source/skill revisions, host/model identity when known, permissions, raw redacted trace, tool outcomes and grading rationale. Derive observation fields from that trace, retain the trace reference, and mark unavailable measurements unknown. Evaluate the same starting task/rules/checks under baseline and selected guidance, repeat trials and retain failures. Use independently reviewed outcome labels for semantic cases. Hosted inference is a separate explicit opt-in; an absent provider is not a passing live test.

Submitted-token accounting sums input/output per actual model call, including retries and auxiliary providers. Tool content already included in input is not counted twice. That sum is not a cost estimate: cached-input pricing and provider billing need separate evidence. The helper cannot detect an omitted call, so completeness must come from the retained trace.

Run the local grader regression tests with `python3 -m unittest discover -s .github/scripts -p test_guidance_efficiency.py`. They also run through the existing `validate_agents.py` entrypoint. No CLI or model credentials are required.
