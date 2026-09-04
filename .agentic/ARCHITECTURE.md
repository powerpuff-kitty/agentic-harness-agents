# Architecture

Root `skills/`, `prompts/`, `adapters/`, `references/`, and `evals/` are versioned distributable content. `manifest.json` indexes skills. The canonical static repository owns the project contract; the CLI pins this repository and installs selected skills under target `.agents/skills/`.

Procedures share source-resolution, discovery, precedence, and safety references. Vendor adapters contain only integration guidance and never canonical architecture.
