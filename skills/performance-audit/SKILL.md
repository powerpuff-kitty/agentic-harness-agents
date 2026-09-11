---
name: performance-audit
description: "Measure and diagnose performance bottlenecks in application, API, database, build, or runtime paths using profiling, tracing, benchmarks, metrics, and repository evidence. Use when latency, throughput, resource use, query cost, bundle/build speed, or performance regressions are explicitly requested. Do not use for generic code quality or incident review without a performance focus."
---
# Performance Audit

## Objective

Identify measurable bottlenecks, quantify impact, and recommend changes whose expected benefit can be verified.

## Inputs

Required: target repository/system and performance concern. Optional: baseline metrics, SLOs, workload, production traces, profiler output, benchmark command, environment, and regression window.

## Context

Read performance/operations architecture relevant to the measured path, source called out by traces/profiles, and datastore/API details implicated by evidence. Avoid speculative full-code scans.

## Procedure

1. Define the metric, workload, environment, and target threshold before optimization.
2. Reproduce or collect a baseline with representative measurements when possible.
3. Use profiling/tracing/query plans/bundle analysis to localize cost.
4. Separate CPU, I/O, memory, network, database, serialization, caching, contention, and build/tooling causes.
5. Rank candidate fixes by measured contribution and implementation risk.
6. Apply changes only when requested/authorized, one causal group at a time.
7. Re-measure under equivalent conditions and report variance/caveats.

## Output

Return baseline, bottleneck evidence, root-cause confidence, prioritized fixes, before/after measurements when applied, and environment/measurement caveats.

## Completion

Claims are tied to measurements or explicitly labeled hypotheses, regressions were checked, and improvements are demonstrated under comparable conditions.
