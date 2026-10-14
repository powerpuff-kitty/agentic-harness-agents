# Code quality decision guide

Use these scenarios to preserve evidence boundaries. They are examples of decisions, not universal project rules.

## TypeScript

A repository has `eslint.config.js`, Prettier configuration and `tsconfig.json` with `"strict": false`.

- Detection may report ESLint, Prettier and TypeScript as present.
- Static analysis may report the explicit strict-mode setting when the accepted Quality Registry profile applies.
- None of the formatter/linter/typechecker commands has run merely because its config exists.
- Do not switch `strict` on as a cosmetic fix. For a legacy codebase, first establish project policy and the expected migration impact.

If `tsconfig.json` is JSONC, extends another config, or expresses strictness through individual compiler flags and the analyzer cannot resolve that combination, report the effective posture as `not_checked` or `unsupported`.

## Rust

A repository contains `Cargo.toml`, `rustfmt.toml` and `clippy.toml`.

- Configuration proves rustfmt/Clippy intent, not that `cargo fmt -- --check` or `cargo clippy` passed.
- When execution is authorized, record the exact toolchain/version, workspace scope, command and exit status.
- Preserve native Clippy lint names/levels when normalizing findings.
- Do not broadly apply `cargo clippy --fix` unless the requested scope explicitly authorizes writes and the resulting diff is reviewed.

## Partial or unsupported ecosystems

A repository contains Kotlin plus an unfamiliar formatter configuration while the installed analyzer only understands JavaScript/TypeScript and Rust quality semantics.

- Inventory the language/config files that can be established safely.
- Do not infer a clean quality pass from the absence of supported findings.
- Mark formatter/linter/type/complexity coverage for Kotlin as unsupported or not checked.
- Use project-authoritative commands only after explicit execution authorization; do not install a guessed Kotlin quality stack.

## Legacy baseline

A stored baseline has 200 lint findings and the current change has 201.

- The historical 200 remain visible debt.
- The new/increased finding is a regression if the accepted ratchet policy says counts may not increase.
- Do not regenerate the baseline to 201 and call the change clean.
- If configuration/tool versions changed materially, treat the old baseline as stale until reconciled.

## Autofix

A formatter can rewrite 40 files while the request only changes one service.

- Preview or constrain the fix to the requested scope where the native tool supports it.
- Formatting capability is not authorization for broad writes.
- Re-run the relevant check after the approved fix and report unrelated existing drift separately.
