# Inspecting Codex usage without double-counting

This optional repository tool addresses #68 under P0 #26, supporting #36 and #32.
It consumes an explicitly selected, reviewed `codex exec --json` JSONL capture.
It does not start Codex, install a CLI, read credentials, fetch URLs or run commands.
No production skill, host adapter, canonical contract or per-call evaluator changes.

## Why snapshots are not a per-call ledger

The reviewed producer is **openai/codex at
`5e5cadad6b90f90a999cbc49745a91c61bc0cdbf`**. Its
`usage_from_last_total` serializes `usage.total` into `turn.completed` and returns
default zero counters when producer usage is absent. The SDK's comments describe
usage during a turn, but the implementation means this inspector must preserve
cumulative thread snapshots, not sum terminal events as independent model calls.
A resumed stream can include earlier thread usage even though its first event is
`thread.started`. That event does not establish a fresh zero-accounted session.

Primary sources reviewed on 2026-09-20:

- [Official non-interactive JSONL documentation](https://developers.openai.com/codex/noninteractive/).
- [Pinned JSONL producer, including usage_from_last_total](https://github.com/openai/codex/blob/5e5cadad6b90f90a999cbc49745a91c61bc0cdbf/codex-rs/exec/src/event_processor_with_jsonl_output.rs).
- [Pinned SDK event definitions](https://github.com/openai/codex/blob/5e5cadad6b90f90a999cbc49745a91c61bc0cdbf/sdk/typescript/src/events.ts).
- [OpenAI token-accounting explanation](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them).

The `producer_profile` identifies the implementation reviewed for this inspector,
**not the version that produced an arbitrary supplied file**. Its verified flag
is always false. Independently retain the actual host version and compatibility
review; do not assume all versions have the same counter semantics.

## Invocation

Review the trace and its destination first. Retain a hash from that review, rather
than recomputing a replacement pin to make modified evidence pass. This command
reads one named file and prints a summary; it writes no trace or project files.

```bash
python3 .github/scripts/codex_usage.py /reviewed/path/trace.jsonl \
  --expected-sha256 "$REVIEWED_TRACE_SHA256" \
  --evidence-kind recorded-session
```

The pin uses `sha256:` followed by 64 lowercase hexadecimal characters. The API is:

```python
report = codex_usage.inspect_trace(
    reviewed_bytes,
    expected_sha256=reviewed_trace_sha256,
    evidence_kind="recorded-session",
)
```

The byte-only API never acquires files. The file wrapper rejects observed symlinks,
reparse points, nonregular files, parent traversal and changed/oversized inputs.
Use a trusted, quiescent filesystem with actual non-symlink ancestor paths; this
is not a sandbox against hostile concurrent directory replacement. Missing paths
and invalid input produce fixed diagnostics without rejected content or paths.

Input bounds: 4 MiB, 256 KiB per event, 16,384 events, 128 turns, bounded JSON
structure and counters up to 10^12. Unknown event envelopes and unknown usage
fields fail rather than silently guessing future protocol meanings. Item bodies
are opaque except for item identities/types and recorded command status/exit.
This is a supported-event inspector, not full validation of every Codex item.

## What the report means

Each usage snapshot has an event-line reference, turn number and the counters
exactly reported by the producer. Optional absent details remain null. Cached
input, reasoning output and cache-write input are retained as details, not added
again to `input_tokens + output_tokens`. The inspector neither estimates tokens
from character count nor calculates prices.

`last_snapshot_input_plus_output` is arithmetic on the **last known snapshot**,
not whole-task use, per-turn use or a sum of snapshots. It remains null when no
usable counters exist, when counters decrease, or when both base counters are
zero and therefore indistinguishable from the producer's missing-usage default.
Earlier snapshots stay visible. A missing intermediate counter does not hide a
later decrease relative to the last known value. Never silently switch to
per-turn semantics or calculate reset-adjusted deltas after a decrease.

Failed/open turns, missing usage, unterminated tails, stream errors, unfinished
items and recorded command failures remain visible. A later successful command
cannot erase an earlier failed attempt. A failure after the last known snapshot
can incur unreported costs; the inspector does not invent those costs or report
unknown usage as zero. MCP/collaboration events carry an external-accounting flag.
No absence of those events proves that all model/provider work was accounted for.

Only typed counters, statuses, hashes and source event positions are emitted.
Commands, outputs, agent/reasoning messages, error text and raw thread/item IDs
are not replayed. This is minimization, **not a secret scanner or anonymizer**:
review even hashed identities and metadata before disclosure. Keep the original
reviewed capture accessible through a separate actual evidence reference.

Exit 0 means a supported sequence with a nonzero terminal snapshot and no reported
inspection concern. Exit 1 retains available observations but flags incomplete,
failed, ambiguous or externally accounted work. Exit 2 rejects invalid, changed,
oversized or unsupported input without a partial report. None certifies task
success, source authenticity, invocation approval, billing or token savings.
`terminal_sequence_observed` concerns turn boundaries and final-newline presence
only; it does not certify capture completeness, item completion or process exit.

## Relationship to paired and repeated trials

[Repeated guidance trials](repeated-guidance-trials.md) still require actual
per-call accounting and matched task/host/source/check identities. This report
is deliberately **not** `guidance-trial-record` v1 and cannot be passed to its
comparator as a trial. It never invents call IDs or sets `usage.complete`.

Use inspected snapshots as supporting accounting evidence. Obtain an independently
reviewed per-call ledger and task-scoped starting boundary before populating trial
usage; include retries, failed/auxiliary work and instruction-loading costs.
Without that evidence, keep usage unavailable and the planned repetition visible.
Do not turn the last cumulative counter into a fabricated single model call.
Model identity, genuine execution, task acceptance, producer/capture authenticity
and whole-task usage remain unverified, even with `recorded-session` selected.
A caller can fabricate both a trace and its pin; hashes establish agreement only.

## Reproducible synthetic counterexample

```bash
python3 .github/scripts/codex_usage.py \
  evals/fixtures/codex-usage/cumulative.jsonl \
  --expected-sha256 "$(cat evals/fixtures/codex-usage/cumulative.sha256)" \
  --evidence-kind synthetic
```

The first snapshot declares 1,000 input and 100 output tokens. The second declares
1,500 input and 140 output. The last reported total is **1,640**, not 2,740 from
adding both snapshots, and not 2,790 from adding cached/reasoning/cache-write details again.
The trace also retains a failed command before a successful attempt, so the command
intentionally exits **1**. These counts and events are authored synthetic fixtures,
not captured real-model evidence, a live-host test or a savings benchmark.

Run `python3 .github/scripts/test_codex_usage.py`. Existing repository validation
runs these tests alongside the unchanged pair/series evaluators. Tests cover
exact hashes, counter semantics, failures, unsupported/malformed input, bounds,
redacted output, no acquisition in the API and actual file-based execution.
