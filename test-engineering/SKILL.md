---
name: test-engineering
description: "Design, add or improve meaningful unit, integration and end-to-end tests for accepted software behavior; diagnose flaky or misleading tests. Use for test strategy, regression coverage and test-first development when requested. Do not use for broad quality scoring, accessibility-only audits, or CI runner and permission diagnosis."
---
# Test Engineering

## Objective

Provide proportionate, reproducible evidence for behavior that matters, with tests that survive legitimate implementation changes.

## Inputs

Required: behavior, change or test problem and the repository. Optional: acceptance criteria, supported environments, known failures and test-first preference. Distinguish test review from permission to edit tests or implementation.

## Context

Read project-required checks, existing test conventions, public interfaces and the affected implementation. Load the [test-design guide](references/test-design.md) for boundary selection, browser coverage or flakiness. Load [browser and recovery evidence](references/browser-recovery.md) for visual baselines, browser-state matrices or failure restoration. For requested independent audits/test reviews or consequential verification gaps, use the [fresh-session review method](references/fresh-review.md) when delegation is available and authorized. Use existing trusted tooling; a missing runner is not automatic installation permission.

## Procedure

1. Identify accepted behavior, meaningful failure modes and relevant boundaries. Map each important risk to an observable result; do not derive requirements from the current implementation or a coverage percentage.
2. Choose the cheapest reliable level that can establish the claim: a pure unit test for local logic, an integration test for a real boundary, or a browser/system test for a user journey. Keep required project gates even when adding focused checks.
3. Record the current baseline and environment. When fixing a demonstrated defect, establish that the regression case fails for the relevant reason before the fix when feasible. Use a test-first loop when requested or helpful; do not mandate it for unrelated reversible edits.
4. Use representative inputs, boundaries and failure paths. Assert public behavior and important side effects; avoid assertions that merely mirror internal calls or repeat the algorithm. Mock only the boundary whose real dependency is outside the test's intended scope.
5. Make timing, randomness, locale, filesystem and network assumptions explicit. Prefer isolated fixtures, controlled clocks and condition-based waits. Preserve failures when diagnosing flaky tests; retries, skipped assertions or longer sleeps do not establish correctness.
6. Run the relevant test through the actual supported runner, then applicable regression/project checks. For browser work, observe rendered behavior, exercise relevant states and retain useful screenshots or traces without private data. A screenshot alone does not prove the journey passed.
7. For an independent pass, use a separate reviewer session without inherited author conversation. Supply accepted requirements, project rules and raw snapshot evidence, not the author’s conclusions or expected findings. Record actual isolation support; if unavailable, label the missing independent perspective. Reproduce and triage findings before accepting them, then recheck changed source.
8. Review whether a plausible broken implementation would fail the test. Report untested platforms, environment limitations and baseline failures separately. Remove redundant tests only when authorized and their important behavioral coverage is retained.

## Output

Give the behavior/risk matrix, tests changed, actual commands and environment, results, flaky/baseline findings and remaining coverage gaps. For a delegated review, retain the brief, source identity, actual context-isolation mode, original report and finding dispositions; a fresh reviewer does not establish exhaustive coverage. A discovered test, fixture or test plan is not an executed result.

## Completion

Requested tests or review are delivered at an appropriate level, assertions establish the intended behavior, and execution evidence or specific unavailable checks are reported without overstating coverage.
