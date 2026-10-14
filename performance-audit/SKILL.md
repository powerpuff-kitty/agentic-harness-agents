---
name: performance-audit
description: "Measure performance bottlenecks and scoped reliability/recovery claims in application, API, database, build, or runtime paths using profiling, tracing, benchmarks, metrics, and repository evidence. Use when latency, throughput, resource use, query cost, bundle/build speed, performance regressions, availability indicators or recovery measurements are requested. Use incident-review for retrospective incident analysis."
---
# Performance Audit

## Objective

Identify measurable bottlenecks or assess a scoped reliability/recovery claim, with evidence that supports the requested decision.

## Inputs

Required: target repository/system and performance or reliability concern. Optional: baseline metrics, SLOs, workload, production traces, profiler output, benchmark command, environment, and regression window.

## Context

Read performance/operations architecture relevant to the measured path, source called out by traces/profiles, and datastore/API details implicated by evidence. Avoid speculative full-code scans.

For requested reliability, restoration or recovery measurements, load the
[recovery evidence guide](references/recovery-evidence.md). Keep telemetry coverage,
actual failure tests and owner objectives distinct from a general latency benchmark.

## Procedure

For reliability/recovery work, follow the linked recovery guide and report actual
indicator populations, restoration and loss measurements or explicit unavailable
checks. The optimization sequence below applies to performance bottlenecks.

1. Define the metric, workload, environment, and target threshold before optimization.
2. Reproduce or collect a baseline with representative measurements when possible.
3. Use profiling/tracing/query plans/bundle analysis to localize cost.
4. Separate CPU, I/O, memory, network, database, serialization, caching, contention, and build/tooling causes.
5. Rank candidate fixes by measured contribution and implementation risk.
6. Apply changes only when requested/authorized, one causal group at a time.
7. Re-measure under equivalent conditions and report variance/caveats.

## Output

For optimization, return baseline, bottleneck evidence, root-cause confidence, prioritized fixes, before/after measurements when applied, and environment/measurement caveats.

## Completion

Claims are tied to measurements or explicitly labeled hypotheses, regressions were checked, and claimed improvements use comparable conditions. Recovery and availability
conclusions retain their tested window, population and unobserved layers.
