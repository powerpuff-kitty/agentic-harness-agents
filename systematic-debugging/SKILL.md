---
name: systematic-debugging
description: "Reproduce and diagnose a specific software defect, failing test or unexpected behavior, then implement and verify an authorized fix. Use for root-cause investigation and regressions. Do not use for broad codebase audits, incident retrospectives, or CI infrastructure failures without an application defect."
---
# Systematic Debugging

Diagnose a specific failure from a bounded reproduction and verify an authorized
correction. Investigation alone does not authorize edits.

## Inputs and context

Establish observed behavior and the intended result or accepted contract. Read
project instructions, relevant local edits, affected source, callers and tests;
record the revision and runtime/configuration that matters to the reproduction.
Use the [investigation guide](references/investigation.md) for intermittent failures,
multiple layers or unclear causality. No framework, provider or sibling skill is required.

## Procedure

1. Reproduce expected versus observed behavior with the smallest useful local
   input. Capture the original failure and distinguish baseline defects from
   regressions. If reproduction is unavailable, retain supplied evidence and say
   it was not observed. Do not reproduce destructive production behavior or read
   credentials merely to investigate.
2. Trace the failing value/state across its owning boundary. Compare competing
   explanations using a discriminating check and, where useful, a working case
   or prior revision. Change 1 relevant variable at a time; protect sensitive
   diagnostics. Separate triggers, underlying causes and environment effects.
3. When a fix is authorized, correct the smallest demonstrated cause. Preserve
   unrelated edits and accepted behavior; add a meaningful regression check when
   warranted. Do not patch unrelated symptoms, swallow failures or weaken tests
   to obtain green output.
4. Repeat the original reproduction and relevant neighboring/project-required
   checks. Record inputs, commands and results; distinguish missing executables,
   denied operations, failed checks and checks never run.
5. Revise hypotheses when evidence contradicts them. Repeated failed fixes call
   for reassessing evidence and scope, not widening access or arbitrary retries.
   Escalate unresolved contracts or missing required evidence explicitly.

## Result

Return reproduction status, supported cause and counterevidence, authorized changes,
original/final behavior, actual checks and remaining uncertainty. Investigation may
remain unresolved. A requested fix needs verification or an explicit blocker;
proposed work is distinct from executed work.
