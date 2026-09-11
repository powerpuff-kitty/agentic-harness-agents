# Architecture

Root `skills/`, `prompts/`, `adapters/`, `references/`, and `evals/` are versioned distributable content. `manifest.json` indexes skills. The canonical static repository owns the project contract; the CLI pins this repository and installs selected skills under target `.agents/skills/`.

Procedures share source-resolution, discovery, precedence, and safety references. Vendor adapters contain only integration guidance and never canonical architecture.

Authored procedures, prompts, adapters, references and evals use the root MIT
[LICENSE](../LICENSE). Canonical licensing scope and generated-project attribution
are defined by `agentic-harness` ADR-007. When copying substantial skill content,
retain the MIT notice; third-party material retains its existing terms.
