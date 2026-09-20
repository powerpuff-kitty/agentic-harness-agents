# Optional lossless log compaction

P0 agents #43/#36: a concrete skill-local helper, not another model, Harness CLI feature or logging agent. The agentic-improvement entrypoint/trigger is unchanged. Its conditional guide introduces `scripts/compact_log.py` only for approved, already-reviewed logs. Manual handling remains available without Python.

## Algorithm and limits

The Python-standard-library helper reads one explicitly named UTF-8 file, bounded to 1 MiB, and forms runs of adjacent identical lines. It preserves every line ending, occurrence, rare failure and ordering boundary. It does not strip timestamps or identifiers, merge nonadjacent failures, redact data, interpret instructions, infer execution status, invoke a provider or write files. A SHA-256/byte-count round trip is checked before stdout. The literal representation wins when run-length encoding would be larger; envelope overhead can still make the output larger than the source.

The complete JSON output includes source reference/identity, payload and byte accounting. `supplied_bytes_complete` applies only to the file given to the helper. An already truncated producer stream remains of unknown completeness; no successful process exit is inferred. Advisory budget overflow returns all evidence with exit 1 rather than truncating it. Exit 0 is helper success, never project-test success. Exit 2 is invalid input, with fixed diagnostics that omit rejected paths/content.

Logs and source references may be sensitive. Review/redact them before invoking the helper or sharing output. Hashes are not author signatures; a trusted quiescent filesystem is assumed. No secret scanning, sandbox or producer authentication is claimed. A record is a display representation, not a canonical completion artifact.

## Actual local synthetic measurements

The retained JSON records an actual subprocess invocation for each deterministic fixture. Source recipes and exact-byte checks are in `test_compact_log.py`. Output sizes include the entire JSON envelope and final newline.

| Fixture | Source bytes | Output bytes | Encoding |
| --- | ---: | ---: | --- |
| Repeated worker polling with a rare permission failure and a later retry | 152,105 | 739 | Adjacent-line runs |
| 100 distinct diagnostics followed by a failure | 5,103 | 5,737 | Literal |

Both returned helper exit 0 and round-trip to their exact input bytes. This is an intentionally repetitive positive fixture plus a negative case, not a representative production benchmark. No provider tokenizer, end-to-end agent trial, billing saving or model-quality improvement was measured. Additional helper/tool invocation and guide-loading overhead remains outside these byte measurements.

## Validation and distribution

Run `python3 -m unittest discover -s .github/scripts -p test_compact_log.py` and the existing `validate_agents.py`. The helper tests exercise actual stdout, error exits, no-write behaviour, limits, links, corrupt counts/hashes, Unicode/line endings and seeded random round trips. The optional-script bundle tests separately exercise v1 archive byte compatibility, v2 declarations, sealed verification after source removal and the actual collection packager. Packaging never executes bundled scripts; tests deliberately invoke only the reviewed helper on synthetic data.

The bundle declaration changes to v2 to explicitly list this optional Python script, manual fallback and no-auto-run boundary. v1 remains documentation-only. A bundle digest proves internal byte consistency, not safety or permission to execute. Both full/progressive preparation modes keep the helper bytes available but explicitly prohibit executing helpers in those read-only synthetic review trials. No model run or existing installation update is implied by preparing or packaging files.
