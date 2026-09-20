# Paired skill-guidance observations

This optional evaluation helper supports agents #26/#36. It is not a new Decision Kernel contract, Harness runtime or required per-task report. Ordinary skill use does not need Python, stored transcripts, a CLI or TypeSafe credentials.

## Reproducible comparisons

Choose a case from `guidance-efficiency.json` and freeze a specification containing exactly `case` and `required_checks` (a nonempty array of check IDs). Define checks before inspecting the candidate outcome. A fixture validates grading machinery; it is not a completed agent trial.

Use a fresh/reset starting project for each treatment. Keep task/source bytes (including uncommitted changes), accepted rules, check implementations, host/model version and settings identical. Record the treatment name and exact instruction-content digest separately: baseline guidance versus selected skill guidance is the intended changed variable. Include all loaded instructions and reference expansion in usage, not just the final prompt. A prior conversation or exposure to expected answers is a confound, not a clean baseline.

Collect raw, appropriately redacted traces and independently reviewed outcome labels. Do not export private transcripts or provider data without approval. Derive the existing `guidance_eval.py` observation fields from the trace rather than constructing them from expected answers. Include every required check and any additional observed failure. A missing tool or log is unverified, not passed.

## Evaluation-local record

Each `guidance-trial-record` has format_version 1 and these fields:

| Field | Meaning |
| --- | --- |
| `evidence_kind` | `synthetic` for grader exercises; `recorded-session` only for an actual observed session. Never mix the two. |
| `spec_digest` | `guidance_comparison.fingerprint(spec)` binds the exact case and required checks. |
| `identity` | `source_snapshot`, `policy_snapshot`, `checks_snapshot`, `settings_snapshot` are SHA-256 identities; `host` and `model` are exact observed version identifiers. Unknown values are null. |
| `treatment` | `{name, sha256}` identifies the actual supplied guidance. Do not fabricate a digest for guidance that was not captured. |
| `observation` | Existing evaluator-local fields described in `guidance-efficiency.md`. These are not provider receipts. |
| `checks` | Check-ID mapping to `{status, evidence}`. Status is `passed`, `failed`, `not-run` or `unsupported`. Evidence is `{reference, sha256}` or null. |
| `trace` | `{reference, sha256}` for the redacted observation trace, or null. Required for recorded sessions. |
| `usage` | `{complete, basis, evidence, calls}`. Basis is `observed-submitted-tokens` or `unknown`; calls have unique IDs and observed input/output token counts or null. |

Hash snapshots with a documented deterministic manifest of exact path/content identities, not HEAD alone. Use SHA-256 of exact captured bytes for trace, check, usage and treatment references. The helper compares these identities but does not retrieve references or verify external byte content. Reference strings cannot cause file reads, network calls or command execution.

## Run and interpret

```sh
python3 .github/scripts/guidance_comparison.py spec.json baseline.json candidate.json
python3 -m unittest discover -s .github/scripts -p test_guidance_comparison.py
```

The three named JSON inputs are bounded to 1 MiB each. Duplicate keys, non-finite numbers, malformed shapes and directly symlinked inputs are rejected. This is a local evaluator, not hostile-filesystem isolation.

Exit 0 means lower submitted-token arithmetic under matching supplied identities and passing supplied acceptance evidence. Exit 1 means incomparable identity, unverified acceptance, unavailable usage, or no reduction. Exit 2 means malformed/unsupported input. All outputs retain `scope: supplied-record-fields`, `trace_authenticated: false`, `model_execution: not-performed` and `optimisation_verified: false`. A result is not an authorisation or empirical verification claim.

Input/output are counted once per model call, including retries and auxiliary providers. Tool-result text already in input is not counted again. A caller must attest complete accounting against the trace; the helper cannot detect a fabricated record, omitted call, stale check falsely labelled current, or an inaccessible reference. Source-byte estimates and cache pricing are not observed submitted tokens. Missing usage never becomes zero or a saving.

Repeated, representative, independently reviewed trials are still needed to assess task success, variance and actual model behaviour. This helper compares one matched pair; it does not aggregate pass rates, authenticate traces, enforce hosts, run Jev or establish billed cost savings. Its synthetic regression fixtures deliberately include passing flags and plausible references to demonstrate that arithmetic output remains non-authenticated.
