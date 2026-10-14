---
name: systematic-debugging
description: "Reproduce and diagnose a specific software defect, failing test or unexpected behavior, then implement and verify an authorized fix. Use for root-cause investigation and regressions. Do not use for broad codebase audits, incident retrospectives, or CI infrastructure failures without an application defect."
---
# Systematic Debugging

## Objective

Turn a reported failure into a bounded reproduction, an evidence-supported cause and a verified correction.

## Inputs

Required: observed behavior and the intended result or accepted contract. Optional: failing input, environment, recent changes, logs and permission to fix. An investigation request alone does not authorize source changes.

## Context

Read the target's instructions, affected source, callers and tests. Record revision, local edits and relevant runtime/configuration. Use the [investigation guide](references/investigation.md) for intermittent failures, multiple layers or unclear causality. No particular framework, provider or sibling skill is required.

## Procedure

1. Establish expected versus observed behavior and a useful reproduction. Prefer a small local fixture; do not reproduce destructive production behavior or read credentials merely to investigate.
2. Capture the original failure and distinguish baseline problems from regressions. If reproduction is unavailable, state that limit and retain the reported evidence without claiming it was observed.
3. Trace the failing value or state across its owning boundary. Form competing explanations and choose a check that can distinguish them. Change one relevant variable at a time; extra logging must preserve sensitive-data boundaries.
4. Compare a working case or prior revision when useful. Separate the trigger, underlying defect and contributing environment. Do not label the last changed file or a plausible story the root cause without supporting evidence.
5. For an authorized fix, correct the smallest owning cause and preserve unrelated edits and accepted behavior. Add a meaningful regression check when the risk warrants one. Do not patch unrelated symptoms, swallow failures or remove assertions to obtain green output.
6. Repeat the original reproduction and applicable neighboring/project-required checks. Record exact inputs, commands and results; changed environments or skipped checks limit comparison.
7. If the evidence contradicts the hypothesis, revise it. Repeated unsuccessful fixes are a reason to reassess evidence and scope, not permission to widen access or continue arbitrary retries. Escalate an unresolved contract or missing required evidence explicitly.

## Output

Report reproduction status, cause and supporting/counterevidence, changed files if authorized, original-versus-final behavior, actual checks and remaining uncertainty. A proposed fix is distinct from an executed and verified one.

## Completion

The requested investigation is evidence-backed or explicitly unresolved. Any requested fix corrects the demonstrated failure, preserves relevant behavior and has actual verification or a specific reported blocker.
