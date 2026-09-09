# Architecture

This repository is the procedure and distribution layer between canonical Agentic Harness truth and deterministic CLI enforcement.

```text
canonical agentic-harness
        ↓
references + skill frontmatter routing
        ↓
skills/ + prompts/ + adapters/
        ↓
Codex plugin / individual skill install
        ↓
target .agents/skills/
        ↓
CLI and repository-native verification
```

`skills/` contains Agent Skills with required YAML frontmatter and a common procedural contract. `references/` contains shared context/source rules loaded only when needed. `evals/` owns routing and behavior acceptance cases. `.codex-plugin/` and `.agents/plugins/` are distribution metadata only and do not become architecture authority.

## Design Intelligence skill topology

Design work is intentionally split by responsibility so no single mega-skill conflates product decisions, art direction, implementation primitives, and verification:

```text
design-intelligence
├── design-analysis
├── design-research
├── identity-design
├── product-design
├── design-system
├── component-resolution
├── design-system-compliance
└── accessibility-audit
```

`design-intelligence` orchestrates the lifecycle but delegates specialist work. Canonical Design Genome/Analysis/Task/Diff schemas remain owned by `agentic-harness`; deterministic analyzers, preservation/compilation, and related mechanics remain owned by `agentic-harness-cli`/other deterministic surfaces.

The procedure layer may interpret evidence and propose changes, but must not silently promote references, model inference, external component defaults, or frequency observations into approved project truth.
