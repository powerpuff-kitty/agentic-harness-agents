---
name: code-quality
description: "Inspect and improve repository formatting, linting, type-safety, complexity, duplication, dead-code and convention drift from deterministic tool/config evidence. Use when the request is specifically about code readability/maintainability quality gates or fixing their findings. Do not use for broad repository health audits, architecture-only reviews, security reviews, or performance profiling."
---
# Code Quality

## Objective

Assess and improve code readability, consistency and maintainability using the target project's accepted quality contract, native tool configuration and reproducible source evidence. Preserve the distinction between configuration discovery, static analysis and checks that were actually executed.

## Inputs

Required: target repository and the requested quality scope. Optional: changed revision/range, accepted project quality contract, baseline artifact, lint/format/typecheck output, CI evidence, and authorization to execute checks or apply fixes.

## Context

Start with the target's `AGENTS.md` and project-selected architecture/quality context. Detect the languages and existing formatter/linter/typechecker configuration before proposing tooling. When an installed compatible `ah` exists, `ah quality detect` and `ah quality analyze` may provide read-only evidence. Load language/tool guidance only for ecosystems present in scope.

Project-native conventions outrank generic preferences. Tool presence does not prove execution, and a missing tool does not authorize installing it. Keep architecture dependency rules separate from quality rules while reusing accepted architecture evidence when import/dependency hygiene is in scope.

## Procedure

1. Establish the reviewed revision/range, languages, generated/vendor exclusions, accepted quality authority and whether execution or writes are authorized.
2. Detect existing formatters, linters, typecheckers, package/workspace scripts, EditorConfig and language-specific configuration. Record discovered commands with `executed: false` until they actually run.
3. Inspect deterministic static evidence first: explicit compiler/type-safety posture, suppressed diagnostics, formatting/lint configuration, import hygiene and project-selected thresholds. Unsupported parser/config semantics remain `not_checked`.
4. For complexity, duplication, dead-code, naming and documentation findings, require a reproducible analyzer/tool result or an accepted project rule plus exact source evidence. Do not turn personal style preferences into violations.
5. Execute only explicitly authorized project-native checks. Record command, working directory, tool/version, exit status and scope. Do not install tools or silently substitute another formatter/linter.
6. Prioritize fixes by correctness and architectural risk before cosmetic churn. Prefer the smallest change that removes the finding while preserving behavior and accepted conventions.
7. Apply autofix only when authorized and bounded to the requested scope. Review the resulting diff; a formatter's ability to rewrite code is not approval to rewrite unrelated files.
8. For legacy debt, preserve the current finding inventory. If a project baseline/ratchet exists, prevent new/increased findings without describing historical debt as clean. Never regenerate a baseline merely to make a regression disappear.
9. Re-run the same relevant checks after a fix when execution is authorized. Report remaining failures, blocked checks and unsupported coverage separately.

## Output

Return repository/revision identity, detected languages and quality tooling, accepted authorities, performed and unperformed checks, and findings with stable Harness rule ID plus native diagnostic code when available. For each finding include category, severity, exact evidence, enforceability/confidence, smallest remediation and verification needed.

When implementation was requested, summarize changed files and the exact validation that ran. Keep `pass`, `blocked`, `not_checked` and `unsupported` distinct. Do not manufacture a blended quality score when the deterministic measurements do not support one.

## Completion

The result makes clear what was detected versus executed, does not replace project conventions with generic preferences, and does not claim unmeasured quality. Any applied fix is bounded, reviewed against the requested scope and followed by the strongest authorized verification available. Legacy baselines remain visible and cannot be refreshed to hide newly introduced debt.
